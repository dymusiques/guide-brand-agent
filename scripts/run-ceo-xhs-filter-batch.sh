#!/usr/bin/env bash
# CEO overnight batch: XHS filter + Gmail notify. Owner deadline: same-day 24:00 Asia/Shanghai.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
export PATH="$ROOT/.venv/bin:${PATH:-}"
PY="$ROOT/.venv/bin/python"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG="$ROOT/content/evolution/00-manager/ceo-inbox/ceo-xhs-filter-run-$STAMP.log"
exec >>"$LOG" 2>&1
echo "=== run-ceo-xhs-filter-batch · $STAMP ==="
echo ">>> upgraded: run-ceo-deep-delivery-cycle.sh (multi-round 筛选→测试→再筛选)"

bash scripts/run-ceo-deep-delivery-cycle.sh
