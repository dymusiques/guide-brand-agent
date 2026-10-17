#!/usr/bin/env bash
# Agent 03 — static lint + Gemini 6 (strategic docs kernel).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1; fi

echo "=== Marketing campaign verify (03) ==="
echo ""
echo "[static] README scaffold"
"$PY" scripts/lint-strategic-doc.py --kind marketing --file content/marketing/README.md
echo ""

if [[ ! -f .env ]] && [[ -z "${GEMINI_API_KEY:-}" ]]; then
  echo "RESULT: FAIL — Gemini 6 requires GEMINI_API_KEY"
  exit 1
fi
echo "[Gemini 6] test_marketing_aligned.py"
exec "$PY" kernels/strategic_docs/line2/tests/test_marketing_aligned.py
