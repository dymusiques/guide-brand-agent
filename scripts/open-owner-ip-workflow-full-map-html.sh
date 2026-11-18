#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HTML="$ROOT/docs/OWNER-IP-WORKFLOW-FULL-MAP.html"
[[ -f "$HTML" ]] || { echo "FAIL: missing $HTML"; exit 1; }
if [[ "$(uname)" == "Darwin" ]]; then
  open "file://$HTML#owner-latest"
else
  echo "file://$HTML#owner-latest"
fi
echo "OK · file://$HTML"