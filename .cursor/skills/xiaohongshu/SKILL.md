---
context_version: "2026-10-30-l012"
repo_path: ".cursor/skills/xiaohongshu/SKILL.md"
goal: "Xiaohongshu"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "a68c5cbf7e8a35ee"
---

# Xiaohongshu

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** **选题、Brief、对齐 IP、强链接、涨粉路径** → 必读 **[topic-manager.md](./topic-manager.md)**，并接 Kernel：
- **Path:** `.cursor/skills/xiaohongshu/SKILL.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **Topic Manager（选题 / IP 对齐）**: **选题、Brief、对齐 IP、强链接、涨粉路径** → 必读 **[topic-manager.md](./topic-manager.md)**，并接 Kernel：
- **读什么**: 1. **Owner 固定总纲（Brief Must）** → [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../../../docs/OWNER…
- **存储默认规则**: 与 [docs/HANDOFF-COMPLETENESS.md](../../../docs/HANDOFF-COMPLETENESS.md) 一致：
- **产出**: - 笔记结构（标题 / 钩子 / 正文 / 标签）
- **验收**: - [ ] 符合小红书语气与合规（无 Web3/NFT；数字藏品表述 OK）


---

## L2 正文

# Xiaohongshu

## Topic Manager（选题 / IP 对齐）

**选题、Brief、对齐 IP、强链接、涨粉路径** → 必读 **[topic-manager.md](./topic-manager.md)**，并接 Kernel：

- 单条判定：`python scripts/evaluate-xhs-topic.py --brief …`
- Kernel 6 case：`bash scripts/verify-xhs-topic.sh`
- 实现与规则：`kernels/xiaohongshu/`

## 读什么

1. **Owner 固定总纲（Brief Must）** → [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../../../docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) · pitfalls · 三镜头 · gap 直到 READY
2. `guide-core/soul.md`（品牌名与语气）
3. **Owner 数据叠加栈（写 Brief/视频/标题前 Must）** → [XHS-CONTENT-INTAKE-STACK.md](../../../docs/XHS-CONTENT-INTAKE-STACK.md) · [CONTENT-DELIVERY-FOR-OWNER.md](../../../content/xiaohongshu/CONTENT-DELIVERY-FOR-OWNER.md)
4. Git `content/xiaohongshu/`（真相源，优先）
5. 个人 Skill `danying-tingjian-daily`（栏目规范，若做长笛内容）
6. Drive `05-xiaohongshu/`（仅 Owner 已同步定稿时查阅）
7. `kernels/templates/xhs-content-brief.template.md`
8. **选题管线** → [topic-manager.md](./topic-manager.md)
9. **定稿前文风自查（仅小红书短文案）** → [xhs-copy-self-check.md](./xhs-copy-self-check.md) · 规则 `.cursor/rules/xhs-copy-quality.mdc`

## 定稿前文风（自动化 · 无需 Owner 口令）

- 修改 `content/xiaohongshu/*.md` 时，**`xhs-copy-quality.mdc`** 自动生效。  
- Agent **定稿前 Must** 跑 `bash scripts/xhs-copy-grep-banned.sh <稿>.md` 并对照 **`xhs-copy-self-check.md`**，回复中报告 `xhs-copy-grep-banned: PASS` 或已改项。

## 不要混淆

| 工具 / 文档 | 何时用 |
|-------------|--------|
| **`xhs-copy-self-check.md`** | 笔记成稿后：去 AI 腔、翻译腔（短文案） |
| **`kernels/xiaohongshu/` + `verify-xhs-topic.sh`** | 选题对齐 IP / 涨粉 / 强链接 |
| **grapeot/writing-skill · `external-prose-lint`** | **不用**于小红书；仅对外**长文** |

**推荐顺序：** 写稿 → Topic Manager（若要 aligned）→ **`xhs-copy-grep-banned.sh`** → **本清单** → commit。

## 存储默认规则

与 [docs/HANDOFF-COMPLETENESS.md](../../../docs/HANDOFF-COMPLETENESS.md) 一致：

1. **草稿** → 写 `content/xiaohongshu/`
2. **稳定 / 定稿** → git commit（Owner 说「定稿」或段落完成时）
3. **Drive** → 仅 Owner 说「同步 Drive」→ 写入 `05-xiaohongshu/`
4. **禁止** → 只写 Drive 不 commit；未 commit 就称交班完成

交班前：`bash scripts/verify-handoff.sh`

## 产出

- 笔记结构（标题 / 钩子 / 正文 / 标签）
- 封面 Brief（交 `brand-visual` 或 Canva）
- 投放/种草方向建议（非实时数据需标注）

## 验收

- [ ] 符合小红书语气与合规（无 Web3/NFT；数字藏品表述 OK）
- [ ] 与 Danying 品牌一致
- [ ] **`xhs-copy-grep-banned.sh` PASS** + 已对照 `xhs-copy-self-check.md` 硬项
- [ ] Topic Manager：`evaluate-xhs-topic.py` 为 `aligned: true`，或 Owner 书面接受风险
- [ ] 已写入 `content/xiaohongshu/` 且稳定后 commit
- [ ] （可选）Owner 说「同步 Drive」时已写入 `05-xiaohongshu/`