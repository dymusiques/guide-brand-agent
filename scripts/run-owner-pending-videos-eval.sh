#!/usr/bin/env bash
# Evaluate all pending-videos/*.md → JSON → HTML (count not fixed).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
OPEN=1
[[ "${1:-}" == "--no-open" ]] && OPEN=0

"$PY" scripts/evaluate-owner-pending-videos.py
"$PY" scripts/build-owner-pending-videos-facts-manifest.py
"$PY" scripts/agent-gate-pending-videos-advice.py --no-refresh
"$PY" scripts/build-owner-pending-videos-eval-html.py

HTML="$ROOT/content/evolution/00-manager/ceo-inbox/OWNER-PENDING-VIDEOS-EVAL-latest.html"
if [[ "$OPEN" == 1 && "$(uname -s)" == Darwin ]]; then
  open "file://${HTML}#owner-latest"
fi
echo "OK file://${HTML}#owner-latest"
