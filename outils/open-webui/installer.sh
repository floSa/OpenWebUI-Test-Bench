#!/usr/bin/env bash
# Installation rejouable et idempotente d'Open WebUI v0.13.3, branchée au service LLM central.
#  1. image officielle à la version figée (étiquette et empreinte) ;
#  2. secret de session généré localement (donnees/open-webui/options.env, ignoré par git) ;
#  3. démarrage du projet compose rag-open-webui (outils/open-webui/compose.yml) et attente de /health ;
#  4. vérification des ports (127.0.0.1 seulement), mesures (durée, RAM au repos, disque).
# Le branchement au service central (chat, embed, transcribe) est porté par les variables du compose, lues au premier
# démarrage ; le compte administrateur se crée ensuite dans l'interface (manuel, chapitre 03) ou par
# outils/open-webui/configurer.py (même résultat, par l'API).
# Usage : outils/open-webui/installer.sh   (journal : outils/resultats/open-webui/installation-<date>.log)
set -euo pipefail
RACINE="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$RACINE"
IMAGE="ghcr.io/open-webui/open-webui:v0.13.3@sha256:46b59158e6558eeb980bc828e0f1b30238ad24d82ed84d5e5eda1dab2a082f14"
DONNEES="$RACINE/donnees/open-webui"
JOURNAL="outils/resultats/open-webui/installation-$(date +%F).log"
mkdir -p "$(dirname "$JOURNAL")"
exec > >(tee -a "$JOURNAL") 2>&1
echo "== installer.sh $(date -Iseconds)"
debut=$(date +%s)

# 0. prérequis
outils/open-webui/compose.sh version >/dev/null || { echo "docker compose indisponible"; exit 1; }
grep -q '^LLM_CENTRAL_KEY=.\+' .env 2>/dev/null || { echo "clé absente : copier .env.example en .env et y mettre la clé du service"; exit 1; }
docker network inspect llm-net >/dev/null 2>&1 || { echo "réseau llm-net absent : démarrer LLM-Service (~/mes_projets/Projet-IA/LLM-Service/scripts/demarrer.sh)"; exit 1; }
docker network inspect rag-local >/dev/null 2>&1 || docker network create rag-local
free -m | awk '/Mem:/{print "RAM disponible avant installation : " $7 " Mo"}'

# 1. image figée
docker image inspect "$IMAGE" >/dev/null 2>&1 || docker pull "$IMAGE"
docker image inspect --format 'image : {{index .RepoTags 0}} {{index .RepoDigests 0}} {{.Size}} octets' "$IMAGE"

# 2. secret de session (une seule fois)
mkdir -p "$DONNEES/data"
if [ ! -f "$DONNEES/options.env" ]; then
  umask 077
  echo "WEBUI_SECRET_KEY=$(openssl rand -hex 32)" > "$DONNEES/options.env"
  echo "secret généré : $DONNEES/options.env (jamais affiché)"
else
  echo "options existantes conservées : $DONNEES/options.env"
fi

# 3. démarrage
outils/open-webui/demarrer.sh

# 4. ports liés à 127.0.0.1 seulement, mesures
docker ps --filter name=rag-open-webui --format '{{.Names}} {{.Ports}}'
hors=$(docker ps --format '{{.Names}} {{.Ports}}' | grep -oE '[0-9a-f.:\[\]]+->' | grep -v '^127\.0\.0\.1:' || true)
[ -z "$hors" ] || { echo "port publié hors de 127.0.0.1 : $hors"; exit 1; }
echo "ports : tous liés à 127.0.0.1"
curl -s http://127.0.0.1:3000/api/version; echo
echo "durée : $(( $(date +%s) - debut )) s"
docker stats --no-stream --format 'RAM au repos : {{.Name}} {{.MemUsage}}' rag-open-webui
du -sh "$DONNEES" | sed 's/^/disque des données : /'
