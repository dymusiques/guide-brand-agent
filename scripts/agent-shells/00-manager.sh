#!/usr/bin/env bash
# Agent 00 function shell — Manager workflow verify (integration health).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
if [[ "${1:-}" == "--check" ]]; then
  [[ -f scripts/manager-workflow-verify.sh ]] || exit 1
  [[ -f agents/00-manager/AUTO-WORKFLOW.md ]] || exit 1
  exit 0
fi
exec bash scripts/manager-workflow-verify.sh "$@"
