#!/usr/bin/env bash
# Per-agent or full 10×6 integration matrix (glue + shells + goals).
# Usage:
#   bash scripts/verify-agent-matrix.sh
#   bash scripts/verify-agent-matrix.sh --agent 04
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1; fi

AGENT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent) AGENT="$2"; shift 2 ;;
    *) echo "Unknown: $1"; exit 2 ;;
  esac
done

echo "=== Goal registry (6) ==="
"$PY" integration/tests/test_goals_registry.py
echo ""

if [[ -n "$AGENT" ]]; then
  exec "$PY" integration/tests/test_agents_matrix.py --agent "$AGENT"
fi
exec "$PY" integration/tests/test_agents_matrix.py
