#!/usr/bin/env bash
# CEO-scheduled daily: GM10 artist · GM11 IP eval · GM12 Owner brief → CEO inbox summary
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
export PATH="$ROOT/.venv/bin:${PATH:-}"
PY="$ROOT/.venv/bin/python"
STAMP="$(date +%Y-%m-%d)"
INBOX="$ROOT/content/evolution/00-manager/ceo-inbox"
mkdir -p "$INBOX"
LOG="$INBOX/daily-gm-trio-$STAMP.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== daily-gm-trio · $STAMP ==="
FAIL=0

step() {
  local name="$1"
  shift
  if "$@"; then echo "PASS: $name"; else echo "FAIL: $name"; FAIL=$((FAIL + 1)); fi
}

if "$PY" scripts/daily-gm-10-artist-benchmark.py; then echo "PASS: GM10-artist"; else echo "WARN: GM10-artist (continuing)"; fi
"$PY" scripts/merge-artist-intel-catalog.py || true
step "GM11-ip-eval" "$PY" scripts/daily-gm-11-ip-evaluator.py
step "GM12-daily-brief" "$PY" scripts/daily-gm-12-owner-daily-brief.py
step "verify-daily-gm-trio" bash scripts/verify-daily-gm-trio.sh

{
  echo "# CEO daily GM summary · $STAMP"
  echo ""
  echo "- GM10: content/evolution/10-artist-intel/$STAMP/"
  echo "- GM11: content/evolution/11-ip-daily-eval/$STAMP/"
  echo "- GM12: content/daily-brief/${STAMP}-owner-daily-brief.md"
  echo "- log: content/evolution/00-manager/ceo-inbox/daily-gm-trio-$STAMP.log"
} >"$INBOX/daily-gm-summary-$STAMP.md"

if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL ($FAIL)"
  exit 1
fi
echo "RESULT: PASS daily-gm-trio"
exit 0
