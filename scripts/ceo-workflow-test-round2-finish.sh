#!/usr/bin/env bash
# Round 2: 01–12 campaign + Owner HTML refresh + open browser (no Owner confirm).
# See docs/OWNER-DELIVERY-NOTIFY-DEFAULT.md · docs/CEO-WORKFLOW-TEST-SOP.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
INBOX="$ROOT/content/evolution/00-manager/ceo-inbox"
DAY="$(date +%Y-%m-%d)"

export VERIFY_GOALS_SKIP_PLATFORM="${VERIFY_GOALS_SKIP_PLATFORM:-1}"
export CEO_OWNER_HTML_REFRESH="${CEO_OWNER_HTML_REFRESH:-1}"
# shellcheck source=scripts/lib/ceo-deep-delivery-lock.sh
source "$ROOT/scripts/lib/ceo-deep-delivery-lock.sh"
if ceo_deep_delivery_active; then
  export SKIP_GEMINI="${SKIP_GEMINI:-1}"
else
  export SKIP_GEMINI="${SKIP_GEMINI:-0}"
fi

echo "=== ceo-workflow-test-round2-finish · SKIP_GEMINI=$SKIP_GEMINI ==="
FAIL=0
bash scripts/run-ceo-ip-all-agents-campaign.sh || FAIL=$((FAIL + 1))
# Must rebuild FILTER + TEST HTML from latest *-test-brief.md (not stale hand-edited HTML)
bash scripts/refresh-owner-notify-html.sh || FAIL=$((FAIL + 1))

DELIVER="$INBOX/OWNER-XHS-FILTER-DELIVERABLE-$DAY.html"
TEST="$INBOX/OWNER-WORKFLOW-TEST-ARTICLE-$DAY.html"
for f in "$DELIVER" "$TEST"; do
  [[ -f "$f" ]] && open "$f" 2>/dev/null || true
done
[[ -x "$INBOX/OPEN-WORKFLOW-TEST-ARTICLE.command" ]] && open "$INBOX/OPEN-WORKFLOW-TEST-ARTICLE.command" 2>/dev/null || true

if [[ "$FAIL" -eq 0 ]]; then
  echo "RESULT: PASS round2-campaign + HTML opened"
  exit 0
fi
echo "RESULT: FAIL round2-campaign ($FAIL) — HTML still refreshed/opened; see ceo-ip-all-agents-campaign-*.md"
exit 1
