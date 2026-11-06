#!/usr/bin/env bash
# Fusion manifest + builder exist; JSON parses.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FAIL=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }

FUSION="$ROOT/integration/handoff/drive-long-context-fusion.json"
FOLDERS="$ROOT/integration/handoff/ceo-drive-corpus-folders.json"
CATALOG="$ROOT/content/personal-ip/intake/_raw/ceo-drive-catalog-live.json"
BUILDER="$ROOT/scripts/build-drive-long-context-fusion.py"
DOC="$ROOT/docs/DRIVE-LONG-CONTEXT-FUSION.md"

[[ -f "$BUILDER" ]] && pass "build-drive-long-context-fusion.py" || fail "missing builder"
[[ -f "$DOC" ]] && pass "DRIVE-LONG-CONTEXT-FUSION.md" || fail "missing doc"
[[ -f "$FOLDERS" ]] && pass "ceo-drive-corpus-folders.json" || fail "missing ceo-drive-corpus-folders.json"
[[ -f "$CATALOG" ]] && pass "ceo-drive-catalog-live.json" || fail "missing ceo-drive-catalog-live.json (run refresh-ceo-drive-catalog.py)"
bash "$ROOT/scripts/verify-drive-corpus-text-extract.sh" || FAIL=1

if [[ ! -f "$FUSION" ]]; then
  "$ROOT/.venv/bin/python" "$BUILDER" --write-manifest 2>/dev/null || python3 "$BUILDER" --write-manifest
fi
[[ -f "$FUSION" ]] && pass "drive-long-context-fusion.json" || fail "missing fusion json"

"$ROOT/.venv/bin/python" - <<'PY' "$FUSION" || FAIL=1
import json, sys
p = sys.argv[1]
data = json.loads(open(p, encoding="utf-8").read())
for key in ("ceo_pipeline_order", "lines", "forbidden", "prompt_templates"):
    assert key in data, key
print("PASS: fusion json schema keys")
PY

if [[ "$FAIL" -ne 0 ]]; then
  echo "RESULT: FAIL verify-drive-long-context-fusion"
  exit 1
fi
echo "RESULT: PASS verify-drive-long-context-fusion"
