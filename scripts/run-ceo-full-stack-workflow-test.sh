#!/usr/bin/env bash
# Full stack: Key boundary checks → Open WebUI (−1) → CEO e2e → workflow verify → round2 campaign (01–12).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

INTAKE="${INTAKE:-content/personal-ip/intake/2026-10-29-ngv-flute-curation-theme.md}"
GOAL="${GOAL:-Personal IP：基于 intake，产出 LinkedIn 系列深度口播分节大纲（NGV×MSO 动线策展 vs 门口四重奏）；须结合 brand-ip-knowledge 事实}"
REPORT="$ROOT/content/evolution/00-manager/ceo-inbox/CEO-FULL-STACK-TEST-$(date +%Y-%m-%d).md"
ENV_OWUI="/Users/danying/Desktop/未命名/LLM-Ollama/RAG/RAG/scripts/brand-drive-sync.env"
FAIL=0

log() { echo ">>> $*"; }
pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*"; FAIL=$((FAIL + 1)); }

log "A · API Key 边界（Google CEO vs Open WebUI OpenRouter）"
[[ -f .env ]] && grep -q '^GEMINI_API_KEY=' .env && pass "CEO .env has GEMINI_API_KEY" || fail "CEO .env missing GEMINI_API_KEY"
if [[ -f "$ENV_OWUI" ]]; then
  grep -qE '^GEMINI_API_KEY=' "$ENV_OWUI" && fail "brand-drive-sync.env must not contain GEMINI_API_KEY" || pass "brand-drive-sync.env has no GEMINI_API_KEY"
  grep -q OPENWEBUI_API_KEY "$ENV_OWUI" && pass "brand-drive-sync.env has OPENWEBUI_API_KEY (localhost only)"
else
  fail "missing $ENV_OWUI"
fi

log "B · Open WebUI router + intake"
bash scripts/verify-openwebui-ceo-router.sh || FAIL=$((FAIL + 1))
bash scripts/run-openwebui-router-pipeline.sh --goal "$GOAL" --intake "$ROOT/$INTAKE" --platform personal_ip \
  || FAIL=$((FAIL + 1))

log "C · Open WebUI e2e bundle"
bash scripts/run-ceo-openwebui-e2e-workflow-test.sh || FAIL=$((FAIL + 1))

log "D · Workflow automation manifest"
bash scripts/verify-workflow-automation.sh || FAIL=$((FAIL + 1))

log "E · Round2 campaign + evaluation 压测（01–12 · 见 CEO-WORKFLOW-TEST-SOP）"
export VERIFY_GOALS_SKIP_PLATFORM="${VERIFY_GOALS_SKIP_PLATFORM:-1}"
if bash scripts/ceo-workflow-test-round2-finish.sh; then
  pass "ceo-workflow-test-round2-finish"
else
  fail "ceo-workflow-test-round2-finish (see ceo-ip-all-agents-campaign-*.md)"
fi

{
  echo "# CEO Full Stack Test · $(date +%Y-%m-%d)"
  echo ""
  echo "## Goal"
  echo "$GOAL"
  echo ""
  echo "## Intake"
  echo "\`$INTAKE\`"
  echo ""
  echo "## Key boundary"
  echo "- Chain A (CEO/campaign): GEMINI_API_KEY in brand-agent .env"
  echo "- Chain B (Router): Open WebUI → OpenRouter Connection"
  echo ""
  echo "## Result"
  echo "FAIL count: $FAIL"
  echo ""
  echo "Intake template: docs/OPENWEBUI-INTAKE-PROMPT-TEMPLATE.md"
} > "$REPORT"

if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL ceo-full-stack-workflow-test ($FAIL) — see $REPORT"
  exit 1
fi
echo "RESULT: PASS ceo-full-stack-workflow-test"
echo "Report: $REPORT"
