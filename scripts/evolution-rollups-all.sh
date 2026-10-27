#!/usr/bin/env bash
# Summarize all content/evolution/**/metrics.jsonl → derived rollup (baseline / evaluator trends).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OUT="$ROOT/content/analytics/derived/evolution-rollups-latest.md"
mkdir -p "$(dirname "$OUT")"
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1; fi

{
  echo "# Evolution rollups · $(date -Iseconds)"
  echo ""
  found=0
  while IFS= read -r -d '' m; do
    found=1
    rel="${m#"$ROOT"/}"
    echo "## \`$rel\`"
    echo '```json'
    "$PY" scripts/evolution-metrics-summary.py "$m" 2>/dev/null || echo '{"error": "summary failed"}'
    echo '```'
    echo ""
  done < <(find content/evolution -name metrics.jsonl -print0 2>/dev/null | sort -z)
  if [[ "$found" -eq 0 ]]; then
    echo "_No metrics.jsonl yet — Collector/Evaluator chains will populate under content/evolution/_._"
  fi
} >"$OUT"
echo "Wrote $OUT"
