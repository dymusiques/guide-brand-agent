#!/usr/bin/env bash
# After Agent writes *-brief.md: evolution + HTML + verify (+ optional round2).
# Owner gives topic in chat → Agent writes brief → Must run this (or run_ceo_xhs_autopilot.py).
# See docs/CEO-XHS-NEW-BRIEF-AUTOPILOT.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
BRIEF=""
ROUND2=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --brief) BRIEF="${2:-}"; shift 2 ;;
    --round2) ROUND2=1; shift ;;
    -h|--help)
      echo "Usage: bash scripts/ceo-new-xhs-brief-pipeline.sh --brief content/xiaohongshu/YYYY-MM-DD-slug-brief.md [--round2]"
      exit 0
      ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done
[[ -n "$BRIEF" && -f "$BRIEF" ]] || { echo "FAIL: --brief required"; exit 1; }
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
export CEO_OWNER_EXTRA_BRIEF="$BRIEF"
export CEO_OWNER_HTML_HASH="#owner-latest"
GOAL="${CEO_OWNER_GOAL:-Owner 新小红书 Brief}"
ARGS=(scripts/run_ceo_full_execution.py --goal "$GOAL" --no-discovery-auto --brief "$BRIEF")
[[ "$ROUND2" -eq 1 ]] && ARGS+=(--round2)
exec "$PY" "${ARGS[@]}"
