#!/usr/bin/env bash
# GM10/11/12 L1 six-case + optional same-day artifacts (post run-daily-gm-trio).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
else PY="python3"; fi

STAMP="${VERIFY_FUSED_DATE:-$(date +%Y-%m-%d)}"
echo "=== verify daily-gm-trio (L1 10+11+12) · $STAMP ==="

VERIFY_FUSED_DATE="$STAMP" bash scripts/verify-agent-fused.sh --agent all-daily --with-artifacts

echo "PASS: verify-daily-gm-trio"
