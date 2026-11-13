#!/usr/bin/env bash
# Série de bancs sur la même base « Banc » (même corpus, mêmes questions) : seuls les réglages de recherche changent.
# free -m et santé du service central relevés avant chaque banc (kit/PROMPT.md §2).
# Usage : outils/open-webui/serie_banc.sh <étiquette> [arguments de banc.py]
set -uo pipefail
cd "$(dirname "$0")/../.."
etiq="$1"; shift
log="outils/resultats/open-webui/banc-$(date +%F)-$etiq.log"
{ date -Iseconds; free -m | head -2; outils/communs/llm_central_sante.sh --essai 2>&1 | tail -12; } > "$log" 2>&1
python3 outils/open-webui/banc.py --etiquette "$etiq" "$@" >> "$log" 2>&1
tail -1 "$log"
