#!/usr/bin/env bash
# CEO · 01–12 全员 IP campaign：顺序 real verify / agent shell（见 agents/README.md）
# 与 run-ceo-deep-delivery-cycle.sh 协调：深交付在跑时 SKIP_GEMINI + 跳过重复 kernel/daily Gemini
# Owner deadline · 见 content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
export PATH="$ROOT/.venv/bin:${PATH:-}"
PY="$ROOT/.venv/bin/python"
INBOX="$ROOT/content/evolution/00-manager/ceo-inbox"
DISPATCH="$INBOX/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27.md"
DEEP_LOCK="/tmp/ceo-deep-delivery.lock"
CAMPAIGN_LOCK="/tmp/ceo-ip-all-agents-campaign.lock"
# shellcheck source=scripts/lib/ceo-deep-delivery-lock.sh
source "$ROOT/scripts/lib/ceo-deep-delivery-lock.sh"
STAMP="$(date +%Y%m%d-%H%M%S)"
DATE="${VERIFY_FUSED_DATE:-$(date +%Y-%m-%d)}"
LOG="$INBOX/ceo-ip-all-agents-campaign-$STAMP.log"
REPORT="$INBOX/ceo-ip-all-agents-campaign-$STAMP.md"
HTML="$INBOX/OWNER-XHS-FILTER-DELIVERABLE-$DATE.html"

mkdir -p "$INBOX"
exec > >(tee -a "$LOG") 2>&1

deep_delivery_active() {
  ceo_deep_delivery_active
}

sync_skip_gemini_from_deep() {
  if deep_delivery_active; then
    if [[ "$SKIP_GEMINI" != "1" ]]; then
      echo ">>> deep-delivery active — SKIP_GEMINI=1 for duplicate Gemini shells"
    fi
    SKIP_GEMINI=1
    export SKIP_GEMINI
  fi
}

acquire_campaign_lock() {
  if [[ -f "$CAMPAIGN_LOCK" ]]; then
    local old_pid
    old_pid="$(cat "$CAMPAIGN_LOCK" 2>/dev/null || true)"
    if [[ -n "$old_pid" ]] && kill -0 "$old_pid" 2>/dev/null; then
      echo "Another ceo-ip-all-agents-campaign is running (pid $old_pid · $CAMPAIGN_LOCK)"
      exit 2
    fi
  fi
  echo $$ >"$CAMPAIGN_LOCK"
  trap 'rm -f "$CAMPAIGN_LOCK"' EXIT
}

acquire_campaign_lock
ceo_campaign_wait_for_deep

SKIP_GEMINI="${SKIP_GEMINI:-0}"
if [[ -n "${VERIFY_GOALS_SKIP_PLATFORM:-}" ]]; then
  export VERIFY_GOALS_SKIP_PLATFORM
else
  bash scripts/check-google-auth-for-agent.sh >/dev/null 2>&1 || true
  if bash scripts/verify-integration.sh >/dev/null 2>&1; then
    export VERIFY_GOALS_SKIP_PLATFORM=0
    echo ">>> VERIFY_GOALS_SKIP_PLATFORM=0 (verify-integration PASS · Owner Google grant · no chat confirm)"
  else
    export VERIFY_GOALS_SKIP_PLATFORM=1
    echo ">>> VERIFY_GOALS_SKIP_PLATFORM=1 (integration not PASS · skip platform hook silently)"
  fi
fi
sync_skip_gemini_from_deep
if [[ "$SKIP_GEMINI" == "1" ]]; then
  echo ">>> campaign SKIP_GEMINI=1 · no duplicate kernel/daily Gemini (deep lock or CEO override)"
fi

FAIL=0
phase() {
  echo ""
  echo "######## $(date +%H:%M:%S) · Agent $1 · $2 ########"
}

