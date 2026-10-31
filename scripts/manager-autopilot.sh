#!/usr/bin/env bash
# Full auto CEO cycle — excludes Owner-only: post + CSV ingest.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1
fi

echo "=== manager-autopilot (Owner: 发帖 + inbox CSV only) ==="
echo ""

step() {
  local t="$1"; shift
  echo "-------- $t --------"
  if "$@"; then echo ">>> $t: PASS"; else echo ">>> $t: FAIL"; return 1; fi
  echo ""
}

FAIL=0
run_optional() {
  local t="$1"; shift
  echo "-------- $t --------"
  if "$@"; then echo ">>> $t: PASS"; else echo ">>> $t: WARN (non-blocking)"; fi
  echo ""
}

run_optional "ensure background goal-evolution yaml" bash scripts/ensure-background-goal-evolution.sh

step "M4 · Goal verify" bash scripts/verify-goals.sh || FAIL=$((FAIL + 1))

step "CEO dashboard" bash scripts/manager-dashboard.sh || FAIL=$((FAIL + 1))

run_optional "SEO lint (XHS briefs)" "$PY" scripts/seo-lint-xhs-briefs.py

INBOX="$ROOT/content/analytics/inbox"
HAS_CSV=false
if [[ -d "$INBOX" ]]; then
  shopt -s nullglob
  csvs=("$INBOX"/*.csv)
  shopt -u nullglob
  if [[ ${#csvs[@]} -gt 0 ]]; then HAS_CSV=true; fi
fi

NOTES_CSV="$ROOT/content/analytics/xiaohongshu/notes.csv"
HAS_WAREHOUSE=false
if [[ -f "$NOTES_CSV" ]] && [[ $(wc -l < "$NOTES_CSV" | tr -d ' ') -gt 1 ]]; then
  HAS_WAREHOUSE=true
fi

if $HAS_CSV; then
  step "09 · Analytics pipeline (inbox CSV)" bash scripts/analytics-pipeline.sh || FAIL=$((FAIL + 1))
elif $HAS_WAREHOUSE; then
  step "09 · Analytics pipeline (warehouse notes.csv)" bash scripts/analytics-pipeline.sh || FAIL=$((FAIL + 1))
else
  echo "-------- 09 · Analytics (no inbox CSV) --------"
  echo ">>> SKIP live pipeline — Owner: drop CSV in content/analytics/inbox/"
  echo ">>> Running --demo to refresh derived + CEO dispatch"
  bash scripts/analytics-pipeline.sh --demo || true
  echo ""
fi

step "CEO dispatch block (09→04)" "$PY" scripts/ceo-dispatch-refresh.py || FAIL=$((FAIL + 1))

step "XHS briefs auto gate (redteam+L1×6+evaluate)" bash scripts/manager-xhs-briefs-auto-pipeline.sh || FAIL=$((FAIL + 1))

if [[ "${AUTOPILOT_FULL:-0}" == "1" ]]; then
  step "verify-all (CI tier)" env VERIFY_TIER=ci bash scripts/verify-all.sh || FAIL=$((FAIL + 1))
else
  echo "-------- verify-all --------"
  echo ">>> SKIP (set AUTOPILOT_FULL=1 for full CI verify-all)"
  echo ""
fi

echo "=== Owner 待办（系统不会自动做）==="
echo "  1. 发帖：见 content/analytics/derived/ceo-dispatch-latest.md"
echo "  2. 数据：导出 CSV → content/analytics/inbox/ → 再跑本脚本"
echo ""
echo "派活块：content/analytics/derived/ceo-dispatch-latest.md"
echo "仪表盘：content/analytics/derived/manager-dashboard-$(date +%Y-%m-%d).md"
echo ""

if [[ "$FAIL" -eq 0 && "${CEO_OWNER_HTML_REFRESH:-1}" == "1" ]]; then
  run_optional "Owner notify HTML" bash scripts/refresh-owner-notify-html.sh
fi

if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL — autopilot ($FAIL blocking step(s))"
  exit 1
fi
echo "RESULT: PASS — autopilot (Owner: optional HTML · Must post + CSV)"
