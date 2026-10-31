---
context_version: "2026-10-30-l012"
repo_path: "content/xiaohongshu/BRIEF-PITFALLS-RESEARCH-SOP.md"
goal: "Brief 写前 · 同类坑调研 SOP（Owner Must · 2026-10-28）"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "1f24fcf882076ddc"
---

# Brief 写前 · 同类坑调研 SOP（Owner Must · 2026-10-28）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > 隶属 [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../../docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) §1-B。  
> **无本文件不得写 `*-brief.md`**（与 redteam-pre 并列）。
- **Path:** `content/xiaohongshu/BRIEF-PITFALLS-RESEARCH-SOP.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **Must 做什么**: 1. **WebSearch / 深度调研**（≥3 次不同 query）：同类小红书命题、机构号写法、类似 IP（艺术×品牌、古典×商业等）。
- **落盘路径**: `content/xiaohongshu/research/<YYYY-MM-DD-slug>-pitfalls.md`
- **模板**: ```markdown
- **方向（1 段）**: - 受众 · 支柱 · CTA 类型 · 与 IP 一句对齐
- **外部样本（≥3）**: | 来源 | 写法摘要 | 问题 |
- **同类 IP / 机构常犯错误（≥5 条）**: 1. …
- **L2–L3 难自动纠（Must ≥3）**: - **X? / 自定义：** …（为何 L1 仍会绿）
- **本篇回应（进 Brief / redteam）**: - 坑 1 → …


---

## L2 正文

# Brief 写前 · 同类坑调研 SOP（Owner Must · 2026-10-28）

> 隶属 [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../../docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) §1-B。  
> **无本文件不得写 `*-brief.md`**（与 redteam-pre 并列）。

## Must 做什么

1. **WebSearch / 深度调研**（≥3 次不同 query）：同类小红书命题、机构号写法、类似 IP（艺术×品牌、古典×商业等）。  
2. 整理 **别人犯过的错 / 易踩坑**（可引用 URL，不编造数据）。  
3. 标 **至少 3 条 L2–L3 级坑**（难被 L1/禁词自动纠）。  
4. 写 **本篇准备怎么避坑 / 反打**（各 1 句，可进 redteam-pre）。

## 落盘路径

`content/xiaohongshu/research/<YYYY-MM-DD-slug>-pitfalls.md`

（slug 与 Brief 文件名一致，去掉 `-brief.md`）

## 模板

```markdown
# Pitfalls research · <slug> · <date>

## 方向（1 段）
- 受众 · 支柱 · CTA 类型 · 与 IP 一句对齐

## 外部样本（≥3）
| 来源 | 写法摘要 | 问题 |
|------|----------|------|
| … | … | 空案例 / 洗艺 / 命题撞车 … |

## 同类 IP / 机构常犯错误（≥5 条）
1. …
2. …

## L2–L3 难自动纠（Must ≥3）
- **X? / 自定义：** …（为何 L1 仍会绿）

## 本篇回应（进 Brief / redteam）
- 坑 1 → …
- 坑 2 → …
```

## 验收

- CEO / 04：Brief 正文或 redteam-pre **显式引用** 本文件至少 **2 条** 坑。  
- `analyze-brief-evolution-gap.py` 检查文件存在。