#!/usr/bin/env bash
# Rebuild benchmark paths HTML + IP ecosystem HTML (growth-paths section) for Owner review.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
"$PY" scripts/build-owner-benchmark-paths-deliverable-html.py
"$PY" scripts/build-owner-ip-ecosystem-deliverable-html.py
echo "RESULT: refresh-owner-benchmark-html done"
