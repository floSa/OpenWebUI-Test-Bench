#!/usr/bin/env bash
# Démarre (ou arrête) le lecteur de documents Docling, service facultatif du projet rag-open-webui (profil « docling »).
# Sans port publié : Open WebUI le joint à http://rag-docling-serve:5001 par le réseau llm-net.
# Usage : service/docling.sh [start|stop]
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-start}" in
  start)
    service/compose.sh --profile docling up -d docling-serve
    for i in $(seq 1 90); do
      docker exec rag-open-webui curl -s -m 3 -o /dev/null -w '%{http_code}' http://rag-docling-serve:5001/health 2>/dev/null | grep -q 200 \
        && { echo "Docling prêt : http://rag-docling-serve:5001 ($((i*2)) s)"; exit 0; }
      sleep 2
    done
    echo "Docling ne répond pas après 180 s : docker logs rag-docling-serve"; exit 1;;
  stop) docker stop rag-docling-serve >/dev/null && echo "Docling arrêté.";;
esac
