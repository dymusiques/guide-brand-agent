#!/usr/bin/env bash
# Publish/sync CEO benchmark paths MD to Google Doc + refresh Drive catalog links in handoff JSON.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
MD="content/evolution/00-manager/ceo-inbox/CEO-BENCHMARK-GROWTH-PATHS-2026-11-06.md"
HANDOFF="$ROOT/integration/handoff/owner-benchmark-paths-drive-latest.json"
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

bash scripts/check-google-auth-for-agent.sh >/dev/null 2>&1 || true

echo ">>> refresh Drive catalog (ceo-drive-corpus-folders)"
if [[ -x "$PY" ]]; then
  "$PY" scripts/refresh-ceo-drive-catalog.py 2>/dev/null || echo "WARN: refresh-ceo-drive-catalog skipped"
fi

echo ">>> gdocs sync benchmark paths MD"
TITLE="CEO·双线对标路径·国内/国际·Instagram·2026-11-06"
SYNC_OUT=$("$PY" -m gdocs --secrets-dir vendor/gdocs-skill/secrets sync "$MD" --title "$TITLE" 2>&1) || SYNC_OUT="FAIL: $SYNC_OUT"
echo "$SYNC_OUT"

DOC_LINK=""
DOC_ID=""
if echo "$SYNC_OUT" | grep -q '"link"'; then
  DOC_LINK=$(echo "$SYNC_OUT" | "$PY" -c "import sys,json,re; t=sys.stdin.read();
m=re.search(r'\{[^{}]*\"link\"[^{}]*\}', t, re.S)
if m:
  o=json.loads(m.group(0))
  print(o.get('link',''))
  print(o.get('doc_id',''), file=sys.stderr)
" 2>/dev/null | head -1 || true)
  DOC_ID=$(echo "$SYNC_OUT" | "$PY" -c "import sys,json,re; t=sys.stdin.read();
m=re.search(r'\{[^{}]*\"doc_id\"[^{}]*\}', t, re.S)
if m: print(json.loads(m.group(0)).get('doc_id',''))" 2>/dev/null || true)
fi
if [[ -z "$DOC_LINK" ]]; then
  DOC_LINK="https://drive.google.com/drive/folders/1Lpi4A_Ws-StJ47NkK-R0uXFU0z4khdtc"
fi

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
mkdir -p "$(dirname "$HANDOFF")"
"$PY" - <<PY
import json
from pathlib import Path
payload = {
  "synced_at": "$TS",
  "local_md": "$MD",
  "google_doc_id": "$DOC_ID",
  "google_doc_link": "$DOC_LINK",
  "drive_folders": "integration/handoff/ceo-drive-corpus-folders.json",
  "growth_paths_json": "integration/handoff/owner-benchmark-growth-paths.json",
  "catalog": "content/personal-ip/intake/_raw/ceo-drive-catalog-live.json",
}
Path("$HANDOFF").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Wrote", "$HANDOFF")
PY

echo "RESULT: sync-owner-benchmark-paths-to-drive done · doc: $DOC_LINK"
