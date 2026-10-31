#!/usr/bin/env bash
# Clever multi-persona against blocks in Owner longform. See docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
BRIEF=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --brief) BRIEF="${2:-}"; shift 2 ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done
[[ -n "$BRIEF" && -f "$BRIEF" ]] || { echo "FAIL: --brief required"; exit 1; }
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"
exec "$PY" scripts/xhs_clever_advocate.py --brief "$BRIEF"
