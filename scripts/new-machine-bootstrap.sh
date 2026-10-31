#!/usr/bin/env bash
# One-shot new machine / new Agent · after git clone (Owner: 完全克隆 / danying-brand-agent).
# Does NOT configure OAuth, MCP, or Gemini — see SETUP.md §3–4.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== new-machine-bootstrap · $ROOT ==="
echo ""

bash scripts/ensure-venv-deps.sh

if [[ -f .gitmodules ]]; then
  git submodule update --init --recursive 2>/dev/null || echo "WARN: submodule update — fix manually if needed"
fi

echo "-------- background goal-evolution config --------"
bash scripts/ensure-background-goal-evolution.sh
bash scripts/ensure-process-launcher.sh || true
echo ""

FAIL=0
if bash scripts/verify-handoff.sh; then echo ">>> verify-handoff: PASS"; else echo ">>> verify-handoff: WARN/FAIL"; FAIL=$((FAIL + 1)); fi
echo ""

if bash scripts/verify-agent-takeover.sh; then echo ">>> verify-agent-takeover: PASS"; else FAIL=$((FAIL + 1)); fi
echo ""

if bash scripts/manager-autopilot.sh; then echo ">>> manager-autopilot: PASS"; else FAIL=$((FAIL + 1)); fi
echo ""

PL="$ROOT/.venv/bin/process-launcher"
CFG="$ROOT/vendor/process-launcher/config/dba-brand-agent.yaml"
if [[ -x "$PL" && -f "$CFG" ]]; then
  if curl -sf "http://127.0.0.1:7997/health" >/dev/null 2>&1 || curl -sf "http://127.0.0.1:7997/" >/dev/null 2>&1; then
    echo ">>> process-launcher: already reachable on :7997"
  else
    echo ">>> process-launcher: not running — start once (Terminal.app or nohup):"
    echo "    cd \"$ROOT/vendor/process-launcher\" && \"$PL\" start --config config/dba-brand-agent.yaml"
    echo "    (Daily 09:00 cycle · docs/BACKGROUND-GOAL-EVOLUTION.md)"
  fi
else
  echo "WARN: process-launcher or config missing — run: bash scripts/setup-background-goal-evolution.sh"
fi

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  echo "RESULT: PASS new-machine-bootstrap"
else
  echo "RESULT: PASS with warnings ($FAIL) — read output above"
fi
echo ""
echo "Owner 口语：本仓已植入。Cursor 说「请 CEO 开始工作」即可 · docs/CEO-OWNER-ONE-LINE-TRIGGERS.md"
exit 0
