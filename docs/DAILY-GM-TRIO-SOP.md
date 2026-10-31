---
context_version: "2026-10-30-l012"
repo_path: "docs/DAILY-GM-TRIO-SOP.md"
goal: "日更 GM 三件套 · 10 / 11 / 12（CEO 下辖）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "2579cabfebd6fc3f"
---

# 日更 GM 三件套 · 10 / 11 / 12（CEO 下辖）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner 需求（2026-10-27）：** 24h 自动：Artist 对标评分+时间线 · IP evaluate+challenge · **每日 Brief**；三 GM **均含** baseline · 6 test · challenge · evaluator。
- **Path:** `docs/DAILY-GM-TRIO-SOP.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **架构**: ```text
- **自动跑条件**: 1. `bash scripts/setup-background-goal-evolution.sh`
- **Owner 要读的**: `content/daily-brief/<today>-owner-daily-brief.md`
- **Artist 对标名单**: `content/ip-research/artist-watchlist.json` — **Agent 维护**（**艺术门类内各专业均可**，不限定细分专业）· 见 [content/ip-re…
- **Verify**: `bash scripts/verify-daily-gm-trio.sh`（**10+11+12** L1 六 case + 当日 artifact · 见 [VERIFY-AGENT-FUSED.…
- **局限（诚实）**: - GM10 **Gemini 公共知识 + 你给的 urls**；无 url 时 **不可** 保证等同深度 desktop 调研


---

## L2 正文

# 日更 GM 三件套 · 10 / 11 / 12（CEO 下辖）

> **Owner 需求（2026-10-27）：** 24h 自动：Artist 对标评分+时间线 · IP evaluate+challenge · **每日 Brief**；三 GM **均含** baseline · 6 test · challenge · evaluator。

## 架构

```text
00 CEO
 ├── 01–09 职能 GM（写稿/verify 主链）
 └── 日更三 GM（后台 daily cycle 09:00）
      ├── 10 Artist Benchmark  ← 网上对标 · 借鉴分 · 时间线
      ├── 11 IP Daily Evaluator ← rollups · 红队 2 条 · hygiene
      └── 12 Owner Daily Brief ← 汇总给 Owner 的每日 brief
```

## 自动跑条件

1. `bash scripts/setup-background-goal-evolution.sh`
2. Launcher 常驻：`../../.venv/bin/process-launcher start --config config/dba-brand-agent.yaml`
3. 每日 cycle 内 **`run-daily-gm-trio.sh`**（与 verify-goals 等同批）

**手动/Debug：** `bash scripts/run-daily-gm-trio.sh`

## Owner 要读的

`content/daily-brief/<today>-owner-daily-brief.md`

## Artist 对标名单

`content/ip-research/artist-watchlist.json` — **Agent 维护**（**艺术门类内各专业均可**，不限定细分专业）· 见 [content/ip-research/README.md](../content/ip-research/README.md)  
Owner 若有指定名字，口语一句即可，Agent 写入 watchlist。

## Verify

`bash scripts/verify-daily-gm-trio.sh`（**10+11+12** L1 六 case + 当日 artifact · 见 [VERIFY-AGENT-FUSED.md](VERIFY-AGENT-FUSED.md)）

## 局限（诚实）

- GM10 **Gemini 公共知识 + 你给的 urls**；无 url 时 **不可** 保证等同深度 desktop 调研
- **写小红书 Brief 正文** 仍走 **04 + Cursor**；12 是 **决策型 daily brief**，不是自动发笔记