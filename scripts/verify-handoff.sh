#!/usr/bin/env bash
# Verify guide-brand-agent is complete enough for a new AI to take over.
# Policy: docs/HANDOFF-COMPLETENESS.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FAIL=0
WARN=0
pass() { echo "  OK   $1"; }
fail() { echo "  FAIL $1"; FAIL=$((FAIL + 1)); }
warn() { echo "  WARN $1"; WARN=$((WARN + 1)); }

echo "=== Handoff verify: $ROOT ==="
echo ""

echo "[CEO/GM operating pack]"
for f in \
  docs/HANDOFF-CEO-GM-SOP-PACK.md \
  integration/handoff/ceo-gm-operating-manifest.json \
  docs/MANAGER-THREE-PILLARS.md \
  docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md \
  agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md \
  docs/CEO-OWNER-ONE-LINE-TRIGGERS.md \
  scripts/manager-ceo-double-iteration.sh \
  scripts/verify-ceo-iteration-log.py \
  scripts/new-machine-bootstrap.sh \
  scripts/ensure-background-goal-evolution.sh; do
  [[ -f "$f" ]] && pass "$f" || fail "missing $f"
done

if [[ -f vendor/process-launcher/config/dba-brand-agent.yaml ]]; then
  pass "dba-brand-agent.yaml (background launcher config)"
else
  warn "missing dba-brand-agent.yaml — run: bash scripts/ensure-background-goal-evolution.sh"
fi

echo ""
echo "[L0 Git skeleton]"
for f in \
  AGENTS.md INDEX.md integrations/index.md \
  rules/SOUL.md rules/USER.md rules/WORKSPACE.md \
  .gitmodules docs/HANDOFF-COMPLETENESS.md docs/AGENT-TAKEOVER.md; do
  [[ -f "$f" ]] && pass "$f" || fail "missing $f"
done

[[ -d .cursor/skills/guide-core ]] && pass "guide-core skill" || fail "missing .cursor/skills/guide-core"
[[ -f vendor/gdocs-skill/pyproject.toml ]] && pass "gdocs-skill submodule" || fail "vendor/gdocs-skill not initialized (git submodule update --init)"
[[ -f vendor/process-launcher/pyproject.toml ]] && pass "process-launcher submodule" || fail "vendor/process-launcher not initialized (git submodule update --init)"
[[ -f rules/skills/skill_process_launcher.md ]] && pass "skill_process_launcher router" || fail "missing rules/skills/skill_process_launcher.md"
[[ -f integration/process-launcher-adoption.md ]] && pass "process-launcher adoption doc" || fail "missing integration/process-launcher-adoption.md"
[[ -f integration/EXTENSION-POINTS.md ]] && pass "EXTENSION-POINTS.md" || fail "missing integration/EXTENSION-POINTS.md"
[[ -f integration/templates/process-launcher-reserved-jobs.example.yaml ]] && pass "launcher reserved jobs template" || fail "missing integration/templates/process-launcher-reserved-jobs.example.yaml"
[[ -f rules/skills/workflow_parallel_subagents.md ]] && pass "workflow_parallel_subagents skill" || fail "missing rules/skills/workflow_parallel_subagents.md"
[[ -f integration/parallel-subagents-adoption.md ]] && pass "parallel-subagents adoption doc" || fail "missing integration/parallel-subagents-adoption.md"
[[ -f vendor/ai-agent-cli-skill/skills/skill_ai_agent_cli.md ]] && pass "ai-agent-cli-skill submodule" || fail "vendor/ai-agent-cli-skill not initialized (git submodule update --init)"
[[ -f rules/skills/skill_ai_agent_cli.md ]] && pass "skill_ai_agent_cli router" || fail "missing rules/skills/skill_ai_agent_cli.md"
[[ -f integration/ai-agent-cli-adoption.md ]] && pass "ai-agent-cli adoption doc" || fail "missing integration/ai-agent-cli-adoption.md"
[[ -f rules/skills/workflow_deep_research_survey.md ]] && pass "workflow_deep_research_survey skill" || fail "missing rules/skills/workflow_deep_research_survey.md"
[[ -f integration/deep-research-survey-adoption.md ]] && pass "deep-research-survey adoption doc" || fail "missing integration/deep-research-survey-adoption.md"
[[ -f integration/ip-content-skills-adoption.md ]] && pass "ip-content-skills adoption doc" || fail "missing integration/ip-content-skills-adoption.md"
[[ -f vendor/semantic-search-skill/skills/skill_semantic_search.md ]] && pass "semantic-search-skill submodule" || fail "vendor/semantic-search-skill not initialized"
[[ -f vendor/bilibili-upload-skill/skills/bilibili-upload/SKILL.md ]] && pass "bilibili-upload-skill submodule" || fail "vendor/bilibili-upload-skill not initialized"
[[ -f rules/skills/skill_bilibili_upload.md ]] && pass "skill_bilibili_upload router" || fail "missing rules/skills/skill_bilibili_upload.md"
[[ -f scripts/verify-ip-skills-env.sh ]] && pass "verify-ip-skills-env.sh" || fail "missing scripts/verify-ip-skills-env.sh"
if [[ -x scripts/verify-ip-skills-env.sh ]] || [[ -f scripts/verify-ip-skills-env.sh ]]; then
  if bash scripts/verify-ip-skills-env.sh >/tmp/verify-ip-skills-env.out 2>&1; then
    pass "verify-ip-skills-env.sh (see WARN for optional MLX/opus)"
  else
    warn "verify-ip-skills-env.sh failed — run manually after SETUP.md §2 pip"
    tail -5 /tmp/verify-ip-skills-env.out 2>/dev/null || true
  fi
