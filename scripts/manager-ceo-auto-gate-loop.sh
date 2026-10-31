#!/usr/bin/env bash
# CEO auto gate loop — redteam + complete gate + reroute (no Owner). See docs/BRIEF-AUTO-GATE-PIPELINE.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"

BRIEF=""
MAX="${CEO_GATE_MAX_ROUNDS:-3}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --brief) BRIEF="${2:-}"; shift 2 ;;
    --max-rounds) MAX="${2:-3}"; shift 2 ;;
    -h|--help)
      echo "Usage: bash scripts/manager-ceo-auto-gate-loop.sh --brief content/xiaohongshu/foo-brief.md"
      exit 0
      ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done
[[ -n "$BRIEF" && -f "$BRIEF" ]] || { echo "FAIL: --brief required"; exit 1; }

INBOX="$ROOT/content/evolution/00-manager/ceo-inbox"
mkdir -p "$INBOX"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG="$INBOX/auto-gate-loop-$STAMP.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== manager-ceo-auto-gate-loop · $BRIEF · max=$MAX ==="

brief_hash() {
  if command -v md5 >/dev/null 2>&1; then md5 -q "$BRIEF"
  else md5sum "$BRIEF" | awk '{print $1}'; fi
}
round=1
while [[ "$round" -le "$MAX" ]]; do
  HASH_BEFORE="$(brief_hash)"
  echo "--- round $round/$MAX ---"
  "$PY" scripts/ensure-redteam-pre.py --brief "$BRIEF"
  "$PY" scripts/run-xhs-brief-adversarial-challenge.py --brief "$BRIEF" || true

  set +e
  "$PY" scripts/evaluate-xhs-brief-complete.py --brief "$BRIEF" --skip-kernel-six
  EC=$?
  set -e

  if [[ "$EC" -eq 0 ]]; then
    bash scripts/verify-xhs-topic.sh && {
      echo "RESULT: PASS auto-gate-loop round=$round"
      exit 0
    }
    EC=1
  fi

  LATEST_LOG="$(ls -t "$ROOT/content/xiaohongshu/verify-logs/"* 2>/dev/null | head -1 || true)"
  "$PY" scripts/ceo-auto-fix-brief.py --brief "$BRIEF" --round "$round" ${LATEST_LOG:+--report-json "$LATEST_LOG"}
  "$PY" scripts/ceo-action-needed-refresh.py >/dev/null 2>&1 || true

  HASH_AFTER="$(brief_hash)"
  if [[ "$HASH_BEFORE" == "$HASH_AFTER" && "${CEO_GATE_BRUTE_FORCE:-0}" != "1" ]]; then
    echo "RESULT: FAIL auto-gate-loop round=$round — Brief unchanged; AGENT_MUST_EDIT (exit 42)"
    echo "Read: content/evolution/00-manager/ceo-inbox/ceo-action-needed.md"
    exit 42
  fi
  round=$((round + 1))
done

"$PY" scripts/ceo-action-needed-refresh.py >/dev/null 2>&1 || true
echo "RESULT: FAIL auto-gate-loop after $MAX rounds — see CEO-REROUTE; do NOT hand Owner unverified brief"
exit 1
