---
context_version: "2026-10-30-l012"
repo_path: "agents/09-data-analytics/DATA-NEEDS.md"
goal: "数据分析 Agent · 多平台数据规范"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "c7a0cce4e7e0b519"
---

# 数据分析 Agent · 多平台数据规范

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** `content/analytics/` — 见 [README](../../../content/analytics/README.md)
- **Path:** `agents/09-data-analytics/DATA-NEEDS.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **统一仓库**: `content/analytics/` — 见 [README](../../../content/analytics/README.md)
- **Pipeline（自动读 → 算分 → 下一题清单）**: ```bash
- **没有数据时**: 只输出「未验证」假设题；**禁止** 声称阅读/转化一定高。
- **与 IP 其他 Agent**: - **01**：支柱定义 · **04**：Brief + `evaluate` · **00 Manager**：派活与 PASS


---

## L2 正文

# 数据分析 Agent · 多平台数据规范

## 统一仓库

`content/analytics/` — 见 [README](../../../content/analytics/README.md)

| 平台 | 规范文件 | Canonical CSV |
|------|----------|-----------------|
| 小红书 | 本节 below | `xiaohongshu/notes.csv` |
| Instagram | 本节 below | `instagram/posts.csv` |
| YouTube | 本节 below | `youtube/videos.csv` |

示例（可提交 Git）：`*.example.csv`  
真实导出（含隐私）：`notes.csv` / `posts.csv` / `videos.csv`（建议 gitignore，仅本地）


## Pipeline（自动读 → 算分 → 下一题清单）

```bash
bash scripts/analytics-pipeline.sh          # 需已 import CSV
bash scripts/analytics-pipeline.sh --demo   # 用 example 数据试跑
```

产出：

- `content/analytics/derived/summary-YYYY-MM-DD.json`
- `content/analytics/derived/next-topics-YYYY-MM-DD.md` → 交 **04 Topic Manager**

## 没有数据时

只输出「未验证」假设题；**禁止** 声称阅读/转化一定高。

## 与 IP 其他 Agent

- **01**：支柱定义 · **04**：Brief + `evaluate` · **00 Manager**：派活与 PASS