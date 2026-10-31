#!/usr/bin/env bash
# FILTER + TEST HTML must contain subjects from workflow test + Discovery 01–04 briefs.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
DAY="${VERIFY_HTML_DAY:-$(date +%Y-%m-%d)}"
FAIL=0

FILTER="content/evolution/00-manager/ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-$DAY.html"
TEST="content/evolution/00-manager/ceo-inbox/OWNER-WORKFLOW-TEST-ARTICLE-$DAY.html"

SUBJECTS="$(
  python3 <<'PY'
import re
from pathlib import Path
root = Path(".")
paths = sorted(root.glob("content/xiaohongshu/2026-10-17-discovery-0*-brief.md"))
test = sorted(root.glob("content/xiaohongshu/*-test-brief.md"), key=lambda p: p.stat().st_mtime, reverse=True)
extra = __import__("os").environ.get("CEO_OWNER_EXTRA_BRIEF", "").strip()
extra_paths = []
if extra:
    ep = root / extra if not extra.startswith("/") else Path(extra)
    if ep.is_file():
        extra_paths = [ep]
paths = extra_paths + (test[:1] if test else []) + paths
for p in paths:
    t = p.read_text(encoding="utf-8")
    m = re.search(r'"subject":\s*"([^"]+)"', t)
    if m:
        print(m.group(1))
PY
)"

if [[ ! -f "$FILTER" ]]; then
  echo "FAIL: missing FILTER ($FILTER)"
  exit 1
fi

while IFS= read -r sub; do
  [[ -z "$sub" ]] && continue
  if grep -Fq "$sub" "$FILTER"; then
    echo "PASS: FILTER contains · $sub"
  else
    echo "FAIL: FILTER missing subject · $sub"
    FAIL=$((FAIL + 1))
  fi
done <<< "$SUBJECTS"

TEST_BRIEF="$(ls -t content/xiaohongshu/*-test-brief.md 2>/dev/null | head -1 || true)"
if [[ -n "$TEST_BRIEF" && -f "$TEST" ]]; then
  TEST_SUB="$(python3 -c "import re,pathlib; t=pathlib.Path('$TEST_BRIEF').read_text(); m=re.search(r'\"subject\":\s*\"([^\"]+)\"', t); print(m.group(1) if m else '')")"
  if [[ -n "$TEST_SUB" ]] && grep -Fq "$TEST_SUB" "$TEST"; then
    echo "PASS: TEST page contains · $TEST_SUB"
  else
    echo "FAIL: TEST page missing · $TEST_SUB"
    FAIL=$((FAIL + 1))
  fi
fi

# Forbid stale Discovery #1 platitude title in FILTER
if grep -Fq "什么是「站得住」的艺术" "$FILTER"; then
  echo "FAIL: FILTER still contains retired platitude title (discovery-01)"
  FAIL=$((FAIL + 1))
else
  echo "PASS: FILTER no retired platitude title"
fi

# HTML must not be older than any tracked brief (stale deliverable)
if ! python3 <<'PY'
import re
import sys
from pathlib import Path

root = Path(".")
day = __import__("os").environ.get("VERIFY_HTML_DAY", __import__("datetime").datetime.now().strftime("%Y-%m-%d"))
html = root / f"content/evolution/00-manager/ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-{day}.html"
if not html.is_file():
    print("FAIL: FILTER html missing for freshness check")
    sys.exit(1)
html_mtime = html.stat().st_mtime
paths = sorted(root.glob("content/xiaohongshu/2026-10-17-discovery-0*-brief.md"))
paths += sorted(root.glob("content/xiaohongshu/*-test-brief.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:1]
stale = [p for p in paths if p.stat().st_mtime > html_mtime + 1]
if stale:
    for p in stale:
        print(f"FAIL: HTML older than brief · {p}")
    sys.exit(1)
print("PASS: HTML fresh vs discovery + test briefs")
PY
then
  FAIL=$((FAIL + 1))
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "RESULT: PASS verify-owner-html-deliverables"
  exit 0
fi
echo "RESULT: FAIL verify-owner-html-deliverables ($FAIL)"
exit 1
