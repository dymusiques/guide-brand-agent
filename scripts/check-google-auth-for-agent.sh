#!/usr/bin/env bash
# Owner one-time OAuth lives in vendor/gdocs-skill/secrets/ — Agent reads status, never re-ask in chat.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OUT="$ROOT/integration/handoff/google-auth-status.json"
mkdir -p "$(dirname "$OUT")"

CLI=FAIL
INTEG=SKIP
DETAIL=""
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY=python3

if [[ -f vendor/gdocs-skill/secrets/credentials.json && -f vendor/gdocs-skill/secrets/token.json ]]; then
  CLI=OK
fi

if [[ "$CLI" == OK ]]; then
  # Refresh expired access token via refresh_token (no browser); avoid dead local proxy.
  HTTPS_PROXY= HTTP_PROXY= "$PY" - <<REFRESH 2>/dev/null || true
import sys
from pathlib import Path
ROOT = Path("$ROOT")
sys.path.insert(0, str(ROOT / "vendor/gdocs-skill"))
from gdocs.auth import get_credentials
get_credentials(ROOT / "vendor/gdocs-skill/secrets")
REFRESH
  if bash scripts/verify-integration.sh >/tmp/google-auth-verify.log 2>&1; then
    INTEG=PASS
    DETAIL="verify-integration 6/6"
  else
    INTEG=FAIL
    DETAIL="$(tail -3 /tmp/google-auth-verify.log | tr '\n' ' ')"
  fi
fi

OWNER_MUST=0
AGENT_ASK=0
if [[ "$INTEG" != PASS ]]; then
  OWNER_MUST=1
  AGENT_ASK=0
  DETAIL="${DETAIL:-missing or expired token — Owner Terminal re-auth once, not chat ping-pong}"
fi

"$PY" - <<PY
import json
from datetime import datetime, timezone
from pathlib import Path
p = Path("$OUT")
p.write_text(json.dumps({
  "checked_at": datetime.now(timezone.utc).isoformat(),
  "cli_secrets_present": "$CLI" == "OK",
  "verify_integration": "$INTEG",
  "owner_must_reauth_terminal_only": bool($OWNER_MUST),
  "agent_must_not_ask_owner_confirm_google": True,
  "agent_use": "python -m gdocs --secrets-dir vendor/gdocs-skill/secrets (primary); Cursor MCP Google plugins optional duplicate — do NOT prompt Owner when this file says verify_integration PASS",
  "detail": """$DETAIL""",
  "doc": "docs/OWNER-GOOGLE-GRANT-AGENT.md",
}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PY

echo "google-auth-status: verify_integration=$INTEG · agent_must_not_ask=true"
if [[ "$INTEG" == PASS ]]; then
  echo "RESULT: PASS check-google-auth-for-agent"
  exit 0
fi
echo "RESULT: WARN check-google-auth-for-agent — see $OUT (Owner Terminal only if token dead)"
exit 0
