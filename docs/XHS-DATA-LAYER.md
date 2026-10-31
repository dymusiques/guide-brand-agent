---
context_version: "2026-10-30-l012"
repo_path: "docs/XHS-DATA-LAYER.md"
goal: "小红书数据层 · 接手必读（AI + Owner）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "b3dd0cf875b5493e"
---

# 小红书数据层 · 接手必读（AI + Owner）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **机器索引：** [`content/analytics/xiaohongshu/DATA-MANIFEST.json`](../content/analytics/xiaohongshu/DATA-MANIFEST.json)  
> **行级快照（可提交 Git）：** [`notes-snapshot-2026-10-20.json`](../c
- **Path:** `docs/XHS-DATA-LAYER.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **状态（2026-10-20）**: | 项 | 值 |
- **三层存放（记路径即可）**: ```text
- **一行命令（新机恢复 pipeline）**: ```bash
- **CSV 长什么样**: 列定义：`scripts/analytics/schemas.py` → `XHS_CSV_FIELDNAMES`。
- **与成稿的衔接**: | 数据结论 | 成稿位置 |
- **强链接口径**: 约课私信 **不计** 认知期有效 `dm_count` → [discovery-phase-signal-baseline.md](../content/marketing/discovery-p…


---

## L2 正文

# 小红书数据层 · 接手必读（AI + Owner）

> **机器索引：** [`content/analytics/xiaohongshu/DATA-MANIFEST.json`](../content/analytics/xiaohongshu/DATA-MANIFEST.json)  
> **行级快照（可提交 Git）：** [`notes-snapshot-2026-10-20.json`](../content/analytics/xiaohongshu/notes-snapshot-2026-10-20.json)  
> **策略（09→04）：** [`derived/xhs-data-strategy-2026-10-20.md`](../content/analytics/derived/xhs-data-strategy-2026-10-20.md)

## 状态（2026-10-20）

| 项 | 值 |
|----|-----|
| 笔记行数 | **23** |
| 真实链接 | **23/23**（`note-links.csv`） |
| 单篇明细 xlsx | **23**（归档 + `detail-json/`） |
| Owner 侧是否还有未导入表 | **否**（笔记级已齐） |
| 缺平台导出 | **私信**（`dm_count` 手填/口述） |

## 三层存放（记路径即可）

```text
L1 原始（gitignore · 换机需拷贝或重导）
  content/analytics/raw/xiaohongshu/2026-10-20/notes-detail.xlsx   # 列表总表
  content/analytics/raw/xiaohongshu/note-details/*数据明细表.xlsx  # 单篇明细
  content/analytics/raw/xiaohongshu/2026-10-20/account-*.xlsx      # 账号 30 天（pipeline 未自动读）

L2 可维护注册表（建议 commit）
  content/analytics/xiaohongshu/note-links.csv
  content/analytics/xiaohongshu/笔记链接回填表.xlsx
  content/analytics/xiaohongshu/DATA-MANIFEST.json
  content/analytics/xiaohongshu/notes-snapshot-YYYY-MM-DD.json

L3 运行产物（gitignore 或 derived）
  content/analytics/xiaohongshu/notes.csv          # canonical 仓库
  content/analytics/xiaohongshu/detail-json/*.json # 按日序列
  content/analytics/derived/summary-*.json
  content/analytics/derived/next-topics-*.md
  content/analytics/derived/ceo-dispatch-latest.md
```

## 一行命令（新机恢复 pipeline）

```bash
bash scripts/ensure-venv-deps.sh
bash scripts/manager-autopilot.sh
```

有 **新** 列表 xlsx 时：

```bash
python scripts/analytics/xhs_note_links.py import-workbook   # 若改了回填表
python scripts/analytics/xhs_convert_notes_detail.py \
  --xlsx content/analytics/raw/xiaohongshu/2026-10-20/notes-detail.xlsx
bash scripts/analytics-fetch.sh && bash scripts/analytics-pipeline.sh
```

新 **单篇明细** 放进目录后：

```bash
python scripts/analytics/xhs_note_detail.py ingest --dir ~/Downloads
# 再跑 convert + fetch + pipeline（同上）
```

## CSV 长什么样

列定义：`scripts/analytics/schemas.py` → `XHS_CSV_FIELDNAMES`。  
示例（可 commit）：`notes.example.csv`。

## 与成稿的衔接

| 数据结论 | 成稿位置 |
|----------|----------|
| 选题/排序 | `derived/next-topics-*.md` |
| 策略叙述 | `derived/xhs-data-strategy-2026-10-20.md` |
| 可直发正文 | `content/xiaohongshu/2026-10-20-publish-ready-queue.md` |
| Brief 定稿 | `content/xiaohongshu/2026-10-17-discovery-*.md` |

## 强链接口径

约课私信 **不计** 认知期有效 `dm_count` → [discovery-phase-signal-baseline.md](../content/marketing/discovery-phase-signal-baseline.md)