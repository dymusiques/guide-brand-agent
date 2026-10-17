#!/usr/bin/env bash
# Agent 02 — business brand content scaffold check.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
README="$ROOT/content/business-brand/README.md"
if [[ "${1:-}" == "--check" ]]; then
  [[ -f "$README" ]] && grep -q "SWOT" "$README" && grep -q "定位" "$README"
  [[ -f scripts/evaluate-business-brand.py ]] && [[ -f scripts/verify-business-brand.sh ]]
  exit 0
fi
if [[ "${1:-}" == "--verify" ]]; then
  exec bash scripts/verify-business-brand.sh
fi
if [[ -n "${1:-}" ]] && [[ -f "$1" ]]; then
  exec python3 scripts/evaluate-business-brand.py --file "$1"
fi
echo "=== Agent 02 business-brand shell ==="
head -20 "$README"
echo "Usage: $0 --verify | --check | path/to/doc.md"
