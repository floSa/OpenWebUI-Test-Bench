#!/usr/bin/env bash
# État d'Open WebUI : conteneurs, ports (liés à 127.0.0.1), santé, mémoire, disque ; santé du service LLM central (lecture seule).
set -uo pipefail
cd "$(dirname "$0")/.."
echo "== conteneurs"; docker ps -a --filter name=rag-open-webui --filter name=rag-docling --format '{{.Names}} {{.Status}} {{.Ports}}'
echo "== /health";    curl -s -m 5 http://127.0.0.1:3000/health; echo
echo "== version";    curl -s -m 5 http://127.0.0.1:3000/api/version; echo
echo "== mémoire";    docker stats --no-stream --format '{{.Name}} {{.MemUsage}} {{.CPUPerc}}' $(docker ps -q --filter name=rag-open-webui --filter name=rag-docling) 2>/dev/null
echo "== disque";     du -sh donnees/open-webui 2>/dev/null
echo "== ports publiés hors de 127.0.0.1 (doit être vide)"; docker ps --format '{{.Names}} {{.Ports}}' | grep -oE '[0-9a-f.:\[\]]+->' | grep -v '^127\.0\.0\.1:'
echo "== service LLM central"; banc-essai/communs/llm_central_sante.sh 2>&1 | head -6
