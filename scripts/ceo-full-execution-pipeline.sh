#!/usr/bin/env bash
# CEO full stack: recover + router + matrix + run_ceo_xhs_autopilot + HTML open.
# See docs/CEO-FULL-EXECUTION-MANDATE.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
exec "$PY" scripts/run_ceo_full_execution.py "$@"
