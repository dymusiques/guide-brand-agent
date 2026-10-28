#!/usr/bin/env bash
# Idempotent: write vendor/process-launcher/config/dba-brand-agent.yaml for this repo path.
# Called from new-machine-bootstrap, manager-autopilot, verify-handoff (warn if missing).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OUT="$ROOT/vendor/process-launcher/config/dba-brand-agent.yaml"
TPL="$ROOT/integration/templates/dba-launcher-goal-evolution.yaml"

need_write=0
if [[ ! -f "$OUT" ]]; then
  need_write=1
elif ! grep -q "$ROOT" "$OUT" 2>/dev/null; then
  need_write=1
fi

if [[ "$need_write" -eq 0 ]]; then
  echo "OK ensure-background-goal-evolution · config present for this repo"
  exit 0
fi

echo ">>> ensure-background-goal-evolution · writing config (repo path or missing yaml)"
bash scripts/setup-background-goal-evolution.sh
exit 0
