#!/usr/bin/env bash
# Arrête Open WebUI (données conservées dans donnees/open-webui). LLM-Service n'est jamais arrêté ici : il est partagé.
set -euo pipefail
cd "$(dirname "$0")/.."
service/compose.sh stop
docker ps -a --format '{{.Names}}' | grep -qx rag-docling-serve && docker stop rag-docling-serve >/dev/null && echo "rag-docling-serve arrêté."
echo "Open WebUI arrêté."
