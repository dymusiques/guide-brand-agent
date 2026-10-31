#!/usr/bin/env bash
# Rebuild Owner daily HTML notify page. See docs/OWNER-DELIVERY-NOTIFY-DEFAULT.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
DAY="$(date +%Y-%m-%d)"
OUT="content/evolution/00-manager/ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-$DAY.html"
TEST="content/evolution/00-manager/ceo-inbox/OWNER-WORKFLOW-TEST-ARTICLE-$DAY.html"
"$PY" scripts/build-owner-xhs-report-html.py
if ls content/xiaohongshu/*-test-brief.md >/dev/null 2>&1; then
  "$PY" scripts/build-owner-workflow-test-article-html.py
fi
if [[ -f content/marketing/linkedin/2026-10-30-musicians-business-cognition-carousel-en.md ]]; then
  "$PY" scripts/build-owner-multichannel-deliverable-html.py || true
fi
bash scripts/verify-owner-html-deliverables.sh || {
  echo "FAIL: HTML out of sync with test brief — rebuild aborted verify"
  exit 1
}
echo "OK refresh-owner-notify-html · $OUT · $TEST"
bash scripts/open-owner-xhs-deliverable-html.sh || true
exit 0
