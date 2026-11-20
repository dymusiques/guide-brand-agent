# Automation HTML handoff（Layer C · 本机）

每条 Cursor Automation 跑完后写入 `<slug>-latest.json`，再由 `scripts/build-owner-automation-run-html.py` 生成 HTML。

规范：`docs/OWNER-AUTOMATION-HTML-CHROME-STANDARD.md`