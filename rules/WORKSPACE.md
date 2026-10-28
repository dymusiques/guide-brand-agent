# WORKSPACE.md — 目录路由速查

目标：让 AI 每轮 session 都能快速知道「去哪里找/放什么」。**找任何文件前先查这里。**

## 路由规则

### 项目与代码
- 工作区根目录：`/`（本 repo = **danying-brand-agent**，建议路径 `~/Desktop/danying-brand-agent`）
- **Agent 总目录：** `agents/`（00-manager … 09-data-analytics）· `integration/`（含 `goals/registry.json`）· `content/` 品牌/IP 定稿
- **集成构建：** `scripts/verify-all.sh` · `scripts/verify-agent-matrix.sh` · `scripts/verify-agent-fused.sh` · `scripts/agent-shells/`
- **多平台数据仓库：** `content/analytics/` · `scripts/analytics-pipeline.sh`
- 通用 Q&A / 操作问题专用 Agent 工作区：`问题解决/`（单独开 Folder；聊天与品牌产线分开）
- Python 虚拟环境：`.venv/`（工作区级，已安装 vendored skills）
- 第三方 public skill repos（只读，可 `git pull` 更新）：`vendor/<repo-name>/`
- 总控 + 领域 Skills：`.cursor/skills/guide-core/`、`.cursor/skills/{personal-ip,business-brand,marketing-strategy,xiaohongshu,brand-visual}/`
- CLI / API 路由与 overlay：`rules/skills/`（Meta：[skill 写作](./skills/bestpractice_skill_writing.md) · [AI 编程](./skills/bestpractice_ai_programming_mindset.md) · [temporal](./skills/bestpractice_temporal_info_verification.md)）
- Generative Kernels（模板与案例）：`kernels/templates/`、`kernels/examples/`
- 小红书 Topic Manager（Gemini 6 case）：`kernels/xiaohongshu/`（README + `docs/`；kernel `scripts/verify-xhs-topic.sh`）
- 小红书 Brief 管线：`content/xiaohongshu/PIPELINE.md` · 批量 `scripts/verify-xhs-content-dir.sh`
- 小红书视频迭代 / 声音：`content/xiaohongshu/XHS-VIDEO-ITERATION.md` · `VOICE-ANCHOR.md` · `scripts/verify-xhs-voice-qa.sh`
- CV Git 源：`content/personal-ip/cv-source-2026-09-15.md`

### 知识与品牌资产
- Google Drive Knowledge Bank：`AI-Agent-Knowledge-Bank/`（通过 gdocs 或 Drive MCP；folder ID 在 overlay）
- 本地草稿与同步 Markdown：`content/{personal-ip,business-brand,marketing,xiaohongshu,visual}/`
- 并行 Subagent 中间工件（gitignored）：`tmp/parallel/<session_slug>/` · skill [workflow_parallel_subagents.md](./skills/workflow_parallel_subagents.md)
- 深度调研 scratch（gitignored）：`tmp/survey/<session_slug>/` · 定稿报告 [content/marketing/research/](../content/marketing/research/) · [workflow_deep_research_survey.md](./skills/workflow_deep_research_survey.md)
- 小红书平台 PDF（gitignore）：`content/marketing/research/raw/*.pdf` · Agent 读 [xhs-platform-research-index.md](../content/marketing/research/xhs-platform-research-index.md)
- Headless CLI scratch（gitignored）：`tmp/ai-agent-cli/<job_id>/` · skill [skill_ai_agent_cli.md](./skills/skill_ai_agent_cli.md)
- **个人 IP / KPI playbook：** `content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md`（CAPSTONE · Five Ps · 新机 Agent 写 Pitch 用）

### 系统与规则
- **新 Agent 接手（Must）：** `docs/AGENT-TAKEOVER.md` · `docs/WORKFLOW-CEO-ARCHITECTURE.md` · `docs/workflow-mindmap.html` · `docs/XHS-DATA-LAYER.md` · `bash scripts/verify-agent-takeover.sh`
- **Manager 三支柱（主框架 · 每个 GM 真正在做的事：可观察性 / 可衡量基准 / 教练→SOP 资产）：** `docs/MANAGER-THREE-PILLARS.md`
- **CEO/Manager 运营标准（Owner 五原则）：** `docs/CEO-MANAGER-OPERATING-STANDARDS.md` · 派活模板 `agents/00-manager/CEO-DISPATCH-SOP.md`
- **Manager 评估改进环（Owner 图 ↔ 01–12 对照）：** `docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md` · 图 `docs/assets/manager-eval-improvement-loop.png`
- **CEO / Senior Manager 改进环（Owner 第二张图 · Consult SOP→…→Analyze · 两轮串行迭代审计）：** `docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md` · 图 `docs/assets/ceo-senior-manager-improvement-loop.png` · 落地 SOP `agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md` · **命令** `bash scripts/manager-ceo-double-iteration.sh --brief … --phase 1|2`
- **Owner 一句话启动 CEO（不必贴 bash）：** `docs/CEO-OWNER-ONE-LINE-TRIGGERS.md` · 可选 `bash scripts/ceo-start-work.sh`
- **新 Agent / 新机 · CEO+GM 接手包（总览 + JSON 索引）：** `docs/HANDOFF-CEO-GM-SOP-PACK.md` · `integration/handoff/ceo-gm-operating-manifest.json`
- **CEO/Manager 运营五原则 SOP：** `docs/CEO-MANAGER-OPERATING-PRINCIPLES.md`
- 本仓索引：`INDEX.md`
- 任务路由：`integrations/index.md`
- Agent 入口：`AGENTS.md`
- 人格与 Owner 信息：`rules/SOUL.md`、`rules/USER.md`
- Skill 索引与本地 overlay：`rules/skills/INDEX.md`、`rules/skills/overlays/`

