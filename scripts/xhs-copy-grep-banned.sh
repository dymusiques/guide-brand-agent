#!/usr/bin/env bash
# Mechanical banned-lexicon scan for Xiaohongshu copy (xhs-copy-self-check.md §11).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/xhs-copy-grep-banned.sh <path-to.md>" >&2
  echo "Example: bash scripts/xhs-copy-grep-banned.sh content/xiaohongshu/draft-note.md" >&2
  exit 2
fi

PY="${ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  PY=python3
fi

exec "$PY" "${ROOT}/scripts/xhs_copy_grep_banned.py" "$@"
