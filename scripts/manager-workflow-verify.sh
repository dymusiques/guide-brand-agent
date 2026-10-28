#!/usr/bin/env bash
# 00 Manager workflow verify — integration health + optional single Brief gate.
# Usage:
#   bash scripts/manager-workflow-verify.sh
#   bash scripts/manager-workflow-verify.sh content/xiaohongshu/YYYY-MM-DD-slug-brief.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BRIEF="${1:-}"

echo "=== Manager workflow verify ==="
echo ""

if [[ "${VERIFY_SKIP_INTEGRATION_MATRIX:-0}" != "1" ]]; then
  bash scripts/verify-manager-integration.sh
  echo ""
else
  echo "(VERIFY_SKIP_INTEGRATION_MATRIX=1 — skipped duplicate agent matrix)"
  echo ""
fi

if [[ -n "$BRIEF" ]]; then
  if [[ ! -f "$BRIEF" ]]; then
    echo "RESULT: FAIL — Brief not found: $BRIEF"
    exit 1
  fi
  PY=""
  if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
  elif command -v python3 >/dev/null 2>&1; then PY="python3"
  else echo "RESULT: FAIL — no python"; exit 1; fi
  echo "=== Single Brief auto gate (redteam + L1×6 + evaluate + kernel) ==="
  if ! bash scripts/manager-ceo-auto-gate-loop.sh --brief "$BRIEF"; then
    echo "RESULT: FAIL — auto gate loop; see CEO-REROUTE (Owner not involved)"
    exit 1
  fi
  echo ""
  bash scripts/verify-xhs-content-dir.sh
else
  echo "(No Brief path — skipped evaluate + content-dir; pass Brief path for full gate)"
fi

echo ""
echo "RESULT: PASS — manager workflow verify complete"
