#!/usr/bin/env bash
# Open FluteBuddy Owner HTML (not FILTER). See docs/CEO-OWNER-HTML-ROUTING.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ "${CEO_OWNER_HTML_OPEN:-1}" == "0" ]]; then
  echo "SKIP open-owner-flutebuddy-deliverable-html (CEO_OWNER_HTML_OPEN=0)"
  exit 0
fi

bash scripts/ensure-venv-deps.sh
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
"$PY" scripts/build-owner-flutebuddy-deliverable-html.py

DAY="${CEO_OWNER_HTML_DAY:-$(date +%Y-%m-%d)}"
HTML="$ROOT/content/evolution/00-manager/ceo-inbox/OWNER-FLUTEBUDDY-DELIVERABLE-$DAY.html"
[[ -f "$HTML" ]] || HTML="$(ls -t "$ROOT/content/evolution/00-manager/ceo-inbox"/OWNER-FLUTEBUDDY-DELIVERABLE-*.html 2>/dev/null | head -1)"
[[ -f "$HTML" ]] || { echo "FAIL: no FluteBuddy deliverable HTML"; exit 1; }

if [[ "$(uname -s)" != Darwin ]]; then
  echo "HINT: open manually: $HTML"
  exit 0
fi
open "file://${HTML}"
echo "OK open-owner-flutebuddy-deliverable-html · file://${HTML}"
