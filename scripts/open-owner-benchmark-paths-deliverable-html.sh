#!/usr/bin/env bash
# Rebuild + open pivot-IP benchmark paths HTML (always fresh from JSON).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
"$PY" scripts/build-owner-benchmark-paths-deliverable-html.py

HTML="$ROOT/content/evolution/00-manager/ceo-inbox/OWNER-BENCHMARK-PATHS-DELIVERABLE-latest.html"
[[ -f "$HTML" ]] || { echo "FAIL: no benchmark HTML"; exit 1; }

if [[ "$(uname -s)" != Darwin ]]; then
  echo "HINT: open manually: file://${HTML}#owner-latest"
  exit 0
fi
open "file://${HTML}#owner-latest"
echo "OK open-owner-benchmark-paths-deliverable-html · file://${HTML}#owner-latest"
