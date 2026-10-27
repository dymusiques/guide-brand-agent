#!/usr/bin/env bash
# Owner: run ONCE in Terminal.app to wire background baseline + evaluator + verify loop.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== setup background goal-evolution loop ==="
bash scripts/ensure-venv-deps.sh

if [[ -d vendor/process-launcher ]] && ! command -v process-launcher >/dev/null 2>&1; then
  echo "Installing process-launcher into .venv..."
  .venv/bin/pip install -e 'vendor/process-launcher[dev]' -q
fi
if ! command -v process-launcher >/dev/null 2>&1 && [[ -x .venv/bin/process-launcher ]]; then
  export PATH="$ROOT/.venv/bin:$PATH"
fi
if ! command -v process-launcher >/dev/null 2>&1; then
  echo "WARN: process-launcher CLI not on PATH — pip install -e vendor/process-launcher[dev] then start manually"
fi

chmod +x scripts/background-goal-evolution-cycle.sh \
  scripts/background-goal-evolution-loop.sh \
  scripts/evolution-rollups-all.sh \
  scripts/setup-background-goal-evolution.sh

TPL="$ROOT/integration/templates/dba-launcher-goal-evolution.yaml"
OUT="$ROOT/vendor/process-launcher/config/dba-brand-agent.yaml"
sed "s|__REPO_ROOT__|$ROOT|g" "$TPL" >"$OUT"

echo ""
echo "=== Setup complete ==="
echo ""
echo "Wrote: vendor/process-launcher/config/dba-brand-agent.yaml"
echo "Schedule: daily 09:00 Asia/Shanghai (dba_goal_evolution_daily + 6 case)"
echo "Cycle contents: docs/BACKGROUND-GOAL-EVOLUTION.md §「一轮 cycle」"
echo "Interval changes: integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md (Agent must ask Owner)"
echo ""
PL="$ROOT/.venv/bin/process-launcher"
echo "Start ONCE from Terminal.app / iTerm2:"
echo ""
echo "  cd \"$ROOT/vendor/process-launcher\""
echo "  \"$PL\" start --config config/dba-brand-agent.yaml"
echo ""
echo "(process-launcher is in .venv — not on global PATH unless you activate venv)"
echo ""
echo "Docs: docs/BACKGROUND-GOAL-EVOLUTION.md"
echo "Owner ongoing: 发帖 + CSV → content/analytics/inbox/ only."
