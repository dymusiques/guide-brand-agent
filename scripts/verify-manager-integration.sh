#!/usr/bin/env bash
# Manager integration layer — 6 glue cases (see integration/tests/).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1; fi
echo "=== Manager integration verify (6 cases) ==="
echo ""
exec "$PY" integration/tests/test_manager_integration.py
