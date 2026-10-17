#!/usr/bin/env bash
# Agent 06 — batch brief verify.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
if [[ "${1:-}" == "--check" ]]; then
  [[ -f scripts/verify-xhs-content-dir.sh ]] || exit 1
  exit 0
fi
exec bash scripts/verify-xhs-content-dir.sh
