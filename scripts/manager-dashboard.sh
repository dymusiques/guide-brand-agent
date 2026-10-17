#!/usr/bin/env bash
# 00 Manager CEO dashboard — status rollup for Owner + Agent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh 2>/dev/null || true
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1; fi
exec "$PY" scripts/manager_dashboard.py
