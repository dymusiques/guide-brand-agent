---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-AGENT-ROSTER-AND-PARALLELISM.md"
goal: "Agent 调用清单 · 并行说明（Must · Owner 2026-10-30）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "c125d634fe62750e"
---

# Agent 调用清单 · 并行说明（Must · Owner 2026-10-30）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **每次弹出 HTML / 交付结果时**，Cursor 回复 **Must** 附 **01–12 全表**（见 [`OWNER-CHAT-DELIVERY-FORMAT.md`](./OWNER-CHAT-DELIVERY-FORMAT.md)）并 **明确回答：是否全员并行**。
- **Path:** `docs/CEO-AGENT-ROSTER-AND-PARALLELISM.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **1. 诚实结论（默认 · 单篇小红书 CEO full execution）**: | 问题 | 答案 |
- **2. 全仓 Agent 名册（对照用）**: | ID | 目录 | 典型能力（集成层） | 单篇 XHS full execution |
- **3. 机器产物**: `run_ceo_full_execution.py` 结束写入：


---

## L2 正文

# Agent 调用清单 · 并行说明（Must · Owner 2026-10-30）

> **每次弹出 HTML / 交付结果时**，Cursor 回复 **Must** 附 **01–12 全表**（见 [`OWNER-CHAT-DELIVERY-FORMAT.md`](./OWNER-CHAT-DELIVERY-FORMAT.md)）并 **明确回答：是否全员并行**。

## 1. 诚实结论（默认 · 单篇小红书 CEO full execution）

| 问题 | 答案 |
|------|------|
| **是否调用了全部 12 个 Agent？** | **否。** 常规路径调用 **00 + 01 + 04 + 05 + 08（集成 verify）**；02/03/06/07/09/10/11/12 **本任务未派活则标 `skipped`**。 |
| **是否「全员能力并行」才产出 HTML？** | **否。** 主链是 **CEO 串行指挥链**（GM 顺序 → CEO 复核 → HTML）；**不是** 12 Agent 同时并行写稿。 |
| **何时才接近「全员」？** | Owner 触发 **`run-ceo-ip-all-agents-campaign.sh`** / 深交付 / 日更 trio（10–12）等 **战役**；仍多为 **脚本顺序 + 少量 lock 协调**，非 12 路并行 Brief。 |
| **Brief 写稿能否并行？** | **禁止** 同一 slug 多 Agent 并行写（AUTO-WORKFLOW）；调研 Task 并行 **不** 替代 GM 步序。 |

## 2. 全仓 Agent 名册（对照用）

| ID | 目录 | 典型能力（集成层） | 单篇 XHS full execution |
|----|------|-------------------|-------------------------|
| 00 | 00-manager | recover · dispatch · manifest · HTML 门控 | **invoked** |
| 01 | 01-personal-ip | `evaluate_personal_ip.py` · fused 01 | **invoked** |
| 02 | 02-business-brand | SWOT · `evaluate-business-brand` | skipped |
| 03 | 03-marketing-strategy | campaign · `evaluate-marketing-campaign` | skipped |
| 04 | 04-xhs-topic-manager | pitfalls · 长稿 · gate · GM-REPORT | **invoked** |
| 05 | 05-xhs-kernel | L1/kernel 6-case · fused 05 | **invoked** |
| 06 | 06-xhs-content-pipeline | `verify-xhs-content-dir` | skipped（批量时 invoked） |
| 07 | 07-brand-visual | Canva / 封面 | skipped（除非 Owner 要视觉） |
| 08 | 08-platform-integration | `verify-integration` · gdocs | **invoked**（集成 6-case） |
| 09 | 09-data-analytics | analytics pipeline · 选题 | skipped（无 CSV 时） |
| 10 | 10-artist-benchmark | fused 10 · Artist DB | skipped（非 campaign） |
| 11 | 11-ip-daily-evaluator | fused 11 · daily eval | skipped |
| 12 | 12-owner-daily-brief | fused 12 · Owner 汇总 | skipped |

状态枚举：**`invoked`** · **`skipped`**（本任务未派）· **`not_applicable`**

## 3. 机器产物

`run_ceo_full_execution.py` 结束写入：

- `content/evolution/00-manager/ceo-inbox/CEO-RUN-MANIFEST-latest.json`  
  - 字段：`roster[]` · `parallelism.all_agents_invoked` · `parallelism.mode`

Agent 交付 HTML 时 **Must 把 roster 表贴进 Cursor chat**（可读 JSON 或 Markdown 表）。