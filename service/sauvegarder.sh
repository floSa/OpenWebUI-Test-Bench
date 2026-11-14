#!/usr/bin/env bash
# Sauvegarde à froid d'Open WebUI : arrêt, archive du dossier de données (base SQLite, index des documents, fichiers
# téléversés), redémarrage. Archive : donnees/sauvegardes/open-webui-AAAA-MM-JJ-HHMM.tar.gz (hors git).
# Usage : service/sauvegarder.sh
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p donnees/sauvegardes
ARCHIVE="donnees/sauvegardes/open-webui-$(date +%Y-%m-%d-%H%M).tar.gz"
DOCLING=$(docker ps --format '{{.Names}}' | grep -cx rag-docling-serve || true)
service/arreter.sh
tar czf "$ARCHIVE" -C donnees/open-webui data options.env
echo "Archive : $ARCHIVE ($(du -h "$ARCHIVE" | cut -f1))"
service/demarrer.sh
[ "$DOCLING" = 1 ] && service/docling.sh start
exit 0
