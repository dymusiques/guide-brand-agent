#!/bin/bash
# 双击本文件 → 用默认浏览器打开 Owner HTML 报告（不要在 Cursor 里当代码看）
DIR="$(cd "$(dirname "$0")" && pwd)"
HTML="$DIR/OWNER-XHS-FILTER-DELIVERABLE-2026-10-27.html"
if [[ ! -f "$HTML" ]]; then
  HTML="$(ls -t "$DIR"/OWNER-XHS-FILTER-DELIVERABLE-*.html 2>/dev/null | head -1)"
fi
if [[ -z "$HTML" || ! -f "$HTML" ]]; then
  echo "找不到 HTML 报告"
  read -r -p "按回车关闭…"
  exit 1
fi
open "$HTML"
echo "已在浏览器打开：$HTML"
sleep 1
