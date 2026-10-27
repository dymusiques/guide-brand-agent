#!/usr/bin/env bash
# Extract Momentum 2026 PDF → markdown excerpt for agents.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PDF="$ROOT/content/marketing/research/raw/momentum-2026.pdf"
ALT="$ROOT/content/marketing/research/raw/《Momentum 2026》小红书商业年度特刊.pdf"
if [[ ! -f "$PDF" && -f "$ALT" ]]; then
  ln -sf "$(basename "$ALT")" "$PDF" 2>/dev/null || cp "$ALT" "$PDF"
fi
OUT="$ROOT/content/marketing/research/xhs-momentum-2026-extract.md"
TXT="${PDF%.pdf}.txt"

if [[ ! -f "$PDF" ]]; then
  echo "FAIL: place Drive PDF at content/marketing/research/raw/momentum-2026.pdf"
  echo "See content/marketing/research/raw/README.md"
  exit 1
fi
if ! command -v pdftotext >/dev/null 2>&1; then
  echo "FAIL: install pdftotext (poppler)"
  exit 1
fi
pdftotext "$PDF" "$TXT"
{
  echo "# Momentum 2026 · 文本摘录（pdftotext）"
  echo ""
  echo "源文件: \`raw/momentum-2026.pdf\` · 生成: $(date -u +%Y-%m-%d)"
  echo ""
  echo "---"
  echo ""
  head -c 120000 "$TXT"
  echo ""
  echo "---"
  echo "（截断前 120k 字符；完整文本见 raw/momentum-2026.txt）"
} > "$OUT"
echo "wrote $OUT"
