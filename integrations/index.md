# Integrations · 任务路由表

> **用法：** 用户说任务 → 匹配「意图」列 → 只读对应 Skill + **Git `content/`** + 本地目录。**禁止**无路由全盘 grep。  
> **存储策略：** [docs/HANDOFF-COMPLETENESS.md](../docs/HANDOFF-COMPLETENESS.md) — Git 真相源；Drive 仅 Owner 说「同步 Drive」时写定稿。

## 产出默认流程

1. 草稿 → `content/<domain>/`
2. 稳定 / 定稿 → **git commit**（新 Agent 接手必需）
3. 可选 → Drive 同路径文件夹（分享用，不占必须）

交班前：`bash scripts/verify-handoff.sh` → `bash scripts/verify-integration.sh`（见 [check.md](../check.md)）

## 领域任务

| 意图（语义） | Skill | Drive 文件夹 | 本地产出 | 模板 |
|-------------|-------|-------------|----------|------|
| 个人 IP、人设、定位、内容支柱 | `.cursor/skills/personal-ip/` | `02-personal-ip/` | `content/personal-ip/` | `kernels/templates/ip-positioning-brief.template.md` |
| 商业策划、品牌策略、SWOT | `.cursor/skills/business-brand/` | `03-business-brand/` | `content/business-brand/` | `kernels/templates/campaign-plan.template.md` |
| 宣传、营销、campaign、渠道 | `.cursor/skills/marketing-strategy/` | `04-marketing/` | `content/marketing/` | `kernels/templates/campaign-plan.template.md` |
| 小红书、笔记、种草、投放、**选题对齐 verify** | `.cursor/skills/xiaohongshu/` · Kernel [`kernels/xiaohongshu/README.md`](../kernels/xiaohongshu/README.md) · `bash scripts/verify-xhs-topic.sh` | `05-xiaohongshu/` | `content/xiaohongshu/` | `kernels/templates/xhs-content-brief.template.md` |
| 视觉、Canva、配色、封面 | `.cursor/skills/brand-visual/` | `06-visual/` | `content/visual/` | — |
| 多领域 / 未指定 | `.cursor/skills/guide-core/` | 按 routing 选 | 按领域 | — |

## 工具集成

| 意图 | 入口 | 配置 |
|------|------|------|
| Google Doc / Gmail / Calendar / Drive 下载 | `rules/skills/skill_google_docs.md` | overlay · `vendor/gdocs-skill/secrets/` |
| 长文 / memo / prose lint（**非** XHS Brief） | `rules/skills/skill_writing.md` | `pip install -e vendor/writing-skill` |
| Word DOCX inspect/填表 | `rules/skills/skill_docx.md` | `pip install -e vendor/docx-skill` |
| PPTX 读改/渲染 | `rules/skills/skill_pptx.md` | `pip install -e vendor/pptx.skill` · LibreOffice 可选 |
| 本机延时/周期任务、进程日志 API | `rules/skills/skill_process_launcher.md` | `pip install -e vendor/process-launcher` · 边界 [process-launcher-adoption.md](../integration/process-launcher-adoption.md) · launcher **Owner GUI 终端启动** |
| Drive 读写（Cursor MCP） | MCP `plugin-google-drive-google-drive` | Cursor Settings → MCP 授权 |
| Canva 设计 | MCP `plugin-canva-canva` | Cursor Settings → MCP 授权 |
| 听见 Daily 日更 | `~/.cursor/skills/danying-tingjian-daily/` | 独立 app 仓，非本仓业务代码 |

## Drive Knowledge Bank（folder ID）

Root: `1jLcbbr0WkmEI8mJlsf5R4Y1NtSGEP8_c` — 完整表见 `rules/skills/overlays/gdocs-skill.local.md`（gitignored）

## 上下文信号

| 信号 | 路由 |
|------|------|
| 打开文件在 `content/xiaohongshu/` | → xiaohongshu |
| 用户提「听见 Daily」「长笛资讯」 | → danying-tingjian-daily skill + 本仓 IP 分层 |
| 用户提「Google Doc」「sync markdown」 | → skill_google_docs |
| 用户说 **「全部克隆」** / 换机 / 新电脑 | → **Hub [全部克隆.md](https://github.com/dymusiques/danying-apps/blob/main/全部克隆.md)** + `scripts/clone-all.sh`；**禁止**反问 clone 哪些 |
