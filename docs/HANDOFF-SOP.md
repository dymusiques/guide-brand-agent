# 交班 SOP · 一页纸（M5）

> **CEO/GM 接手包（2026-10-28）：** [HANDOFF-CEO-GM-SOP-PACK.md](HANDOFF-CEO-GM-SOP-PACK.md) · JSON `integration/handoff/ceo-gm-operating-manifest.json`  
> **新 Agent 主 SOP：** [NEW-AGENT-WORKFLOW-SOP.md](NEW-AGENT-WORKFLOW-SOP.md) · 思维导图：[workflow-handoff-mindmap.html](workflow-handoff-mindmap.html)  
> 程序状态全文：[AGENT-TAKEOVER.md](AGENT-TAKEOVER.md) · 本页 = **交班最小步骤**。

## Owner 只做两件事（系统不能替代）

1. **各平台发帖**（小红书 / IG 等）  
2. **导出 CSV →** `content/analytics/inbox/`（暂无 API 自动拉数）

## 机器层（Owner setup 后 · 其余）

见 [BACKGROUND-GOAL-EVOLUTION.md](BACKGROUND-GOAL-EVOLUTION.md)（**每日 09:00** cycle）。Debug 单次：`bash scripts/manager-autopilot.sh`

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
git submodule update --init --recursive
bash scripts/ensure-venv-deps.sh
bash scripts/verify-handoff.sh
bash scripts/manager-autopilot.sh
python scripts/screen-artist-watchlist.py
VERIFY_TIER=release bash scripts/verify-all.sh   # 有 key 时
```

**Artist 对标 · 新机/full：** [SOP-ARTIST-BENCHMARK-AND-HANDOFF.md](SOP-ARTIST-BENCHMARK-AND-HANDOFF.md)（**勿**对 artist 用 SWOT；用 DB/PLD/APO/CTD）。

## 认知期节奏

- 每周 1 深度 Brief · Daily 日更  
- **每 15 天** OPERATING-PLAN 快检  
- **每 4 篇深度** 轮检  

## 定时提醒（可选）

见 `content/marketing/automation/CURSOR-AUTOMATION-15D.md` — 在 Cursor Automations 里每 15 天跑 autopilot。
