# 新 Agent 接手 · Workflow + MD + Verify SOP（2026-10-27）

> **可视化：** [workflow-handoff-mindmap.html](./workflow-handoff-mindmap.html) · 打开：`bash scripts/open-workflow-handoff-mindmap.sh`  
> **Owner 与 Agent 对齐：** 思维导图底部 **双方确认清单** 全勾后，本 SOP 即为交班真相源。  
> **替代关系：** 接管 [HANDOFF-SOP.md](./HANDOFF-SOP.md) 中的「日常主路径」描述；交班 verify 表仍有效。

---

## 0 · 一句话

**Owner** 口语给目标 + 发帖 + CSV。**Cursor 内 00 CEO** 派 **01–09 GM** 写稿/进化/红队/Gate。**机器层** 每天 09:00 跑验收与 evolution rollup（Launcher）。**新 Agent** 按本 SOP 读 MD、跑 verify，**不**依赖旧 chat。

---

## 1 · Owner 边界（Must）

| Owner | 系统 |
|-------|------|
| 口语/碎片目标 + 资料 | CEO 解析 → Collector intake |
| 确认 gold / 发布 / 裁决 | 内部 Gate PASS 后才交接 |
| 小红书/App 发帖 | Agent 不代发 |
| CSV → `content/analytics/inbox/` | 后台 cycle 自动 pipeline |

文档：[OWNER-INPUT-PRINCIPLES.md](./OWNER-INPUT-PRINCIPLES.md) · [integration/IMPORTANT.md](../integration/IMPORTANT.md)

---

## 2 · 日更 GM 三件套（10 / 11 / 12）

见 [DAILY-GM-TRIO-SOP.md](./DAILY-GM-TRIO-SOP.md) · Owner 每日读 `content/daily-brief/<date>-owner-daily-brief.md`

## 3 · 三层架构

```text
┌─ Owner ─────────────────────────────────────────┐
└────────────────────┬────────────────────────────┘
                     ▼
┌─ 00 CEO（Cursor 会话）───────────────────────────┐
│  AUTO-WORKFLOW · CEO Gate · 收 GM-REPORT        │
└────────────────────┬────────────────────────────┘
                     ▼
┌─ 01–09 部门 GM ─────────────────────────────────┐
│  Collector · v0→vN · Evaluator · INTEGRATION    │
└────────────────────┬────────────────────────────┘
                     ▼
┌─ 机器层（Process Launcher · 每日 09:00）───────┐
│  verify-goals · 6case · rollups · work-queue     │
└─────────────────────────────────────────────────┘
```

| 文档 |
|------|
| [IP-MANAGEMENT-HIERARCHY.md](./IP-MANAGEMENT-HIERARCHY.md) · [CEO-AUTO-QA-LOOP.md](./CEO-AUTO-QA-LOOP.md) · [BACKGROUND-GOAL-EVOLUTION.md](./BACKGROUND-GOAL-EVOLUTION.md) |

---

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

---

## 4 · MD 读序（Must · 与 manifest 一致）

**权威清单：** [HANDOFF-MD-MANIFEST.md](./HANDOFF-MD-MANIFEST.md)

**2026-10-27 增量（Must 追加）：**

| 路径 | 用途 |
|------|------|
| [NEW-AGENT-WORKFLOW-SOP.md](./NEW-AGENT-WORKFLOW-SOP.md) | 本 SOP |
| [BACKGROUND-GOAL-EVOLUTION.md](./BACKGROUND-GOAL-EVOLUTION.md) | 后台 cycle |
| [BRIEF-REDTEAM-PRE.md](../content/xiaohongshu/BRIEF-REDTEAM-PRE.md) | Brief 前红队 |
| [COLLECTOR-EVALUATOR-PIPELINE.md](./COLLECTOR-EVALUATOR-PIPELINE.md) | baseline / 编辑距离 |
| [GEMINI-NETWORK-AUTO.md](./GEMINI-NETWORK-AUTO.md) | VPN / 代理 |
| [IP-SUBAGENT-ROSTER.md](../content/personal-ip/IP-SUBAGENT-ROSTER.md) | 01–09 编制 |

---

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

---

## 6 · 新 Agent 第一天（终端）

```bash
cd ~/Desktop/danying-brand-agent   # 或本机路径
bash scripts/ensure-venv-deps.sh
bash scripts/verify-agent-takeover.sh
bash scripts/verify-handoff.sh
bash scripts/open-workflow-handoff-mindmap.sh   # 与 Owner 过思维导图 + 勾选清单
```

**读生成/刷新：**

- `content/evolution/00-manager/ceo-inbox/agent-work-queue.md`
- `content/analytics/derived/ceo-dispatch-latest.md`
- `content/analytics/derived/evolution-rollups-latest.md`
- `content/evolution/00-manager/ceo-inbox/background-cycle-latest.md`

**Owner 口令：** `danying-brand-agent` → [danying-brand-agent-bootstrap.mdc](../.cursor/rules/danying-brand-agent-bootstrap.mdc)

---

## 7 · 后台 Setup（Owner 一次 · Agent 只文档化）

```bash
bash scripts/setup-background-goal-evolution.sh
cd vendor/process-launcher
../../.venv/bin/process-launcher start --config config/dba-brand-agent.yaml
```

改 cycle 频率：**Must 问 Owner** · [BACKGROUND-CYCLE-INTERVAL-TRIGGER.md](../integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md)

---

## 8 · 双方确认记录（交班勾选）

| # | 项 | Owner | Agent |
|---|-----|-------|-------|
| 1 | 思维导图清单已对齐 | ☐ | ☐ |
| 2 | `verify-agent-takeover.sh` PASS | — | ☐ |
| 3 | `verify-handoff.sh` PASS（或已知 FAIL 项文档化） | ☐ | ☐ |
| 4 | Launcher / 每日 cycle 策略已理解 | ☐ | ☐ |
| 5 | 旧 chat 不覆盖 Git L0 | — | ☐ |

**日期：** __________ **备注：** __________

---

## 9 · 刻意不做

- 多进程第二 CEO · 自动发帖 · 未 aligned 定稿 · 编造数据 · Owner 逐条手跑 verify

见 IMPORTANT Dry Run · [AUTOPILOT.md](./AUTOPILOT.md)（单次 Debug 仅）
