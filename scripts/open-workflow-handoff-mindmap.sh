#!/usr/bin/env bash
# Open workflow + MD handoff mindmap in browser (popup-friendly URL).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PORT="${WORKFLOW_MINDMAP_PORT:-8765}"
URL="http://127.0.0.1:${PORT}/docs/workflow-handoff-mindmap.html"
if ! curl -sf "${URL%/*/*}/docs/workflow-handoff-mindmap.html" >/dev/null 2>&1; then
  if lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "Using existing http.server on $PORT"
  else
    python3 -m http.server "$PORT" >/dev/null 2>&1 &
    echo $! > /tmp/dba-mindmap-http.pid
    sleep 0.5
  fi
fi
if [[ "$(uname)" == Darwin ]]; then
  open "${URL}?open=1"
else
  echo "Open: ${URL}?open=1"
fi
