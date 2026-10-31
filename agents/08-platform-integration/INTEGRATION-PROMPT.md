---
context_version: "2026-10-30-l012"
repo_path: "agents/08-platform-integration/INTEGRATION-PROMPT.md"
goal: "08 Platform Integration · 集成"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "50b40209548bf386"
---

# 08 Platform Integration · 集成

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../d
- **Path:** `agents/08-platform-integration/INTEGRATION-PROMPT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

> **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../docs/COURSE-METHOD-TO-YOUR-STACK.md) · JSON [integration/handoff/cursor-openwebui-task-routing.json](../../integration/handoff/cursor-openwebui-task-routing.json)  
> - **长文/翻译** → Open WebUI Router + intake；**gate/verify/改 Brief** → Cursor only  
> - 本文件下方内容 = **本部门专属**；勿重复粘贴 SOUL / 整份 IP Brief 正文
# 08 Platform Integration · 集成

> **Collector + Evaluator（Must）：** [../_shared/COLLECTOR-EVALUATOR.md](../_shared/COLLECTOR-EVALUATOR.md) · slot `08-platform`

**成功目标：** `G-PLATFORM-SYNC`

1. gdocs / Drive / Gmail / Calendar：`rules/skills/skill_google_docs.md` + overlay。
2. **函数壳：** `bash scripts/agent-shells/08-platform.sh`（= `verify-integration.sh` 6 case）。
3. **验收：** `bash scripts/verify-agent-matrix.sh --agent 08` + 全仓 `verify-all.sh` 平台段。
4. **禁止** 未 Git commit 定稿仅 sync Drive（见 IMPORTANT）。