# INDEX · danying-brand-agent

> **Hub 总入口：** [danying-apps](https://origin.cursor.com/danying/danying-apps) → `apps/guide-brand-agent/`  
> **换机：** [新电脑一句话.md](新电脑一句话.md) → 本文 → [integrations/index.md](integrations/index.md)

---

## 本仓库是什么

**多面品牌 Agent 业务仓**（个人 IP · 商业品牌 · 营销 · 小红书 · 视觉），不是 danying-apps 总 Hub。

| 层 | 路径 | 作用 |
|----|------|------|
| Agent 入口 | [AGENTS.md](AGENTS.md) | 每 session 先读 |
| 路由 | [integrations/index.md](integrations/index.md) | 任务 → Skill → Drive → 本地目录 |
| 人格 / Owner | [rules/SOUL.md](rules/SOUL.md) · [rules/USER.md](rules/USER.md) | L3 约束 |
| 领域 Skill | [.cursor/skills/](.cursor/skills/) | guide-core + 5 领域 |
| Kernel 模板 | [kernels/templates/](kernels/templates/) | Generative Kernel |
| 小红书 Topic Kernel | [kernels/xiaohongshu/README.md](kernels/xiaohongshu/README.md) | Gemini 选题对齐 · 6 case verify |
| **Agent 集成 + 内容** | [agents/](agents/) · [docs/DANYING-BRAND-AGENT-INTEGRATION.md](docs/DANYING-BRAND-AGENT-INTEGRATION.md) · [content/](content/) | Manager Loop · Git 定稿 |
| 接手验证 | `scripts/verify-handoff.sh` | L0 新 Agent 能否接手 |
| 集成验证 | `scripts/verify-integration.sh` | 6 case · gdocs + Git/Drive 读 |
| Google CLI | [rules/skills/skill_google_docs.md](rules/skills/skill_google_docs.md) | gdocs-skill |
| Drive 知识库 | `AI-Agent-Knowledge-Bank/`（云端） | folder ID 见 overlay |

---

## 新 Agent 开工顺序

0. **[docs/AGENT-TAKEOVER.md](docs/AGENT-TAKEOVER.md)** — 当前程序状态 · 三轨 · CEO 链 · verify（换机 Must）
1. [AGENTS.md](AGENTS.md)
2. [integrations/index.md](integrations/index.md) — **按任务查表，禁止全盘搜索**
3. 命中领域 → 读 `.cursor/skills/<domain>/SKILL.md`
4. 读 Git `content/<domain>/`（真相源）；Drive 仅 Owner 已同步时查阅
5. 参考 `kernels/templates/` 产出 → `content/` → 稳定后 commit → （可选）Owner 说「同步 Drive」
6. 交班前：`bash scripts/verify-handoff.sh`
7. Hub 共享规则：[danying-apps rules/check](https://github.com/dymusiques/danying-apps/blob/main/rules/check/check.md)

---

## 相关 App（hub 注册）

| App | 关系 |
|-----|------|
| 听见 Daily | 独立仓 `danying-tingjian-daily`；栏目日更，与本仓 IP 分层 |
| danying-agent-workspace | Playbook 大仓；project 4 / Module 3 等 |
| danying-apps | **总 Hub** · INDEX · 装机 · check |

---

*最后更新：2026-10-05*
