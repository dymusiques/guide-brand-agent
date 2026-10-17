#!/usr/bin/env bash
# Agent 08 — platform integration verify (gdocs 6 case).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
if [[ "${1:-}" == "--check" ]]; then
  [[ -f scripts/verify-integration.sh ]] || exit 1
  exit 0
fi
exec bash scripts/verify-integration.sh
