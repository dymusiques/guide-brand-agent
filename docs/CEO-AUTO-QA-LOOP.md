---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-AUTO-QA-LOOP.md"
goal: "CEO 自动纠错 · Owner 门控（默认不让 Owner 逐条验）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "e5c27ec4501e42d3"
---

# CEO 自动纠错 · Owner 门控（默认不让 Owner 逐条验）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** - 层级：[IP-MANAGEMENT-HIERARCHY.md](./IP-MANAGEMENT-HIERARCHY.md)
- 指挥链：[agents/00-manager/AUTO-WORKFLOW.md](../agents/00-manager/AUTO-WORKFLOW.md)
- Collector/Evaluator：[agents/_sha
- **Path:** `docs/CEO-AUTO-QA-LOOP.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > **Owner 要求（2026-10-27）：** 按目标 **自动产出** → **CEO 自动验收/纠错** → 不过则 **打回部门 GM 再 evaluate**；…
- **章节锚点**: - **闭环（Produce → CEO Gate → Owner 或 Reroute）**: ```text
- **相关**: - 层级：[IP-MANAGEMENT-HIERARCHY.md](./IP-MANAGEMENT-HIERARCHY.md)


---

## L2 正文

# CEO 自动纠错 · Owner 门控（默认不让 Owner 逐条验）

> **Owner 要求（2026-10-27）：** 按目标 **自动产出** → **CEO 自动验收/纠错** → 不过则 **打回部门 GM 再 evaluate**；**不要**每轮都让 Owner 跑 verify。**交给 Owner 的任何交付物，Agent 必须先自验一遍**；只有需要 Owner 决策时才来确认。

> **Owner 输入（2026-10-27）：** 怎么说都行 — **内部** Gate/提示词/Evaluator 负责抬高质量；**不** 要求 Owner 公式化 prompt。见 [OWNER-INPUT-PRINCIPLES.md](./OWNER-INPUT-PRINCIPLES.md)。


## 闭环（Produce → CEO Gate → Owner 或 Reroute）

```text
Owner 目标 + 资料
    → CEO 派 GM（slug · G-* · 验收命令清单）
    → GM：v0 → Evaluator → GM-REPORT（自报 PASS 前须本部门命令全绿）
    → CEO：bash scripts/manager-ceo-owner-gate.sh …
         ├─ PASS → **流程结束** · 刷新 `OWNER-XHS-FILTER-DELIVERABLE-<date>.html`（见 OWNER-DELIVERY-NOTIFY-DEFAULT）
         └─ FAIL → CEO-REROUTE.md → GM 改 v(N+1) → 再 Gate（循环）
    → 达上限仍 FAIL → 只向 Owner 报 **阻塞项 + 已跑命令输出**（仍不甩未验稿）
```

**打回上限（默认）：** `CEO_GATE_MAX_ROUNDS=3`（Agent 自计轮次；第 4 轮仍 FAIL 才 escalation）。可在 Owner 当轮指定覆盖。


## CEO 打回 GM（CEO-REROUTE）

Gate 或 GM-REPORT 与终端不一致时，CEO 在同 slug 目录写（或更新）：

`content/evolution/<dept-slot>/<slug>/CEO-REROUTE.md`

模板：[`content/evolution/_template/CEO-REROUTE.md`](../content/evolution/_template/CEO-REROUTE.md)

GM **Must：** 读 REROUTE → 出 v(N+1) → 重跑 REROUTE 里列出的命令 → 更新 GM-REPORT → 通知 CEO 复 gate。


## Agent 每轮输出（CEO 派活记录扩展）

除 AUTO-WORKFLOW 派活记录外，**交 Owner 前** 增加一行：

```markdown
- Owner Gate：PASS/FAIL · `manager-ceo-owner-gate.sh …` · 打回轮次 n/3
- 交 Owner：是/否（否则说明仍在 GM 纠错环）
```

---

## 相关

- 层级：[IP-MANAGEMENT-HIERARCHY.md](./IP-MANAGEMENT-HIERARCHY.md)
- 指挥链：[agents/00-manager/AUTO-WORKFLOW.md](../agents/00-manager/AUTO-WORKFLOW.md)
- Collector/Evaluator：[agents/_shared/COLLECTOR-EVALUATOR.md](../agents/_shared/COLLECTOR-EVALUATOR.md)