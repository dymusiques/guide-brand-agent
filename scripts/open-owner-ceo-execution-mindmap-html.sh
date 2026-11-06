#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HTML="$ROOT/docs/CEO-EXECUTION-MINDMAP.html"
[[ -f "$HTML" ]] || { echo "FAIL: missing $HTML"; exit 1; }
if [[ "$(uname)" == "Darwin" ]]; then
  open "file://$HTML"
else
  echo "file://$HTML"
fi
echo "OK open-owner-ceo-execution-mindmap · file://$HTML"
