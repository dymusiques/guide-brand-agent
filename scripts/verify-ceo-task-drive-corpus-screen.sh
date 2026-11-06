#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
FAIL=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }

[[ -f scripts/ceo-task-drive-corpus-screen.py ]] && pass "ceo-task-drive-corpus-screen.py" || fail "missing screen"
[[ -f scripts/ceo_corpus_screen_lib.py ]] && pass "ceo_corpus_screen_lib.py" || fail "missing lib"

OUT=$("$PY" scripts/ceo-task-drive-corpus-screen.py --goal "品牌策划与小红书笔记" --json)
echo "$OUT" | "$PY" -c "import json,sys; d=json.load(sys.stdin); assert d['reference_count']>=1; assert d['catalog_files']>=500"
pass "smoke screen"

if [[ "$FAIL" -ne 0 ]]; then
  echo "RESULT: FAIL verify-ceo-task-drive-corpus-screen"
  exit 1
fi
echo "RESULT: PASS verify-ceo-task-drive-corpus-screen"
