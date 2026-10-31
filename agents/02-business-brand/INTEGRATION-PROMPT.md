---
context_version: "2026-10-30-l012"
repo_path: "agents/02-business-brand/INTEGRATION-PROMPT.md"
goal: "02 Business Brand · 集成"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "218c6bff15b92e6e"
---

# 02 Business Brand · 集成

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../d
- **Path:** `agents/02-business-brand/INTEGRATION-PROMPT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

> **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../docs/COURSE-METHOD-TO-YOUR-STACK.md) · JSON [integration/handoff/cursor-openwebui-task-routing.json](../../integration/handoff/cursor-openwebui-task-routing.json)  
> - **长文/翻译** → Open WebUI Router + intake；**gate/verify/改 Brief** → Cursor only  
> - 本文件下方内容 = **本部门专属**；勿重复粘贴 SOUL / 整份 IP Brief 正文
# 02 Business Brand · 集成

> **Collector + Evaluator（Must）：** [../_shared/COLLECTOR-EVALUATOR.md](../_shared/COLLECTOR-EVALUATOR.md) · slot `02-business-brand`

**成功目标：** `G-BUSINESS-BRAND` · `G-CROSS-INDUSTRY`（见 `integration/GOALS-REGISTRY.md`）

1. 读 `integration/IMPORTANT.md` + IP Brief；产出进 `content/business-brand/`（用 README 模板）。
2. **静态 lint：** `python scripts/lint-strategic-doc.py --kind business_brand --file <doc.md>`
3. **Gemini 审阅（与 05 分工）：** `python scripts/evaluate-business-brand.py --file <doc.md>` · 规则 `G-NOT-SINGLE-VERTICAL-LOCK` + 强链接
4. **部门验收：** `bash scripts/verify-business-brand.sh`（lint README + Gemini 6）
5. **矩阵 6 case：** `bash scripts/verify-agent-matrix.sh --agent 02`
6. Release 全仓：`VERIFY_TIER=release bash scripts/verify-all.sh`（见 `docs/VERIFY-TIERS.md`）