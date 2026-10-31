#!/usr/bin/env bash
# Owner Mandate §2: gate + gap analyze loop until READY or max rounds. No Owner confirm.
# See docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"

BRIEF=""
MAX="${CEO_EVOLUTION_MAX_ROUNDS:-6}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --brief) BRIEF="${2:-}"; shift 2 ;;
    --max-rounds) MAX="${2:-6}"; shift 2 ;;
    -h|--help)
      echo "Usage: bash scripts/manager-brief-evolution-until-gap.sh --brief content/xiaohongshu/foo-brief.md"
      exit 0
      ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done
[[ -n "$BRIEF" && -f "$BRIEF" ]] || { echo "FAIL: --brief required"; exit 1; }

brief_hash() {
  if command -v md5 >/dev/null 2>&1; then md5 -q "$BRIEF"
  else md5sum "$BRIEF" | awk '{print $1}'; fi
}

SLUG="$(basename "$BRIEF" -brief.md)"
EVO="$ROOT/content/evolution/04-xhs-topic-manager/$SLUG"
mkdir -p "$EVO"
STATE="$EVO/.evolution-round.state"
ROUND=1
[[ -f "$STATE" ]] && ROUND="$(cat "$STATE" 2>/dev/null || echo 1)"

echo "=== manager-brief-evolution-until-gap · $BRIEF · round=$ROUND max=$MAX ==="

HASH_BEFORE="$(brief_hash)"
set +e
bash scripts/manager-ceo-gate-one-round.sh --brief "$BRIEF"
GATE_EC=$?
set -e

"$PY" scripts/analyze-brief-evolution-gap.py --brief "$BRIEF"
GAP_EC=$?

if [[ "$GAP_EC" -eq 0 ]]; then
  echo "RESULT: PASS evolution-until-gap READY round=$ROUND"
  rm -f "$STATE"
  exit 0
fi

ROUND=$((ROUND + 1))
echo "$ROUND" > "$STATE"

if [[ "$ROUND" -gt "$MAX" ]]; then
  echo "RESULT: FAIL evolution-until-gap after $MAX rounds — escalate Owner"
  rm -f "$STATE"
  exit 1
fi

HASH_AFTER="$(brief_hash)"
if [[ "$GATE_EC" -ne 0 || "$GAP_EC" -eq 42 ]]; then
  if [[ "$HASH_BEFORE" == "$HASH_AFTER" ]]; then
    echo "RESULT: NEEDS_WORK — Brief unchanged; read EVOLUTION-GAP-latest.md + CEO-REROUTE; substantive edit (exit 42)"
    exit 42
  fi
  echo "RESULT: NEEDS_WORK round=$((ROUND - 1)) — re-run after next substantive edit (exit 42)"
  exit 42
fi

echo "RESULT: FAIL unexpected gate=$GATE_EC gap=$GAP_EC"
exit 1
