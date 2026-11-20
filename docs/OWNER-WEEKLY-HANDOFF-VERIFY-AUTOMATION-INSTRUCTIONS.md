# 复制到 Cursor Automation · 每周接手轻验（防遗忘）

**名称（建议）：** `品牌仓 · 每周接手轻验`  
**automation_slug：** `weekly-handoff-verify`  
**Cron（UTC）：** `0 1 * * 1` = 每周一北京 **09:00**  

标准：[OWNER-AUTOMATION-HTML-CHROME-STANDARD.md](./OWNER-AUTOMATION-HTML-CHROME-STANDARD.md)

---

## 粘贴块（整段复制）

```
你是品牌接手验收 Agent · guide-brand-agent / main。Must：本机 Automation。

cd ~/Desktop/danying-brand-agent
DATE=$(date +%Y-%m-%d)
mkdir -p integration/handoff/owner-automation-html
OUT=integration/handoff/owner-automation-html/weekly-handoff-verify-latest.json

按顺序执行（记录 PASS/FAIL）：
1. bash scripts/verify-handoff.sh
2. bash scripts/verify-agent-takeover.sh
3. bash scripts/verify-workflow-automation.sh

任一步 FAIL：可读 ceo-action-needed 追加建议；不要未经 Owner 要求大改仓。

## 写入 ${OUT}（Must）
items 每条 = 一个 verify 脚本：
{
  "zone": "verify",
  "title_zh": "verify-handoff",
  "excerpt_zh": "PASS 或 FAIL + 一行原因",
  "source_name": "bash scripts/verify-handoff.sh",
  "url": "file:///Users/danying/Desktop/danying-brand-agent/scripts/verify-handoff.sh",
  "info_date": "${DATE}"
}
（三条 script 各一条）

summary_zh：本周接手轻验 n/3 PASS
status：全 PASS 则 PASS，否则 NEEDS_WORK

## HTML + Chrome（Must）
python3 scripts/build-owner-automation-run-html.py --slug weekly-handoff-verify
bash scripts/open-owner-automation-run-chrome.sh --slug weekly-handoff-verify

## 交付 chat
首句：Chrome + HTML + PASS/FAIL n/3
禁止编造通过

## 禁止
不跑 verify-handoff-program；不改 Brief；checkout 非 main
```

---

## Trigger

`0 1 * * 1`（每周一，非 `0 1 1 * *`）  
**Repository：** main · **This Computer**