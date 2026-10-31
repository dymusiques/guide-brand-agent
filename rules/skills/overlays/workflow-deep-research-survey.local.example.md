---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/overlays/workflow-deep-research-survey.local.example.md"
goal: "workflow-deep-research-survey · Local Overlay (example)"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "62ba06aa328e0675"
---

# workflow-deep-research-survey · Local Overlay (example)

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 复制为 `workflow-deep-research-survey.local.md`（gitignored）。
- **Path:** `rules/skills/overlays/workflow-deep-research-survey.local.example.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# workflow-deep-research-survey · Local Overlay (example)

复制为 `workflow-deep-research-survey.local.md`（gitignored）。

| Key | Value |
|-----|-------|
| Session scratch | `tmp/survey/<YYYY-MM-DD-topic>/` |
| Final survey report | `content/marketing/research/<topic>_survey_YYYYMMDD.md` |
| Search tools | WebSearch / WebFetch（默认）；Tavily MCP 若 Cursor 已授权则 `max_results=6`, `search_depth=advanced` |
| Parallel execution | Cursor Task · 见 `workflow_parallel_subagents.md` |
| Brief 出口 | 调研完成后由 04 写 `content/xiaohongshu/*-brief.md` |

**勿** 将未核实 Tier 1–2 claim 直接写进 Brief classifier 作事实。