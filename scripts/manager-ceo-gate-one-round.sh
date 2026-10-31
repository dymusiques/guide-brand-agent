#!/usr/bin/env bash
# One gate round — for Cursor Agent loop. See docs/WORKFLOW-AUTOMATION-MATRIX.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
exec bash scripts/manager-ceo-auto-gate-loop.sh --max-rounds 1 "$@"
