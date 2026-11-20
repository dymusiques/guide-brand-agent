#!/usr/bin/env bash
# Open Owner Automation HTML in Google Chrome. See docs/OWNER-AUTOMATION-HTML-CHROME-STANDARD.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SLUG="${1:-}"
if [[ "$SLUG" == "--slug" ]]; then
  SLUG="${2:-}"
fi
[[ -n "$SLUG" ]] || { echo "Usage: $0 --slug <slug>"; exit 1; }

if [[ "${CEO_OWNER_HTML_OPEN:-1}" == "0" ]]; then
  echo "SKIP open (CEO_OWNER_HTML_OPEN=0)"
  exit 0
fi

PTR="$ROOT/integration/handoff/owner-automation-html/${SLUG}-latest.html"
[[ -f "$PTR" ]] || { echo "FAIL: missing $PTR — run build-owner-automation-run-html.py first"; exit 1; }

HTML_REL="$(python3 -c "import json; print(json.load(open('$PTR'))['html_path'])")"
HTML="$ROOT/$HTML_REL"
[[ -f "$HTML" ]] || { echo "FAIL: missing $HTML"; exit 1; }

if [[ "$(uname -s)" != Darwin ]]; then
  echo "HINT: open manually: $HTML"
  exit 0
fi

open -a "Google Chrome" "file://${HTML}"
echo "OK Chrome · file://${HTML}"