#!/usr/bin/env bash
# Archive exported CSV from content/analytics/inbox/ into platform warehouses.
# Does not call platform APIs — place backend exports in inbox/ first.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
INBOX="$ROOT/content/analytics/inbox"
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"
else echo "FAIL no python"; exit 1; fi

shopt -s nullglob
files=("$INBOX"/*.csv "$INBOX"/*.CSV)
if [[ ${#files[@]} -eq 0 ]]; then
  echo "inbox empty — export CSV from 小红书/Instagram/YouTube 后台 into:"
  echo "  $INBOX"
  echo "Naming hint: xiaohongshu-*.csv | instagram-*.csv | youtube-*.csv"
  exit 0
fi

import_one() {
  local platform="$1" file="$2"
  echo "→ import $platform: $(basename "$file")"
  "$PY" scripts/analytics-import.py --platform "$platform" --file "$file"
  mkdir -p "$INBOX/done"
  mv "$file" "$INBOX/done/"
}

for f in "${files[@]}"; do
  base=$(basename "$f" | tr '[:upper:]' '[:lower:]')
  if [[ "$base" == *xiaohongshu* || "$base" == *xhs* || "$base" == *redbook* ]]; then
    import_one xiaohongshu "$f"
  elif [[ "$base" == *instagram* || "$base" == *ig* ]]; then
    import_one instagram "$f"
  elif [[ "$base" == *youtube* || "$base" == *yt* ]]; then
    import_one youtube "$f"
  else
    echo "SKIP $(basename "$f") — cannot detect platform; rename with xiaohongshu|instagram|youtube"
  fi
done

echo "fetch/archive done"
