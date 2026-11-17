# 全平台交付包（一篇文章类 = 同一标准）

真源：`integration/handoff/owner-deliverable-pack-mandate.json`

## 四块（全平台同义）

| 块 | 含义 |
|----|------|
| **简报** | 标题、钩子、结构、标签/话题、CTA |
| **架构说明** | 三镜头 / 段落骨架 / 分镜备忘 / 平台适配 |
| **完整文稿** | 可发布全文（小红书长稿、LinkedIn 帖、Medium 文、口播全文） |
| **为什么这样写** | 数据、队列、案例依据 |

磁盘命名习惯（**不改历史脚本参数**）：

| 平台 | 路径模式 | 验证 |
|------|----------|------|
| 小红书笔记 | `content/xiaohongshu/*-brief.md` | `verify-owner-deliverable-pack.py --brief …` |
| 小红书口播视频 | `content/xiaohongshu/inbox/pending-videos/*.md` | 同上 `--oral …` |
| LinkedIn | `content/deliverables/linkedin/*-pack.md` | `--linkedin …` |
| Medium | `content/deliverables/medium/*-pack.md` | `--medium …` |

模板：`content/deliverables/TEMPLATE-*-pack.md` · 口播见 `pending-videos/TEMPLATE.md`

## CEO / gate

凡 **写稿 / 派活给 CEO / 交付 Owner HTML** → Must 达到交付包 READY（见 mandate · `verify-owner-deliverable-pack.py` FAIL 则继续进化，不交 Owner 半成品）。