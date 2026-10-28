#!/usr/bin/env bash
# One background cycle: standards verify + baseline/evolution metrics + CEO work queue.
# Invoked by process-launcher daily job (setup-background-goal-evolution.sh). Owner does not run manually.
# Schedule / interval: integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash "$ROOT/scripts/ensure-venv-deps.sh"
export PATH="$ROOT/.venv/bin:${PATH:-}"

STAMP="$(date +%Y%m%d-%H%M%S)"
INBOX="$ROOT/content/evolution/00-manager/ceo-inbox"
DERIVED="$ROOT/content/analytics/derived"
mkdir -p "$INBOX" "$DERIVED"
LOG="$INBOX/background-cycle-$STAMP.log"
LATEST="$INBOX/background-cycle-latest.md"
JSON="$DERIVED/background-cycle-latest.json"

exec > >(tee -a "$LOG") 2>&1
echo "=== background-goal-evolution-cycle · $STAMP ==="

FAIL=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }
skip() { echo "SKIP: $1"; }

run() {
  local name="$1"
  shift
  if "$@"; then pass "$name"; else fail "$name"; fi
}

PY=".venv/bin/python"
[[ -x "$PY" ]] || PY="python3"

# --- Standards (faithful to verify map) ---
run "verify-collector-evaluator" bash scripts/verify-collector-evaluator.sh
run "verify-xhs-content-intake" bash scripts/verify-xhs-content-intake.sh
run "ensure-redteam-pre all" "$PY" scripts/ensure-redteam-pre.py --all
if [[ -f .env ]] || [[ -n "${GEMINI_API_KEY:-}" ]]; then
  run "xhs-briefs-auto-pipeline" bash scripts/manager-xhs-briefs-auto-pipeline.sh
else
  skip "xhs-briefs-auto-pipeline (no GEMINI_API_KEY)"
fi
run "verify-goals M4" bash scripts/verify-goals.sh

# Gemini 6 case: daily depth only (expensive)
if [[ "${GOAL_EVOLUTION_DEEP:-0}" == "1" ]]; then
  run "verify-xhs-topic 6case" bash scripts/verify-xhs-topic.sh
fi

# --- 09 / CEO dispatch (no Owner prompt) ---
INBOX_CSV="$ROOT/content/analytics/inbox"
HAS_CSV=false
if [[ -d "$INBOX_CSV" ]]; then
  shopt -s nullglob
  csvs=("$INBOX_CSV"/*.csv)
  shopt -u nullglob
  [[ ${#csvs[@]} -gt 0 ]] && HAS_CSV=true
fi
if $HAS_CSV || [[ -f "$ROOT/content/analytics/xiaohongshu/notes.csv" ]]; then
  run "analytics-pipeline" bash scripts/analytics-pipeline.sh
else
  skip "analytics-pipeline (no CSV)"
  bash scripts/analytics-pipeline.sh --demo >/dev/null 2>&1 || true
fi

run "ceo-dispatch-refresh" "$PY" scripts/ceo-dispatch-refresh.py
run "manager-dashboard" bash scripts/manager-dashboard.sh

# --- Baseline + Evaluator rollups ---
run "evolution-rollups-all" bash scripts/evolution-rollups-all.sh

# --- Daily GM trio (10/11/12 · CEO 日更子链) ---
run "daily-gm-trio" bash scripts/run-daily-gm-trio.sh

# --- Work queue for Cursor CEO (no Owner utterance) ---
QUEUE="$INBOX/agent-work-queue.md"
{
  echo "# Agent work queue · auto · $STAMP"
  echo ""
  echo "## Brief hygiene (auto ensure-redteam + complete gate in cycle)"
  echo "- pipeline: \`bash scripts/manager-xhs-briefs-auto-pipeline.sh\`"
  while IFS= read -r brief; do
    base=$(basename "$brief" -brief.md)
    pre="$ROOT/content/xiaohongshu/redteam/${base}-pre.md"
    if [[ ! -f "$pre" ]]; then
      echo "- STILL MISSING redteam-pre: \`$brief\` (ensure-redteam should have run)"
    fi
  done < <(find "$ROOT/content/xiaohongshu" -maxdepth 1 -name '*-brief.md' 2>/dev/null | sort)

  echo ""
  echo "## Evolution slugs (metrics present)"
  find content/evolution -name metrics.jsonl 2>/dev/null | head -20 | while read -r m; do echo "- \`$m\`"; done

  echo ""
  echo "## Last cycle log"
  echo "\`content/evolution/00-manager/ceo-inbox/background-cycle-$STAMP.log\`"
} >"$QUEUE"

# SEO non-blocking
"$PY" scripts/seo-lint-xhs-briefs.py >/dev/null 2>&1 && pass "seo-lint" || skip "seo-lint warnings"

{
  echo "# Background cycle · $STAMP"
  echo ""
  echo "- failures: $FAIL"
  echo "- rollups: \`content/analytics/derived/evolution-rollups-latest.md\`"
  echo "- queue: \`content/evolution/00-manager/ceo-inbox/agent-work-queue.md\`"
  echo "- dispatch: \`content/analytics/derived/ceo-dispatch-latest.md\`"
  if [[ "$FAIL" -gt 0 ]]; then
    echo ""
    echo "**RESULT: FAIL** — see log; Cursor CEO should REROUTE GM on next session (Owner not asked to verify)."
  else
    echo ""
    echo "**RESULT: PASS**"
  fi
} >"$LATEST"

"$PY" - <<PY
import json, datetime
from pathlib import Path
p = Path("$JSON")
p.write_text(json.dumps({
  "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "failures": $FAIL,
  "log": "content/evolution/00-manager/ceo-inbox/background-cycle-$STAMP.log",
}, indent=2), encoding="utf-8")
PY

if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL ($FAIL)"
  exit 1
fi
echo "RESULT: PASS"
exit 0
