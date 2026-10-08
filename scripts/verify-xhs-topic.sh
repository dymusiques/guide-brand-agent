#!/usr/bin/env bash
# Xiaohongshu Topic Manager verify — 6 Gemini classifier cases (Module 3 pattern).
# Reads GEMINI_API_KEY from Guide/0/.env via Python dotenv at startup.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== Xiaohongshu topic verify (6 cases) ==="
echo ""

if [[ ! -f .env ]] && [[ -z "${GEMINI_API_KEY:-}" ]]; then
  echo "  WARN .env missing — copy .env.example → .env and set GEMINI_API_KEY"
  echo "RESULT: FAIL — no API key on disk"
  exit 1
fi

PY=""
if [[ -x .venv/bin/python ]]; then
  PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PY="python3"
else
  echo "  FAIL no python3 or .venv"
  exit 1
fi

exec "$PY" kernels/xiaohongshu/line2/tests/test_is_xhs_growth_aligned.py
