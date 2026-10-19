# Skills Index

本索引只做路由：告诉你「什么时候该看哪个 skill」，不教你怎么调。命中后先读对应 skill 文件再动手。

- **要用某个能力** → 按下方分类定位到 skill 文件，然后**读它**
- **要加新 skill** → 先读 [Skill 写作指南（Meta）](./bestpractice_skill_writing.md)，再加到对应分类
- **想安装更多 public skill repo** → 见 [grapeot/gdocs-skill](https://github.com/grapeot/gdocs-skill) 等同源安装流程；更新 WORKSPACE.md 与 INDEX

---

## 组件状态

### 已安装（本 workspace）

- ✅ **Google Workspace CLI** — `vendor/gdocs-skill` + `rules/skills/skill_google_docs.md`
- ✅ **Skill 写作 Meta** — [bestpractice_skill_writing.md](./bestpractice_skill_writing.md)（上游 [context-infrastructure](https://github.com/grapeot/context-infrastructure) standalone MD）
- ✅ **Rules 框架** — SOUL / USER / WORKSPACE / AGENTS

### Guide 多面 Agent（本 workspace `.cursor/skills/`）

- ✅ `guide-core` — 总控路由
- ✅ `personal-ip` / `business-brand` / `marketing-strategy` / `xiaohongshu`（含 [Topic Manager](../../.cursor/skills/xiaohongshu/topic-manager.md)）/ `brand-visual`
- ✅ `kernels/templates/` — Generative Kernel 模板

### Cursor 全局（个人 skills，非本 repo）

- `danying-tingjian-daily` — 听见 Daily 栏目
- `playwright-anti-bot-images` — Playwright 反爬参考

---

## 分类索引

### API Guide（API 指南）

- [Google Workspace（Docs / Gmail / Calendar）](./skill_google_docs.md) ✅ — CLI `python -m gdocs`；触发词："Google Doc"、"sync markdown"、"Gmail"、"Calendar"、"Drive download"

### BestPractice（最佳实践 / Meta）

- [Skill 写作指南（Meta-Skill）](./bestpractice_skill_writing.md) ✅ — 创建或重写 skill、INTEGRATION-PROMPT、vendor 单 root 路由；触发词："写 skill"、"重写 skill"、"skill 验收"、"添加 skill"

---

## 如何添加 Skill

创建或重写 `rules/skills/` 或 `.cursor/skills/` 下的能力说明前，先读 [`bestpractice_skill_writing.md`](./bestpractice_skill_writing.md)。写完后在本 INDEX 对应分类添加入口，并视需要更新 `rules/WORKSPACE.md` 与 `integrations/index.md`。

---

## Progressive Disclosure

- **INDEX.md** 只提供路由
- **skill 文件** 包含完整步骤 — 命中后必须读它
- **本地 overlay**（`overlays/*.local.md`）含路径与账号别名，gitignored
