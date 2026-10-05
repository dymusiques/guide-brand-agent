---
name: xiaohongshu
description: >-
  Xiaohongshu content, ads, and growth — notes, hooks, covers, posting strategy.
  Use for 小红书, 笔记, 种草, 投放, 小红书广告.
---

# Xiaohongshu

## 读什么

1. `guide-core/soul.md`（品牌名与语气）
2. Git `content/xiaohongshu/`（真相源，优先）
3. 个人 Skill `danying-tingjian-daily`（栏目规范，若做长笛内容）
4. Drive `05-xiaohongshu/`（仅 Owner 已同步定稿时查阅）
5. `kernels/templates/xhs-content-brief.template.md`

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

- [ ] 符合小红书语气与合规
- [ ] 与 Danying 品牌一致
- [ ] 已写入 `content/xiaohongshu/` 且稳定后 commit
- [ ] （可选）Owner 说「同步 Drive」时已写入 `05-xiaohongshu/`
