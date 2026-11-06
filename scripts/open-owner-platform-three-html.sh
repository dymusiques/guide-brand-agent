#!/usr/bin/env bash
# LinkedIn → 小红书 → Medium：三平台成稿依次在浏览器打开。
# evolve / Gate FAIL 时也 Must 执行（见 docs/CEO-FULL-EXECUTION-MANDATE.md）。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="${1:-$ROOT/content/evolution/00-manager/ceo-inbox/2026-11-03-artists-three}"
GAP="${CEO_PLATFORM_HTML_OPEN_GAP:-2}"

if [[ "${CEO_OWNER_HTML_OPEN:-1}" == "0" ]]; then
  echo "SKIP open-owner-platform-three-html (CEO_OWNER_HTML_OPEN=0)"
  exit 0
fi

for name in linkedin.html xiaohongshu.html medium.html; do
  f="$DIR/$name"
  [[ -f "$f" ]] || { echo "FAIL: missing $f"; exit 1; }
done

if [[ "$(uname -s)" != Darwin ]]; then
  echo "HINT: non-macOS — open manually:"
  echo "  file://$DIR/linkedin.html"
  echo "  file://$DIR/xiaohongshu.html"
  echo "  file://$DIR/medium.html"
  exit 0
fi

open "file://${DIR}/linkedin.html"
sleep "$GAP"
open "file://${DIR}/xiaohongshu.html"
sleep "$GAP"
open "file://${DIR}/medium.html"
echo "OK open-owner-platform-three-html · linkedin → xiaohongshu → medium · $DIR"
