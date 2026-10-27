#!/usr/bin/env bash
# L0: Collector + edit-distance evaluator scripts smoke test
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
TMP="$ROOT/content/evolution/_selftest-verify"
rm -rf "$TMP"
mkdir -p "$TMP/versions" "$TMP/reference"
echo "hello world v0" >"$TMP/versions/v0.md"
echo "hello world gold" >"$TMP/reference/gold.md"
echo "hello world v0 fixed" >"$TMP/versions/v0-corrected.md"

python3 scripts/evaluate-edit-distance.py \
  --candidate "$TMP/versions/v0.md" \
  --reference "$TMP/reference/gold.md" \
  --corrected "$TMP/versions/v0-corrected.md" \
  --label v0 \
  --append "$TMP/metrics.jsonl" >/dev/null

python3 scripts/collector-intake.py --agent _selftest --slug verify --text "ok" --dry-run >/dev/null
python3 scripts/evolution-metrics-summary.py "$TMP/metrics.jsonl" | grep -q '"mean"'

echo "PASS: verify-collector-evaluator"
