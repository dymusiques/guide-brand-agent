#!/usr/bin/env bash
# L0: Owner data + platform research stack present for content production.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FAIL=0
check() { [[ -f "$1" ]] || { echo "FAIL missing $1"; FAIL=1; }; }

check "docs/XHS-CONTENT-INTAKE-STACK.md"
check "content/xiaohongshu/CONTENT-DELIVERY-FOR-OWNER.md"
check "content/analytics/xiaohongshu/DATA-MANIFEST.json"
check "content/analytics/xiaohongshu/notes-snapshot-2026-10-20.json"
check "content/analytics/derived/xhs-data-strategy-2026-10-20.md"
check "content/marketing/research/xhs-platform-research-index.md"
check "content/xiaohongshu/platform-notes-2026.md"
check "content/xiaohongshu/XHS-VIDEO-ITERATION.md"
check "content/xiaohongshu/VOICE-ANCHOR.md"
check "content/personal-ip/cv-source-2026-09-15.md"

RAW="$ROOT/content/marketing/research/raw/momentum-2026.pdf"
if [[ ! -f "$RAW" ]]; then
  echo "WARN optional: $RAW (PDF gitignored; MD extracts still OK)"
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "RESULT: PASS xhs-content-intake stack"
  exit 0
fi
echo "RESULT: FAIL xhs-content-intake stack"
exit 1
