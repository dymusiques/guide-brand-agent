# Owner 工作区保洁 · 日程与 Automation

真源：`integration/handoff/owner-workspace-hygiene-schedule.json`

## 机械检查

```bash
cd ~/Desktop/danying-brand-agent
python3 scripts/owner-workspace-hygiene-alert.py
```

## 建议 Cursor Automation（周一 09:00 本地）

- **触发**：Cron `0 9 * * 1`（每周一 09:00）
- **仓库**：`guide-brand-agent` / `main`
- **指令（摘要）**：跑 `owner-workspace-hygiene-alert.py`；若有 WARN，在 chat 列出并建议归档或清 Layer C；不要 commit xlsx / `owner-*-latest.json`。

归档仍须 Owner 口令「定稿 / 归档」后由 Agent 执行 `archive-ceo-campaign-deliverables.sh`。

## 每周选题 Automation（周日）

- 名称：`品牌仓小红书每周选题包`（LinkedIn/Medium 见周日 12:00 另一条）
- Cron：`0 11 * * 0`（周日 11:00 GMT+8）
- 手册：[OWNER-WEEKLY-TOPIC-PACK.md](./OWNER-WEEKLY-TOPIC-PACK.md)