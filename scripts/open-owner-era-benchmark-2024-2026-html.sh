#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
"$PY" scripts/build-owner-era-benchmark-2024-2026-html.py
HTML="$ROOT/content/evolution/00-manager/ceo-inbox/OWNER-ERA-BENCHMARK-2024-2026-DELIVERABLE-latest.html"
[[ -f "$HTML" ]] || exit 1
if [[ "$(uname -s)" == Darwin ]]; then
  open "file://${HTML}#owner-latest"
fi
echo "OK file://${HTML}#owner-latest"
