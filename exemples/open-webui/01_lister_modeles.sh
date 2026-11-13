#!/usr/bin/env bash
# Exemple 01 (curl) : connexion, puis liste des modèles proposés par l'instance (GET /api/models).
# Secrets : OWUI_CLE, ou OWUI_EMAIL et OWUI_MOT_DE_PASSE (variables d'environnement). Le jeton n'est jamais affiché.
set -euo pipefail
URL="${OWUI_URL:-http://127.0.0.1:3000}"
echo "santé : HTTP $(curl -s -o /dev/null -w '%{http_code}' "$URL/health")"
if [ -n "${OWUI_CLE:-}" ]; then
  JETON="$OWUI_CLE"; echo "authentification : clé d'API (OWUI_CLE)"
else
  CORPS=$(python3 -c 'import json,os; print(json.dumps({"email": os.environ["OWUI_EMAIL"], "password": os.environ["OWUI_MOT_DE_PASSE"]}))')
  JETON=$(curl -s -X POST "$URL/api/v1/auths/signin" -H 'Content-Type: application/json' -d "$CORPS" \
          | python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])')
  echo "authentification : connexion (jeton de session)"
fi
curl -s "$URL/api/models" -H "Authorization: Bearer $JETON" | python3 -c '
import json, sys
for m in json.load(sys.stdin)["data"]:
    base = (m.get("info") or {}).get("base_model_id")
    print("-", m["id"], ": «", m["name"], "»" + (", assistant fondé sur " + base if base else ""))'
