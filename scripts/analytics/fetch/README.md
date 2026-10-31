---
context_version: "2026-10-30-l012"
repo_path: "scripts/analytics/fetch/README.md"
goal: "Platform fetch / export（非 live API 默认）"
openwebui_route: "skip"
cursor_route: "exec"
content_sha256: "748a4150f6fecc57"
---

# Platform fetch / export（非 live API 默认）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 本仓 **默认** 不持有小红书 / Meta / Google OAuth 用于自动拉数。
- **Path:** `scripts/analytics/fetch/README.md`
- **Open WebUI:** `skip`
- **Cursor:** `exec`

## 章节锚点
- **将来 API 扩展点**: 在此目录增加 `fetch_<platform>.py`，读取 gitignored `.env` 中的 key，写入 `content/analytics/inbox/`，再由 `analytics…


---

## L2 正文

# Platform fetch / export（非 live API 默认）

本仓 **默认** 不持有小红书 / Meta / Google OAuth 用于自动拉数。

| 平台 | Owner 动作 | 归档 |
|------|------------|------|
| 小红书 | 创作者后台「笔记列表明细表」xlsx | 归档 raw → **`xhs_note_links.py scaffold`** 维护 `note-links.csv` → **`xhs_convert_notes_detail.py`**（合并真实 `note_id`）→ `analytics-fetch.sh` |
| Instagram | Insights 导出 / 第三方表格 | `inbox/instagram-*.csv` |
| YouTube | Studio 导出 / Analytics 表格 | `inbox/youtube-*.csv` |

## 将来 API 扩展点

在此目录增加 `fetch_<platform>.py`，读取 gitignored `.env` 中的 key，写入 `content/analytics/inbox/`，再由 `analytics-fetch.sh` 统一 import。  
未配置 key 时 **必须** 失败并提示手动导出，**禁止** 编造数据。