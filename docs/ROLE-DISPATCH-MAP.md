---
context_version: "2026-10-30-l012"
repo_path: "docs/ROLE-DISPATCH-MAP.md"
goal: "角色与派活一张图（防 Agent 混淆）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "fc86af80b612f3ad"
---

# 角色与派活一张图（防 Agent 混淆）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **读者：** Cursor 里任何一次会话。  
> **原则：** 层级可以多，但 **同一时刻只有一个「我在扮演谁」**；按 **步序** 切换，不要混 Key、混工具、混终稿标准。
- **Path:** `docs/ROLE-DISPATCH-MAP.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **谁是谁（不要混）**: | 角色 | 是什么 | 不是什么 |
- **派活顺序（Must · 有任务就按表走）**: | 步 | 谁执行 | 做什么 | 用什么 Key/API | 产出 |
- **效率：为什么层级多但不乱**: | 看起来多 | 实际分工 |
- **Agent 会话入口（只读这三处即可开工）**: 1. [`agents/00-manager/AUTO-WORKFLOW.md`](../agents/00-manager/AUTO-WORKFLOW.md) — 步序表


---

## L2 正文

# 角色与派活一张图（防 Agent 混淆）

> **读者：** Cursor 里任何一次会话。  
> **原则：** 层级可以多，但 **同一时刻只有一个「我在扮演谁」**；按 **步序** 切换，不要混 Key、混工具、混终稿标准。

## 谁是谁（不要混）

| 角色 | 是什么 | 不是什么 |
|------|--------|----------|
| **Owner** | 你 · 目标、否决、发帖、OAuth 一次 | 不替 Agent 跑 verify / 不手动测 Open WebUI |
| **00 Manager / CEO** | **单会话指挥塔** · 写计划、派步、gate、派活记录 | 不是 Open WebUI 里的聊天模型；不代替 04 写 Brief 正文（除非步 2 未派） |
| **01–09 sub-agent** | **职能 GM** · 各读 `INTEGRATION-PROMPT.md` · 产出进固定目录 | 不是独立 Cursor chat；由 Manager **顺序扮演** 或脚本 verify |
| **Open WebUI** | **长文/RAG 外包引擎** · outbox 素材 | 不是 CEO · 不是 PASS 终稿 · 不用 CEO `GEMINI_API_KEY` |
| **Cursor Agent** | 执行上面步序的 **同一工人** | 不要在一步里同时「像 CEO 拍板终稿」又「像 OWUI 生成长文」而不写清步序 |

## 派活顺序（Must · 有任务就按表走）

| 步 | 谁执行 | 做什么 | 用什么 Key/API | 产出 |
|----|--------|--------|----------------|------|
| **−1** | Manager 自跑脚本 | `run-openwebui-router-pipeline.sh`（可 `--intake`） | Open WebUI → **OpenRouter** | outbox `.md` + `openwebui-jobs/*.json` |
| **−1b** | 若 route=**SKIP** | 跳过 Open WebUI | — | 直接步 0 |
| **0** | **00 Manager** | 3 行计划；若有 outbox → **intake: outbox**（素材，非终稿） | — | 计划 / 派活记录 |
| **1–2** | **01 / 03 / 04…** | 战略、Brief、三镜头（见 AUTO-WORKFLOW） | **GEMINI**（CEO `.env`） | `content/…` |
| **3** | **04 + 05 进化** | gap / adversarial / gate | **GEMINI** | READY Brief |
| **4+** | **06–09** | pipeline / 视觉 / 数据 | 按 agent | 可选 |

**混淆红线：**

- Open WebUI outbox **不得** 当 Owner 终稿；必须经 **04 + CEO gate**。
- **SKIP** 任务（gate、verify、小改）**不得** 为了「走流程」硬调 Open WebUI。
- **Gemini Key** 只给 Cursor/CEO 链；**OpenRouter** 只给 Open WebUI 链（见 `API-KEY-BOUNDARIES.md`）。

## 效率：为什么层级多但不乱

| 看起来多 | 实际分工 |
|----------|----------|
| 很多 `docs/*.md` | **索引层**：本文件 + `AUTO-WORKFLOW` + `workflow-automation-manifest.json` 三件套够 Agent 路由 |
| 01–12 agent 文件夹 | **并行开发边界**；运行时 Manager **按步点表**，不必一次读完全部 |
| CEO + Manager 同名混用 | **同一人格**：对外 CEO，对内 Manager 指挥链；文档里 **00 = 指挥塔** |
| Open WebUI + Cursor | **引擎分离**：长文/RAG 外包 OWUI；判断/改稿/派活在 Cursor |

## Agent 会话入口（只读这三处即可开工）

1. [`agents/00-manager/AUTO-WORKFLOW.md`](../agents/00-manager/AUTO-WORKFLOW.md) — 步序表  
2. [`integration/handoff/workflow-automation-manifest.json`](../integration/handoff/workflow-automation-manifest.json) — 机器层  
3. **本文件** — 角色边界  

Open WebUI 专项：[`OPENWEBUI-CEO-ROUTER.md`](./OPENWEBUI-CEO-ROUTER.md) · Key：[`API-KEY-BOUNDARIES.md`](./API-KEY-BOUNDARIES.md)