---
context_version: "2026-10-30-l012"
repo_path: "agents/05-xhs-kernel/INTEGRATION-PROMPT.md"
goal: "INTEGRATION-PROMPT"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "15459a62c5b7b157"
---

# INTEGRATION-PROMPT

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../d
- **Path:** `agents/05-xhs-kernel/INTEGRATION-PROMPT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

> **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../docs/COURSE-METHOD-TO-YOUR-STACK.md) · JSON [integration/handoff/cursor-openwebui-task-routing.json](../../integration/handoff/cursor-openwebui-task-routing.json)  
> - **长文/翻译** → Open WebUI Router + intake；**gate/verify/改 Brief** → Cursor only  
> - 本文件下方内容 = **本部门专属**；勿重复粘贴 SOUL / 整份 IP Brief 正文
> **Collector + Evaluator：** 05 不产 v0 文案；进化距离挂在 04 的 `content/evolution/04-xhs/<slug>/`。本 Agent 仍跑 [../_shared/COLLECTOR-EVALUATOR.md](../_shared/COLLECTOR-EVALUATOR.md) 中的 **aligned gate**（`evaluate-xhs-topic.py`）。

只改 `is_xhs_growth_aligned` docstring/实现；改后必跑 verify-xhs-topic 6/6。集成层只 import 调用，不在此写 Brief。