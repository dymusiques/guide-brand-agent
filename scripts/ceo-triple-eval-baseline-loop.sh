#!/usr/bin/env bash
# Three evaluate rounds: gate → gap → edit-distance. See docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
BRIEF=""
MAX="${CEO_TRIPLE_EVAL_MAX:-3}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --brief) BRIEF="${2:-}"; shift 2 ;;
    --max) MAX="${2:-3}"; shift 2 ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done
[[ -n "$BRIEF" && -f "$BRIEF" ]] || { echo "FAIL: --brief required"; exit 1; }
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
slug="$(basename "$BRIEF" -brief.md)"
evo="$ROOT/content/evolution/04-xhs-topic-manager/$slug"
mkdir -p "$evo/versions" "$evo/reference"

round=1
while [[ "$round" -le "$MAX" ]]; do
  echo "=== ceo-triple-eval · round $round/$MAX · $BRIEF ==="
  if ! bash scripts/manager-ceo-gate-one-round.sh --brief "$BRIEF"; then
    echo "NEEDS_WORK: gate round $round FAIL (exit 42)" >&2
    exit 42
  fi
  bash scripts/verify-xhs-clever-advocate.sh --brief "$BRIEF" || {
    echo "NEEDS_WORK: clever-advocate round $round FAIL" >&2
    exit 42
  }
  "$PY" scripts/analyze-brief-evolution-gap.py --brief "$BRIEF" || true
  if [[ -f "$evo/reference/gold-body.md" ]]; then
    "$PY" scripts/evaluate-edit-distance.py \
      --candidate "$BRIEF" \
      --reference "$evo/reference/gold-body.md" \
      --label "triple-eval-r${round}" \
      --append "$evo/metrics.jsonl" 2>/dev/null || true
  elif [[ -f "$evo/reference/gold.md" ]]; then
    "$PY" scripts/evaluate-edit-distance.py \
      --candidate "$BRIEF" \
      --reference "$evo/reference/gold.md" \
      --label "triple-eval-r${round}" \
      --append "$evo/metrics.jsonl" 2>/dev/null || true
  fi
  if grep -q '`READY`' "$evo/EVOLUTION-GAP-latest.md" 2>/dev/null; then
    echo "RESULT: PASS ceo-triple-eval READY round=$round"
    exit 0
  fi
  round=$((round + 1))
done
echo "RESULT: FAIL ceo-triple-eval max rounds ($MAX) NEEDS_WORK" >&2
exit 42
