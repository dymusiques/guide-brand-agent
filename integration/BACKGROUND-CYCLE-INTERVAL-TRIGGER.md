---
context_version: "2026-10-30-l012"
repo_path: "integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md"
goal: "TRIGGER · 后台 cycle 频率变更（Agent Must 问 Owner）"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "20bb774f99237d98"
---

# TRIGGER · 后台 cycle 频率变更（Agent Must 问 Owner）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner 固定（2026-10-27）：** **每天 1 次** · 09:00 Asia/Shanghai · `dba_goal_evolution_daily`  
> **Agent：** 下列任一情况 **必须先向 Owner 确认** 再改 `integration/templates/dba-launcher-goal-evolut
- **Path:** `integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **必须确认 Owner 的情况**: | 触发 | 示例 |
- **不必问（可直接改集成层）**: - Bugfix cycle 脚本崩溃
- **改完必做**: 1. `bash scripts/setup-background-goal-evolution.sh`（重写 `vendor/process-launcher/config/dba-brand-ag…
- **当前真相源**: - 模板：`integration/templates/dba-launcher-goal-evolution.yaml`


---

## L2 正文

# TRIGGER · 后台 cycle 频率变更（Agent Must 问 Owner）

> **Owner 固定（2026-10-27）：** **每天 1 次** · 09:00 Asia/Shanghai · `dba_goal_evolution_daily`  
> **Agent：** 下列任一情况 **必须先向 Owner 确认** 再改 `integration/templates/dba-launcher-goal-evolution.yaml` 并说明需 **重启 Launcher**。

## 必须确认 Owner 的情况

| 触发 | 示例 |
|------|------|
| **cycle 间隔** | 30 分钟 / 每小时 / 每周 / 改 daily 时刻 |
| **验收档位变重** | 每 cycle 跑 `verify-all` release、加 agent-matrix 全量 |
| **验收档位变轻** | 跳过 `verify-goals` 或 6 case |
| **自动写稿** | headless `cursor agent` 进 loop |
| **日更 GM 三件套职责/频率** | 10/11/12 见 [DAILY-GM-TRIO-SOP.md](../docs/DAILY-GM-TRIO-SOP.md) — **已 Owner 确认 daily** |
| **自动 commit / Drive / 发帖** | 任何离开 IMPORTANT 红线的自动化 |

## 不必问（可直接改集成层）

- Bugfix cycle 脚本崩溃  
- 与 Owner 已确认策略 **一致** 的文档 typo  
- Gemini 智能代理（`gemini_config.py`）不改变 schedule  

## 改完必做

1. `bash scripts/setup-background-goal-evolution.sh`（重写 `vendor/process-launcher/config/dba-brand-agent.yaml`）  
2. 告知 Owner：**Terminal 重启** `process-launcher`（见 [BACKGROUND-GOAL-EVOLUTION.md](../docs/BACKGROUND-GOAL-EVOLUTION.md)）  
3. Collector 记一条 intake（`00-manager` · slug `background-interval`）

## 当前真相源

- 模板：`integration/templates/dba-launcher-goal-evolution.yaml`  
- 说明：`docs/BACKGROUND-GOAL-EVOLUTION.md` §「一轮 cycle 里有什么」