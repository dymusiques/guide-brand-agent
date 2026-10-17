# 交班 SOP · 一页纸（M5）

> **新 Agent 必读全文：** [AGENT-TAKEOVER.md](AGENT-TAKEOVER.md)（程序状态 + 三轨 + verify）  
> 详细：`docs/HANDOFF-COMPLETENESS.md` · 本页 = **换机 / 新 Agent / 大改后** 最小步骤。

## Owner 只做两件事（系统不能替代）

1. **各平台发帖**（小红书 / IG 等）  
2. **导出 CSV →** `content/analytics/inbox/`（暂无 API 自动拉数）

## 全自动编排（其余）

```bash
bash scripts/manager-autopilot.sh
```

可选全量质检：`AUTOPILOT_FULL=1 bash scripts/manager-autopilot.sh`（含 CI 档 verify-all）

## 交班前 Must（约 15 分钟）

| 步 | 命令 / 动作 |
|----|-------------|
| 1 | `bash scripts/manager-autopilot.sh` |
| 2 | `VERIFY_TIER=release bash scripts/verify-all.sh`（有 Gemini key） |
| 3 | `bash scripts/verify-handoff.sh` |
| 4 | 读 `content/analytics/derived/ceo-dispatch-latest.md` + `manager-dashboard-*.md` |
| 5 | **git commit** 定稿（Owner 要求时） |

## 新 Agent clone 后 Must

```bash
bash scripts/ensure-venv-deps.sh
bash scripts/manager-autopilot.sh
VERIFY_TIER=release bash scripts/verify-all.sh   # 有 key 时
```

## 认知期节奏

- 每周 1 深度 Brief · Daily 日更  
- **每 15 天** OPERATING-PLAN 快检  
- **每 4 篇深度** 轮检  

## 定时提醒（可选）

见 `content/marketing/automation/CURSOR-AUTOMATION-15D.md` — 在 Cursor Automations 里每 15 天跑 autopilot。
