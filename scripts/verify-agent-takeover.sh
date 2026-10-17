#!/usr/bin/env bash
# L0 — docs/AGENT-TAKEOVER.md present and contains handoff anchors.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
DOC="$ROOT/docs/AGENT-TAKEOVER.md"
FAIL=0
pass() { echo "  PASS · $1"; }
fail() { echo "  FAIL · $1"; FAIL=$((FAIL + 1)); }

echo "=== Agent takeover doc verify ==="
echo ""

if [[ ! -f "$DOC" ]]; then
  fail "missing docs/AGENT-TAKEOVER.md"
  echo "RESULT: FAIL"
  exit 1
fi

pass "docs/AGENT-TAKEOVER.md exists"

for needle in \
  "三轨" \
  "Owner 架构三要求" \
  "总 CEO" \
  "反馈回 CEO" \
  "G-STRONG-LINK" \
  "manager-autopilot.sh" \
  "ceo-dispatch-latest.md" \
  "discovery-01-irreplaceability" \
  "VERIFY-TIERS" \
  "仅 Owner" \
  "verify-agent-takeover.sh"; do
  if grep -q "$needle" "$DOC"; then
    pass "section marker: $needle"
  else
    fail "missing content: $needle"
  fi
done

for path in \
  agents/00-manager/AUTO-WORKFLOW.md \
  integration/goals/registry.json \
  content/marketing/2026-10-brand-discovery-phase.md \
  content/xiaohongshu/2026-10-17-discovery-01-irreplaceability-brief.md \
  scripts/manager-autopilot.sh; do
  if [[ -e "$ROOT/$path" ]]; then
    pass "path: $path"
  else
    fail "missing path: $path"
  fi
done

echo ""
if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL — agent takeover ($FAIL)"
  exit 1
fi
echo "RESULT: PASS — agent takeover doc ready for new Agent"
exit 0
