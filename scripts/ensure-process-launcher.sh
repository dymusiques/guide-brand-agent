#!/usr/bin/env bash
# Start process-launcher if config exists and :7997 is down. Idempotent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PL="$ROOT/.venv/bin/process-launcher"
CFG="$ROOT/vendor/process-launcher/config/dba-brand-agent.yaml"
LOG="$ROOT/content/evolution/00-manager/ceo-inbox/process-launcher-nohup.log"

if [[ ! -x "$PL" || ! -f "$CFG" ]]; then
  echo "SKIP ensure-process-launcher — missing binary or config (run ensure-background-goal-evolution.sh)"
  exit 0
fi

if curl --max-time 2 -sf http://127.0.0.1:7997/health >/dev/null 2>&1; then
  echo "OK ensure-process-launcher · :7997 healthy"
  exit 0
fi

mkdir -p "$(dirname "$LOG")"
echo ">>> ensure-process-launcher · starting nohup (log: ${LOG#"$ROOT/"})"
(
  cd "$ROOT/vendor/process-launcher"
  nohup "$PL" start --config config/dba-brand-agent.yaml >>"$LOG" 2>&1 &
)
sleep 2
if curl --max-time 3 -sf http://127.0.0.1:7997/health >/dev/null 2>&1; then
  echo "OK ensure-process-launcher · started"
  exit 0
fi
echo "WARN ensure-process-launcher · start attempted but :7997 not up — Owner Terminal or see $LOG"
exit 0
