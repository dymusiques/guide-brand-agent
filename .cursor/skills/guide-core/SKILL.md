---
context_version: "2026-10-30-l012"
repo_path: ".cursor/skills/guide-core/SKILL.md"
goal: "Guide Core — 总控"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "534e6644f512b5fc"
---

# Guide Core — 总控

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** **Canonical 集成：** [agents/README.md](../../../agents/README.md) · [docs/DANYING-BRAND-AGENT-INTEGRATION.md](../../../docs/DANYING-BRAND-AGENT-INTEGRATION.md) · [00-manager INTEGRAT
- **Path:** `.cursor/skills/guide-core/SKILL.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **启动顺序**: **Canonical 集成：** [agents/README.md](../../../agents/README.md) · [docs/DANYING-BRAND-AGENT-INTEGRAT…
- **路由规则**: | 用户意图关键词 | 领域 Skill |
- **Knowledge Bank · 存储（少占 Drive）**: 读 [docs/HANDOFF-COMPLETENESS.md](../../../docs/HANDOFF-COMPLETENESS.md)：
- **Generative Kernel 原则**: - 复用 `kernels/` 里的参考实现与模板，现场组装，不跑死程序


---

## L2 正文

# Guide Core — 总控

## 启动顺序

**Canonical 集成：** [agents/README.md](../../../agents/README.md) · [docs/DANYING-BRAND-AGENT-INTEGRATION.md](../../../docs/DANYING-BRAND-AGENT-INTEGRATION.md) · [00-manager INTEGRATION-PROMPT](../../../agents/00-manager/INTEGRATION-PROMPT.md)

1. `soul.md` — 品牌人格与边界
2. `user.md` — Owner 背景（张丹瀛 / Danying）
3. `routing.md` — 任务路由到领域 Skill
4. `rules/skills/INDEX.md` — 工具型能力（gdocs 等）

## 路由规则

| 用户意图关键词 | 领域 Skill |
|---------------|-----------|
| 个人IP、人设、定位、内容支柱 | `personal-ip` |
| 商业计划、品牌策略、竞品、SWOT | `business-brand` |
| 宣传、推广、campaign、渠道 | `marketing-strategy` |
| 小红书、笔记、种草、投放 | `xiaohongshu` |
| 视觉、Canva、配色、品牌一致性 | `brand-visual` |
| Google Doc、Gmail、Calendar、Drive | `rules/skills/skill_google_docs.md` |

多领域任务：先读 `guide-core/soul.md`，再并行读各相关领域 Skill，产出统一 Brief。

## Knowledge Bank · 存储（少占 Drive）

读 [docs/HANDOFF-COMPLETENESS.md](../../../docs/HANDOFF-COMPLETENESS.md)：

1. **Git 真相源：** `rules/USER.md` + `content/<domain>/`（稳定后 Must commit）
2. **Drive 可选：** 仅 Owner 说「同步 Drive」→ 写 Knowledge Bank 定稿文件夹
3. **禁止：** 只写 Drive 不 commit；只留未 commit 本地就交班

交班前：`bash scripts/verify-handoff.sh`

## Generative Kernel 原则

- 复用 `kernels/` 里的参考实现与模板，现场组装，不跑死程序
- 每个任务结束：可沉淀案例到 `kernels/examples/`（commit）；Drive `99-examples/` 仅 Owner 说「同步 Drive」时