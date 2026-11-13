#!/usr/bin/env python3
"""Client minimal de l'API d'Open WebUI (bibliothèque standard seulement), pour le banc et les essais.

Connexion par les identifiants fictifs de donnees/IDENTIFIANTS-LOCAUX.txt (POST /api/v1/auths/signin, jeton JWT).
Le jeton et la clé du service central ne sont jamais affichés.
Usage en ligne de commande : client.py GET /api/v1/retrieval/config   |   client.py POST <route> '<json>'
"""
import json, mimetypes, os, re, sys, time, urllib.error, urllib.request, uuid
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
BASE = os.environ.get("OPENWEBUI_URL", "http://127.0.0.1:3000")
IDENT = RACINE / "donnees/IDENTIFIANTS-LOCAUX.txt"
PENSEE = re.compile(r"<(think|details)[^>]*>.*?</\1>", re.S)


def identifiants():
    d = {}
    for l in IDENT.read_text().splitlines():
        if "=" in l and l.startswith("open-webui."):
            k, v = l.split("=", 1); d[k.strip()] = v.strip()
    return d


def sans_pensee(t):
    return PENSEE.sub("", t or "").strip()


class API:
    def __init__(self, compte="admin", jeton=None):
        self.jeton = jeton
        if not jeton:
            d = identifiants()
            r = self.post("/api/v1/auths/signin", {"email": d[f"open-webui.{compte}.email"],
                                                   "password": d[f"open-webui.{compte}.mot_de_passe"]}, auth=False)
            self.jeton = r["token"]

    def _req(self, methode, route, corps=None, auth=True, entetes=None, delai=600):
        h = {"Accept": "application/json"}
        if auth:
            h["Authorization"] = f"Bearer {self.jeton}"
        donnees = None
        if corps is not None:
            if isinstance(corps, (bytes, bytearray)):
                donnees = bytes(corps)
            else:
                donnees = json.dumps(corps).encode(); h["Content-Type"] = "application/json"
        h.update(entetes or {})
        req = urllib.request.Request(BASE + route, data=donnees, headers=h, method=methode)
        try:
            with urllib.request.urlopen(req, timeout=delai) as r:
                txt = r.read().decode()
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"{methode} {route} -> {e.code} {e.read().decode()[:500]}") from None
        try:
            return json.loads(txt)
        except json.JSONDecodeError:
            return txt

    def get(self, route, **kw):
        return self._req("GET", route, **kw)

    def post(self, route, corps=None, **kw):
        return self._req("POST", route, corps if corps is not None else {}, **kw)

    def delete(self, route, **kw):
        return self._req("DELETE", route, **kw)

    def televerser(self, chemin, attendre=True, delai=900):
        """POST /api/v1/files/ (multipart) puis attente du traitement (statut du fichier)."""
        chemin = Path(chemin)
        borne = uuid.uuid4().hex
        type_ = mimetypes.guess_type(chemin.name)[0] or "application/octet-stream"
        corps = (f"--{borne}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{chemin.name}\"\r\n"
                 f"Content-Type: {type_}\r\n\r\n").encode() + chemin.read_bytes() + f"\r\n--{borne}--\r\n".encode()
        f = self._req("POST", "/api/v1/files/?process=true", corps,
                      entetes={"Content-Type": f"multipart/form-data; boundary={borne}"})
        if attendre:
            f = self.attendre_fichier(f["id"], delai)
        return f

    def attendre_fichier(self, fid, delai=900):
        debut = time.time()
        while time.time() - debut < delai:
            st = self.get(f"/api/v1/files/{fid}/process/status")
            if st.get("status") in ("completed", "failed"):
                f = self.get(f"/api/v1/files/{fid}")
                f["_statut"] = st
                return f
            time.sleep(1.5)
        raise TimeoutError(f"fichier {fid} non traité après {delai} s")


if __name__ == "__main__":
    api = API()
    meth, route = sys.argv[1], sys.argv[2]
    corps = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    r = api._req(meth, route, corps)
    txt = json.dumps(r, ensure_ascii=False, indent=1)
    cle = next((l.split("=", 1)[1].strip() for l in (RACINE / ".env").read_text().splitlines()
                if l.startswith("LLM_CENTRAL_KEY=")), "")
    print(txt.replace(cle, "[clé masquée]") if cle else txt)
