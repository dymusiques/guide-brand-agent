#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FAIL=0

check() {
  if "$@"; then echo "OK $*"
  else echo "FAIL $*"; FAIL=$((FAIL + 1)); fi
}

check test -f "$ROOT/scripts/route-openwebui-for-goal.py"
check test -f "$ROOT/scripts/openwebui-pipe-to-outbox.py"
check test -x "$ROOT/scripts/run-openwebui-router-pipeline.sh"
check test -f "$ROOT/scripts/sync-openwebui-pipe-valves.py"
check test -d "$ROOT/integration/handoff/openwebui-jobs"

ENV="/Users/danying/Desktop/未命名/LLM-Ollama/RAG/RAG/scripts/brand-drive-sync.env"
if [[ -f "$ENV" ]]; then
  check grep -q OPENWEBUI_API_KEY "$ENV"
  if grep -qE '^GEMINI_API_KEY=' "$ENV" 2>/dev/null; then
    echo "FAIL brand-drive-sync.env must not contain GEMINI_API_KEY (use CEO .env + Open WebUI Connections)"
    FAIL=$((FAIL + 1))
  else
    echo "OK brand-drive-sync.env has no GEMINI_API_KEY"
  fi
else
  echo "WARN missing $ENV"; FAIL=$((FAIL + 1))
fi

if docker ps --format '{{.Names}}' | grep -qx open-webui; then
  check docker exec open-webui python3 -c "
import sqlite3
c=sqlite3.connect('/app/backend/data/webui.db')
for fid in ('yage_cot','yage_long_context'):
    r=c.execute('SELECT id,is_active,valves FROM function WHERE id=?',(fid,)).fetchone()
    assert r and r[1], fid+' not active'
    import json
    v=json.loads(r[2] or '{}')
    assert 'openrouter' in v.get('base_url',''), fid+' valves base_url'
    assert v.get('api_key') and 'Put your' not in v.get('api_key',''), fid+' valves api_key'
    assert v.get('my_model_id'), fid+' valves model'
kb=c.execute(\"SELECT id FROM knowledge WHERE name='brand-ip-knowledge'\").fetchone()
assert kb, 'no brand-ip-knowledge'
print('pipes+kb ok')
"
else
  echo "WARN open-webui container not running"; FAIL=$((FAIL + 1))
fi

OUT="$ROOT/integration/handoff/openwebui-setup-status.json"
python3 - <<PY
import json, subprocess
from pathlib import Path
from datetime import datetime, timezone
st = {"checked_at": datetime.now(timezone.utc).isoformat(), "docker": False, "pipes": {}, "knowledge": False}
try:
    subprocess.run(["docker","ps","--filter","name=open-webui","--format","{{.Status}}"], check=True, capture_output=True, text=True)
    st["docker"] = True
except Exception:
    pass
Path("$OUT").write_text(json.dumps(st, indent=2), encoding="utf-8")
PY

if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL verify-openwebui-ceo-router ($FAIL)"
  exit 1
fi
echo "RESULT: PASS verify-openwebui-ceo-router"
