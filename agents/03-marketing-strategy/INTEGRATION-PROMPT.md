---
context_version: "2026-10-30-l012"
repo_path: "agents/03-marketing-strategy/INTEGRATION-PROMPT.md"
goal: "03 Marketing Strategy · 集成"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "25a8a3628c19da03"
---

# 03 Marketing Strategy · 集成

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../d
- **Path:** `agents/03-marketing-strategy/INTEGRATION-PROMPT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

> **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../docs/COURSE-METHOD-TO-YOUR-STACK.md) · JSON [integration/handoff/cursor-openwebui-task-routing.json](../../integration/handoff/cursor-openwebui-task-routing.json)  
> - **长文/翻译** → Open WebUI Router + intake；**gate/verify/改 Brief** → Cursor only  
> - 本文件下方内容 = **本部门专属**；勿重复粘贴 SOUL / 整份 IP Brief 正文
# 03 Marketing Strategy · 集成

> **Collector + Evaluator（Must）：** [../_shared/COLLECTOR-EVALUATOR.md](../_shared/COLLECTOR-EVALUATOR.md) · slot `03-marketing`

**成功目标：** `G-MARKETING-CAMPAIGN` · `G-STRONG-LINK`

1. Campaign / 渠道 Brief → `content/marketing/`（README 模板）。
2. **静态 lint：** `python scripts/lint-strategic-doc.py --kind marketing --file <doc.md>`
3. **Gemini 审阅：** `python scripts/evaluate-marketing-campaign.py --file <doc.md>`
4. **部门验收：** `bash scripts/verify-marketing-campaign.sh`
5. **矩阵：** `bash scripts/verify-agent-matrix.sh --agent 03`
6. 与 **04** 并列：campaign 定稿与 XHS Brief 均须各自 evaluate；**00** 用 Release 档 `verify-all`