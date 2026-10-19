# 多平台数据仓库 · Analytics

统一存放 **小红书 / Instagram / YouTube** 运营数据（Git 内为 **示例 + 派生报告**；真实导出 CSV 建议本地命名 `notes.csv` 且勿含私信正文）。

## 目录

| 路径 | 用途 |
|------|------|
| `inbox/` | Owner 从各平台后台 **导出** 后暂放；由 `analytics-fetch.sh` 归档 |
| `xiaohongshu/` | 小红书笔记级 CSV |
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
# 1. 导出 CSV 放进 inbox/（或指定文件 import）
bash scripts/analytics-fetch.sh

# 2. 校验 + 汇总 + 生成下一选题建议
bash scripts/analytics-pipeline.sh
```

产出交给 **09 → 04 Topic Manager**（见 `agents/09-data-analytics/INTEGRATION-PROMPT.md`）。

集成层 Dry Run 清单：[integration/IMPORTANT.md](../../integration/IMPORTANT.md#dry-run破坏性--发布侧--摘录)

## API 说明

各平台 **无统一公开 API** 给本仓自动拉取；`analytics-fetch.sh` 处理 **后台导出的 CSV/表格**。  
若日后接入官方 API，扩展 `scripts/analytics/fetch/`（见该目录 README）。
