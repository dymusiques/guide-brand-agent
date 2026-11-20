#!/usr/bin/env bash
# Open owner-automation-html/<slug>-latest.html in Chrome (macOS open, else google-chrome).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SLUG=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --slug)
      SLUG="${2:-}"
      shift 2
      ;;
    *)
      echo "FAIL: unknown arg $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$SLUG" || "$SLUG" == *"/"* ]]; then
  echo "FAIL: need --slug" >&2
  exit 2
fi

HTML="$ROOT/integration/handoff/owner-automation-html/${SLUG}-latest.html"
if [[ ! -f "$HTML" ]]; then
  echo "FAIL: no HTML $HTML" >&2
  exit 1
fi

FILE_URL="file://${HTML}"

if [[ "$(uname -s)" == Darwin ]]; then
  open -a "Google Chrome" "$FILE_URL" 2>/dev/null || open "$FILE_URL"
  echo "OK chrome ${FILE_URL}"
  exit 0
fi

CHROME=""
for c in google-chrome google-chrome-stable chromium-browser chromium; do
  if command -v "$c" >/dev/null 2>&1; then
    CHROME="$c"
    break
  fi
done

if [[ -z "$CHROME" ]]; then
  echo "HINT: Chrome not installed — open manually: ${FILE_URL}"
  exit 0
fi

"$CHROME" --new-window "$FILE_URL" >/tmp/owner-automation-chrome-${SLUG}.log 2>&1 &
echo "OK chrome ${FILE_URL}"
