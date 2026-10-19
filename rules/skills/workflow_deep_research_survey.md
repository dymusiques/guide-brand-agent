# 深度调研工作流

> **上游：** [grapeot/context-infrastructure · workflow_deep_research_survey.md](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/workflow_deep_research_survey.md)（standalone 拷贝，已做 Cursor / 本仓裁剪。）  
> **本仓边界：** [integration/deep-research-survey-adoption.md](../../integration/deep-research-survey-adoption.md) · 并行执行见 [workflow_parallel_subagents.md](./workflow_parallel_subagents.md)  
> **私有路径：** [overlays/workflow-deep-research-survey.local.example.md](./overlays/workflow-deep-research-survey.local.example.md)

## 元数据

- **类型**: Workflow
- **适用场景**: 第三方主题深度、可验证调研（竞品、品类、工具、合作方背景）；**非** 单篇小红书 Brief 默认路径
- **本仓安装**: 2026-10-20

## 本仓运行时（先读）

| 上游 | 本仓 |
|------|------|
| `contexts/survey_sessions/` 最终报告 | `content/marketing/research/<topic>_survey_YYYYMMDD.md` |
| `tmp/<session_slug>/` 工件 | `tmp/survey/<session_slug>/`（gitignored scratch） |
| Tavily 搜索 | **优先** Cursor WebSearch / WebFetch；有 Tavily MCP 时用 Tavily，参数偏好见下文 |
| Phase 2 `functions.task` | Cursor **Task** 并行（`generalPurpose` / `explore`），见 parallel subagents skill |
| Phase 4 外稿 / memo | [skill_writing.md](./skill_writing.md) → vendor writing workflows；headless 见 [skill_ai_agent_cli.md](./skill_ai_agent_cli.md) |
| 小红书 Brief 定稿 | 调研完成后仍 **04 单线程** 写 Brief + `evaluate` — 调研报告 **不** 代替 aligned |

**时间敏感 claim：** 并行 [bestpractice_temporal_info_verification.md](./bestpractice_temporal_info_verification.md)。

---

## 核心原则

1. **激励感知验证**：厂商叙事提取 claim，独立 Tier 3–4 验证。  
2. **交叉验证**：多 Task overlap ≥50%（与 parallel skill 一致）。  
3. **可追溯**：URL + 原文摘录。  
4. **逐步聚焦**：扫描 → claim 表 → 分维度深入。  
5. **单一主交付 + 可复用工件**：最终报告一份；session 目录留 manifest / fact_check。  
6. **Internal vs External reader mode**：见上游 §「两种 reader mode」；Brief 触达稿偏 External 论证；内部选题 memo 偏 Internal。

## 信息源层级（Tier 1–4）

保留上游表格与「证据可信度递增」段（态度 < migration < post-mortem < commit）。写进 Brief 的 fact **至少** Tier 3–4 或标注 `[待核实]` / temporal skill。

## 工作流程（摘要）

### Phase 1 · 扫描 + Claim 提取

2–3 轮搜索（官方 / 市场 / 批评）→ `tmp/survey/<session_slug>/scratchpad.md` 含 **Claim Extraction** 表。

### Phase 1.5 · Prior Work（仅学术论文主题）

否则跳过；产出 `prior_work_survey.md`。

### Phase 2 · 分割 + 并行 Task

3–5 维度（官方叙事 / 独立体验 / 失败边界 / 迁移行为等），overlap 30–50%。每路 Task prompt：本维度 claim、要 Tier 3–4 行为证据、URL+摘录、落盘路径 under `tmp/survey/<session_slug>/`。

### Phase 3 · 整合 + claim 状态

更新 scratchpad 验证列；矛盾以 Tier 3–4 优先。

### Phase 3.3 · 溯源 fact_check.md

5–10 关键源 **重新打开原文**（WebFetch），不互用 subagent 摘要验摘要。

### Phase 3.5 · Brainstorm（观点型 / external 默认）

`brainstorm_brief.md` → 并行多视角 Task → `brainstorm_synthesis.md` → 窄范围补查。

### Phase 4 · 写作

- **Survey 报告（本 workflow 默认终点）** → `content/marketing/research/<topic>_survey_YYYYMMDD.md`  
- **长文外稿 / memo** → `skill_writing.md`  
- **不** 自动发小红书/推特；发帖仍 Owner + PIPELINE  
- **若调研服务于 Brief：** 04 读 survey + IP Brief，**新写** `content/xiaohongshu/*-brief.md`，再 evaluate

## Search Manifest

`tmp/survey/<session_slug>/search_manifest.md` 含产出索引表、各 Task 状态、覆盖评估（格式见上游）。

## URL 与陷阱

保留上游「URL 留存规范」「常见陷阱」表。专门搜 criticism / negative review 防 vendor 汇总。

## 与 00 Manager

Owner 目标若仅为 **一篇认知期 Brief** 且材料已够：可 **简化** Phase 1–2（单会话搜索 + 可选 2 路 Task），不必全套 brainstorm。  
目标为 **品类进入、合作方尽调、长文论据**：走完整 workflow。
