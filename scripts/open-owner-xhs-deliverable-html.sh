#!/usr/bin/env bash
# Open Owner FILTER HTML in the default browser (macOS `open`). See docs/OWNER-DELIVERY-NOTIFY-DEFAULT.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ "${CEO_OWNER_HTML_OPEN:-1}" == "0" ]]; then
  echo "SKIP open-owner-xhs-deliverable-html (CEO_OWNER_HTML_OPEN=0)"
  exit 0
fi

DAY="${CEO_OWNER_HTML_DAY:-$(date +%Y-%m-%d)}"
HTML="$ROOT/content/evolution/00-manager/ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-$DAY.html"
HASH="${CEO_OWNER_HTML_HASH:-}"

if [[ ! -f "$HTML" ]]; then
  HTML="$(ls -t "$ROOT/content/evolution/00-manager/ceo-inbox"/OWNER-XHS-FILTER-DELIVERABLE-*.html 2>/dev/null | head -1 || true)"
fi
[[ -n "$HTML" && -f "$HTML" ]] || { echo "FAIL: no OWNER-XHS-FILTER-DELIVERABLE HTML"; exit 1; }

if [[ "$(uname -s)" != Darwin ]]; then
  echo "HINT: non-macOS — open manually: $HTML"
  exit 0
fi

# file:// + optional hash → auto-open modal in page (e.g. #owner-latest)
FILE_URL="file://${HTML}${HASH}"
open "$FILE_URL"
echo "OK open-owner-xhs-deliverable-html · $FILE_URL"