run_step() {
  local name="$1"
  shift
  if "$@"; then
    echo ">>> $name: PASS"
  else
    echo ">>> $name: FAIL"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== CEO IP all-agents campaign · $STAMP ==="
echo "dispatch: $DISPATCH"
echo "SKIP_GEMINI=$SKIP_GEMINI · DATE=$DATE"
[[ -f "$DISPATCH" ]] || echo "WARN: dispatch file missing — continuing verify chain"
date
echo ""

export VERIFY_FUSED_DATE="$DATE"

# —— 00 · CEO 轻量总览（非 01–12 编号，但先于矩阵）——
phase "00" "CEO dashboard + dispatch refresh"
run_step "manager-dashboard" bash scripts/manager-dashboard.sh
if [[ "$SKIP_GEMINI" != "1" ]]; then
  run_step "ceo-dispatch-refresh" "$PY" scripts/ceo-dispatch-refresh.py
else
  echo ">>> ceo-dispatch-refresh: SKIP (deep delivery owns refresh chain)"
fi

fused() {
  local id="$1"
  if [[ "$id" == "10" || "$id" == "11" || "$id" == "12" ]]; then
    SKIP_GEMINI="$SKIP_GEMINI" bash scripts/verify-agent-fused.sh --agent "$id" --with-artifacts
  else
    SKIP_GEMINI="$SKIP_GEMINI" bash scripts/verify-agent-fused.sh --agent "$id"
  fi
}

# —— 01–12 顺序 ——
phase "01" "personal-ip"
run_step "shell-01-check" bash scripts/agent-shells/01-personal-ip.sh --check
run_step "fused-01" fused 01

phase "02" "business-brand"
sync_skip_gemini_from_deep
if [[ "$SKIP_GEMINI" == "1" ]]; then
  run_step "shell-02-check" bash scripts/agent-shells/02-business-brand.sh --check
else
  run_step "shell-02-verify" env CEO_GEMINI_VERIFY_TIMEOUT="${CEO_GEMINI_VERIFY_TIMEOUT:-900}" bash scripts/verify-business-brand.sh
fi
run_step "fused-02" fused 02

phase "03" "marketing-strategy"
sync_skip_gemini_from_deep
if [[ "$SKIP_GEMINI" == "1" ]]; then
  run_step "shell-03-check" bash scripts/agent-shells/03-marketing.sh --check
else
  run_step "shell-03-verify" env CEO_GEMINI_VERIFY_TIMEOUT="${CEO_GEMINI_VERIFY_TIMEOUT:-900}" bash scripts/verify-marketing-campaign.sh
fi
run_step "fused-03" fused 03

phase "04" "xhs-topic-manager"
run_step "fused-04" fused 04

phase "05" "xhs-kernel"
sync_skip_gemini_from_deep
if [[ "$SKIP_GEMINI" == "1" ]]; then
  run_step "shell-05-check" bash scripts/agent-shells/05-xhs-kernel.sh --check
else
  run_step "shell-05-kernel" bash scripts/agent-shells/05-xhs-kernel.sh
fi
run_step "fused-05" fused 05

phase "06" "xhs-content-pipeline"
run_step "shell-06-pipeline" bash scripts/agent-shells/06-xhs-pipeline.sh
run_step "fused-06" fused 06

phase "07" "brand-visual"
run_step "shell-07-check" bash scripts/agent-shells/07-brand-visual.sh --check
run_step "fused-07" fused 07

phase "08" "platform-integration"
sync_skip_gemini_from_deep
if [[ "$SKIP_GEMINI" == "1" ]]; then
  run_step "shell-08-check" bash scripts/agent-shells/08-platform.sh --check
else
  run_step "shell-08-verify" bash scripts/agent-shells/08-platform.sh
fi
run_step "fused-08" fused 08

phase "09" "data-analytics"
if [[ -d content/analytics/inbox ]] && compgen -G "content/analytics/inbox/*" >/dev/null; then
  run_step "shell-09-live" bash scripts/agent-shells/09-analytics.sh --live
else
  run_step "shell-09-demo" bash scripts/agent-shells/09-analytics.sh --demo
fi
run_step "screen-artist-watchlist" "$PY" scripts/screen-artist-watchlist.py
run_step "fused-09" fused 09

phase "10" "artist-benchmark (verify; Gemini via deep/daily if active)"
run_step "fused-10" fused 10

phase "11" "ip-daily-evaluator"
run_step "fused-11" fused 11

phase "12" "owner-daily-brief"
run_step "fused-12" fused 12

# —— HTML · 不与 deep-delivery 重复构建 ——
phase "HTML" "Owner deliverable"
if deep_delivery_active; then
  echo ">>> refresh-owner-notify-html: SKIP (deep-delivery will refresh HTML)"
elif [[ "${CEO_OWNER_HTML_REFRESH:-1}" == "1" ]]; then
  run_step "owner-html" bash scripts/refresh-owner-notify-html.sh
else
  echo ">>> refresh-owner-notify-html: SKIP (CEO_OWNER_HTML_REFRESH=0)"
fi

{
  echo "# CEO IP all-agents campaign · $STAMP"
  echo ""
  echo "- dispatch: \`content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27.md\`"
  echo "- agents: 01–12 sequential verify + shells"
  echo "- SKIP_GEMINI: $SKIP_GEMINI"
  echo "- failures: $FAIL"
  echo "- log: \`content/evolution/00-manager/ceo-inbox/ceo-ip-all-agents-campaign-$STAMP.log\`"
  echo "- Owner HTML: \`$HTML\`"
  echo ""
  if [[ "$FAIL" -gt 0 ]]; then
    echo "**RESULT: FAIL ($FAIL)** — 读 CEO-REROUTE / campaign log 继续 GM loop。"
  else
    echo "**RESULT: PASS** — 01–12 verify 链完成；Owner 打开 HTML + daily brief。"
  fi
} >"$REPORT"

echo ""
echo "Report: $REPORT"
echo "Owner HTML: $HTML"
if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL ceo-ip-all-agents-campaign ($FAIL)"
  exit 1
fi
echo "RESULT: PASS ceo-ip-all-agents-campaign"
exit 0
