#!/usr/bin/env bash
# Batch verify all *-brief.md — default: full auto pipeline (redteam + L1×6 + evaluate + kernel 6).
# Legacy evaluate-only: XHS_VERIFY_MODE=evaluate-only bash scripts/verify-xhs-content-dir.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ "${XHS_VERIFY_MODE:-complete}" != "evaluate-only" ]]; then
  exec bash scripts/manager-xhs-briefs-auto-pipeline.sh
fi

CONTENT_DIR="$ROOT/content/xiaohongshu"

echo "=== Xiaohongshu content dir verify (evaluate-only legacy) ==="
echo ""

if [[ ! -d "$CONTENT_DIR" ]]; then
  echo "  FAIL missing $CONTENT_DIR"
  exit 1
fi

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

shopt -s nullglob
briefs=("$CONTENT_DIR"/*-brief.md)
shopt -u nullglob

if [[ ${#briefs[@]} -eq 0 ]]; then
  echo "RESULT: PASS — empty content dir"
  exit 0
fi

passed=0
failed=0
errors=0

for brief in "${briefs[@]}"; do
  name="$(basename "$brief")"
  set +e
  out=$("$PY" scripts/evaluate-xhs-topic.py --brief "$brief" 2>&1)
  ec=$?
  set -e
  if [[ "$ec" -eq 0 ]]; then
    echo "$name: Passed (aligned)"
    passed=$((passed + 1))
  elif [[ "$ec" -eq 1 ]]; then
    echo "$name: Failed (not aligned)"
    failed=$((failed + 1))
  else
    echo "$name: Failed (error exit $ec)"
    errors=$((errors + 1))
  fi
done

if [[ "$failed" -gt 0 ]] || [[ "$errors" -gt 0 ]]; then
  echo "RESULT: FAIL"
  exit 1
fi
echo "RESULT: PASS — all briefs aligned"
exit 0
