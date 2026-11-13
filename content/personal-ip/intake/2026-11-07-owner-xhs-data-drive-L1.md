---
context_version: "2026-11-07-owner-xhs-data"
repo_path: "content/personal-ip/intake/2026-11-07-owner-xhs-data-drive-L1.md"
goal: "Owner 账号后台数据 · Drive 真源 + Git 快照"
openwebui_route: "rag_l1"
cursor_route: "read"
---

# L1 · 我的小红书数据（Owner 后台 · Drive）

## 裁定

- **真相在 Drive，不是 chat 附件。** [文件夹 `1kFYScZvFgd52983gK0gItIuRq0-43WyR`](https://drive.google.com/drive/folders/1kFYScZvFgd52983gK0gItIuRq0-43WyR?usp=drive_link)
- **机器配置：** `integration/handoff/owner-xhs-data-drive.json`
- **清单（Agent 每次同步后更新）：** `_raw/owner-xhs-data/drive-listing-latest.json`
- **Git 可提交索引：** `content/analytics/xiaohongshu/DATA-MANIFEST.json` · `notes-snapshot-*.json`
- **与「小红书 IP 方法论库」分开：** 后者是 `1SrD2n_…`（380+ 份别人写的运营 PDF）；**本文件夹只放你账号导出。**

## Owner 更新 ritual

1. 发完视频/笔记 → 创作者后台导出 xlsx → 丢进 **My Drive · 我的小红书数据**（建议含**排序后全量**「笔记列表明细表」+ 单篇「数据明细表」）。
2. **不必再下口令。** 在 Cursor 附上文件或仅更新 Drive 后继续聊，Agent **Must 自动**跑 `bash scripts/xhs-owner-data-auto-sync.sh`（Drive 场景先 `sync-owner-xhs-data-from-drive.sh`）。
3. Agent 读本机 `小红书笔记数据汇总-全指标-*.xlsx` + `derived/xhs-data-strategy-*.md`，再改 Brief/队列。

## Agent Must

| 任务 | 读什么 |
|------|--------|
| 选题/排序/钩子 | `content/analytics/derived/xhs-data-strategy-*.md` + manifest |
| 对标 pivot IP | `integration/handoff/owner-benchmark-growth-paths.json` · `owner-era-benchmark-2024-2026-creators.json` |
| 三平台方向 | `content/evolution/00-manager/ceo-inbox/2026-11-05-owner-ip-ecosystem-strategy.md` |
| 平台规则背书 | `2026-11-03-xhs-drive-corpus-L1.md`（screen 方法论库，**非**个人数据） |

## 内容类型（2026-11-07 Drive 清点）

| 类型 | 约数量 | 说明 |
|------|--------|------|
| 单篇「数据明细表」xlsx | 23 | 标题=笔记名；指标+完播/CTR |
| 笔记列表明细表 / 笔记链接回填表 | 各 1 | 全账号列表 + 链接 |
| 近 30 日 互动/发布/涨粉/观看 | 各 1 | 账号级趋势 |

**文案正文** 在 `content/xiaohongshu/` Brief 与 `published-notes-index.md`；xlsx **不含长正文**，对比时用 **标题 + 数据 + 已发 Brief**。

## 同步命令（Owner 日常可不开终端）

| 场景 | Agent / 脚本 |
|------|----------------|
| Drive 已更新 | `bash scripts/sync-owner-xhs-data-from-drive.sh`（内建 auto-sync） |
| chat 附 Downloads xlsx | `bash scripts/xhs-owner-data-auto-sync.sh --from-dir <路径>` |
| 仅重算合并 | `bash scripts/xhs-owner-data-auto-sync.sh` |

配置：`integration/handoff/owner-xhs-data-drive.json` → `agent_auto_sync`

```bash
# 只拉 Drive 清单、不跑 pipeline：
SKIP_ANALYTICS_PIPELINE=1 bash scripts/sync-owner-xhs-data-from-drive.sh
```

## 纳入 CEO 背书 catalog

本文件夹已写入 `integration/handoff/ceo-drive-corpus-folders.json`；跑 `refresh-ceo-drive-catalog.py` 后 screen 可检索文件名（例如「近30日涨粉」）。
