#!/usr/bin/env bash
# Integration verify: gdocs smoke + Git/Drive read paths (6 Python cases).
# Complements scripts/verify-handoff.sh (L0 skeleton).
# Policy: check.md · docs/HANDOFF-COMPLETENESS.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== Integration verify (wrapper) ==="
echo ""

PY=""
if [[ -x .venv/bin/python ]]; then
  PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PY="python3"
else
  echo "  FAIL no python3 or .venv"
  echo "RESULT: FAIL"
  exit 1
fi

exec "$PY" scripts/verify_integration.py
