# 内容交付 · Owner 确认门（Agent 必守）

> **数据叠加栈：** [docs/XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md)

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
