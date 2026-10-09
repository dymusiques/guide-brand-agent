# 数据分析 Agent · 你需要提供什么

有了下列数据，才能 **客观** 比较笔记好坏，并给 **下一选题** 建议（仍须 Topic Manager + `evaluate --brief`）。

## 建议每条笔记一行（CSV / Sheet / Markdown 表）

| 字段 | 说明 |
|------|------|
| `note_id` 或链接 | 小红书笔记 URL / 后台 ID |
| `publish_date` | 发布日期 |
| `title` | 标题（对应 Brief `subject`） |
| `pillar` | 支柱 1/2/3 或标签（艺术专业 / 跨界品牌 / AI×数字藏品） |
| `impressions` | 曝光（若后台有） |
| `views` | 阅读 |
| `likes` | 赞 |
| `collects` | 收藏 |
| `comments` | 评论 |
| `shares` | 分享（若有） |
| `follows_from_note` | 来自该笔记的粉丝增量（若有） |
| `dm_count` | 私信数（**强链接核心**，可手工记） |
| `dm_keywords` | 私信关键词统计（合作 / 案例 / 共建 / 评估） |
| `aligned_at_publish` | 发布时 evaluate 是否 true（可选） |
| `brief_path` | Git 中 Brief 路径 |

## 汇总层（每周 / 每月）

- 粉丝总数、净增（与 1700→5000 目标对照）
- 哪类 **pillar** / **CTA 关键词** 带来 DM 更多
- 哪类标题点击高但 DM 低（vanity vs 强链接）

## 存储建议（Git）

`content/xiaohongshu/analytics/YYYY-MM-notes.csv`（不含隐私私信正文，只含计数）

## 没有数据时

Analytics Agent **只能** 给基于 IP 的 **假设选题**，必须标注「未验证」；**不能** 声称某题阅读/转化一定高。
