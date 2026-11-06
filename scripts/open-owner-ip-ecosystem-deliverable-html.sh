#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ "${CEO_OWNER_HTML_OPEN:-1}" == "0" ]]; then
  echo "SKIP open-owner-ip-ecosystem-deliverable-html (CEO_OWNER_HTML_OPEN=0)"
  exit 0
fi

bash scripts/ensure-venv-deps.sh
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
"$PY" scripts/build-owner-ip-ecosystem-deliverable-html.py

DAY="${CEO_OWNER_HTML_DAY:-$(date +%Y-%m-%d)}"
HTML="$ROOT/content/evolution/00-manager/ceo-inbox/OWNER-IP-ECOSYSTEM-DELIVERABLE-$DAY.html"
[[ -f "$HTML" ]] || HTML="$(ls -t "$ROOT/content/evolution/00-manager/ceo-inbox"/OWNER-IP-ECOSYSTEM-DELIVERABLE-*.html 2>/dev/null | head -1)"
[[ -f "$HTML" ]] || { echo "FAIL: no IP ecosystem HTML"; exit 1; }

if [[ "$(uname -s)" != Darwin ]]; then
  echo "HINT: open manually: $HTML"
  exit 0
fi
open "file://${HTML}"
echo "OK open-owner-ip-ecosystem-deliverable-html · file://${HTML}"
