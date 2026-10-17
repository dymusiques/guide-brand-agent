#!/usr/bin/env bash
# Agent 09 — analytics pipeline (demo or live).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
if [[ "${1:-}" == "--check" ]]; then
  [[ -f scripts/analytics-pipeline.sh ]] || exit 1
  exit 0
fi
if [[ "${1:-}" == "--live" ]]; then
  exec bash scripts/analytics-pipeline.sh
fi
exec bash scripts/analytics-pipeline.sh --demo
