---
context_version: "2026-10-30-l012"
repo_path: "content/marketing/automation/CURSOR-AUTOMATION-15D.md"
goal: "Cursor Automation · 15 天快检提醒（可选）"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "8492cc7e17f7103a"
---

# Cursor Automation · 15 天快检提醒（可选）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** **目的：** 每 15 天自动跑 `manager-autopilot`，提醒你快检（**不** 自动发帖、**不** 拉小红书 API）。
- **Path:** `content/marketing/automation/CURSOR-AUTOMATION-15D.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **建议在 Cursor Automations 里配置**: | 字段 | 建议值 |
- **本地手动（不等 Automation）**: ```bash


---

## L2 正文

# Cursor Automation · 15 天快检提醒（可选）

**目的：** 每 15 天自动跑 `manager-autopilot`，提醒你快检（**不** 自动发帖、**不** 拉小红书 API）。

## 建议在 Cursor Automations 里配置

| 字段 | 建议值 |
|------|--------|
| **名称** | danying-brand · 15d autopilot |
| **触发** | 每 15 天 · 定时（或 cron `0 9 */15 * *` 类） |
| **仓库** | `danying-brand-agent` · branch `main` |
| **指令摘要** | 运行 `bash scripts/manager-autopilot.sh`；读 `derived/ceo-dispatch-latest.md`；列出 Owner 待办（发帖/CSV）；**禁止** 代发帖 |

## 本地手动（不等 Automation）

```bash
bash scripts/manager-autopilot.sh
```

Owner 仍负责：发帖、填 Brief `## 发布状态`、inbox CSV。