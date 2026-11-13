#!/usr/bin/env bash
# Lance un exemple avec les identifiants fictifs de donnees/IDENTIFIANTS-LOCAUX.txt (compte admin), passés par
# variables d'environnement (OWUI_EMAIL, OWUI_MOT_DE_PASSE) sans être affichés. Si OWUI_CLE est déjà définie,
# elle est utilisée à la place de la connexion. Toute clé (sk-...) ou jeton (eyJ...) est masqué dans la sortie.
# Usage : exemples/open-webui/lancer.sh exemples/open-webui/02_question_simple.py
set -uo pipefail
cd "$(dirname "$0")/../.."
lire() { grep "^$1=" donnees/IDENTIFIANTS-LOCAUX.txt | head -1 | cut -d= -f2- | sed 's/^ *//;s/ *$//'; }
export OWUI_EMAIL="$(lire open-webui.admin.email)" OWUI_MOT_DE_PASSE="$(lire open-webui.admin.mot_de_passe)"
echo "== $1 ($(date -Iseconds))"
case "$1" in *.py) cmd=(python3 "$1") ;; *) cmd=(bash "$1") ;; esac
"${cmd[@]}" 2>&1 | sed -E 's/sk-[A-Za-z0-9_-]{8,}/[clé masquée]/g; s/eyJ[A-Za-z0-9._-]{10,}/[jeton masqué]/g'
echo "code ${PIPESTATUS[0]}"
echo
