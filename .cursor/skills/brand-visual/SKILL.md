---
name: brand-visual
description: >-
  Brand visual design direction, Canva workflows, palette and consistency checks.
  Use for 品牌视觉, Canva, 配色, 设计规范, 封面.
---

# Brand Visual

## 读什么

1. `guide-core/soul.md` + `rules/USER.md`（视觉规范）
2. Git `content/visual/`（Brief + Canva 链接，真相源，优先）
3. Canva Brand Kit（MCP 授权后）
4. Drive `06-visual/`（仅 Owner 已同步定稿时查阅）
5. Canva skills：`brand-check`, `edit-design`, `resize-for-social-media`

## 存储默认规则

与 [docs/HANDOFF-COMPLETENESS.md](../../../docs/HANDOFF-COMPLETENESS.md) 一致：

1. **草稿** → 写 `content/visual/`（Brief + Canva 设计链接）
2. **稳定 / 定稿** → git commit（Owner 说「定稿」或段落完成时）
3. **Drive** → 仅 Owner 说「同步 Drive」→ 写入 `06-visual/`
4. **Canva** → 成品留在 Canva；Git 只存链接，不占 Drive
5. **禁止** → 只写 Drive 不 commit；未 commit 就称交班完成

交班前：`bash scripts/verify-handoff.sh`

## 产出

- 视觉 Brief（尺寸、主色、字体、参考）
- Canva 修改指令或设计反馈
- 多平台尺寸清单（小红书 / Instagram）

## 验收

- [ ] 与 Brand Kit 或 `rules/USER.md` 中的视觉规范一致
- [ ] 已写入 `content/visual/`（Brief + Canva 链接）且稳定后 commit
- [ ] （可选）Owner 说「同步 Drive」时已写入 `06-visual/`
