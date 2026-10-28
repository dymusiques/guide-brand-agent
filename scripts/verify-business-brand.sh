#!/usr/bin/env bash
# Agent 02 — static lint + Gemini 6 (strategic docs kernel).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1; fi

echo "=== Business brand verify (02) ==="
echo ""
echo "[static] README scaffold"
"$PY" scripts/lint-strategic-doc.py --kind business_brand --file content/business-brand/README.md
echo ""

if [[ "${SKIP_GEMINI:-0}" == "1" ]]; then
  echo ">>> Gemini 6: SKIP (SKIP_GEMINI=1)"
  echo "RESULT: PASS — static only (SKIP_GEMINI)"
  exit 0
fi

if [[ ! -f .env ]] && [[ -z "${GEMINI_API_KEY:-}" ]]; then
  echo "RESULT: FAIL — Gemini 6 requires GEMINI_API_KEY"
  exit 1
fi
GEMINI_TIMEOUT="${CEO_GEMINI_VERIFY_TIMEOUT:-900}"
echo "[Gemini 6] kernels/strategic_docs/line2/tests/test_business_brand_aligned.py (timeout ${GEMINI_TIMEOUT}s)"
if command -v timeout >/dev/null 2>&1; then
  if timeout "$GEMINI_TIMEOUT" "$PY" kernels/strategic_docs/line2/tests/test_business_brand_aligned.py; then
    echo "RESULT: PASS — business brand Gemini 6"
    exit 0
  fi
  ec=$?
  if [[ "$ec" -eq 124 ]]; then
    echo "RESULT: FAIL — Gemini 6 timeout after ${GEMINI_TIMEOUT}s"
    exit 1
  fi
  echo "RESULT: FAIL — Gemini 6 exit=$ec"
  exit "$ec"
fi
if "$PY" kernels/strategic_docs/line2/tests/test_business_brand_aligned.py; then
  echo "RESULT: PASS — business brand Gemini 6"
  exit 0
fi
echo "RESULT: FAIL — Gemini 6"
exit 1
