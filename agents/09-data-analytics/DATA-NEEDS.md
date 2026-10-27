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

---

## 小红书 · 每笔记一行

| 字段 | 说明 |
|------|------|
| `note_id` | 链接或 ID |
| `publish_date` | 发布日期 |
| `title` | 标题 |
| `pillar` | 艺术专业 / 跨界品牌 / AI×数字藏品 |
| `impressions`, `views`, `likes`, `collects`, `comments`, `shares` | 后台指标 |
| `follows_from_note` | 涨粉（若有） |
| `dm_count`, `dm_keywords` | **强链接核心** · 认知期 `dm_count` = **品牌向**私信（聊聊/合作/品牌），**不含**约课；约课写在 `dm_keywords`（如 `约课×3`）· 见 [signal-baseline](../../content/marketing/discovery-phase-signal-baseline.md) |
| `aligned_at_publish`, `brief_path` | 可选 · 无 Brief 的已发笔记 → `content/xiaohongshu/published-notes-index.md` |
| `cover_ctr_pct`, `avg_watch_sec`, `completion_rate_pct`, `exit_2s_rate_pct`, `detail_source` | 单篇「数据明细表」合并（有则填） |

## Instagram · 每帖一行

| 字段 | 说明 |
|------|------|
| `post_id`, `publish_date`, `title` | 必填 |
| `caption_snippet` | 可选摘要 |
| `pillar` | 与 IP 支柱对齐 |
| `impressions`, `reach`, `likes`, `comments`, `saves`, `shares` | 指标 |
| `follows_from_post`, `dm_count`, `dm_keywords` | 强链接 |
| `brief_path` | 可选 |

## YouTube · 每视频一行

| 字段 | 说明 |
|------|------|
| `video_id`, `publish_date`, `title`, `pillar` | 必填 |
| `views`, `watch_time_hours`, `likes`, `comments`, `shares` | 指标 |
| `subscribers_gained` | 订阅增量 |
| `dm_or_email_inquiries`, `inquiry_keywords` | 强链接近似 |
| `brief_path` | 可选 |

---

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
