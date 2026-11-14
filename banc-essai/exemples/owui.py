"""Petit client de l'API d'Open WebUI, bibliothèque standard seulement, partagé par les exemples.

Secrets lus dans l'environnement, jamais écrits dans le code :
  OWUI_URL           adresse de l'instance (défaut http://127.0.0.1:3000)
  OWUI_CLE           clé d'API d'Open WebUI (sk-...) ; si elle est absente :
  OWUI_EMAIL, OWUI_MOT_DE_PASSE   connexion (POST /api/v1/auths/signin), qui renvoie un jeton de session.
"""
import json, mimetypes, os, time, urllib.error, urllib.request, uuid
from pathlib import Path

URL = os.environ.get("OWUI_URL", "http://127.0.0.1:3000")
_jeton = None


def requete(methode, route, corps=None, entetes=None, auth=True, delai=600):
    """Envoie une requête et renvoie la réponse JSON décodée (lève RuntimeError si le code HTTP est une erreur)."""
    h = {"Accept": "application/json"}
    if auth:
        h["Authorization"] = f"Bearer {jeton()}"
    donnees = None
    if isinstance(corps, (bytes, bytearray)):
        donnees = bytes(corps)
    elif corps is not None:
        donnees = json.dumps(corps).encode()
        h["Content-Type"] = "application/json"
    h.update(entetes or {})
    req = urllib.request.Request(URL + route, data=donnees, headers=h, method=methode)
    try:
        with urllib.request.urlopen(req, timeout=delai) as r:
            return json.loads(r.read().decode() or "null")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{methode} {route} -> HTTP {e.code} {e.read().decode()[:300]}") from None


def jeton():
    """Clé d'API si OWUI_CLE est définie, sinon jeton obtenu par connexion (gardé pour les appels suivants)."""
    global _jeton
    if _jeton is None:
        _jeton = os.environ.get("OWUI_CLE") or requete(
            "POST", "/api/v1/auths/signin",
            {"email": os.environ["OWUI_EMAIL"], "password": os.environ["OWUI_MOT_DE_PASSE"]}, auth=False)["token"]
    return _jeton


def televerser(chemin):
    """POST /api/v1/files/?process=true (formulaire multipart, champ « file ») ; renvoie la fiche du fichier."""
    chemin = Path(chemin)
    borne = uuid.uuid4().hex
    type_ = mimetypes.guess_type(chemin.name)[0] or "application/octet-stream"
    corps = (f'--{borne}\r\nContent-Disposition: form-data; name="file"; filename="{chemin.name}"\r\n'
             f"Content-Type: {type_}\r\n\r\n").encode() + chemin.read_bytes() + f"\r\n--{borne}--\r\n".encode()
    return requete("POST", "/api/v1/files/?process=true", corps,
                   entetes={"Content-Type": f"multipart/form-data; boundary={borne}"})


def attendre_traitement(fid, delai=900):
    """Interroge GET /api/v1/files/{id}/process/status jusqu'à « completed » ou « failed »."""
    debut = time.time()
    while time.time() - debut < delai:
        st = requete("GET", f"/api/v1/files/{fid}/process/status")
        if st.get("status") in ("completed", "failed"):
            return st, round(time.time() - debut, 1)
        time.sleep(1.5)
    raise TimeoutError(f"fichier {fid} non traité après {delai} s")


def liste(r):
    """Certaines routes renvoient une liste, d'autres {"items": [...], "total": n}."""
    return r.get("items", []) if isinstance(r, dict) else r


def sources(reponse):
    """Champ « sources » d'une réponse non streamée : (document, page, début de l'extrait) par passage."""
    res = []
    for s in reponse.get("sources") or []:
        for doc, meta in zip(s.get("document") or [], s.get("metadata") or []):
            page = meta.get("page_label") or (meta["page"] + 1 if isinstance(meta.get("page"), int) else "-")
            res.append((meta.get("name") or meta.get("source"), page, " ".join((doc or "").split())[:80]))
    return res
