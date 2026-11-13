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

## Drive 真源（Owner 持续更新）

| 项 | 值 |
|----|-----|
| 文件夹 | [我的小红书数据](https://drive.google.com/drive/folders/1kFYScZvFgd52983gK0gItIuRq0-43WyR?usp=drive_link) |
| 配置 | `integration/handoff/owner-xhs-data-drive.json` |
| Agent L1 | `content/personal-ip/intake/2026-11-07-owner-xhs-data-drive-L1.md` |
| 同步 | `bash scripts/sync-owner-xhs-data-from-drive.sh` |

发完笔记/视频 → 更新 Drive xlsx（**或**在 Cursor 附上 xlsx）→ **Agent 自动同步**（`xhs-owner-data-auto-sync.sh` · 见 `owner-xhs-data-drive.json` `agent_auto_sync`）→ 再读 `derived/xhs-data-strategy-*.md`。**禁止**要求 Owner 另说「同步小红书数据」。

## 三层存放（记路径即可）

```text
L0 Drive（Owner My Drive · 与 L1 raw 镜像）
  我的小红书数据/  # 列表、近30日、单篇明细 xlsx

L1 原始（gitignore · 换机需拷贝或重导）
  content/analytics/raw/xiaohongshu/2026-10-20/notes-detail.xlsx   # 列表总表
  content/analytics/raw/xiaohongshu/note-details/*数据明细表.xlsx  # 单篇明细
  content/analytics/raw/xiaohongshu/YYYY-MM-DD/account-*.xlsx    # 近7日/30日 账号表（观看/互动/涨粉/发布）
  content/analytics/xiaohongshu/account-7d-summary-YYYY-MM-DD.json  # 近7日合并 JSON

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

Owner 上传 **任意组合** xlsx（列表 / 单篇明细 / 近7日）后，Agent **同一会话自动**：

```bash
bash scripts/xhs-owner-data-auto-sync.sh --from-dir <Downloads 或 drive-sync-latest>
# Drive 真源：
bash scripts/sync-owner-xhs-data-from-drive.sh
```

脚本会：归档 raw → 合并全部历史列表 → 融合单篇明细 → `notes.csv` + `笔记链接回填表.xlsx` + `小红书笔记数据汇总-全指标-日期.xlsx`（并复制到 `~/Downloads`）。

手工调试（仅 Agent）：

```bash
python scripts/analytics/xhs_sync_warehouse.py merge
python scripts/analytics/xhs_note_links.py import-workbook   # 若 Owner 手改回填表
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