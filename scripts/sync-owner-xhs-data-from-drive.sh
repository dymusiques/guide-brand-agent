#!/usr/bin/env bash
# Pull Owner「我的小红书数据」Drive folder → listing JSON + raw xlsx → optional analytics pipeline.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

HANDOFF="$ROOT/integration/handoff/owner-xhs-data-drive.json"
FOLDER_ID="1kFYScZvFgd52983gK0gItIuRq0-43WyR"
LISTING_DIR="$ROOT/content/personal-ip/intake/_raw/owner-xhs-data"
DOWNLOAD_DIR="$ROOT/content/analytics/raw/xiaohongshu/drive-sync-latest"

PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1
fi

if [[ -f "$HANDOFF" ]]; then
  FOLDER_ID="$("$PY" -c "import json; print(json.load(open('$HANDOFF'))['drive_folder_id'])")"
fi

mkdir -p "$LISTING_DIR" "$DOWNLOAD_DIR"

echo ">>> refresh Drive listing (owner xhs data)"
"$PY" "$ROOT/scripts/refresh-owner-xhs-drive-listing.py"

echo ">>> download xlsx from Drive → $DOWNLOAD_DIR"
"$PY" -m gdocs --secrets-dir vendor/gdocs-skill/secrets drive download "$FOLDER_ID" \
  --output-dir "$DOWNLOAD_DIR"

echo ">>> merge CEO corpus catalog (includes 我的小红书数据 folder)"
"$PY" "$ROOT/scripts/refresh-ceo-drive-catalog.py" || echo "WARN: refresh-ceo-drive-catalog skipped"

NOTES_XLSX=""
shopt -s nullglob globstar
for candidate in \
  "$DOWNLOAD_DIR"/笔记列表明细表*.xlsx \
  "$DOWNLOAD_DIR"/*/*笔记列表明细表*.xlsx \
  "$DOWNLOAD_DIR"/*notes-detail*.xlsx; do
  NOTES_XLSX="$candidate"
  break
done

if [[ "${SKIP_ANALYTICS_PIPELINE:-0}" != "1" ]]; then
  echo ">>> auto-sync warehouse (Drive → raw → notes.csv + Excel)"
  bash "$ROOT/scripts/xhs-owner-data-auto-sync.sh" --from-dir "$DOWNLOAD_DIR" || \
    echo "WARN: xhs-owner-data-auto-sync failed — check Drive xlsx in $DOWNLOAD_DIR"
fi

echo "OK sync-owner-xhs-data-from-drive · listing=$LISTING_DIR/drive-listing-latest.json"
