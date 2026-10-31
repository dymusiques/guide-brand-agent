#!/usr/bin/env bash
# Owner one-shot: recover + print CEO next actions (chat trigger doc: docs/CEO-OWNER-ONE-LINE-TRIGGERS.md)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
INBOX="$ROOT/content/evolution/00-manager/ceo-inbox"

echo "=== CEO start-work (status + recover) ==="
bash scripts/ceo-auto-recover-blocked.sh || true
echo ""

latest_dispatch="$(ls -t "$INBOX"/CEO-IP-ALL-AGENTS-DISPATCH-*.md 2>/dev/null | head -1 || true)"
latest_campaign="$(ls -t "$INBOX"/ceo-ip-all-agents-campaign-*.md 2>/dev/null | head -1 || true)"
latest_deep="$(ls -t "$INBOX"/ceo-deep-delivery-*.md 2>/dev/null | head -1 || true)"

echo "Latest dispatch: ${latest_dispatch#"$ROOT/"}"
echo "Latest campaign:  ${latest_campaign#"$ROOT/"}"
echo "Latest deep:      ${latest_deep#"$ROOT/"}"
echo ""

echo "Pending CEO double-iteration (phase 1 done, need log + phase 2):"
found=0
while IFS= read -r st; do
  [[ -n "$st" ]] || continue
  found=1
  dir="$(dirname "$st")"
  brief_guess="$(basename "$dir")"
  echo "  - $dir · run phase 2 after ITERATION-LOG filled"
done < <(find "$ROOT/content/evolution/04-xhs-topic-manager" -name '.ceo-double-iteration-state.json' 2>/dev/null || true)
[[ "$found" -eq 0 ]] && echo "  (none)"

action="$INBOX/ceo-action-needed.md"
if [[ -f "$action" ]]; then
  echo "CEO action needed: ${action#"$ROOT/"}"
fi
echo ""
echo "In Cursor chat, say: 请 CEO 开始工作"
echo "Doc: docs/CEO-OWNER-ONE-LINE-TRIGGERS.md · automation: docs/WORKFLOW-AUTOMATION-MATRIX.md"
exit 0
