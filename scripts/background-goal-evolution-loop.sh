#!/usr/bin/env bash
# Legacy interval loop — NOT default (Owner 2026-10-27: daily job). See BACKGROUND-CYCLE-INTERVAL-TRIGGER.md before re-enabling.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
INTERVAL="${GOAL_EVOLUTION_INTERVAL_SEC:-1800}"
DEEP_EVERY="${GOAL_EVOLUTION_DEEP_EVERY_CYCLES:-48}"
cycle=0

echo "goal-evolution loop · interval=${INTERVAL}s · cwd=$ROOT"
while true; do
  cycle=$((cycle + 1))
  if [[ $((cycle % DEEP_EVERY)) -eq 0 ]]; then
    export GOAL_EVOLUTION_DEEP=1
  else
    export GOAL_EVOLUTION_DEEP=0
  fi
  echo "-------- loop cycle $cycle (DEEP=$GOAL_EVOLUTION_DEEP) --------"
  bash "$ROOT/scripts/background-goal-evolution-cycle.sh" || true
  sleep "$INTERVAL"
done
