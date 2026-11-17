# Owner 交付包（文件名仍叫 Brief）

> **你说 Brief 时，我们按「交付包」执行，不是英语里那一页简报。**

真源：`integration/handoff/owner-deliverable-pack-mandate.json`

## 交付包 = 四块（全平台 · 缺一不可）

| 块 | 内容 |
|----|------|
| **1 · 简报** | 标题、封面/hook、CTA、标签/话题 |
| **2 · 架构说明** | 三镜头 / 段落骨架 / 分镜备忘 / 平台适配 |
| **3 · 完整文稿** | 可发布全文（长稿、帖、Medium 文、口播全文） |
| **4 · 为什么这样写** | 数据 / 队列 / 案例，禁止空话 |

平台路径与模板 → [OWNER-DELIVERABLE-PACK-PLATFORMS.md](./OWNER-DELIVERABLE-PACK-PLATFORMS.md)

磁盘路径习惯仍是 `content/xiaohongshu/*-brief.md`（历史命名）；**语义 = 整包**，不是只有第一节策划表。

## CEO / gate Must

- **派活给 CEO** + 写稿 goal → 进化到 **交付包 READY**（四块齐 · 含完整文稿），**禁止**只交结构提纲当终稿。
- 交付前跑 `python3 scripts/verify-owner-deliverable-pack.py`（`--brief` / `--oral` / `--linkedin` / `--medium`）。
- `manager-ceo-auto-gate-loop` · `ceo-triple-eval-baseline-loop` 评估的是 **整包**，不是摘要 alone。

## 与「派活给 CEO」

你只需：**派活给 CEO + 当句 goal**。不必说 triple-eval；机械层按本 mandate 要求 **完整文稿 + 说明**。