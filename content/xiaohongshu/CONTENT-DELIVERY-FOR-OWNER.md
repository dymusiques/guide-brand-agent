---
context_version: "2026-10-30-l012"
repo_path: "content/xiaohongshu/CONTENT-DELIVERY-FOR-OWNER.md"
goal: "内容交付 · Owner 确认门（Agent 必守）"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "ce23ae998e566bc2"
---

# 内容交付 · Owner 确认门（Agent 必守）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **数据叠加栈：** [docs/XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md)
- **Path:** `content/xiaohongshu/CONTENT-DELIVERY-FOR-OWNER.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **Owner 报告格式（Must · 2026-10-27）**: - **交给 Owner 的汇总/筛选/CEO 交付**：默认 **单文件 HTML**（浏览器双击可开；Discovery 等用 **弹出层** 展示全文）。
- **流程**: ```text
- **Agent 每轮必须交给 Owner 的包**: 规范细则：[OWNER-CONTENT-SPEC.md](./OWNER-CONTENT-SPEC.md) · **视频迭代：** [XHS-VIDEO-ITERATION.md](./XHS-VID…
- **Owner 确认后**: - 在 Brief 填 `## 发布状态`（日期、链接）。
- **禁止**: - 未读 Intake Stack 就称「已数据驱动定稿」。


---

## L2 正文

# 内容交付 · Owner 确认门（Agent 必守）

> **数据叠加栈：** [docs/XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md)

## Owner 报告格式（Must · 2026-10-27）

- **交给 Owner 的汇总/筛选/CEO 交付**：默认 **单文件 HTML**（浏览器双击可开；Discovery 等用 **弹出层** 展示全文）。
- **Markdown（`.md`）**：Agent 协作、Git 版本、Brief 源稿；**不**作为 Owner 主阅读格式（除非 Owner 点名要 MD）。
- **表格类数据**（如 Artist DB/PLD/APO/CTD）：**`.xlsx`**（附 `.csv` 可选）；HTML 内嵌预览 + 链到 Excel。
- **生成：** CEO 筛选批跑后执行 `python scripts/build-owner-xhs-report-html.py`（`ceo-xhs-ip-filter-batch.py` 已自动调用）。
- **交 Owner 前 · 单篇 Brief 必跑（Must）：**  
  `.venv/bin/python scripts/evaluate-xhs-brief-complete.py --brief content/xiaohongshu/<file>.md`  
  = **redteam-pre 存在** + **本篇 6 项 L1 对照** + **Gemini evaluate（aligned）** + **kernel 6 case 回归**（同一次命令）。
- **路径惯例：** `content/evolution/00-manager/ceo-inbox/OWNER-*-DELIVERABLE-<date>.html`
- **怎么打开才是网页：** 在 **Cursor 里点 `.html` 只会看到源代码**（正常）。请任选其一：
  - Finder 里 **双击** 该 `.html`（或右键 → 打开方式 → Safari / Chrome）
  - 双击同目录 **`OPEN-OWNER-REPORT-IN-BROWSER.command`**
  - 终端：`open content/evolution/00-manager/ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-<date>.html`

## 流程

```text
读 Intake Stack（Excel 策略 + PDF 研究 + IP + 认知期）
  → 09 建议 / 04 写稿（标题 · 正文 · 标签 · 视频脚本 · 选题思路）
  → evaluate（Brief）/ 自检清单
  → 写入 Git（draft 或 publish-ready 队列）
  → Owner 审阅确认
  → Owner 在小红书 App 发布（Agent 不代发）
```

## Agent 每轮必须交给 Owner 的包

规范细则：[OWNER-CONTENT-SPEC.md](./OWNER-CONTENT-SPEC.md) · **视频迭代：** [XHS-VIDEO-ITERATION.md](./XHS-VIDEO-ITERATION.md)

至少包含：

1. **依据**：引用了栈里哪几条（数据帖名 / WILL·Momentum 要点 / discovery 命题）。  
2. **标题**（1 主 + 备选；**≤20 字含 emoji/符号**；有数据校对说明）。  
3. **封面字**（打在封面图上的文案，与标题分工）。  
4. **正文**（可粘贴 App）。  
5. **标签**（**10 个** `#`）。  
6. **CTA**（品牌向「聊聊/合作」；非约课主导）。  
7. **视频**（若当轮要求）：分镜/口播/封面一句。  
8. **为什么这样写**（简短）。  
9. **状态**：`draft` / `aligned` / **待 Owner 确认发布**。

## Owner 确认后

- 在 Brief 填 `## 发布状态`（日期、链接）。  
- 可选：`python scripts/analytics/xhs_note_links.py` 更新链接表。

## 禁止

- 未读 Intake Stack 就称「已数据驱动定稿」。  
- 未 `aligned: true`（Brief）或未标注 **待确认** 就要求 Owner 当终稿发。  
- 编造平台或账号数据。