fi

echo ""
echo "[L0 Brand facts]"
if [[ -f rules/USER.md ]] && grep -q "一句话定位" rules/USER.md && ! grep -q "待补充" rules/USER.md 2>/dev/null; then
  if grep -A1 "一句话定位" rules/USER.md | grep -qvE '^\s*[-*]\s*\*\*一句话定位|^\s*$|^\s*#' ; then
    pass "USER.md has IP positioning"
  else
    warn "USER.md 一句话定位可能仍为空"
  fi
else
  # softer check: any content after 一句话定位 line
  if grep -q "法派长笛\|跨界品牌" rules/USER.md 2>/dev/null; then
    pass "USER.md has IP content"
  else
    fail "USER.md missing IP positioning / audience"
  fi
fi

ip_count=$(find content/personal-ip -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
if [[ "${ip_count:-0}" -ge 1 ]]; then
  pass "content/personal-ip/ has $ip_count brief(s)"
else
  fail "content/personal-ip/ has no .md brief"
fi

echo ""
echo "[L1 Local private — not in git]"
if [[ -f vendor/gdocs-skill/secrets/credentials.json ]]; then
  pass "credentials.json present"
else
  warn "credentials.json missing — gdocs CLI needs OAuth setup"
fi
if [[ -f vendor/gdocs-skill/secrets/token.json ]]; then
  pass "token.json present"
else
  warn "token.json missing — first gdocs command will open browser"
fi
if [[ -f rules/skills/overlays/gdocs-skill.local.md ]]; then
  pass "gdocs local overlay present"
else
  warn "gdocs-skill.local.md missing — copy from .local.example.md"
fi

echo ""
echo "[Environment optional]"
if [[ -d .venv/bin ]] && .venv/bin/python -c "import gdocs" 2>/dev/null; then
  pass "venv + gdocs import"
else
  warn ".venv or gdocs not installed — run SETUP.md"
fi

echo ""
echo "[L0 Xiaohongshu content pipeline]"
if [[ -f content/xiaohongshu/PIPELINE.md ]]; then
  pass "content/xiaohongshu/PIPELINE.md"
else
  warn "missing content/xiaohongshu/PIPELINE.md"
fi
xhs_brief_count=$(find content/xiaohongshu -maxdepth 1 -name '*-brief.md' 2>/dev/null | wc -l | tr -d ' ')
if [[ "${xhs_brief_count:-0}" -ge 1 ]]; then
  pass "content/xiaohongshu/ has $xhs_brief_count *-brief.md"
  if [[ -f .env ]] || [[ -n "${GEMINI_API_KEY:-}" ]]; then
    warn "before handoff run: bash scripts/verify-xhs-content-dir.sh ($xhs_brief_count brief(s))"
  else
    warn "XHS briefs present but no .env — batch verify skipped until GEMINI_API_KEY set"
  fi
else
  warn "content/xiaohongshu/ has no *-brief.md yet"
fi

echo ""
echo "[L0 Agent takeover verify]"
if bash scripts/verify-agent-takeover.sh >/dev/null 2>&1; then
  pass "verify-agent-takeover.sh"
else
  fail "verify-agent-takeover.sh — fix docs/AGENT-TAKEOVER.md"
fi

echo ""
echo "[Git sync reminder]"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  dirty=$(git status --porcelain 2>/dev/null | grep -v '^?? vendor/gdocs-skill/secrets' | grep -c . || true)
  if [[ "${dirty:-0}" -gt 0 ]]; then
    warn "uncommitted changes ($dirty lines) — stable content should be committed for handoff"
  else
    pass "working tree clean (excluding secrets)"
  fi
  if git remote get-url origin >/dev/null 2>&1 && git remote get-url github >/dev/null 2>&1; then
    pass "dual remotes origin + github"
  else
    warn "missing origin or github remote"
  fi
fi

echo ""
echo "=== Summary ==="
if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL ($FAIL blocking, $WARN warnings)"
  echo "New AI cannot fully take over until L0 items are fixed."
  echo "See docs/HANDOFF-COMPLETENESS.md"
  exit 1
fi
if [[ "$WARN" -gt 0 ]]; then
  echo "RESULT: PASS with warnings ($WARN)"
  echo "New AI can take over; Google OAuth/MCP may need Owner once."
  exit 0
fi
echo "RESULT: PASS — ready for new AI handoff"
exit 0
