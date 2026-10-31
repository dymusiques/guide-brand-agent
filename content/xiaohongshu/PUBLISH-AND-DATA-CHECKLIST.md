---
context_version: "2026-10-30-l012"
repo_path: "content/xiaohongshu/PUBLISH-AND-DATA-CHECKLIST.md"
goal: "认知期 · 发布与数据回填（Owner 操作 · #5）"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "98ea85e56676c3e4"
---

# 认知期 · 发布与数据回填（Owner 操作 · #5）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** Agent **不能** 替你在 App 内发帖；本清单 = **#5 待办** 的可执行步骤。
- **Path:** `content/xiaohongshu/PUBLISH-AND-DATA-CHECKLIST.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **发布顺序建议**: | 顺序 | Brief 文件 | 建议发完间隔 |
- **CSV 回填（ ideally · 不阻塞发布）**: 1. 小红书创作者后台 → 笔记数据 → 导出或复制到表格
- **15 天快检提醒**: 从 **第 1 篇深度发布日** 起算 15 天：强链接为主，涨粉 ~100 参考。


---

## L2 正文

# 认知期 · 发布与数据回填（Owner 操作 · #5）

Agent **不能** 替你在 App 内发帖；本清单 = **#5 待办** 的可执行步骤。

## 发布顺序建议

| 顺序 | Brief 文件 | 建议发完间隔 |
|------|------------|--------------|
| 1 | `2026-10-17-discovery-01-irreplaceability-brief.md` | 先发 |
| 2 | `2026-10-17-discovery-02-narrative-not-ads-brief.md` | ≥7 天 |
| 3 | `2026-10-17-discovery-03-professional-trust-brief.md` | ≥7 天 |
| 4 | `2026-10-17-discovery-04-open-close-brief.md` | ≥7 天；**可考虑置顶** |

每篇：按 Brief 写正文 → 发布 → 在 Brief **`## 发布状态`** 填：`状态: 已发布`、`发布日期: YYYY-MM-DD`、`笔记链接:` → 跑 `bash scripts/manager-dashboard.sh` 刷新 CEO 视图。

## CSV 回填（ ideally · 不阻塞发布）

1. 小红书创作者后台 → 笔记数据 → 导出或复制到表格  
2. 保存为 `content/analytics/inbox/xiaohongshu-YYYY-MM-DD.csv`  
3. 运行：

```bash
bash scripts/analytics-fetch.sh
bash scripts/analytics-pipeline.sh
```

4. 读 `content/analytics/derived/next-topics-*.md` → 15 天快检对照 [OPERATING-PLAN](../marketing/discovery-phase-OPERATING-PLAN.md)

**无 CSV：** 仍可做 15 天快检（后台看收藏/私信/涨粉）。

## 15 天快检提醒

从 **第 1 篇深度发布日** 起算 15 天：强链接为主，涨粉 ~100 参考。