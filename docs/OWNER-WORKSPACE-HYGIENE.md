# Owner 工作区保洁 · 日程与 Automation

真源：`integration/handoff/owner-workspace-hygiene-schedule.json`

## 机械检查

```bash
cd ~/Desktop/danying-brand-agent
python3 scripts/owner-workspace-hygiene-alert.py
```

## 建议 Cursor Automation（周四 11:00 本地）

- **完整 Instructions：** [OWNER-WORKSPACE-HYGIENE-AUTOMATION-INSTRUCTIONS.md](./OWNER-WORKSPACE-HYGIENE-AUTOMATION-INSTRUCTIONS.md)（含 HTML + Chrome）
- **触发**：Cron 见该文档（每周四 11:00 GMT+8）
- **仓库**：`guide-brand-agent` / `main` · **This Computer**

归档仍须 Owner 口令「定稿 / 归档」后由 Agent 执行 `archive-ceo-campaign-deliverables.sh`。

## 每周选题 Automation（周日）

- 名称：`品牌仓小红书每周选题包`（LinkedIn/Medium 见周日 12:00 另一条）
- Cron：`0 11 * * 0`（周日 11:00 GMT+8）
- 手册：[OWNER-WEEKLY-TOPIC-PACK.md](./OWNER-WEEKLY-TOPIC-PACK.md)