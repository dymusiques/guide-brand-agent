#!/bin/bash
# 双击本文件 → 用默认浏览器打开当日 Owner HTML（含 #owner-latest 时自动弹出新稿）
DIR="$(cd "$(dirname "$0")" && pwd)"
DAY="$(date +%Y-%m-%d)"
HTML="$DIR/OWNER-XHS-FILTER-DELIVERABLE-$DAY.html"
if [[ ! -f "$HTML" ]]; then
  HTML="$(ls -t "$DIR"/OWNER-XHS-FILTER-DELIVERABLE-*.html 2>/dev/null | head -1)"
fi
if [[ -z "$HTML" || ! -f "$HTML" ]]; then
  echo "找不到 HTML 报告"
  read -r -p "按回车关闭…"
  exit 1
fi
open "file://${HTML}#owner-latest"
echo "已在浏览器打开：$HTML#owner-latest"
sleep 1
