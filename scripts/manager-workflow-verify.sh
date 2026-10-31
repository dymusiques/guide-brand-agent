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
  echo "=== Single Brief evolution (gate + gap · Owner Mandate §2) ==="
  if ! bash scripts/manager-brief-evolution-until-gap.sh --brief "$BRIEF"; then
    EC=$?
    if [[ "$EC" -eq 42 ]]; then
      echo "RESULT: NEEDS_WORK — read EVOLUTION-GAP-latest.md; substantive edit; re-run (Owner not involved)"
    else
      echo "RESULT: FAIL — evolution-until-gap; see CEO-REROUTE / escalate Owner"
    fi
    exit "$EC"
  fi
  echo ""
  bash scripts/verify-xhs-content-dir.sh
  echo ""
  echo "=== Owner HTML sync (FILTER + test brief subjects) ==="
  bash scripts/verify-owner-html-deliverables.sh || {
    echo "HINT: run bash scripts/refresh-owner-notify-html.sh"
    exit 1
  }
else
  echo "(No Brief path — skipped evaluate + content-dir; pass Brief path for full gate)"
fi

echo ""
echo "RESULT: PASS — manager workflow verify complete"
