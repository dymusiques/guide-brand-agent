---
context_version: "2026-10-30-l012"
repo_path: "integration/deep-research-survey-adoption.md"
goal: "深度调研 Survey · 本仓采纳说明"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "cc811e31c34af384"
---

# 深度调研 Survey · 本仓采纳说明

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Discovery：** [rules/skills/workflow_deep_research_survey.md](../rules/skills/workflow_deep_research_survey.md)
- **Path:** `integration/deep-research-survey-adoption.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **对你现在有没有用？**: | 情况 | 建议 |
- **路径映射**: | 用途 | 路径 | Git |
- **组合顺序（推荐）**: 1. Owner/Manager 定调研问题 → Phase 1–3（+3.3/3.5 视任务）
- **扩展口子**: | 下一阶段改动 | 接哪里 |
- **验收**: - `rules/skills/workflow_deep_research_survey.md`


---

## L2 正文

# 深度调研 Survey · 本仓采纳说明

> **Discovery：** [rules/skills/workflow_deep_research_survey.md](../rules/skills/workflow_deep_research_survey.md)

## 对你现在有没有用？

| 情况 | 建议 |
|------|------|
| 认知期 4 篇 discovery Brief **已有 aligned 稿** | **非必须**；发帖前不必再跑全套 survey |
| **新选题**需竞品/品类/合作方 **可引用证据** | **有用** — Phase 1 claim 表 + Phase 2 并行 Task，再 04 写 Brief |
| 听见 Daily / 强资讯 | **部分有用** — Tier 验证 + fact_check；日期仍走 temporal skill |
| 深度外稿、投资人 memo | **有用** — Phase 3.5 + `skill_writing.md` |
| 只想改 classifier JSON | **不用** — 直接 evaluate + Manager's Loop |

**结论：** **工具箱 workflow，按需启用**；与 `workflow_parallel_subagents` **叠加**（survey = 结构化阶段，parallel = 执行方式），不替代 00 Manager。

## 路径映射

| 用途 | 路径 | Git |
|------|------|-----|
| Session scratch | `tmp/survey/<session_slug>/` | ignore |
| 最终调研报告 | `content/marketing/research/<topic>_survey_YYYYMMDD.md` | commit 可选（定稿论据时建议 commit） |
| 小红书 Brief | `content/xiaohongshu/*-brief.md` | evaluate 后 commit |

## 组合顺序（推荐）

1. Owner/Manager 定调研问题 → Phase 1–3（+3.3/3.5 视任务）  
2. 产出 survey MD → **04** 写 Brief（Problem/Solution/CTA 对齐 CAPSTONE）  
3. `evaluate-xhs-topic.py` → verify  

## 扩展口子

| 下一阶段改动 | 接哪里 |
|--------------|--------|
| session 命名、Tavily/MCP | `overlays/workflow-deep-research-survey.local.md` |
| 新调研类型一行 | 本文件 + skill 内维度表 |
| 与 parallel 分工 | `parallel-subagents-adoption.md` §推荐组合 |

## 验收

- `rules/skills/workflow_deep_research_survey.md`  
- 本文件  
- `verify-handoff.sh`