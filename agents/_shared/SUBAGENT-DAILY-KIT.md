---
context_version: "2026-10-30-l012"
repo_path: "agents/_shared/SUBAGENT-DAILY-KIT.md"
goal: "日更 Sub-Agent 共用套件 · Baseline → 6 Test → Challenge → Evaluator"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "9147535487ab3c4c"
---

# 日更 Sub-Agent 共用套件 · Baseline → 6 Test → Challenge → Evaluator

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **编制：** **10 · 11 · 12** 三个日更 GM，**均**走本套件，**统一汇报 00 CEO**。  
> **调度：** `scripts/run-daily-gm-trio.sh`（后台 daily cycle 09:00 调用）。
- **Path:** `agents/_shared/SUBAGENT-DAILY-KIT.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **共用四步（每个 GM Must）**: | 步 | 名称 | 产物 |
- **路径**: ```text
- **CEO**: - 收三份 `GM-REPORT.md` → `content/evolution/00-manager/ceo-inbox/daily-gm-summary-<date>.md`


---

## L2 正文

# 日更 Sub-Agent 共用套件 · Baseline → 6 Test → Challenge → Evaluator

> **编制：** **10 · 11 · 12** 三个日更 GM，**均**走本套件，**统一汇报 00 CEO**。  
> **调度：** `scripts/run-daily-gm-trio.sh`（后台 daily cycle 09:00 调用）。

## 共用四步（每个 GM Must）

| 步 | 名称 | 产物 |
|----|------|------|
| 1 | **Baseline** | `reference/gold.md` 或 rubric · Owner IP Brief 摘要 intake |
| 2 | **6 Test** | `bash scripts/verify-agent-fused.sh --agent NN --with-artifacts`（trio 日更后由 `verify-daily-gm-trio.sh` 一次跑 10+11+12） |
| 3 | **Challenge** | 小红书 Brief：`run-xhs-brief-adversarial-challenge.py` → `challenge/<slug>-challenge.md`；日更 GM：`challenge-log.md` / `CEO-REROUTE.md` · [BRIEF-ADVERSARIAL-CHALLENGE.md](./BRIEF-ADVERSARIAL-CHALLENGE.md) |
| 4 | **Evaluator** | 结构化评分 + `metrics.jsonl` · 可选编辑距离 |

## 路径

```text
content/evolution/<10|11|12>-<name>/<YYYY-MM-DD>/ 
  intake/ · reference/ · versions/ · metrics.jsonl · GM-REPORT.md
```

## CEO

- 收三份 `GM-REPORT.md` → `content/evolution/00-manager/ceo-inbox/daily-gm-summary-<date>.md`
- **12** 产出 Owner 可读：`content/daily-brief/YYYY-MM-DD-owner-daily-brief.md`