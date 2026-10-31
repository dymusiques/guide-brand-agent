---
context_version: "2026-10-30-l012"
repo_path: "agents/07-brand-visual/INTEGRATION-PROMPT.md"
goal: "07 Brand Visual · 集成"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "3363958306be36d2"
---

# 07 Brand Visual · 集成

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../d
- **Path:** `agents/07-brand-visual/INTEGRATION-PROMPT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

> **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../docs/COURSE-METHOD-TO-YOUR-STACK.md) · JSON [integration/handoff/cursor-openwebui-task-routing.json](../../integration/handoff/cursor-openwebui-task-routing.json)  
> - **长文/翻译** → Open WebUI Router + intake；**gate/verify/改 Brief** → Cursor only  
> - 本文件下方内容 = **本部门专属**；勿重复粘贴 SOUL / 整份 IP Brief 正文
# 07 Brand Visual · 集成

> **Collector + Evaluator（Must）：** [../_shared/COLLECTOR-EVALUATOR.md](../_shared/COLLECTOR-EVALUATOR.md) · slot `07-visual`

**成功目标：** `G-BRAND-VISUAL`

1. 从 XHS Brief 封面块或 Owner 需求 → `content/visual/` · Canva（`.cursor/skills/brand-visual/`）。
2. **函数壳：** `bash scripts/agent-shells/07-brand-visual.sh`
3. **验收：** `bash scripts/verify-agent-matrix.sh --agent 07`
4. 不替代 **04** 的 `evaluate --brief`；视觉完成后仍由 **00** 定稿 gate。