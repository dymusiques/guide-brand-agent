#!/usr/bin/env bash
# Agent 05 — kernel verify (Gemini 6 when key present).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
if [[ "${1:-}" == "--check" ]]; then
  [[ -f kernels/xiaohongshu/line2/is_xhs_growth_aligned.py ]] || exit 1
  [[ -f scripts/verify-xhs-topic.sh ]] || exit 1
  exit 0
fi
exec bash scripts/verify-xhs-topic.sh