## 已安装的 Public Skill Repos

| Repo | 路径 | Root skill | 更新 |
|------|------|------------|------|
| gdocs-skill | `vendor/gdocs-skill/` | `rules/skills/skill_google_docs.md` | `git submodule update --remote vendor/gdocs-skill` |
| writing-skill | `vendor/writing-skill/` | `rules/skills/skill_writing.md` | `git submodule update --remote vendor/writing-skill` |
| docx-skill | `vendor/docx-skill/` | `rules/skills/skill_docx.md` | `git submodule update --remote vendor/docx-skill` |
| pptx.skill | `vendor/pptx.skill/` | `rules/skills/skill_pptx.md` | `git submodule update --remote vendor/pptx.skill` |
| process-launcher | `vendor/process-launcher/` | `rules/skills/skill_process_launcher.md` | `git submodule update --remote vendor/process-launcher` |
| ai-agent-cli-skill | `vendor/ai-agent-cli-skill/` | `rules/skills/skill_ai_agent_cli.md` | `git submodule update --remote vendor/ai-agent-cli-skill` |

**IP 内容工具链（已 vendor · 默认不启 CLI · 触发见 adoption）：** [integration/ip-content-skills-adoption.md](../integration/ip-content-skills-adoption.md)

| Repo | 路径 | Router |
|------|------|--------|
| semantic-search-skill | `vendor/semantic-search-skill/` | `skill_semantic_search.md` |
| voice-lora | `vendor/voice-lora/` | `skill_voice_lora.md` |
| bilibili-upload-skill | `vendor/bilibili-upload-skill/` | `skill_bilibili_upload.md` |
| asr-skill | `vendor/asr-skill/` | `skill_asr.md` |
| online-media-skill | `vendor/online-media-skill/` | `skill_online_media.md` |
| voice-memos-skill | `vendor/voice-memos-skill/` | `skill_voice_memos.md` |
| intake-skill | `vendor/intake-skill/` | `skill_intake.md` |
| ai_session_export | `vendor/ai_session_export/` | `skill_ai_session_export.md` |
| vlog-skill | `vendor/vlog-skill/` | `skill_vlog.md` |
| opus-video-audio-skill | `vendor/opus-video-audio-skill/` | `skill_opus_video_audio.md` |
| playwright-test-skill | `vendor/playwright-test-skill/` | `skill_playwright_test.md` |
| typefully-twitter-skill | `vendor/typefully-twitter-skill/` | `skill_typefully_twitter.md` |
| dataforseo-skill | `vendor/dataforseo-skill/` | `skill_dataforseo.md` |

- B 站 / Insta360 流程：[integration/bilibili-inst360-channel-adoption.md](../integration/bilibili-inst360-channel-adoption.md) · 成片/素材 `content/video/` · 文案 `content/bilibili/`

**本仓采纳边界：** [integration/process-launcher-adoption.md](../integration/process-launcher-adoption.md) · [integration/ai-agent-cli-adoption.md](../integration/ai-agent-cli-adoption.md) · [integration/ip-content-skills-adoption.md](../integration/ip-content-skills-adoption.md) · 扩展接口 [integration/EXTENSION-POINTS.md](../integration/EXTENSION-POINTS.md) · 预留 job 模板 `integration/templates/process-launcher-reserved-jobs.example.yaml` · 私有 overlay `*.local.md`（example 可 commit）

**仍暂缓（未 vendor）：** image-generation、presentation_skill、design_skill、kit-skill、circle-post-skill、imessage_skill、tts-clone-skill、lizheng-video-production 等 — 按需再装。

## Python 环境

- 根目录 `.venv/` 为工作区级环境
- 激活：`source .venv/bin/activate`（Cursor 新终端会自动激活）
- 安装 vendored skill：`pip install -e vendor/<repo>`

## 命名规则

- 目录和文件名：小写 + 下划线（snake_case）
- 私有 overlay 文件：`*.local.md`（gitignored）
