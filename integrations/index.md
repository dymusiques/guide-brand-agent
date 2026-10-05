# Integrations · 任务路由表

> **用法：** 用户说任务 → 匹配「意图」列 → 只读对应 Skill + Drive + 本地目录。**禁止**无路由全盘 grep。

## 领域任务

| 意图（语义） | Skill | Drive 文件夹 | 本地产出 | 模板 |
|-------------|-------|-------------|----------|------|
| 个人 IP、人设、定位、内容支柱 | `.cursor/skills/personal-ip/` | `02-personal-ip/` | `content/personal-ip/` | `kernels/templates/ip-positioning-brief.template.md` |
| 商业策划、品牌策略、SWOT | `.cursor/skills/business-brand/` | `03-business-brand/` | `content/business-brand/` | `kernels/templates/campaign-plan.template.md` |
| 宣传、营销、campaign、渠道 | `.cursor/skills/marketing-strategy/` | `04-marketing/` | `content/marketing/` | `kernels/templates/campaign-plan.template.md` |
| 小红书、笔记、种草、投放 | `.cursor/skills/xiaohongshu/` | `05-xiaohongshu/` | `content/xiaohongshu/` | `kernels/templates/xhs-content-brief.template.md` |
| 视觉、Canva、配色、封面 | `.cursor/skills/brand-visual/` | `06-visual/` | `content/visual/` | — |
| 多领域 / 未指定 | `.cursor/skills/guide-core/` | 按 routing 选 | 按领域 | — |

## 工具集成

| 意图 | 入口 | 配置 |
|------|------|------|
| Google Doc / Gmail / Calendar / Drive 下载 | `rules/skills/skill_google_docs.md` | overlay · `vendor/gdocs-skill/secrets/` |
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
