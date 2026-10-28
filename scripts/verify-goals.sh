#!/usr/bin/env bash
# M4 — verify each G-* goal hook.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1; fi
# G-PLATFORM-SYNC needs Drive OAuth; set VERIFY_GOALS_SKIP_PLATFORM=1 to skip (CEO scripts default 1).
export VERIFY_GOALS_SKIP_PLATFORM="${VERIFY_GOALS_SKIP_PLATFORM:-}"
exec "$PY" integration/tests/test_goals_verify.py
