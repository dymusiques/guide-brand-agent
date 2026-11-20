# 复制到 Cursor Automation · 小红书每周选题（Instructions 全文）

**名称：** `品牌仓小红书每周选题包`  
**automation_slug：** `weekly-topic-xhs`  
**Cron：** `0 3 * * 0`（UTC）= 每周日 **11:00 GMT+8**  
**分工：** LinkedIn + Medium → 周日 12:00 · [OWNER-WEEKLY-LI-MEDIUM-TOPIC-AUTOMATION-INSTRUCTIONS.md](./OWNER-WEEKLY-LI-MEDIUM-TOPIC-AUTOMATION-INSTRUCTIONS.md)

标准：[OWNER-AUTOMATION-HTML-CHROME-STANDARD.md](./OWNER-AUTOMATION-HTML-CHROME-STANDARD.md)

---

## 粘贴块（整段复制）

```
你是品牌选题 Agent · 仓库 guide-brand-agent / main。Must：本机 Automation。

本 Automation 仅小红书。禁止交付 LinkedIn/Medium 选题。

飞轮自检（Must）：先跑 python3 scripts/check-owner-flywheel-phase.py，交付开头复述 next_owner_action_zh 一句。

cd ~/Desktop/danying-brand-agent
DATE=$(date +%Y-%m-%d)
mkdir -p integration/handoff/owner-automation-html
HTML_JSON=integration/handoff/owner-automation-html/weekly-topic-xhs-latest.json

## 0. 机械链（Must）
1. bash scripts/run-owner-pending-videos-eval.sh --no-open
2. python3 scripts/owner-weekly-topic-pack.py

核对：
- content/strategy/weekly-topic-pack/weekly-topic-pack-<date>.md
- integration/handoff/owner-weekly-topic-pack-latest.json
- integration/handoff/owner-weekly-topic-pack-eval-latest.json

## 1–4. 选题规则（同 OWNER-WEEKLY-TOPIC-PACK.md）
5–10 条小红书；每条含标题、topic_kind、角度、evaluate 分；热点检索注明检索日期与依据（禁止编造搜索量）。

## 5. 写入 ${HTML_JSON}（Must）
items[]：每条选题一条
- zone: "topic"
- title_zh: 选题标题
- excerpt_zh: 角度 + 热点/常青依据 + evaluate 分
- source_name: Web 检索来源名 或「owner-weekly-topic-pack.py」
- url: 检索文章 URL（热点向 Must）；常青无外链则填 weekly-topic-pack md 路径 file://...
- info_date: ${DATE}

summary_zh：pass 条数 / 阈值 58
status：evaluate PASS 则 PASS，否则 NEEDS_WORK
md_path：content/strategy/weekly-topic-pack/weekly-topic-pack-${DATE}.md

## 6. HTML + Chrome（Must）
python3 scripts/build-owner-automation-run-html.py --slug weekly-topic-xhs
bash scripts/open-owner-automation-run-chrome.sh --slug weekly-topic-xhs

## 7. 交付 chat
首句：Chrome + HTML 路径 + evaluate 小结
表末 Evaluate 小结；结尾请 Owner 勾选序号
未勾选前不写 Brief、不 commit、不发帖

## 8. 禁止
编造分数；跳过 owner-weekly-topic-pack.py；交付 LinkedIn/Medium；checkout 非 main
```