#!/usr/bin/env bash
# One-click smoke: minimal JSON → HTML → Google Chrome (This Mac only).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
SLUG="${1:-smoke-test}"
DATE="$(date +%Y-%m-%d)"
mkdir -p integration/handoff/owner-automation-html
mkdir -p content/evolution/00-manager/ceo-inbox/automation-runs

JSON="integration/handoff/owner-automation-html/${SLUG}-latest.json"
cat >"$JSON" <<EOF
{
  "version": "2026-11-20",
  "automation_slug": "${SLUG}",
  "automation_title_zh": "Automation 冒烟测试",
  "run_date": "${DATE}",
  "status": "PASS",
  "summary_zh": "本机 Chrome 弹出链路的自检（非真实业务数据）",
  "md_path": "docs/OWNER-AUTOMATION-HTML-CHROME-STANDARD.md",
  "items": [
    {
      "zone": "verify",
      "title_zh": "Chrome 冒烟",
      "excerpt_zh": "若你看到本页，说明 build + open 脚本正常。",
      "source_name": "smoke-owner-automation-chrome.sh",
      "url": "file://${ROOT}/docs/OWNER-AUTOMATION-HTML-CHROME-STANDARD.md",
      "info_date": "${DATE}"
    }
  ]
}
EOF

python3 scripts/build-owner-automation-run-html.py --slug "$SLUG"
bash scripts/open-owner-automation-run-chrome.sh --slug "$SLUG"
echo "OK smoke · slug=${SLUG}"