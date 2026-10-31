---
context_version: "2026-10-30-l012"
repo_path: "docs/COURSE-METHOD-TO-YOUR-STACK.md"
goal: "课程方法论 → 你的真实栈（不是抄 WBR 作业）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "6cc201880e6b9175"
---

# 课程方法论 → 你的真实栈（不是抄 WBR 作业）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **原则：** 复刻 **思路与能力**，不硬套课件里的 **WBR / events.db / 课例 SQL**。  
> **课例** 只用于理解 Tool 调用；**日常** 走 Brand / Drive / CEO 循环。
- **Path:** `docs/COURSE-METHOD-TO-YOUR-STACK.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **你的「私有数据」主路径（推荐）**: 1. **Google Drive**（营销 / IP / 广告 / 策展等）→ 镜像 → `_rag` → **`# brand-ip-knowledge`**
- **部署与验收**: ```bash


---

## L2 正文

# 课程方法论 → 你的真实栈（不是抄 WBR 作业）

> **原则：** 复刻 **思路与能力**，不硬套课件里的 **WBR / events.db / 课例 SQL**。  
> **课例** 只用于理解 Tool 调用；**日常** 走 Brand / Drive / CEO 循环。


## 你的「私有数据」主路径（推荐）

1. **Google Drive**（营销 / IP / 广告 / 策展等）→ 镜像 → `_rag` → **`# brand-ip-knowledge`**  
2. **Git `content/`**（定稿 Brief、IP Brief）→ Cursor Agent + CEO 链  
3. **可选 SQLite Tool**：仅当你有 **结构化表**（选题库、指标、练习日志导出）时再配路径；**与课例 events 无关**


## 部署与验收

```bash
bash scripts/deploy-learning-stack.sh
```

详见 [CONTEXT-WINDOW-AND-DATA-ROUTING.md](./CONTEXT-WINDOW-AND-DATA-ROUTING.md)