#!/usr/bin/env bash
# Agent 03 — marketing / campaign scaffold check.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
README="$ROOT/content/marketing/README.md"
if [[ "${1:-}" == "--check" ]]; then
  [[ -f "$README" ]] && grep -qi "campaign" "$README"
  [[ -f scripts/evaluate-marketing-campaign.py ]] && [[ -f scripts/verify-marketing-campaign.sh ]]
  exit 0
fi
if [[ "${1:-}" == "--verify" ]]; then
  exec bash scripts/verify-marketing-campaign.sh
fi
if [[ -n "${1:-}" ]] && [[ -f "$1" ]]; then
  exec python3 scripts/evaluate-marketing-campaign.py --file "$1"
fi
echo "=== Agent 03 marketing shell ==="
head -20 "$README"
echo "Usage: $0 --verify | --check | path/to/campaign.md"
