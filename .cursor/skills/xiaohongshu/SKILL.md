---
name: xiaohongshu
description: >-
  Xiaohongshu content, ads, growth, and Topic Manager — notes, hooks, topic selection,
  IP-aligned verify. Use for 小红书, 笔记, 种草, 投放, 选题, Topic Manager, 爆款, 涨粉.
---

# Xiaohongshu

## Topic Manager（选题 / IP 对齐）

**选题、Brief、对齐 IP、强链接、涨粉路径** → 必读 **[topic-manager.md](./topic-manager.md)**，并接 Kernel：

- 单条判定：`python scripts/evaluate-xhs-topic.py --brief …`
- Kernel 6 case：`bash scripts/verify-xhs-topic.sh`
- 实现与规则：`kernels/xiaohongshu/`

## 读什么

1. `guide-core/soul.md`（品牌名与语气）
2. **Owner 数据叠加栈（写 Brief/视频/标题前 Must）** → [XHS-CONTENT-INTAKE-STACK.md](../../../docs/XHS-CONTENT-INTAKE-STACK.md) · [CONTENT-DELIVERY-FOR-OWNER.md](../../../content/xiaohongshu/CONTENT-DELIVERY-FOR-OWNER.md)
3. Git `content/xiaohongshu/`（真相源，优先）
4. 个人 Skill `danying-tingjian-daily`（栏目规范，若做长笛内容）
5. Drive `05-xiaohongshu/`（仅 Owner 已同步定稿时查阅）
6. `kernels/templates/xhs-content-brief.template.md`
7. **选题管线** → [topic-manager.md](./topic-manager.md)

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
- [ ] Topic Manager：`evaluate-xhs-topic.py` 为 `aligned: true`，或 Owner 书面接受风险
- [ ] 已写入 `content/xiaohongshu/` 且稳定后 commit
- [ ] （可选）Owner 说「同步 Drive」时已写入 `05-xiaohongshu/`
