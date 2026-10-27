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
