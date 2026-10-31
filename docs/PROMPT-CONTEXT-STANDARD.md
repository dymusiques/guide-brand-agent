---
context_version: "2026-10-30-l012"
repo_path: "docs/PROMPT-CONTEXT-STANDARD.md"
goal: "Prompt 与上下文窗口标准（Brand Agent · 全仓 Must）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "fcac933726efa12f"
---

# Prompt 与上下文窗口标准（Brand Agent · 全仓 Must）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **课程方法论：** 输入上下文要**结构化、自包含**；长**输出**走 Open WebUI **Pipe**；事实走 **RAG**；结构化表走 **SQLite Tool**（可选）。  
> **平台分工：** [COURSE-METHOD-TO-YOUR-STACK.md](./COURSE-METHOD-TO-YOUR-STACK.md) 
- **Path:** `docs/PROMPT-CONTEXT-STANDARD.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **2. 输出长度 → 路由（防输出窗口偷懒）**: | 输出类型 | 路由 | Prompt 写法 |
- **4. CEO / Manager Prompt（Cursor 专用）**: - **步 −1：** `run-openwebui-router-pipeline.sh --goal "原话"`（长文才跑）
- **6. 交叉验证（Must 写进交付要求）**: - RAG：**Sources** 或 mirror 路径
- **8. Flute Practice Buddy（独立 app）**: 见 `flute-practice-buddy/docs/PROMPT-AND-AGENT-ROUTING.md` — **应用内 Gemini** 短输出；长文档不进 app prompt。


---

## L2 正文

# Prompt 与上下文窗口标准（Brand Agent · 全仓 Must）

> **课程方法论：** 输入上下文要**结构化、自包含**；长**输出**走 Open WebUI **Pipe**；事实走 **RAG**；结构化表走 **SQLite Tool**（可选）。  
> **平台分工：** [COURSE-METHOD-TO-YOUR-STACK.md](./COURSE-METHOD-TO-YOUR-STACK.md) · **Open WebUI intake：** [OPENWEBUI-INTAKE-PROMPT-TEMPLATE.md](./OPENWEBUI-INTAKE-PROMPT-TEMPLATE.md)


## 2. 输出长度 → 路由（防输出窗口偷懒）

| 输出类型 | 路由 | Prompt 写法 |
|----------|------|-------------|
| ≤1000 字、标题、标签、gate 改稿 | **Cursor** 普通模型 | L0+L1；材料 `@file` 或路径 |
| 1000–4000+ 字、分节长文、口播系列 | **Open WebUI CoT / HYBRID** | `--goal` + `--intake`；Router 自动 |
| 整份长文翻译/改写 | **Open WebUI Diligent** | 整段进 Pipe，**不要** Cursor 单轮 |
| 只要事实 + Sources | **Open WebUI RAG_ONLY** | goal 含「只要事实」「引用 Sources」 |
| 摘要压短 | **Cursor 或普通聊天** | 输出短，无需 Pipe |
| verify / gate / HTML / Canva | **SKIP Open WebUI** | Router → CEO 链 |


## 4. CEO / Manager Prompt（Cursor 专用）

- **步 −1：** `run-openwebui-router-pipeline.sh --goal "原话"`（长文才跑）  
- **步 0–N：** [AUTO-WORKFLOW.md](../agents/00-manager/AUTO-WORKFLOW.md) 不变  
- **Owner 目标：** 原话进 `--goal`；细节进 **intake** 或 **Brief**，不扩写进 Manager chat


## 6. 交叉验证（Must 写进交付要求）

- RAG：**Sources** 或 mirror 路径  
- SQL Tool：工具 CSV vs 正文  
- Brief：gate / adversarial


## 8. Flute Practice Buddy（独立 app）

见 `flute-practice-buddy/docs/PROMPT-AND-AGENT-ROUTING.md` — **应用内 Gemini** 短输出；长文档不进 app prompt。