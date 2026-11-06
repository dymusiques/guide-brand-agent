#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
FAIL=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }

EX="$ROOT/scripts/drive_corpus_extract_text.py"
[[ -f "$EX" ]] && pass "drive_corpus_extract_text.py" || fail "missing extract script"

"$PY" "$EX" --self-test && pass "self-test" || fail "self-test"

if command -v pdftotext >/dev/null 2>&1; then
  pass "pdftotext on PATH"
else
  echo "WARN: pdftotext missing — PDF extract may be empty (install poppler)"
fi

if command -v ebook-convert >/dev/null 2>&1 \
  || [[ -x "$HOME/.local/bin/ebook-convert" ]] \
  || [[ -x /Applications/calibre.app/Contents/MacOS/ebook-convert ]]; then
  pass "calibre ebook-convert available"
else
  echo "WARN: run bash scripts/ensure-calibre-cli.sh — mobi/azw/azw3 need ebook-convert"
fi

if [[ "$FAIL" -ne 0 ]]; then
  echo "RESULT: FAIL verify-drive-corpus-text-extract"
  exit 1
fi
echo "RESULT: PASS verify-drive-corpus-text-extract"
