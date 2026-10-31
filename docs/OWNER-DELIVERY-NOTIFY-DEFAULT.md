---
context_version: "2026-10-30-l012"
repo_path: "docs/OWNER-DELIVERY-NOTIFY-DEFAULT.md"
goal: "Owner 交付默认 · PASS 即闭环 · HTML 通知（2026-10-28 · Owner 授权）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "4e6d1d6853d3a30e"
---

# Owner 交付默认 · PASS 即闭环 · HTML 通知（2026-10-28 · Owner 授权）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **一句话：** Brief **Owner Gate PASS**（或 deep/campaign 闭合 PASS）= **CEO 流程结束**；**不**等 Owner 回复、**不**为 routine 写 `OWNER-HANDOFF.md` 勾选单。Owner **日常通知** = 当日 **`OWNER-XHS-FILTER-DELIVERA
- **Path:** `docs/OWNER-DELIVERY-NOTIFY-DEFAULT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **1. 派活记录字段（Agent Must）**: | 字段 | routine Brief Gate PASS | 例外（才「交 Owner：是」） |
- **2. Owner 时间（设计边界）**: | 环节 | Owner |
- **3. HTML 刷新 + 浏览器弹出（Must）**: - 默认 **`CEO_OWNER_HTML_REFRESH=1`**：deep/campaign/autopilot（PASS）/owner-gate（PASS）后跑 `bash scripts/r…
- **4. OWNER-HANDOFF.md（模板）**: - **仅** gold / 战略裁决 / Owner 当轮明确要求时使用 [`content/evolution/_template/OWNER-HANDOFF.md`](../content/ev…
- **5. 工作流测试 · 第二轮（Must · 无需 Owner 确认）**: Brief 全链路测试 PASS 后：**自动** `bash scripts/ceo-workflow-test-round2-finish.sh` → campaign → 刷新 HTML → 浏…
- **6. 相关**: - [CEO-AUTO-QA-LOOP.md](./CEO-AUTO-QA-LOOP.md) · [WORKFLOW-AUTOMATION-MATRIX.md](./WORKFLOW-AUTOMATI…


---

## L2 正文

# Owner 交付默认 · PASS 即闭环 · HTML 通知（2026-10-28 · Owner 授权）

> **一句话：** Brief **Owner Gate PASS**（或 deep/campaign 闭合 PASS）= **CEO 流程结束**；**不**等 Owner 回复、**不**为 routine 写 `OWNER-HANDOFF.md` 勾选单。Owner **日常通知** = 当日 **`OWNER-XHS-FILTER-DELIVERABLE-<YYYY-MM-DD>.html`**。Owner **仍必做**：App **发帖** + **CSV** → `content/analytics/inbox/`。

## 1. 派活记录字段（Agent Must）

| 字段 | routine Brief Gate PASS | 例外（才「交 Owner：是」） |
|------|-------------------------|----------------------------|
| **Owner Gate** | PASS | FAIL 或 PASS 但见右列 |
| **打回轮次 n/3** | 实际轮次 | — |
| **交 Owner** | **否** | gold · 战略红线 · 不可逆（Drive 覆盖/代发/ mass 私信）· Gate **3 轮仍 FAIL** 裁决 |
| **Owner 通知** | **是（HTML）** | 路径：`content/evolution/00-manager/ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-<date>.html` |

**禁止：** 把 PASS 稿配上「请你确认可发」当第二道 Gate；**禁止** routine 落盘 `OWNER-HANDOFF.md` 并等待 Owner 勾选。

## 2. Owner 时间（设计边界）

| 环节 | Owner |
|------|--------|
| 跑 verify / evaluate / gate | **0**（Agent） |
| 回复 chat 才算流程继续 | **0**（PASS 已闭合） |
| 打开 HTML 看一眼 | **可选** |
| 小红书/IG 发帖 + 回填 Brief | **Must** |
| 导出 CSV | **Must**（有数据时） |

## 3. HTML 刷新 + 浏览器弹出（Must）

- 默认 **`CEO_OWNER_HTML_REFRESH=1`**：deep/campaign/autopilot（PASS）/owner-gate（PASS）后跑 `bash scripts/refresh-owner-notify-html.sh`。
- **刷新成功后 Must 自动** `bash scripts/open-owner-xhs-deliverable-html.sh`（macOS 默认浏览器打开 FILTER HTML；**不是**在 Cursor 里点开 `.html` 看源码）。
- 新 Owner 指定稿：`CEO_OWNER_HTML_HASH=#owner-latest` → 打开页时 **自动弹出**「Owner 指定新稿」全文层（见 `build-owner-xhs-report-html.py`）。
- 关闭浏览器打开：`CEO_OWNER_HTML_OPEN=0`。
- deep 与 campaign 并行时 campaign **仍 SKIP** HTML（由 deep Phase E 刷新）。
- 关闭刷新：`CEO_OWNER_HTML_REFRESH=0`。

**Agent Must（Cursor 会话）：** delivery PASS 后除跑上述脚本外，在 chat **Must** 按 [`OWNER-CHAT-DELIVERY-FORMAT.md`](./OWNER-CHAT-DELIVERY-FORMAT.md) 附 **01–12 Agent 全表 + 非全员并行说明 + HTML file:// URI**；若 Owner 仍没看到浏览器，再跑 `open-owner-xhs-deliverable-html.sh`。

## 4. OWNER-HANDOFF.md（模板）

- **仅** gold / 战略裁决 / Owner 当轮明确要求时使用 [`content/evolution/_template/OWNER-HANDOFF.md`](../content/evolution/_template/OWNER-HANDOFF.md)。
- 不是 routine 交付物。

## 5. 工作流测试 · 第二轮（Must · 无需 Owner 确认）

Brief 全链路测试 PASS 后：**自动** `bash scripts/ceo-workflow-test-round2-finish.sh` → campaign → 刷新 HTML → 浏览器打开。见 [CEO-WORKFLOW-TEST-SOP.md](./CEO-WORKFLOW-TEST-SOP.md)。

## 6. 相关

- [CEO-AUTO-QA-LOOP.md](./CEO-AUTO-QA-LOOP.md) · [WORKFLOW-AUTOMATION-MATRIX.md](./WORKFLOW-AUTOMATION-MATRIX.md) · `integration/IMPORTANT.md`