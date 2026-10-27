# 多平台数据仓库 · Analytics

统一存放 **小红书 / Instagram / YouTube** 运营数据（Git 内为 **示例 + 派生报告**；真实导出 CSV 建议本地命名 `notes.csv` 且勿含私信正文）。

## 目录

| 路径 | 用途 |
|------|------|
| `inbox/` | Owner 从各平台后台 **导出** 后暂放；由 `analytics-fetch.sh` 归档 |
| `xiaohongshu/` | 小红书笔记级 CSV · **`note-links.csv`** · **`DATA-MANIFEST.json`** · **`notes-snapshot-*.json`**（接手索引，见 [XHS-DATA-LAYER.md](../../docs/XHS-DATA-LAYER.md)） |
| `instagram/` | IG 帖文级 CSV |
| `youtube/` | YouTube 视频级 CSV |
| `derived/` | Pipeline 输出：`next-topics-*.md` / `summary-*.json` |

## 三阶段（摘录 · 与 staged 对齐）

| Stage | 本仓动作 | 边界 |
|-------|----------|------|
| **1 · 采集** | Owner 后台导出 → 放入 `inbox/` → `analytics-fetch.sh` 归档 | 只读平台导出；**不**自动爬取私信/账号 |
| **2 · 本地处理** | `analytics-pipeline.sh` → `derived/` 报告与 `next-topics` | AI/脚本只在 Git 内算分；**不**改 Brief 正文、不发帖 |
| **3 · 确认** | Owner 看 `derived/`；09→04 派活；是否写新 Brief 由 Manager/Owner 定 | 选题建议 **非** 自动发布 |

## Pipeline（读 → 算分 → 下一题清单）

```bash
# 0. （首次 / 新导出）维护笔记链接注册表 — 后台 xlsx 无 URL
python scripts/analytics/xhs_note_links.py scaffold \
  --xlsx content/analytics/raw/xiaohongshu/YYYY-MM-DD/notes-detail.xlsx
**推荐（Excel 一张表）：** 生成 `xiaohongshu/笔记链接回填表.xlsx`（含后台全部指标 + **笔记链接（请填写）** 列）→ 填链接后：

```bash
python scripts/analytics/xhs_note_links.py import-workbook
python scripts/analytics/xhs_convert_notes_detail.py --xlsx content/analytics/raw/xiaohongshu/YYYY-MM-DD/notes-detail.xlsx
bash scripts/analytics-fetch.sh && bash scripts/analytics-pipeline.sh
```

生成表：`python scripts/analytics/xhs_note_links.py export-workbook --xlsx content/analytics/raw/xiaohongshu/YYYY-MM-DD/notes-detail.xlsx`

**或** 在 `note-links.csv` 填 `note_url`（App 分享→复制链接）
python scripts/analytics/xhs_note_links.py sync-briefs   # 已填 Brief「笔记链接」的会自动合并

# 1. xlsx → inbox（自动读 note-links.csv 写入 note_id）
python scripts/analytics/xhs_convert_notes_detail.py \
  --xlsx content/analytics/raw/xiaohongshu/YYYY-MM-DD/notes-detail.xlsx
bash scripts/analytics-fetch.sh

# 2. 校验 + 汇总 + 生成下一选题建议
bash scripts/analytics-pipeline.sh
```

已有 `notes.csv` 仅缺链接时：`python scripts/analytics/xhs_note_links.py apply --csv content/analytics/xiaohongshu/notes.csv`

模板列见 `xiaohongshu/note-links.example.csv`。

产出交给 **09 → 04 Topic Manager**（见 `agents/09-data-analytics/INTEGRATION-PROMPT.md`）。

集成层 Dry Run 清单：[integration/IMPORTANT.md](../../integration/IMPORTANT.md#dry-run破坏性--发布侧--摘录)

## API 说明

各平台 **无统一公开 API** 给本仓自动拉取；`analytics-fetch.sh` 处理 **后台导出的 CSV/表格**。  
若日后接入官方 API，扩展 `scripts/analytics/fetch/`（见该目录 README）。
