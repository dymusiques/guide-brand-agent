#!/usr/bin/env bash
# After a CEO/eval round: stage dated deliverables + evolution evidence for one archive commit.
# Rolling files (manifest, *-latest.html, owner-*-latest.json) stay local per .gitignore.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== archive-ceo-campaign-deliverables (dry list; run git add manually or via Agent) ==="
echo "Add: content/evolution/00-manager/ceo-inbox/OWNER-*-<date>.* (not *-latest.html)"
echo "Add: content/evolution/00-manager/ceo-inbox/OWNER-PENDING-VIDEOS-EVAL-<date>.html"
echo "Add: content/evolution/00-manager/ceo-inbox/OWNER-WORKFLOW-TEST-ARTICLE-<date>.html"
echo "Add: slug dirs under ceo-inbox/ and evolution/04|10|11|12/<date>/"
echo "Skip: CEO-RUN-MANIFEST-latest.* · integration/handoff/owner-*-latest.json"
echo "See docs/CEO-MANAGER-OPERATING-PRINCIPLES.md §6 · .gitignore Layer C"