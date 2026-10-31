#!/usr/bin/env bash
# Two stress passes: adversarial (+ optional round2). See docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
BRIEF=""
SKIP_ROUND2=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --brief) BRIEF="${2:-}"; shift 2 ;;
    --skip-round2) SKIP_ROUND2=1; shift ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done
[[ -n "$BRIEF" && -f "$BRIEF" ]] || { echo "FAIL: --brief required"; exit 1; }
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
FAIL=0

echo "=== ceo-double-stress · pass 0 · clever-advocate (longform) ==="
if ! bash scripts/verify-xhs-clever-advocate.sh --brief "$BRIEF"; then
  FAIL=1
fi

echo "=== ceo-double-stress · pass 1 · adversarial ==="
if ! "$PY" scripts/run-xhs-brief-adversarial-challenge.py --brief "$BRIEF"; then
  FAIL=$((FAIL + 1))
fi

echo "=== ceo-double-stress · pass 2 · adversarial (re-run) ==="
if ! "$PY" scripts/run-xhs-brief-adversarial-challenge.py --brief "$BRIEF"; then
  FAIL=$((FAIL + 1))
fi

if [[ "$SKIP_ROUND2" -eq 0 ]] && [[ "$BRIEF" == *"-test-brief.md" ]]; then
  echo "=== ceo-double-stress · pass 2b · workflow round2 ==="
  if ! bash scripts/ceo-workflow-test-round2-finish.sh; then
    FAIL=$((FAIL + 1))
  fi
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "RESULT: PASS ceo-double-stress"
  exit 0
fi
echo "RESULT: FAIL ceo-double-stress ($FAIL)"
exit 1
