#!/usr/bin/env bash
# Agent 04 — evaluate-xhs-topic wrapper.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else exit 1; fi
if [[ "${1:-}" == "--check" ]]; then
  [[ -f scripts/evaluate-xhs-topic.py ]] || exit 1
  exit 0
fi
if [[ -z "${1:-}" ]]; then
  echo "Usage: $0 --check | --brief path/to/brief.md"
  exit 2
fi
if [[ "$1" == "--brief" ]]; then
  shift
  exec "$PY" scripts/evaluate-xhs-topic.py --brief "$1"
fi
echo "Unknown args: $*"
exit 2
