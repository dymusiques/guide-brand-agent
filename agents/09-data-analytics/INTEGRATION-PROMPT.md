---
context_version: "2026-10-30-l012"
repo_path: "agents/09-data-analytics/INTEGRATION-PROMPT.md"
goal: "Data Analytics 集成 Prompt"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "62cf1056c46b7f45"
---

# Data Analytics 集成 Prompt

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../d
- **Path:** `agents/09-data-analytics/INTEGRATION-PROMPT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

> **上下文与平台（Must · 全部门通用）**  
> - 标准：[docs/PROMPT-CONTEXT-STANDARD.md](../../docs/PROMPT-CONTEXT-STANDARD.md)  
> - Cursor ↔ Open WebUI：[docs/COURSE-METHOD-TO-YOUR-STACK.md](../../docs/COURSE-METHOD-TO-YOUR-STACK.md) · JSON [integration/handoff/cursor-openwebui-task-routing.json](../../integration/handoff/cursor-openwebui-task-routing.json)  
> - **长文/翻译** → Open WebUI Router + intake；**gate/verify/改 Brief** → Cursor only  
> - 本文件下方内容 = **本部门专属**；勿重复粘贴 SOUL / 整份 IP Brief 正文
# Data Analytics 集成 Prompt

> **Collector + Evaluator（Must）：** [../_shared/COLLECTOR-EVALUATOR.md](../_shared/COLLECTOR-EVALUATOR.md) · slot `09-analytics` · CSV/Owner _feed 进 intake；next-topics v0→vN

0. **与 04 叠加：** 复盘/选题建议须可被 [XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md) 引用（MANIFEST + snapshot + strategy + PDF 研究 MD）。

1. 读 `DATA-NEEDS.md`；Owner 导出 CSV/xlsx → inbox 或 `raw/xiaohongshu/` → `bash scripts/analytics-fetch.sh`。
2. 跑 `bash scripts/analytics-pipeline.sh`（试跑加 `--demo`）；读 `content/analytics/derived/next-topics-*.md` + `summary-*.json`。
3. 结合 `integration/IMPORTANT.md` + IP Brief 写 **简短复盘**；**不编造** 未导入的平台数据。
4. 将 **3 条 subject 建议** 交给 **04-xhs-topic-manager** 写 Brief → `evaluate --brief` → Manager `manager-workflow-verify.sh`。
5. **禁止** 用历史数据反改 kernel 6 case；若需改规则 → 05-kernel + Owner。