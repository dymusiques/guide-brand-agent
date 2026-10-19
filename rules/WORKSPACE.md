# WORKSPACE.md — 目录路由速查

目标：让 AI 每轮 session 都能快速知道「去哪里找/放什么」。**找任何文件前先查这里。**

## 路由规则

### 项目与代码
- 工作区根目录：`/`（本 repo = **danying-brand-agent**，建议路径 `~/Desktop/danying-brand-agent`）
- **Agent 总目录：** `agents/`（00-manager … 09-data-analytics）· `integration/`（含 `goals/registry.json`）· `content/` 品牌/IP 定稿
- **集成构建：** `scripts/verify-all.sh` · `scripts/verify-agent-matrix.sh` · `scripts/agent-shells/`
- **多平台数据仓库：** `content/analytics/` · `scripts/analytics-pipeline.sh`
- 通用 Q&A / 操作问题专用 Agent 工作区：`问题解决/`（单独开 Folder；聊天与品牌产线分开）
- Python 虚拟环境：`.venv/`（工作区级，已安装 vendored skills）
- 第三方 public skill repos（只读，可 `git pull` 更新）：`vendor/<repo-name>/`
- 总控 + 领域 Skills：`.cursor/skills/guide-core/`、`.cursor/skills/{personal-ip,business-brand,marketing-strategy,xiaohongshu,brand-visual}/`
- CLI / API 路由与 overlay：`rules/skills/`（Meta：[skill 写作](./skills/bestpractice_skill_writing.md) · [AI 编程](./skills/bestpractice_ai_programming_mindset.md) · [temporal](./skills/bestpractice_temporal_info_verification.md)）
- Generative Kernels（模板与案例）：`kernels/templates/`、`kernels/examples/`
- 小红书 Topic Manager（Gemini 6 case）：`kernels/xiaohongshu/`（README + `docs/`；kernel `scripts/verify-xhs-topic.sh`）
- 小红书 Brief 管线：`content/xiaohongshu/PIPELINE.md` · 批量 `scripts/verify-xhs-content-dir.sh`

### 知识与品牌资产
- Google Drive Knowledge Bank：`AI-Agent-Knowledge-Bank/`（通过 gdocs 或 Drive MCP；folder ID 在 overlay）
- 本地草稿与同步 Markdown：`content/{personal-ip,business-brand,marketing,xiaohongshu,visual}/`
- 并行 Subagent 中间工件（gitignored）：`tmp/parallel/<session_slug>/` · skill [workflow_parallel_subagents.md](./skills/workflow_parallel_subagents.md)
- **个人 IP / KPI playbook：** `content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md`（CAPSTONE · Five Ps · 新机 Agent 写 Pitch 用）

### 系统与规则
- **新 Agent 接手（Must）：** `docs/AGENT-TAKEOVER.md` · `bash scripts/verify-agent-takeover.sh`
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

**本仓采纳边界：** [integration/process-launcher-adoption.md](../integration/process-launcher-adoption.md) · 扩展接口 [integration/EXTENSION-POINTS.md](../integration/EXTENSION-POINTS.md) · 预留 job 模板 `integration/templates/process-launcher-reserved-jobs.example.yaml` · 私有配方 `rules/skills/overlays/process-launcher.local.md`（example 可 commit）

**暂缓（1-A～4-A）：** voice-lora、image-generation、presentation_skill、design_skill、kit-skill、circle-post-skill、imessage_skill、opus-video-audio-skill、tts-clone-skill、lizheng-video-production 等 — 视频号/额外渠道定调后再 `git submodule add`。

## Python 环境

- 根目录 `.venv/` 为工作区级环境
- 激活：`source .venv/bin/activate`（Cursor 新终端会自动激活）
- 安装 vendored skill：`pip install -e vendor/<repo>`

## 命名规则

- 目录和文件名：小写 + 下划线（snake_case）
- 私有 overlay 文件：`*.local.md`（gitignored）
