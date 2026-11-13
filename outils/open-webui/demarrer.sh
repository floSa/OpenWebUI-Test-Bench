#!/usr/bin/env bash
# Démarre Open WebUI (données conservées) et attend /health. LLM-Service n'est pas démarré ici : il est géré à part.
set -euo pipefail
cd "$(dirname "$0")/../.."
docker network inspect llm-net >/dev/null 2>&1 || { echo "réseau llm-net absent : démarrer LLM-Service (~/mes_projets/Projet-IA/LLM-Service/scripts/demarrer.sh)"; exit 1; }
docker network inspect rag-local >/dev/null 2>&1 || docker network create rag-local >/dev/null
outils/open-webui/compose.sh up -d
for i in $(seq 1 150); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3000/health)" = 200 ] && { echo "Open WebUI prêt : http://127.0.0.1:3000 ($((i*2)) s)"; exit 0; }
  sleep 2
done
echo "Open WebUI ne répond pas après 300 s : docker logs rag-open-webui"; exit 1
