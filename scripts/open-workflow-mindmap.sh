#!/usr/bin/env bash
# 打开小红书顺序思维导图（系统浏览器 file://）
# 在 Cursor 里看图：请让 Agent 用内置 Browser 打开 http://127.0.0.1:8765/workflow-mindmap.html
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HTML="$ROOT/docs/workflow-mindmap.html"
PORT="${WORKFLOW_MINDMAP_PORT:-8765}"

if [[ ! -f "$HTML" ]]; then
  echo "Missing: $HTML" >&2
  exit 1
fi

open_in_browser() {
  local target="$1"
  if [[ "$(uname -s)" == "Darwin" ]]; then
    open "$target" 2>/dev/null && return 0
  fi
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$target" && return 0
  fi
  echo "Could not launch browser. Open manually:" >&2
  echo "  $target" >&2
  return 1
}

# 优先 file:// — 无需 HTTP 服务，最稳
FILE_URL="file://${HTML}"
echo "Opening mind map (file URL)..."
if open_in_browser "$FILE_URL"; then
  echo "OK: $FILE_URL"
  exit 0
fi

# 备选：本机临时 HTTP（Cursor 内置浏览器有时只能 http）
if ! lsof -i ":$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Starting http.server on port $PORT ..."
  python3 -m http.server "$PORT" --directory "$ROOT/docs" >/tmp/workflow-mindmap-http.log 2>&1 &
  sleep 0.8
fi
HTTP_URL="http://127.0.0.1:${PORT}/workflow-mindmap.html"
if curl -sf --connect-timeout 2 "$HTTP_URL" >/dev/null; then
  open_in_browser "$HTTP_URL"
  echo "OK: $HTTP_URL"
  echo "Log: /tmp/workflow-mindmap-http.log"
else
  echo "Server failed. Use file URL in browser:" >&2
  echo "  $FILE_URL" >&2
  exit 1
fi
