#!/usr/bin/env bash
# Deploy / verify: Context-window Pipes + WBR SQLite + Drive→Knowledge (two-lesson stack).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RAG_SCRIPTS="$ROOT/integration/openwebui-rag/scripts"
LOCAL_FIX="$ROOT/scripts/fix-openwebui-local-models.py"
WBR_COURSE="/Users/danying/Desktop/未命名/WBR/WBR/scripts/fix-openwebui-wbr-sqlite.py"
FAIL=0

ok() { echo "OK  $*"; }
warn() { echo "WARN $*"; }
fail() { echo "FAIL $*"; FAIL=$((FAIL + 1)); }

echo "== 1) Open WebUI container =="
if docker ps --format '{{.Names}}' | grep -qx open-webui; then
  ok "open-webui running"
else
  fail "open-webui not running"
fi

echo "== 2) Local models + SQLite Tool (production; not course events.db) =="
if [[ -f "$LOCAL_FIX" ]] && docker ps --format '{{.Names}}' | grep -qx open-webui; then
  docker cp "$LOCAL_FIX" open-webui:/tmp/fix-openwebui-local-models.py
  if [[ -f "$WBR_COURSE" ]]; then
    docker cp "$WBR_COURSE" open-webui:/tmp/fix-openwebui-wbr-sqlite.py
  fi
  docker exec open-webui python3 /tmp/fix-openwebui-local-models.py && ok "local-llama3.2-3b + sqlite tool (no homework db)"
else
  warn "skip local Open WebUI model fix"
fi

echo "== 3) Pipe Valves sync (OpenRouter from Admin Connections) =="
docker exec open-webui python3 -c "
import sqlite3, json
c=sqlite3.connect('/app/backend/data/webui.db')
row=c.execute(\"SELECT value FROM config WHERE key='openai.api_configs'\").fetchone()
if row and row[0]:
    cfg=json.loads(row[0])
    if isinstance(cfg.get('0'), dict):
        cfg['0']['enable']=True
        c.execute(\"UPDATE config SET value=? WHERE key='openai.api_configs'\",(json.dumps(cfg),))
        c.commit()
" 2>/dev/null || true
if python3 "$ROOT/scripts/sync-openwebui-pipe-valves.py"; then
  ok "pipe valves synced"
else
  fail "sync-openwebui-pipe-valves.py"
fi

echo "== 4) CEO Open WebUI router verify =="
if bash "$ROOT/scripts/verify-openwebui-ceo-router.sh"; then
  ok "verify-openwebui-ceo-router"
else
  fail "verify-openwebui-ceo-router"
fi

echo "== 5) Export agent prompt pack → RAG mirror =="
if bash "$ROOT/scripts/export-agent-prompt-pack.sh"; then
  ok "agent-prompt-pack exported"
else
  warn "export-agent-prompt-pack failed"
fi

echo "== 6) Brand Drive → Open WebUI (incremental sync if env present) =="
ENV_FILE="$RAG_SCRIPTS/brand-drive-sync.env"
if [[ -f "$ENV_FILE" ]] && [[ -f "$RAG_SCRIPTS/sync_brand_drive_to_openwebui.py" ]]; then
  if (cd "$RAG_SCRIPTS" && python3 sync_brand_drive_to_openwebui.py); then
    ok "brand-ip-knowledge sync"
  else
    warn "sync_brand_drive_to_openwebui.py failed — Knowledge may be partial; retry or run run_full_brand_ingest.sh"
  fi
else
  warn "missing $ENV_FILE or sync script — Drive RAG sync skipped"
fi

echo "== 7) Workflow automation manifest =="
if bash "$ROOT/scripts/verify-workflow-automation.sh"; then
  ok "verify-workflow-automation"
else
  warn "verify-workflow-automation had issues"
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "DEPLOY-LEARNING-STACK: PASS"
  exit 0
fi
echo "DEPLOY-LEARNING-STACK: FAIL ($FAIL hard failures)"
exit 1
