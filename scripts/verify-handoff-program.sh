#!/usr/bin/env bash
# Full program handoff verify — MD anchors + CEO + 10×6 + M4 + Gemini 6 + autopilot.
# Usage: bash scripts/verify-handoff-program.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
FAIL=0
step() {
  echo ""
  echo "######## $1 ########"
  if shift && "$@"; then
    echo ">>> $1: PASS"
  else
    echo ">>> $1: FAIL"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== verify-handoff-program (clone 接手全量) ==="

step "Agent takeover MD + 口令" bash scripts/verify-agent-takeover.sh
step "L0 handoff" bash scripts/verify-handoff.sh
step "M4 goals G-*" bash scripts/verify-goals.sh
step "Manager integration 10×6" bash scripts/verify-manager-integration.sh
step "Platform integration 6" bash scripts/verify-integration.sh

gemini_skip_reason=""
if [[ ! -f .env ]] && [[ -z "${GEMINI_API_KEY:-}" ]]; then
  gemini_skip_reason="no GEMINI_API_KEY / .env"
fi
if [[ -z "$gemini_skip_reason" ]] && [[ "${VERIFY_PROGRAM_SKIP_GEMINI:-0}" == "1" ]]; then
  gemini_skip_reason="VERIFY_PROGRAM_SKIP_GEMINI=1"
fi

if [[ -n "$gemini_skip_reason" ]]; then
  echo ""
  echo "######## Gemini 6 + brief batch ########"
  echo ">>> SKIP ($gemini_skip_reason)"
else
  run_gemini() {
    local title="$1"; shift
    echo ""
    echo "######## $title ########"
    local out ec
    set +e
    out=$("$@" 2>&1)
    ec=$?
    set -e
    if [[ "$ec" -eq 0 ]]; then
      echo ">>> $title: PASS"
    elif echo "$out" | grep -q "User location is not supported"; then
      echo ">>> $title: SKIP (Gemini 地区限制 — Brief Verify log 仍以 Git 为准)"
    else
      echo "$out" | tail -8
      echo ">>> $title: FAIL"
      FAIL=$((FAIL + 1))
    fi
  }
  run_gemini "05 XHS Gemini 6" bash scripts/verify-xhs-topic.sh
  run_gemini "02 business brand 6" bash scripts/verify-business-brand.sh
  run_gemini "03 marketing campaign 6" bash scripts/verify-marketing-campaign.sh
  run_gemini "XHS briefs batch aligned" bash scripts/verify-xhs-content-dir.sh
fi

step "CEO autopilot" bash scripts/manager-autopilot.sh

echo ""
if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL — handoff program ($FAIL step(s))"
  exit 1
fi
echo "RESULT: PASS — handoff program (MD + CEO + managers + goals + verify)"
exit 0
