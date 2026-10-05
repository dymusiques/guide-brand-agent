---
name: business-brand
description: >-
  Business planning and brand strategy — positioning, SWOT, competitor framing.
  Use for 商业策划, 品牌策划, 品牌策略, 竞品, SWOT.
---

# Business & Brand Planning

## 读什么

1. `guide-core/soul.md` + `guide-core/user.md`
2. Git `content/business-brand/` + `rules/USER.md`（真相源，优先）
3. Drive `03-business-brand/`（仅 Owner 已同步定稿时查阅）
4. `kernels/templates/campaign-plan.template.md`（商业层）

## 存储默认规则

与 [docs/HANDOFF-COMPLETENESS.md](../../../docs/HANDOFF-COMPLETENESS.md) 一致：

1. **草稿** → 写 `content/business-brand/`
2. **稳定 / 定稿** → git commit（Owner 说「定稿」或段落完成时）
3. **Drive** → 仅 Owner 说「同步 Drive」→ 写入 `03-business-brand/`
4. **禁止** → 只写 Drive 不 commit；未 commit 就称交班完成

交班前：`bash scripts/verify-handoff.sh`

## 产出

- 品牌定位 / 价值主张
- SWOT 或竞品对比（需 WebSearch 补充公开信息）
- 品牌手册大纲

## 验收

- [ ] 结论可验证（不编造竞品数据）
- [ ] 已写入 `content/business-brand/` 且稳定后 commit
- [ ] （可选）Owner 说「同步 Drive」时已写入 `03-business-brand/`
