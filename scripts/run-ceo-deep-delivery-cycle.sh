#!/usr/bin/env bash
# CEO 深交付循环 · 筛选 → 测试 → 再筛选（非 5 分钟应付）
# Owner deadline: 当日 24:00 Asia/Shanghai · 见 docs/CEO-OWNER-DEADLINE-DELIVERY.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
export PATH="$ROOT/.venv/bin:${PATH:-}"
PY="$ROOT/.venv/bin/python"
INBOX="$ROOT/content/evolution/00-manager/ceo-inbox"
DEEP_LOCK="/tmp/ceo-deep-delivery.lock"
# shellcheck source=scripts/lib/ceo-deep-delivery-lock.sh
source "$ROOT/scripts/lib/ceo-deep-delivery-lock.sh"
mkdir -p "$INBOX"
ceo_acquire_deep_lock_or_exit
export VERIFY_GOALS_SKIP_PLATFORM="${VERIFY_GOALS_SKIP_PLATFORM:-1}"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG="$INBOX/ceo-deep-delivery-$STAMP.log"
REPORT="$INBOX/ceo-deep-delivery-$STAMP.md"
exec > >(tee -a "$LOG") 2>&1

DEEP_ROUNDS="${CEO_DEEP_ROUNDS:-2}"
GATE_ROUNDS="${CEO_GATE_MAX_ROUNDS:-3}"

echo "=== CEO deep delivery cycle · $STAMP ==="
echo "DEEP_ROUNDS=$DEEP_ROUNDS · GATE_ROUNDS=$GATE_ROUNDS"
date
echo ""

phase() {
  echo ""
  echo "######## $(date +%H:%M:%S) · $1 ########"
}

FAIL=0
run_phase() {
  local name="$1"
  shift
  if "$@"; then
    echo ">>> $name: PASS"
  else
    echo ">>> $name: FAIL"
    FAIL=$((FAIL + 1))
  fi
}

# —— Phase A · 资料收集（09/10/CEO dispatch）——
phase "A · 收集 · artist + analytics + dispatch"
run_phase "screen-artist-watchlist" "$PY" scripts/screen-artist-watchlist.py
run_phase "analytics-pipeline" bash scripts/analytics-pipeline.sh --demo
run_phase "ceo-dispatch-refresh" "$PY" scripts/ceo-dispatch-refresh.py
run_phase "manager-dashboard" bash scripts/manager-dashboard.sh

# —— Phase B · 筛选汇总 MD（内容清单）——
phase "B · 筛选 · ceo-xhs-ip-filter-batch"
run_phase "ceo-xhs-ip-filter-batch" "$PY" scripts/ceo-xhs-ip-filter-batch.py

deep=1
while [[ "$deep" -le "$DEEP_ROUNDS" ]]; do
  phase "C${deep} · 测试 · redteam + adversarial + complete gate · round ${deep} of ${DEEP_ROUNDS}"
  run_phase "xhs-briefs-auto-pipeline" bash scripts/manager-xhs-briefs-auto-pipeline.sh

  phase "D${deep} · 单篇 gate loop · discovery 01-04"
  for brief in content/xiaohongshu/2026-10-17-discovery-0*-brief.md; do
    [[ -f "$brief" ]] || continue
    echo "--- gate loop: $brief ---"
    CEO_GATE_MAX_ROUNDS="$GATE_ROUNDS" bash scripts/manager-ceo-auto-gate-loop.sh --brief "$brief" || FAIL=$((FAIL + 1))
  done

  phase "E${deep} · 再筛选 · 刷新 adversarial + Owner HTML"
  run_phase "adversarial-refresh" "$PY" scripts/run-xhs-brief-adversarial-challenge.py --all
  run_phase "owner-html" "$PY" scripts/build-owner-xhs-report-html.py

  deep=$((deep + 1))
done

phase "F · 日更 GM trio（10/11/12 · challenge hygiene）"
run_phase "daily-gm-trio" bash scripts/run-daily-gm-trio.sh || true

phase "G · 通知"
"$PY" scripts/ceo-xhs-filter-notify-gmail.py || true

{
  echo "# CEO 深交付报告 · $STAMP"
  echo ""
  echo "- deep_rounds: $DEEP_ROUNDS"
  echo "- gate_rounds_per_brief: $GATE_ROUNDS"
  echo "- failures: $FAIL"
  echo "- log: \`content/evolution/00-manager/ceo-inbox/ceo-deep-delivery-$STAMP.log\`"
  echo "- Owner HTML: \`content/evolution/00-manager/ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-$(date +%Y-%m-%d).html\`"
  echo ""
  if [[ "$FAIL" -gt 0 ]]; then
    echo "**RESULT: FAIL ($FAIL)** — Agent 须读 CEO-REROUTE 继续 GM loop；**勿**把未验完稿当终稿交 Owner。"
  else
    echo "**RESULT: PASS** — 完成多轮筛选→测试→再筛选；可交 Owner 阅读 HTML。"
  fi
} >"$REPORT"

echo ""
echo "Report: $REPORT"
if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL ceo-deep-delivery ($FAIL)"
  exit 1
fi
echo "RESULT: PASS ceo-deep-delivery"
exit 0
