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
- ✅ **AI 编程方法论** — [bestpractice_ai_programming_mindset.md](./bestpractice_ai_programming_mindset.md)（verify / scripts / 反馈环）
- ✅ **时间敏感验证** — [bestpractice_temporal_info_verification.md](./bestpractice_temporal_info_verification.md)（听见 / 日期 / 版本号）
- ✅ **长文写作** — [skill_writing.md](./skill_writing.md) → `vendor/writing-skill/`（**非** 小红书 Brief）
- ✅ **DOCX / PPTX** — [skill_docx.md](./skill_docx.md) · [skill_pptx.md](./skill_pptx.md)（办公稿；封面仍 Canva）
- ✅ **Rules 框架** — SOUL / USER / WORKSPACE / AGENTS

### Tier 3 · 暂缓（Owner 2026-10 · 全选 A）

未 vendor：voice-lora、image-generation、presentation_skill、design_skill、kit/circle/imessage、opus-video/tts/lizheng 等。视频号/Newsletter 定调后再装；见 [WORKSPACE.md](../WORKSPACE.md) Public Skill 表。

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
- [DOCX（Word 表单/inspect）](./skill_docx.md) ✅ — `vendor/docx-skill`；触发词："DOCX"、"Word 表单"
- [PPTX（读改/渲染）](./skill_pptx.md) ✅ — `vendor/pptx.skill`；触发词："pptx"、"slide"（Brief 封面 → brand-visual）

### Workflow（长文 · 非 XHS Brief）

- [Writing（internal / external）](./skill_writing.md) ✅ — `vendor/writing-skill/skills/writing_workflows.md`；触发词："深度稿"、"memo"、"prose lint"（**非** Brief / Pitch）

### BestPractice（最佳实践 / Meta）

- [Skill 写作指南（Meta-Skill）](./bestpractice_skill_writing.md) ✅ — 创建或重写 skill、INTEGRATION-PROMPT、vendor 单 root 路由；触发词："写 skill"、"重写 skill"、"skill 验收"、"添加 skill"
- [AI 编程核心方法论](./bestpractice_ai_programming_mindset.md) ✅ — 70% 问题、成功标准、verify 反馈环；触发词："改脚本"、"verify"、"集成"、"autopilot"、"evaluate"
- [时间敏感信息验证](./bestpractice_temporal_info_verification.md) ✅ — 日期、版本、「最新」、听见 Daily；触发词："听见"、"资讯日期"、"模型版本"、"待核实"

---

## 如何添加 Skill

创建或重写 `rules/skills/` 或 `.cursor/skills/` 下的能力说明前，先读 [`bestpractice_skill_writing.md`](./bestpractice_skill_writing.md)。写完后在本 INDEX 对应分类添加入口，并视需要更新 `rules/WORKSPACE.md` 与 `integrations/index.md`。

**注册表纪律（摘录 · [skill registry lifecycle](https://github.com/grapeot/skills/blob/master/skills/skill_registry_lifecycle.md)，本仓不装全文）：**

- **INDEX 是路由，不是第二份 skill 正文** — 能力以 **一个 canonical 文件或 vendor root** 为准；勿把 public repo 全文复制进 INDEX。
- **Public repo** — 只暴露 **一个 root** 到 INDEX；私有路径/alias 进 `overlays/*.local.md`，不 commit。
- **增/改** — 先查 INDEX 是否已有同类；优先 **改已有** 而非平行新建。
- **删** — 同步去掉 INDEX、AGENTS 速查、`WORKSPACE` 中的入口，避免死链。
- **推广门槛** — 无验收标准、无边界、含私钥/私路径的草稿 **不进** INDEX。

**独立产品仓脚手架：** 不在本仓安装 `project_scaffold`；新开 App/产品 repo 时读 [context-infrastructure · project_scaffold](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/project_scaffold.md)。

---

## Progressive Disclosure

- **INDEX.md** 只提供路由
- **skill 文件** 包含完整步骤 — 命中后必须读它
- **本地 overlay**（`overlays/*.local.md`）含路径与账号别名，gitignored
