# Cursor Automation 索引（品牌仓）

各自 **独立** Cron · 互不可替代。

**分支：** 全部 `guide-brand-agent @ main` · 见 [OWNER-CURSOR-AUTOMATION-BRANCH-PIN.md](./OWNER-CURSOR-AUTOMATION-BRANCH-PIN.md)

**Cron 时区：** 手填 `30 10 * * *` 若变成 18:30，说明按 UTC 算了 → 用 UI 选 10:30 GMT+8 或 UTC `30 2 * * *`。

| # | 名称（建议） | Cron (GMT+8) | Instructions 文档 |
|---|--------------|--------------|-------------------|
| 1 | **品牌仓 · 小红书每周选题包** | 周日 11:00 | `OWNER-WEEKLY-TOPIC-AUTOMATION-INSTRUCTIONS.md` |
| 1b | **品牌仓 · LinkedIn+Medium 每周选题** | 周日 12:00 | `OWNER-WEEKLY-LI-MEDIUM-TOPIC-AUTOMATION-INSTRUCTIONS.md` |
| 2 | 品牌仓 · 每周保洁提醒 | 周四 11:00（你已配） | `OWNER-WORKSPACE-HYGIENE.md` 内 Automation 段 |
| 3 | **（可选）小红书 · 导表提醒** | **周三+周日 20:30** | `OWNER-XHS-EXPORT-REMINDER-AUTOMATION-INSTRUCTIONS.md` |
| 4 | **（可选）Drive 日检 · 小红书数据** | **每天 10:30** | `OWNER-XHS-DRIVE-WATCH-AUTOMATION-INSTRUCTIONS.md` |

**说明：** 你目前常见只有 **#1 + #2**。#3、#4 是飞轮补强，**不**替代选题/保洁。

**#1b 尚未进 Cursor UI 时：** 只存在仓库文档 `OWNER-WEEKLY-LI-MEDIUM-TOPIC-AUTOMATION-INSTRUCTIONS.md`；须在 Cursor **Automations → New** 粘贴指令并保存。Agent 可用 `open_automation` 预填草稿（周日 12:00 GMT+8 · `guide-brand-agent @ main`）。

另：**本机** `process-launcher` 09:00 跑 `background-goal-evolution-cycle` —— 那是 **第 5 类**（非 Cursor Automation）。