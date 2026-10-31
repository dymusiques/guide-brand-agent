#!/usr/bin/env bash
# Sanity: workflow automation manifest + key scripts exist.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FAIL=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }

MANIFEST="$ROOT/integration/handoff/workflow-automation-manifest.json"
DOC="$ROOT/docs/WORKFLOW-AUTOMATION-MATRIX.md"
DEFAULT="$ROOT/docs/OWNER-DELIVERY-NOTIFY-DEFAULT.md"
MANDATE="$ROOT/docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md"
[[ -f "$MANIFEST" ]] && pass "workflow-automation-manifest.json" || fail "missing manifest"
[[ -f "$DOC" ]] && pass "WORKFLOW-AUTOMATION-MATRIX.md" || fail "missing matrix doc"
[[ -f "$DEFAULT" ]] && pass "OWNER-DELIVERY-NOTIFY-DEFAULT.md" || fail "missing delivery default"
[[ -f "$MANDATE" ]] && pass "OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md" || fail "missing owner mandate"

for s in \
  scripts/manager-brief-evolution-until-gap.sh \
  scripts/analyze-brief-evolution-gap.py \
  scripts/build-owner-workflow-test-article-html.py \
  scripts/verify-owner-html-deliverables.sh \
  scripts/manager-ceo-xhs-owner-delivery.sh \
  scripts/run_ceo_xhs_autopilot.py \
  scripts/run_ceo_full_execution.py \
  scripts/ceo-full-execution-pipeline.sh \
  scripts/ceo-six-case-battery.sh \
  scripts/ceo-triple-eval-baseline-loop.sh \
  scripts/ceo-double-stress.sh \
  scripts/verify-xhs-clever-advocate.sh \
  scripts/xhs_clever_advocate.py \
  docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md \
  scripts/ceo_write_run_manifest.py \
  docs/CEO-FULL-EXECUTION-MANDATE.md \
  docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md \
  docs/OWNER-CHAT-DELIVERY-FORMAT.md \
  docs/CEO-AGENT-ROSTER-AND-PARALLELISM.md \
  scripts/ceo_agent_roster.py \
  scripts/build-owner-multichannel-deliverable-html.py \
  scripts/open-owner-multichannel-deliverable-html.sh \
  docs/OWNER-MULTICHANNEL-LINKEDIN-IMAGE-DELIVERABLE.md \
  integration/handoff/ceo-full-execution-cycle.json \
  content/xiaohongshu/OWNER-LONGFORM-XHS-SPEC.md \
  scripts/evaluate_personal_ip.py \
  docs/AUTOMATION-LAYERS-MD-VS-PYTHON.md \
  docs/CEO-XHS-OWNER-DELIVERY-AUTOPILOT.md \
  integration/handoff/ceo-xhs-delivery-cycle.json \
  content/xiaohongshu/BRIEF-PITFALLS-RESEARCH-SOP.md \
  scripts/run-openwebui-router-pipeline.sh \
  scripts/verify-openwebui-ceo-router.sh \
  docs/OPENWEBUI-CEO-ROUTER.md \
  integration/handoff/openwebui-router-defaults.json \
  scripts/manager-ceo-gate-one-round.sh \
  scripts/ensure-process-launcher.sh \
  scripts/ceo-action-needed-refresh.py \
  scripts/new-machine-bootstrap.sh \
  scripts/background-goal-evolution-cycle.sh \
  scripts/ceo-auto-recover-blocked.sh \
  scripts/refresh-owner-notify-html.sh \
  scripts/ceo-workflow-test-round2-finish.sh \
  docs/CEO-WORKFLOW-TEST-SOP.md \
  docs/WORKFLOW-AUTOMATION-L1-INDEX.md \
  integration/handoff/workflow-automation-catalog-l1.json \
  scripts/build-workflow-automation-catalog.py \
  scripts/run-workflow-from-manifest.py \
  scripts/export-workflow-automation-pack.sh \
  scripts/run-context-reorg-pipeline.sh \
  .cursor/rules/xhs-copy-quality.mdc \
  .cursor/skills/xiaohongshu/xhs-copy-self-check.md \
  scripts/xhs-copy-grep-banned.sh \
  scripts/xhs_copy_grep_banned.py \
  integration/openwebui-rag/README.md \
  integration/openwebui-rag/scripts/openwebui_rag_paths.py \
  integration/openwebui-rag/scripts/sync_all_brand_rag_to_openwebui.py \
  integration/openwebui-rag/scripts/verify_openwebui_knowledge_status.py \
  integration/openwebui-rag/scripts/brand-drive-sync.env.example \
  scripts/build-context-reorg-pipeline-html.py \
  scripts/verify-context-reorg-html.sh \
  content/evolution/00-manager/ceo-inbox/CONTEXT-REORG-PIPELINE-LATEST.html \
  docs/owner-stack-openwebui-mindmap.html; do
  [[ -f "$ROOT/$s" ]] && pass "$s" || fail "missing $s"
done

for s in scripts/manager-ceo-gate-one-round.sh scripts/ensure-process-launcher.sh; do
  [[ -x "$ROOT/$s" ]] && pass "executable $s" || fail "not executable $s"
done

if command -v python3 >/dev/null 2>&1; then
  python3 -c "import json; json.load(open('$MANIFEST'))" && pass "manifest JSON valid" || fail "manifest JSON invalid"
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "RESULT: PASS verify-workflow-automation"
  exit 0
fi
echo "RESULT: FAIL verify-workflow-automation ($FAIL)"
exit 1
