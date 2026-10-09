#!/usr/bin/env bash
# Read analytics warehouse → score → next-topics report (Agent 09 → 04).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1; fi

DEMO=false
if [[ "${1:-}" == "--demo" ]]; then
  DEMO=true
  shift
fi

echo "=== Analytics pipeline ==="
echo ""

if $DEMO; then
  echo "(demo) seeding from *.example.csv"
  cp -f content/analytics/xiaohongshu/notes.example.csv content/analytics/xiaohongshu/notes.csv
  cp -f content/analytics/instagram/posts.example.csv content/analytics/instagram/posts.csv
  cp -f content/analytics/youtube/videos.example.csv content/analytics/youtube/videos.csv
fi

bash scripts/analytics-fetch.sh || true
echo ""

set +e
OUT=$("$PY" scripts/analytics-summarize.py)
EC=$?
set -e
echo "$OUT"
if [[ "$EC" -ne 0 ]]; then
  echo ""
  echo "RESULT: WARN — no canonical CSV rows (import inbox or run with --demo)"
  echo "See content/analytics/README.md"
  exit 1
fi

echo ""
echo "RESULT: PASS — next-topics written under content/analytics/derived/"
echo "Manager: 派 09 读 derived/next-topics-*.md → 04 写 Brief → evaluate --brief"
