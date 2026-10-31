#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DAY="${CEO_OWNER_HTML_DAY:-$(date +%Y-%m-%d)}"
HTML="$ROOT/content/evolution/00-manager/ceo-inbox/OWNER-MULTICHANNEL-DELIVERABLE-$DAY.html"
[[ -f "$HTML" ]] || HTML="$(ls -t "$ROOT/content/evolution/00-manager/ceo-inbox"/OWNER-MULTICHANNEL-DELIVERABLE-*.html 2>/dev/null | head -1)"
[[ -f "$HTML" ]] || { echo "FAIL: no multichannel HTML"; exit 1; }
open "file://${HTML}#multichannel"
echo "OK open multichannel · file://${HTML}#multichannel"
