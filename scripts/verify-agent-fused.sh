#!/usr/bin/env bash
# Fused verify per agent: A (matrix 00-09) + B (kernel Gemini 04/05) + C (daily-gm L1 10-12).
# Shared gold: kernels/daily-gm/shared_gold.py · adversarial + IP brief.
#
# Usage:
#   bash scripts/verify-agent-fused.sh --agent 04
#   bash scripts/verify-agent-fused.sh --agent 11 --with-artifacts
#   bash scripts/verify-agent-fused.sh --agent all-daily   # 10+11+12 L1 only
#   bash scripts/verify-agent-fused.sh --agent all-09       # matrix 00-09 only
#
# B-layer Gemini: skipped when SKIP_GEMINI=1 or no .env key (same as verify-all).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1; fi

AGENT=""
WITH_ARTIFACTS=0
DATE="${VERIFY_FUSED_DATE:-$(date +%Y-%m-%d)}"
SKIP_GEMINI="${SKIP_GEMINI:-0}"
if [[ ! -f .env ]] && [[ -z "${GEMINI_API_KEY:-}" ]]; then
  SKIP_GEMINI=1
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent) AGENT="$2"; shift 2 ;;
    --with-artifacts) WITH_ARTIFACTS=1; shift ;;
    --date) DATE="$2"; shift 2 ;;
    *) echo "Unknown: $1"; exit 2 ;;
  esac
done

[[ -n "$AGENT" ]] || { echo "Usage: --agent NN|all-09|all-daily|04|05|10|11|12"; exit 2; }

FAIL=0
layer() {
  local name="$1"
  shift
  if "$@"; then echo ">>> fused $name: PASS"
  else echo ">>> fused $name: FAIL"; FAIL=$((FAIL + 1)); fi
}

run_a_matrix() {
  local id="$1"
  bash scripts/verify-agent-matrix.sh --agent "$id"
}

run_b_xhs_kernel() {
  if [[ "$SKIP_GEMINI" == "1" ]]; then
    echo ">>> fused B (05 Gemini 6): SKIP (SKIP_GEMINI or no key)"
    return 0
  fi
  bash scripts/verify-xhs-topic.sh
}

run_c_l1() {
  local id="$1"
  case "$id" in
    10) "$PY" kernels/daily-gm/tests/test_artist_benchmark_6.py ;;
    11) "$PY" kernels/daily-gm/tests/test_ip_daily_eval_6.py ;;
    12) "$PY" kernels/daily-gm/tests/test_owner_daily_brief_6.py ;;
    *) echo "no L1 for agent $id"; return 1 ;;
  esac
}

validate_artifacts() {
  local id="$1"
  case "$id" in
    10)
      local found=0
      shopt -s nullglob
      for f in "$ROOT/content/evolution/10-artist-intel/$DATE"/*/versions/v0-benchmark.json; do
        found=1
        if ! "$PY" -c "
import json, sys
sys.path.insert(0, 'kernels/daily-gm')
from artist_benchmark_schema import validate_payload
d=json.load(open('$f'))
e=validate_payload(d)
sys.exit(0 if not e else 1)
"; then return 1; fi
      done
      shopt -u nullglob
      if [[ "$found" -eq 0 ]]; then
        echo "WARN: no GM10 v0-benchmark.json for $DATE (Gemini may have skipped)"
        return 0
      fi
      ;;
    11)
      local base="$ROOT/content/evolution/11-ip-daily-eval/$DATE"
      [[ -f "$base/versions/v0-eval.json" ]] || { echo "missing v0-eval.json"; return 1; }
      [[ -f "$base/challenge-log.md" ]] || { echo "missing challenge-log.md"; return 1; }
      [[ -f "$base/reference/gold.md" ]] || { echo "missing reference/gold.md"; return 1; }
      "$PY" -c "
import json, sys
from pathlib import Path
sys.path.insert(0, 'kernels/daily-gm')
from ip_daily_eval_schema import validate_eval_doc, validate_challenge_log, validate_gold_reference
root = Path('$base')
ev = json.loads((root/'versions/v0-eval.json').read_text())
errs = validate_eval_doc(ev)
errs += validate_challenge_log((root/'challenge-log.md').read_text())
errs += validate_gold_reference((root/'reference/gold.md').read_text())
if errs:
    print(errs); sys.exit(1)
"
      ;;
    12)
      local brief="$ROOT/content/daily-brief/${DATE}-owner-daily-brief.md"
      [[ -f "$brief" ]] || { echo "missing owner daily brief"; return 1; }
      "$PY" -c "
import sys
from pathlib import Path
sys.path.insert(0, 'kernels/daily-gm')
from owner_daily_brief_schema import validate_brief_markdown
t = Path('$brief').read_text()
errs = validate_brief_markdown(t)
if errs:
    print(errs); sys.exit(1)
"
      ;;
  esac
}

fuse_one() {
  local raw="$1"
  local id
  id="$(printf '%02d' "$((10#$raw))")"

  echo ""
  echo "######## verify-agent-fused · agent $id · date=$DATE ########"

  if [[ "$id" =~ ^(0[0-9])$ ]]; then
    layer "A matrix" run_a_matrix "$id"
    if [[ "$id" == "04" || "$id" == "05" ]]; then
      layer "B XHS kernel (04/05 → 05)" run_b_xhs_kernel
    fi
    return 0
  fi

  if [[ "$id" == "10" || "$id" == "11" || "$id" == "12" ]]; then
    layer "C L1 six-case" run_c_l1 "$id"
    if [[ "$WITH_ARTIFACTS" -eq 1 ]]; then
      layer "C artifacts+hygiene" validate_artifacts "$id"
    fi
    return 0
  fi

  echo "Unknown agent id: $id"
  return 1
}

case "$AGENT" in
  all-09)
    layer "A matrix full" bash scripts/verify-agent-matrix.sh
    ;;
  all-daily)
    for id in 10 11 12; do
      fuse_one "$id" || FAIL=$((FAIL + 1))
    done
    ;;
  *)
    fuse_one "$AGENT" || FAIL=$((FAIL + 1))
    ;;
esac

echo ""
echo "=== verify-agent-fused summary (agent=$AGENT SKIP_GEMINI=$SKIP_GEMINI) ==="
if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL"
  exit 1
fi
echo "RESULT: PASS"
exit 0
