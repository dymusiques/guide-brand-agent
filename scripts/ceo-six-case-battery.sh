#!/usr/bin/env bash
# Six-layer 6-case battery before CEO accepts GM work. See docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
BRIEF="${CEO_SIX_CASE_BRIEF:-${1:-}}"
FAIL=0
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"

run() {
  local name="$1"; shift
  if "$@"; then
    echo "PASS six-case · $name"
  else
    echo "FAIL six-case · $name" >&2
    FAIL=$((FAIL + 1))
  fi
}

run "integration-6" bash scripts/verify-integration.sh
run "01-ip-shell" "$PY" scripts/evaluate_personal_ip.py --check
run "fused-01" bash scripts/verify-agent-fused.sh --agent 01
run "fused-04" bash scripts/verify-agent-fused.sh --agent 04
run "fused-05" bash scripts/verify-agent-fused.sh --agent 05

if [[ -n "$BRIEF" && -f "$BRIEF" ]]; then
  run "brief-l1-gemini-6" "$PY" scripts/evaluate-xhs-brief-complete.py --brief "$BRIEF"
  run "kernel-regression-6" bash scripts/verify-xhs-topic.sh
else
  echo "SKIP six-case · brief L1+kernel (no --brief)"
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "RESULT: PASS ceo-six-case-battery"
  exit 0
fi
echo "RESULT: FAIL ceo-six-case-battery ($FAIL)"
exit 1
