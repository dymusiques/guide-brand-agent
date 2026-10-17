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
