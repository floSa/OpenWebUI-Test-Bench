#!/usr/bin/env bash
# Démarre ou arrête le serveur MCP d'essai (outils/open-webui/extensions/serveur_mcp_velanor.py), relu avant lancement.
# Conteneur rag-mcp-velanor, image Open WebUI déjà présente (paquet mcp inclus), réseau rag-local, sans port publié.
# Usage : outils/open-webui/mcp.sh [start|stop]
set -euo pipefail
cd "$(dirname "$0")/../.."
IMAGE="ghcr.io/open-webui/open-webui:v0.13.3@sha256:46b59158e6558eeb980bc828e0f1b30238ad24d82ed84d5e5eda1dab2a082f14"
case "${1:-start}" in
  start)
    docker rm -f rag-mcp-velanor >/dev/null 2>&1 || true
    docker run -d --name rag-mcp-velanor --network rag-local --restart unless-stopped --read-only --tmpfs /tmp --no-healthcheck \
      -v "$PWD/outils/open-webui/extensions/serveur_mcp_velanor.py:/srv/serveur.py:ro" \
      --entrypoint python "$IMAGE" /srv/serveur.py >/dev/null
    docker network connect rag-local rag-open-webui 2>/dev/null || true
    for i in $(seq 1 30); do
      docker exec rag-open-webui curl -s -m 3 -o /dev/null -w '%{http_code}' -X POST http://rag-mcp-velanor:8000/mcp \
        -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
        -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"essai","version":"1"}}}' \
        | grep -q 200 && { echo "Serveur MCP prêt : http://rag-mcp-velanor:8000/mcp ($i s)"; exit 0; }
      sleep 1
    done
    echo "serveur MCP muet : docker logs rag-mcp-velanor"; exit 1;;
  stop) docker rm -f rag-mcp-velanor >/dev/null && echo "Serveur MCP arrêté.";;
esac
