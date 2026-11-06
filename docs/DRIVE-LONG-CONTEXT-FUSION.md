---
context_version: "2026-11-05"
repo_path: "docs/DRIVE-LONG-CONTEXT-FUSION.md"
goal: "Drive 长上下文 · Simon + Anthropic 融合 · Agent/CEO Must"
openwebui_route: "rag_l1"
cursor_route: "read"
---

# Drive 长上下文 · Simon + Anthropic 融合

> **机器层（Agent 先读这个 JSON）：** [`integration/handoff/drive-long-context-fusion.json`](../integration/handoff/drive-long-context-fusion.json)  
> **全自动（Owner 不必再手打 bind/validate）：** `bash scripts/run-drive-long-context-fusion-auto.sh`  
> **阶段：** `DRIVE_FUSION_PHASE=ceo_dispatch|pre_delivery|full`（**Cursor CEO 主链**自动调用；Open WebUI 可选步 −1 **不替代**本链 Drive 背书）  
> **主入口：** `ceo-full-execution-pipeline.sh` / `run_ceo_full_execution.py`（非 Open WebUI 专属）  
> **资料库文件夹（多文件夹合并）：** [`integration/handoff/ceo-drive-corpus-folders.json`](../integration/handoff/ceo-drive-corpus-folders.json)  
> **刷新目录快照：** `python3 scripts/refresh-ceo-drive-catalog.py`  
> **按 CEO 任务全库筛选（不遗漏域内参考）：** `python3 scripts/ceo-task-drive-corpus-screen.py --auto --goal "<原话>"` → `content/evolution/00-manager/ceo-inbox/corpus-screens/<slug>/`  
> **验收：** `bash scripts/verify-drive-long-context-fusion.sh`

## L1

- **Simon：** 目录 → 按需读原件（gdocs）→ 少把正文塞进 chat。  
- **Anthropic：** 阶段 A 只抽「原文」→ 阶段 B 只许引用 evidence 文件 → 多轮事实外置 Git。  
- **CEO：** screen → bind-task → gdocs 下载 → **`drive_corpus_extract_text.py`**（PDF / Office / EPUB / MOBI 等）→ 填 `{slug}-drive-evidence.md` → 再写稿 / evolution。
- **正文格式：** PDF（`pdftotext`）、docx/pptx/xlsx、epub/fb2、txt/md/html；mobi/azw 需本机 **Calibre `ebook-convert`**；扫描版 PDF 可能仍为空 → 标未解决 / OCR。

## 与现有文档

- 三层 Drive：[AGENT-DRIVE-CONTEXT-EXTERNALIZATION.md](./AGENT-DRIVE-CONTEXT-EXTERNALIZATION.md)  
- 路由：[CONTEXT-WINDOW-AND-DATA-ROUTING.md](./CONTEXT-WINDOW-AND-DATA-ROUTING.md)  
- Prompt 标准：[PROMPT-CONTEXT-STANDARD.md](./PROMPT-CONTEXT-STANDARD.md)
