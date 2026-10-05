---
name: marketing-strategy
description: >-
  Promotion direction, channel strategy, campaign briefs, and scheduling.
  Use for 宣传, 营销, 推广, campaign, 渠道策略.
---

# Marketing Strategy

## 读什么

1. `guide-core/soul.md` + `guide-core/user.md`
2. Git `content/marketing/`（真相源，优先）
3. Drive `04-marketing/`（仅 Owner 已同步定稿时查阅）
4. `kernels/templates/campaign-plan.template.md`

## 存储默认规则

与 [docs/HANDOFF-COMPLETENESS.md](../../../docs/HANDOFF-COMPLETENESS.md) 一致：

1. **草稿** → 写 `content/marketing/`
2. **稳定 / 定稿** → git commit（Owner 说「定稿」或段落完成时）
3. **Drive** → 仅 Owner 说「同步 Drive」→ 写入 `04-marketing/`
4. **禁止** → 只写 Drive 不 commit；未 commit 就称交班完成

交班前：`bash scripts/verify-handoff.sh`

## 产出

- Campaign Brief（目标、受众、渠道、KPI、时间线）
- 渠道组合建议（小红书 / Instagram / 未来视频号）
- 与 `xiaohongshu` / `brand-visual` skill 的交接说明

## 验收

- [ ] Brief 含可执行下一步
- [ ] 已写入 `content/marketing/` 且稳定后 commit
- [ ] （可选）Owner 说「同步 Drive」时已写入 `04-marketing/`
