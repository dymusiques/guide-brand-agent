---
context_version: "2026-10-30-l012"
repo_path: "content/xiaohongshu/OWNER-CONTENT-SPEC.md"
goal: "Owner · 小红书成稿交付规范"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "f2810b6eb6e952f0"
---

# Owner · 小红书成稿交付规范

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** | 规则 | 说明 |
|------|------|
| **吸睛** | 具体冲突 / 判断 / 问句；忌空泛「高端」「赋能」 |
| **数据背书** | 先对照 **账号 23 篇 snapshot / xhs-data-strategy**（哪类帖 CTR、收藏、涨粉更强），再写标题；**不编造** 平台大盘假数进标题 |
| **字数** | *
- **Path:** `content/xiaohongshu/OWNER-CONTENT-SPEC.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > Agent（04 / 00 Manager）产出 **待 Owner 确认** 的笔记包时 **Must** 遵守。
- **章节锚点**: - **1. 标题 + 封面**: | 规则 | 说明 |
- **1. 标题 + 封面**: | 规则 | 说明 |
- **2. 正文与主题**: - **长稿（Must）：** [OWNER-LONGFORM-XHS-SPEC.md](./OWNER-LONGFORM-XHS-SPEC.md) — **3000–5000 字** Owner 发…
- **3. 标签**: - **必须 10 个** `#` 标签（evaluate / seo-lint 仍要求 ≥3，本规范以 10 为准）。
- **4. 说明**: - 每包附 **「为什么这样写」**：对应哪条 **自有数据**、哪条 **平台 MD**、哪条 **认知期队列**。
- **5. 流程**: - 成稿 → Owner 确认 → App 发布 → 回填 Brief `## 发布状态`。


---

## L2 正文

# Owner · 小红书成稿交付规范

> Agent（04 / 00 Manager）产出 **待 Owner 确认** 的笔记包时 **Must** 遵守。  
> 数据与平台栈：[docs/XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md)

---

## 1. 标题 + 封面

| 规则 | 说明 |
|------|------|
| **吸睛** | 具体冲突 / 判断 / 问句；忌空泛「高端」「赋能」 |
| **数据背书** | 先对照 **账号 23 篇 snapshot / xhs-data-strategy**（哪类帖 CTR、收藏、涨粉更强），再写标题；**不编造** 平台大盘假数进标题 |
| **字数** | **≤20 字**（**含 emoji、标点、符号**，发布前人工再数一遍） |
| **封面字** | 单独给出 **打在封面图上的文案**（通常 1～2 行、比标题更短、更抓眼）；与标题 **不重复堆砌** |

## 2. 正文与主题

- **长稿（Must）：** [OWNER-LONGFORM-XHS-SPEC.md](./OWNER-LONGFORM-XHS-SPEC.md) — **3000–5000 字** Owner 发布版 + classifier 短摘要。  
- 列出 **主题一句话** + **完整可粘贴长稿**（含钩子、CTA）。  
- 结构对齐：数据（故事+判断）+ 认知期主轴 + [platform-notes-2026.md](./platform-notes-2026.md)。  
- CTA：收藏 + 私信「聊聊」/「合作/品牌」；**约课** 不作强链接主 KPI。

## 3. 标签

- **必须 10 个** `#` 标签（evaluate / seo-lint 仍要求 ≥3，本规范以 10 为准）。

## 4. 说明

- 每包附 **「为什么这样写」**：对应哪条 **自有数据**、哪条 **平台 MD**、哪条 **认知期队列**。

## 5. 流程

- 成稿 → Owner 确认 → App 发布 → 回填 Brief `## 发布状态`。  
- Brief 定稿仍跑 `evaluate-xhs-topic.py`（`aligned: true`）。