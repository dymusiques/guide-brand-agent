#!/usr/bin/env bash
# L2: Video iteration + voice anchor stack (no Gemini).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FAIL=0
check() { [[ -f "$1" ]] || { echo "FAIL missing $1"; FAIL=1; }; }

check "content/xiaohongshu/XHS-VIDEO-ITERATION.md"
check "content/xiaohongshu/VOICE-ANCHOR.md"
check "content/xiaohongshu/voice-anchor-sources.json"
check "content/personal-ip/cv-source-2026-09-15.md"
check "integration/xhs-video-iteration-adoption.md"

PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1; fi

ROUND1="${1:-}"
if [[ -z "$ROUND1" ]]; then
  ROUND1="$(ls -t content/xiaohongshu/*video-round1*.md 2>/dev/null | head -1 || true)"
fi
if [[ -n "$ROUND1" && -f "$ROUND1" ]]; then
  if ! "$PY" scripts/analytics/xhs_voice_qa_lint.py "$ROUND1"; then
    FAIL=1
  fi
else
  echo "WARN no round1 md passed/found — skipped lint"
fi

# At least one anchor must have title; caption may be pending
if ! "$PY" - <<'PY'
import json, sys
from pathlib import Path
p = Path("content/xiaohongshu/voice-anchor-sources.json")
d = json.loads(p.read_text())
anchors = d.get("anchors") or []
if len(anchors) < 5:
    sys.exit("FAIL anchors < 5")
for a in anchors:
    if not a.get("title"):
        sys.exit("FAIL anchor missing title")
print("voice-anchor-sources.json: 5 titles OK")
PY
then
  FAIL=1
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "RESULT: PASS xhs-voice-qa L2"
  exit 0
fi
echo "RESULT: FAIL xhs-voice-qa L2"
exit 1
