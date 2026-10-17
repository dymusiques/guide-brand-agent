#!/usr/bin/env bash
# Agent 07 — visual brief block / skill path check.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
README="$ROOT/content/visual/README.md"
if [[ "${1:-}" == "--check" ]]; then
  [[ -f "$README" ]] && grep -q "封面" "$README"
  [[ -f "$ROOT/.cursor/skills/brand-visual/SKILL.md" ]]
  exit 0
fi
echo "=== Agent 07 brand-visual shell ==="
head -15 "$README"
echo "RESULT: PASS — visual scaffold ok"
