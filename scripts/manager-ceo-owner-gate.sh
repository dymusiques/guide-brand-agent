#!/usr/bin/env bash
# CEO Owner Gate — MUST PASS before presenting deliverables to Owner.
# See docs/CEO-AUTO-QA-LOOP.md
#
# Usage:
#   bash scripts/manager-ceo-owner-gate.sh --brief content/xiaohongshu/foo-brief.md
#   bash scripts/manager-ceo-owner-gate.sh --brief foo.md --voice content/xiaohongshu/foo-round1.md
#   bash scripts/manager-ceo-owner-gate.sh --brief foo.md --evolution content/evolution/04-xhs/slug
#   bash scripts/manager-ceo-owner-gate.sh --integration-only   # no Brief; matrix only
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BRIEF=""
VOICE=""
EVOLUTION=""
INTEGRATION_ONLY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --brief) BRIEF="${2:-}"; shift 2 ;;
    --voice) VOICE="${2:-}"; shift 2 ;;
    --evolution) EVOLUTION="${2:-}"; shift 2 ;;
    --integration-only) INTEGRATION_ONLY=1; shift ;;
    -h|--help)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 2
      ;;
  esac
done

INBOX="$ROOT/content/evolution/00-manager/ceo-inbox"
mkdir -p "$INBOX"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG="$INBOX/gate-$STAMP.log"
LATEST="$INBOX/gate-latest.md"

failures=()
run_check() {
  local name="$1"
  shift
  echo "=== $name ===" | tee -a "$LOG"
  if "$@" >>"$LOG" 2>&1; then
    echo "PASS: $name" | tee -a "$LOG"
    return 0
  fi
  echo "FAIL: $name" | tee -a "$LOG"
  failures+=("$name")
  return 0
}

echo "CEO Owner Gate · $STAMP" | tee "$LOG"
echo "cwd: $ROOT" >>"$LOG"
echo "" >>"$LOG"

if [[ "$INTEGRATION_ONLY" == 1 && -z "$BRIEF" ]]; then
  run_check "verify-manager-integration" bash scripts/verify-manager-integration.sh
elif [[ -n "$BRIEF" ]]; then
  if [[ ! -f "$BRIEF" ]]; then
    echo "FAIL: Brief not found: $BRIEF" | tee -a "$LOG"
    failures+=("brief-missing")
  else
    PY=""
    if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
    elif command -v python3 >/dev/null 2>&1; then PY="python3"
    fi
    if [[ -n "$PY" ]]; then
      run_check "auto-gate-loop" bash scripts/manager-ceo-auto-gate-loop.sh --brief "$BRIEF"
      run_check "seo-lint-brief" "$PY" scripts/seo-lint-xhs-briefs.py "$BRIEF"
    else
      run_check "manager-workflow-verify" bash scripts/manager-workflow-verify.sh "$BRIEF"
    fi
  fi
else
  echo "(no --brief; use --integration-only or pass --brief for full Owner gate)" | tee -a "$LOG"
  failures+=("no-brief-or-integration-only")
fi

if [[ -n "$VOICE" ]]; then
  if [[ ! -f "$VOICE" ]]; then
    echo "FAIL: voice file not found: $VOICE" | tee -a "$LOG"
    failures+=("voice-missing")
  else
    run_check "verify-xhs-voice-qa" bash scripts/verify-xhs-voice-qa.sh "$VOICE"
  fi
fi

if [[ -n "$EVOLUTION" ]]; then
  if [[ ! -d "$EVOLUTION" ]]; then
    echo "FAIL: evolution dir not found: $EVOLUTION" | tee -a "$LOG"
    failures+=("evolution-missing")
  else
    METRICS="$EVOLUTION/metrics.jsonl"
    if [[ -f "$METRICS" ]]; then
      run_check "evolution-metrics-summary" python3 scripts/evolution-metrics-summary.py "$METRICS"
    else
      echo "SKIP: no metrics.jsonl in $EVOLUTION" | tee -a "$LOG"
    fi
    if [[ ! -f "$EVOLUTION/reference/gold.md" ]]; then
      echo "NOTE: no reference/gold.md — edit-distance gate skipped (Owner gold TBD)" | tee -a "$LOG"
    fi
  fi
fi

{
  echo "# CEO Owner Gate · $STAMP"
  echo ""
  echo "- brief: \`${BRIEF:-—}\`"
  echo "- voice: \`${VOICE:-—}\`"
  echo "- evolution: \`${EVOLUTION:-—}\`"
  echo "- log: \`content/evolution/00-manager/ceo-inbox/gate-$STAMP.log\`"
  echo ""
  if ((${#failures[@]} == 0)); then
    echo "**RESULT: PASS** — CEO flow closed (routine: Owner notify HTML only; see OWNER-DELIVERY-NOTIFY-DEFAULT.md)."
  else
    echo "**RESULT: FAIL** — CEO must CEO-REROUTE to GM; do **not** ask Owner to verify."
    echo ""
    echo "Failed checks:"
    for f in "${failures[@]}"; do
      echo "- $f"
    done
    echo ""
    echo "Template: \`content/evolution/_template/CEO-REROUTE.md\`"
  fi
} >"$LATEST"

if ((${#failures[@]} > 0)); then
  echo ""
  echo "RESULT: FAIL — ${failures[*]}"
  echo "See $LATEST and $LOG"
  exit 1
fi

if [[ "${CEO_OWNER_HTML_REFRESH:-1}" == "1" ]]; then
  bash "$ROOT/scripts/refresh-owner-notify-html.sh" || true
fi
echo ""
echo "RESULT: PASS — Owner gate complete (routine 交 Owner：否 · HTML refreshed if enabled)"
echo "See $LATEST"
