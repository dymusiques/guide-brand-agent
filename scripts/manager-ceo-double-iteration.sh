#!/usr/bin/env bash
# CEO Senior Manager loop: iteration 1 → (AI: analyze + ITERATION-LOG) → iteration 2.
# NOT the same as auto-gate default 3 rounds or CEO_DEEP_ROUNDS=2.
# See agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"

BRIEF=""
PHASE=""
LOG=""

usage() {
  echo "Usage: bash scripts/manager-ceo-double-iteration.sh --brief PATH --phase 1|2 [--iteration-log PATH]"
  echo "  phase 1: run gate --max-rounds 1; then AI Must fill ITERATION-LOG (iter 1 analyze) before phase 2"
  echo "  phase 2: verify ITERATION-LOG; run gate --max-rounds 1 again"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --brief) BRIEF="${2:-}"; shift 2 ;;
    --phase) PHASE="${2:-}"; shift 2 ;;
    --iteration-log) LOG="${2:-}"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done

[[ -n "$BRIEF" && -f "$BRIEF" ]] || { echo "FAIL: --brief required"; exit 1; }
[[ "$PHASE" == "1" || "$PHASE" == "2" ]] || { echo "FAIL: --phase 1 or 2 required"; exit 1; }

slug="$(basename "$BRIEF" .md)"
slug="${slug%-brief}"
EVO="$ROOT/content/evolution/04-xhs-topic-manager/$slug"
mkdir -p "$EVO"
STATE="$EVO/.ceo-double-iteration-state.json"
if [[ -z "$LOG" ]]; then
  LOG="$EVO/ITERATION-LOG.md"
fi

echo "=== CEO double iteration · phase $PHASE · $BRIEF ==="
echo "Consult SOP: agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md"
echo "ITERATION-LOG: ${LOG#"$ROOT/"}"

if [[ "$PHASE" == "1" ]]; then
  echo ""
  echo ">>> phase 1 · gate --max-rounds 1"
  set +e
  bash scripts/manager-ceo-auto-gate-loop.sh --brief "$BRIEF" --max-rounds 1
  EC=$?
  set -e
  LATEST_LOG="$(ls -t "$ROOT/content/xiaohongshu/verify-logs/"* 2>/dev/null | head -1 || true)"
  "$PY" - <<PY
import json
from datetime import datetime, timezone
from pathlib import Path
state = {
  "brief": "$BRIEF",
  "phase": 1,
  "gate_exit": $EC,
  "verify_log": "$LATEST_LOG",
  "at": datetime.now(timezone.utc).isoformat(),
}
Path("$STATE").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
PY
  if [[ ! -f "$LOG" ]]; then
    cat >"$LOG" <<EOF
# ITERATION-LOG · $slug · $(date +%Y-%m-%d)

- Owner 口令：CEO double iteration phase 1 complete
- 已读 SOP：CEO-DOUBLE-ITERATION-SOP.md §1
- 基线分：见 verify-logs · gate exit=$EC

## 迭代 1

- 提案：（§3 · AI 必填）
- 改后分：
- 分析（Analyze · PASS/FAIL 均写）：
- 迭代 2 将只改：

## 迭代 2

- Consult：已读迭代 1 分析
- 提案：（须引用迭代 1 分析）
- 改后分：
- 分析：
EOF
    echo ">>> created stub ITERATION-LOG — AI Must complete before --phase 2"
  fi
  echo ""
  if [[ "$EC" -eq 0 ]]; then
    echo "RESULT: phase 1 gate PASS — still Must write iter-1 分析 in ITERATION-LOG before phase 2"
  else
    echo "RESULT: phase 1 gate FAIL — fill 提案 + 分析 + 改稿, then --phase 2"
  fi
  exit "$EC"
fi

# phase 2
"$PY" scripts/verify-ceo-iteration-log.py --log "$LOG" || exit 1
echo ""
echo ">>> phase 2 · gate --max-rounds 1 (changes Must be based on iter-1 分析)"
set +e
bash scripts/manager-ceo-auto-gate-loop.sh --brief "$BRIEF" --max-rounds 1
EC=$?
set -e
"$PY" - <<PY
import json
from datetime import datetime, timezone
from pathlib import Path
p = Path("$STATE")
state = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
state.update({"phase": 2, "gate_exit_phase2": $EC, "at_phase2": datetime.now(timezone.utc).isoformat()})
p.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
PY
if [[ "$EC" -eq 0 ]]; then
  echo "RESULT: PASS ceo-double-iteration phase 2"
else
  echo "RESULT: FAIL ceo-double-iteration phase 2 — see CEO-REROUTE / ITERATION-LOG"
fi
exit "$EC"
