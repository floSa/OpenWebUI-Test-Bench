#!/usr/bin/env bash
# Essai de restauration : extrait une archive de sauvegarde dans donnees/restauration-essai, démarre une seconde instance
# (conteneur rag-open-webui-restauration, port 127.0.0.1:3001, même image), s'y connecte avec le compte administrateur
# fictif, liste bases, modèles personnalisés et conversations, puis supprime le conteneur et le dossier extrait.
# L'instance principale n'est pas touchée. Usage : outils/open-webui/essai_restauration.sh <archive.tar.gz>
set -euo pipefail
cd "$(dirname "$0")/../.."
ARCHIVE="${1:?archive attendue}"
IMAGE="ghcr.io/open-webui/open-webui:v0.13.3@sha256:46b59158e6558eeb980bc828e0f1b30238ad24d82ed84d5e5eda1dab2a082f14"
DOSSIER="donnees/restauration-essai"
rm -rf "$DOSSIER"; mkdir -p "$DOSSIER"
tar xzf "$ARCHIVE" -C "$DOSSIER"
docker rm -f rag-open-webui-restauration >/dev/null 2>&1 || true
trap 'docker rm -f rag-open-webui-restauration >/dev/null 2>&1; rm -rf "$DOSSIER"; echo "Instance d'"'"'essai et dossier extrait supprimés."' EXIT
docker run -d --name rag-open-webui-restauration --network llm-net -p 127.0.0.1:3001:8080 --env-file "$DOSSIER/options.env" \
  -e ENABLE_OLLAMA_API=false -e OPENAI_API_BASE_URL=http://llm-central:8080/v1 \
  -v "$PWD/$DOSSIER/data:/app/backend/data" "$IMAGE" >/dev/null
for i in $(seq 1 150); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3001/health)" = 200 ] && { echo "Instance restaurée prête ($((i*2)) s)"; break; }
  sleep 2
done
OWUI_URL=http://127.0.0.1:3001 python3 - <<'PY'
import json, os, urllib.request
ident = dict(l.split("=", 1) for l in open("donnees/IDENTIFIANTS-LOCAUX.txt").read().splitlines() if l.startswith("open-webui.admin.") and "=" in l)
base = os.environ["OWUI_URL"]
def req(chemin, corps=None, jeton=None):
    r = urllib.request.Request(base + chemin, data=json.dumps(corps).encode() if corps else None,
                               headers={"Content-Type": "application/json", **({"Authorization": "Bearer " + jeton} if jeton else {})})
    return json.load(urllib.request.urlopen(r, timeout=60))
j = req("/api/v1/auths/signin", {"email": ident["open-webui.admin.email"].strip(), "password": ident["open-webui.admin.mot_de_passe"].strip()})["token"]
print("connexion du compte administrateur : réussie")
k = req("/api/v1/knowledge/", jeton=j); k = k.get("items", k) if isinstance(k, dict) else k
print("bases :", [b["name"] for b in k])
fi = req("/api/v1/files/", jeton=j); fi = fi.get("items", fi) if isinstance(fi, dict) else fi
print("fichiers téléversés :", len(fi))
m = req("/api/models", jeton=j)["data"]
print("modèles :", [x["id"] for x in m])
c = req("/api/v1/chats/?page=1", jeton=j)
print("conversations (première page) :", len(c))
demo = [b for b in k if b["name"] == "Démo Vélanor"][0]["id"]
r = req("/api/chat/completions", {"model": "chat", "stream": False, "chat_template_kwargs": {"enable_thinking": False},
        "messages": [{"role": "user", "content": "Quel est le prix unitaire des batteries prévu par le contrat Batterix ?"}],
        "files": [{"type": "collection", "id": demo}]}, jeton=j)
print("question sur la base restaurée :", r["choices"][0]["message"]["content"][:200].replace("\n", " "))
print("sources :", sorted({m.get("name") or m.get("source", "") for s in r.get("sources") or [] for m in s.get("metadata") or []}))
PY
