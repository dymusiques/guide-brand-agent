---
context_version: "2026-10-30-l012"
repo_path: "docs/OWNER-MULTICHANNEL-LINKEDIN-IMAGE-DELIVERABLE.md"
goal: "Owner · 多通道交付（小红书 + LinkedIn 图文 + 生图 · Must）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "380e31a2550f7de7"
---

# Owner · 多通道交付（小红书 + LinkedIn 图文 + 生图 · Must）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **触发：** Owner 要求 LinkedIn 同步 / 图文 / 生图 / 弹窗 HTML 时 **Must** 读本 SOP。
- **Path:** `docs/OWNER-MULTICHANNEL-LINKEDIN-IMAGE-DELIVERABLE.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **1. 产出物**: | 通道 | 路径 |
- **2. 生图工具优先级**: 1. **Cursor GenerateImage** / 仓库内资产（默认 · 可进 Git 相对路径）
- **3. 构建与打开**: ```bash
- **4. Evaluate / 压测**: 改 Brief/长稿后 **Must**：
- **5. Cursor 回复 Must**: [`OWNER-CHAT-DELIVERY-FORMAT.md`](./OWNER-CHAT-DELIVERY-FORMAT.md) + **多通道 HTML URI** + 01–12 roster…


---

## L2 正文

# Owner · 多通道交付（小红书 + LinkedIn 图文 + 生图 · Must）

> **触发：** Owner 要求 LinkedIn 同步 / 图文 / 生图 / 弹窗 HTML 时 **Must** 读本 SOP。

## 1. 产出物

| 通道 | 路径 |
|------|------|
| 小红书长稿 | `content/xiaohongshu/drafts/<slug>-longform.md`（**感想≥60%** · [OWNER-LONGFORM-DE-AI-VOICE.md](./OWNER-LONGFORM-DE-AI-VOICE.md) · 引用只进 Brief） |
| LinkedIn carousel EN | `content/marketing/linkedin/<date>-<slug>-carousel-en.md` |
| Slide 图片 | `content/evolution/00-manager/ceo-inbox/assets/<date>-<slug>/` |
| **弹窗 HTML** | `content/evolution/00-manager/ceo-inbox/OWNER-MULTICHANNEL-DELIVERABLE-<date>.html` |

## 2. 生图工具优先级

1. **Cursor GenerateImage** / 仓库内资产（默认 · 可进 Git 相对路径）  
2. **Canva MCP** `generate-image`（Owner 已授权时 · 记录 jobId）  
3. **禁止** 无图仅文字冒充「图文交付」

## 3. 构建与打开

```bash
python scripts/build-owner-multichannel-deliverable-html.py
bash scripts/open-owner-multichannel-deliverable-html.sh
```

默认 hash **`#multichannel`** → 进页弹 **小红书 v2 长稿**；LinkedIn slides 各 card 可再弹。

## 4. Evaluate / 压测

改 Brief/长稿后 **Must**：

```bash
bash scripts/ceo-triple-eval-baseline-loop.sh --brief content/xiaohongshu/<file>-brief.md
bash scripts/ceo-double-stress.sh --brief …
bash scripts/refresh-owner-notify-html.sh
python scripts/build-owner-multichannel-deliverable-html.py
```

## 5. Cursor 回复 Must

[`OWNER-CHAT-DELIVERY-FORMAT.md`](./OWNER-CHAT-DELIVERY-FORMAT.md) + **多通道 HTML URI** + 01–12 roster。