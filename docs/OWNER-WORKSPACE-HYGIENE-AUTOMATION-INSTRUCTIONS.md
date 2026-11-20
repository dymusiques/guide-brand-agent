# 复制到 Cursor Automation · 每周工作区保洁

**名称（建议）：** `品牌仓 · 每周保洁提醒`  
**automation_slug：** `workspace-hygiene`  
**Cron：** `0 3 * * 4`（UTC）= 每周四 **11:00 GMT+8**  

（原摘要见 [OWNER-WORKSPACE-HYGIENE.md](./OWNER-WORKSPACE-HYGIENE.md)）

标准：[OWNER-AUTOMATION-HTML-CHROME-STANDARD.md](./OWNER-AUTOMATION-HTML-CHROME-STANDARD.md)

---

## 粘贴块（整段复制）

```
你是品牌仓保洁 Agent · guide-brand-agent / main。Must：本机 Automation。

cd ~/Desktop/danying-brand-agent
DATE=$(date +%Y-%m-%d)
mkdir -p integration/handoff/owner-automation-html
OUT=integration/handoff/owner-automation-html/workspace-hygiene-latest.json

python3 scripts/owner-workspace-hygiene-alert.py 2>&1 | tee /tmp/workspace-hygiene-${DATE}.log

## 写入 ${OUT}（Must）
items[]：每个 WARN 一条（无 WARN 则一条「本日无 WARN」）
- excerpt_zh：告警说明
- source_name：owner-workspace-hygiene-alert.py
- url：file:///.../integration/handoff/owner-workspace-hygiene-schedule.json
- info_date：${DATE}

status：有 WARN 则 NEEDS_WORK，否则 PASS
summary_zh：告警条数

勿 commit xlsx / owner-*-latest.json；归档须 Owner 口令。

## HTML + Chrome（Must）
python3 scripts/build-owner-automation-run-html.py --slug workspace-hygiene
bash scripts/open-owner-automation-run-chrome.sh --slug workspace-hygiene

## 交付 chat
首句：Chrome + HTML + WARN 列表

禁止未经 Owner 要求归档或 commit 大改。
```