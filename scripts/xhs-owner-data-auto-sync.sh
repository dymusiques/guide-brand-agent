#!/usr/bin/env bash
# Owner 上传小红书后台 xlsx（Drive 同步目录 / Downloads / chat 路径）→ 全自动合并仓库 + Excel。
# Agent：见到新 xlsx 即跑本脚本；禁止再要求 Owner 说「同步小红书数据」。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1
fi

FROM_DIR=""
AS_OF="$(date +%Y-%m-%d)"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --from-dir)
      FROM_DIR="$2"
      shift 2
      ;;
    --as-of)
      AS_OF="$2"
      shift 2
      ;;
    *)
      echo "usage: $0 [--from-dir PATH] [--as-of YYYY-MM-DD]"
      exit 2
      ;;
  esac
done

if [[ -z "$FROM_DIR" ]]; then
  FROM_DIR="$ROOT/content/analytics/raw/xiaohongshu/drive-sync-latest"
fi
if [[ ! -d "$FROM_DIR" ]]; then
  echo "WARN: no upload dir $FROM_DIR (skip stage)"
fi

echo "=== xhs-owner-data-auto-sync · as_of=$AS_OF · from=$FROM_DIR ==="

if [[ -d "$FROM_DIR" ]] && compgen -G "$FROM_DIR/*.xlsx" >/dev/null; then
  echo ">>> stage Owner xlsx"
  "$PY" scripts/analytics/xhs_sync_warehouse.py stage --from-dir "$FROM_DIR" --as-of "$AS_OF"
else
  echo ">>> merge warehouse (no new files in $FROM_DIR)"
  "$PY" scripts/analytics/xhs_sync_warehouse.py merge --as-of "$AS_OF"
fi

if [[ -d "$FROM_DIR" ]] && compgen -G "$FROM_DIR/*数据明细表*.xlsx" >/dev/null; then
  echo ">>> detail-json from uploads"
  "$PY" scripts/analytics/xhs_note_detail.py ingest --dir "$FROM_DIR" || true
fi

echo ">>> analytics pipeline"
bash "$ROOT/scripts/analytics-pipeline.sh"

echo "OK xhs-owner-data-auto-sync · notes=$(wc -l < content/analytics/xiaohongshu/notes.csv | tr -d ' ') lines"
