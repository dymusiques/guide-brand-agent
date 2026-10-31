---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/INDEX.md"
goal: "Skills Index"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "c367e36ed793246e"
---

# Skills Index

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 本索引只做路由：告诉你「什么时候该看哪个 skill」，不教你怎么调。命中后先读对应 skill 文件再动手。
- **Path:** `rules/skills/INDEX.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **分类索引**
- **Progressive Disclosure**: - **INDEX.md** 只提供路由


---

## L2 正文

# Skills Index

本索引只做路由：告诉你「什么时候该看哪个 skill」，不教你怎么调。命中后先读对应 skill 文件再动手。

- **要用某个能力** → 按下方分类定位到 skill 文件，然后**读它**
- **要加新 skill** → 先读 [Skill 写作指南（Meta）](./bestpractice_skill_writing.md)，再加到对应分类
- **想安装更多 public skill repo** → 见 [grapeot/gdocs-skill](https://github.com/grapeot/gdocs-skill) 等同源安装流程；更新 WORKSPACE.md 与 INDEX


## 分类索引

### API Guide（API 指南）

- [Google Workspace（Docs / Gmail / Calendar）](./skill_google_docs.md) ✅ — CLI `python -m gdocs`；触发词："Google Doc"、"sync markdown"、"Gmail"、"Calendar"、"Drive download"
- [DOCX（Word 表单/inspect）](./skill_docx.md) ✅ — `vendor/docx-skill`；触发词："DOCX"、"Word 表单"
- [PPTX（读改/渲染）](./skill_pptx.md) ✅ — `vendor/pptx.skill`；触发词："pptx"、"slide"（Brief 封面 → brand-visual）
- [Process Launcher（本机延时/周期/进程 API）](./skill_process_launcher.md) ✅ — `vendor/process-launcher`；触发词："定时任务"、"延时执行"、"process launcher"、`POST /run`（**不**替代 manager-autopilot）
- [AI Agent CLI（Claude/Codex/Cursor/agy 等 headless）](./skill_ai_agent_cli.md) ✅ — `vendor/ai-agent-cli-skill`；触发词：`cursor agent -p`、headless、file-response（**不**替代 IDE 内 00 Manager）
- [IP 内容工具链总表](../../integration/ip-content-skills-adoption.md) ✅ — 触发条件 · 非 Brief 边界
- [Semantic Search](./skill_semantic_search.md) · [voice-lora](./skill_voice_lora.md) · [B 站 upload](./skill_bilibili_upload.md) · [ASR](./skill_asr.md) · [Online Media](./skill_online_media.md) · [Voice Memos](./skill_voice_memos.md) · [Intake](./skill_intake.md) · [Session Export](./skill_ai_session_export.md) · [vlog](./skill_vlog.md) · [opus-video](./skill_opus_video_audio.md) · [Playwright test](./skill_playwright_test.md) · [Typefully](./skill_typefully_twitter.md) · [DataForSEO](./skill_dataforseo.md) ✅

### Workflow（长文 · 非 XHS Brief）

- [Writing（internal / external）](./skill_writing.md) ✅ — `vendor/writing-skill/skills/writing_workflows.md`；触发词："深度稿"、"memo"、"prose lint"（**非** Brief / Pitch）
- [鸭哥口吻 / 去 AI 腔](./skill_yage_voice.md) ✅ — 触发词："鸭哥口吻"、"去 AI 腔"、"yage voice"（Owner 对话 / 说明；**非** XHS Brief）
- [并行 Subagent（调研 / explore / 独立 review）](./workflow_parallel_subagents.md) ✅ — 触发词："并行调研"、"多 agent 搜"、"explore 并行"（**不**替代 00 Manager Brief 步序）
- [深度调研 Survey（Tier 验证 · claim · fact_check）](./workflow_deep_research_survey.md) ✅ — 触发词："深度调研"、"竞品 survey"、"尽调"；scratch `tmp/survey/` · 报告 `content/marketing/research/`

### BestPractice（最佳实践 / Meta）

- [Skill 写作指南（Meta-Skill）](./bestpractice_skill_writing.md) ✅ — 创建或重写 skill、INTEGRATION-PROMPT、vendor 单 root 路由；触发词："写 skill"、"重写 skill"、"skill 验收"、"添加 skill"
- [AI 编程核心方法论](./bestpractice_ai_programming_mindset.md) ✅ — 70% 问题、成功标准、verify 反馈环；触发词："改脚本"、"verify"、"集成"、"autopilot"、"evaluate"
- [时间敏感信息验证](./bestpractice_temporal_info_verification.md) ✅ — 日期、版本、「最新」、听见 Daily；触发词："听见"、"资讯日期"、"模型版本"、"待核实"


## Progressive Disclosure

- **INDEX.md** 只提供路由
- **skill 文件** 包含完整步骤 — 命中后必须读它
- **本地 overlay**（`overlays/*.local.md`）含路径与账号别名，gitignored