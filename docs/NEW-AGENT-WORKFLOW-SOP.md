---
context_version: "2026-10-30-l012"
repo_path: "docs/NEW-AGENT-WORKFLOW-SOP.md"
goal: "新 Agent 接手 · Workflow + MD + Verify SOP（2026-10-27）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "19d5c5217d4931c9"
---

# 新 Agent 接手 · Workflow + MD + Verify SOP（2026-10-27）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **可视化：** [workflow-handoff-mindmap.html](./workflow-handoff-mindmap.html) · 打开：`bash scripts/open-workflow-handoff-mindmap.sh`  
> **Owner 与 Agent 对齐：** 思维导图底部 **双方确认清单** 全勾后，本 S
- **Path:** `docs/NEW-AGENT-WORKFLOW-SOP.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **1 · Owner 边界（Must）**: | Owner | 系统 |
- **3 · 写单篇小红书 Brief（CEO 步序摘要）**: | 步 | 动作 | MD / Verify |
- **5 · Verify 地图（忠实标准）**: | 场景 | 命令 |
- **7 · 后台 Setup（Owner 一次 · Agent 只文档化）**: ```bash
- **9 · 刻意不做**: - 多进程第二 CEO · 自动发帖 · 未 aligned 定稿 · 编造数据 · Owner 逐条手跑 verify


---

## L2 正文

# 新 Agent 接手 · Workflow + MD + Verify SOP（2026-10-27）

> **可视化：** [workflow-handoff-mindmap.html](./workflow-handoff-mindmap.html) · 打开：`bash scripts/open-workflow-handoff-mindmap.sh`  
> **Owner 与 Agent 对齐：** 思维导图底部 **双方确认清单** 全勾后，本 SOP 即为交班真相源。  
> **替代关系：** 接管 [HANDOFF-SOP.md](./HANDOFF-SOP.md) 中的「日常主路径」描述；交班 verify 表仍有效。


## 1 · Owner 边界（Must）

| Owner | 系统 |
|-------|------|
| 口语/碎片目标 + 资料 | CEO 解析 → Collector intake |
| 确认 gold / 发布 / 裁决 | 内部 Gate PASS 后才交接 |
| 小红书/App 发帖 | Agent 不代发 |
| CSV → `content/analytics/inbox/` | 后台 cycle 自动 pipeline |

文档：[OWNER-INPUT-PRINCIPLES.md](./OWNER-INPUT-PRINCIPLES.md) · [integration/IMPORTANT.md](../integration/IMPORTANT.md)


## 3 · 写单篇小红书 Brief（CEO 步序摘要）

| 步 | 动作 | MD / Verify |
|----|------|-------------|
| 0 | CEO 计划 | `agents/00-manager/AUTO-WORKFLOW.md` |
| 0a | Intake 读栈 | `docs/XHS-CONTENT-INTAKE-STACK.md` · `verify-xhs-content-intake.sh` |
| **1c** | **红队 2 条**（Owner 固定） | `content/xiaohongshu/BRIEF-REDTEAM-PRE.md` · `redteam/<slug>-pre.md` |
| 2a? | 视频 Round1/2 | `content/xiaohongshu/XHS-VIDEO-ITERATION.md` · `verify-xhs-voice-qa.sh` |
| 2 | 04 写 Brief | `PIPELINE.md` · `evaluate-xhs-topic.py --brief` |
| 3 | aligned + 目录 | `manager-workflow-verify.sh <brief>` |
| Gate | 交 Owner 前 | `manager-ceo-owner-gate.sh --brief <brief>` |
| — | Owner 确认发布 | `CONTENT-DELIVERY-FOR-OWNER.md` |

单篇顺序图：[workflow-mindmap.html](./workflow-mindmap.html)


## 5 · Verify 地图（忠实标准）

| 场景 | 命令 |
|------|------|
| 新 Agent 植入 | `bash scripts/verify-agent-takeover.sh` |
| 交班 L0 | `bash scripts/verify-handoff.sh` |
| 全程序（Owner/交班） | `bash scripts/verify-handoff-program.sh` |
| 单 Brief 定稿 | `bash scripts/manager-workflow-verify.sh content/xiaohongshu/<brief>.md` |
| 交 Owner 前 Gate | `bash scripts/manager-ceo-owner-gate.sh --brief …` |
| M4 Goals | `bash scripts/verify-goals.sh` |
| 05 kernel | `bash scripts/verify-xhs-topic.sh` |
| Release 大交班 | `VERIFY_TIER=release bash scripts/verify-all.sh` |
| 后台 cycle 内容 | 见 [BACKGROUND-GOAL-EVOLUTION.md §一轮 cycle](./BACKGROUND-GOAL-EVOLUTION.md) |

分层：[VERIFY-TIERS.md](./VERIFY-TIERS.md) · Hub 表：[check.md](../check.md)


## 7 · 后台 Setup（Owner 一次 · Agent 只文档化）

```bash
bash scripts/setup-background-goal-evolution.sh
cd vendor/process-launcher
../../.venv/bin/process-launcher start --config config/dba-brand-agent.yaml
```

改 cycle 频率：**Must 问 Owner** · [BACKGROUND-CYCLE-INTERVAL-TRIGGER.md](../integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md)


## 9 · 刻意不做

- 多进程第二 CEO · 自动发帖 · 未 aligned 定稿 · 编造数据 · Owner 逐条手跑 verify

见 IMPORTANT Dry Run · [AUTOPILOT.md](./AUTOPILOT.md)（单次 Debug 仅）