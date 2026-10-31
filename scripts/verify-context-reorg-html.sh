#!/usr/bin/env bash
# CONTEXT-REORG-PIPELINE-LATEST.html must open offline (no CDN) + mind map present.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HTML="$ROOT/content/evolution/00-manager/ceo-inbox/CONTEXT-REORG-PIPELINE-LATEST.html"
FAIL=0

if [[ ! -f "$HTML" ]]; then
  echo "FAIL: missing $HTML — run python3 scripts/build-context-reorg-pipeline-html.py"
  exit 1
fi

grep -q 'id="mindmap-grid"' "$HTML" || { echo "FAIL: mindmap-grid missing"; FAIL=$((FAIL + 1)); }
grep -q 'id="panel"' "$HTML" || { echo "FAIL: panel missing"; FAIL=$((FAIL + 1)); }
grep -q 'id="owner-latest"' "$HTML" || { echo "FAIL: owner-latest anchor missing"; FAIL=$((FAIL + 1)); }

if grep -q 'cdn.jsdelivr.net' "$HTML"; then
  echo "FAIL: HTML still depends on external CDN (offline break risk)"
  FAIL=$((FAIL + 1))
else
  echo "PASS: no external CDN"
fi

if grep -q 'href="" +' "$HTML"; then
  echo "FAIL: broken JavaScript string (mindmap clicks will not work)"
  FAIL=$((FAIL + 1))
else
  echo "PASS: mindmap JS href concatenation"
fi

if grep -q 'LLM-Ollama/RAG/RAG/scripts' "$HTML"; then
  echo "WARN: legacy LLM-Ollama path still in HTML body"
else
  echo "PASS: vendored integration/openwebui-rag paths in sync block"
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "RESULT: PASS verify-context-reorg-html"
  exit 0
fi
echo "RESULT: FAIL verify-context-reorg-html ($FAIL)"
exit 1
