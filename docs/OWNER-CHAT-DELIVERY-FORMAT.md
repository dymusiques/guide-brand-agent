---
context_version: "2026-10-30-l012"
repo_path: "docs/OWNER-CHAT-DELIVERY-FORMAT.md"
goal: "Owner · Cursor 会话交付格式（Must · 2026-10-30）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "93169cf44b4c3c08"
---

# Owner · Cursor 会话交付格式（Must · 2026-10-30）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **每次弹出 HTML / 交付结果**（含 `refresh-owner-notify-html` · `open-owner-xhs-deliverable-html`）时，**同一条 Cursor 回复 Must 含下列四块**。  
> 并行说明：[CEO-AGENT-ROSTER-AND-PARALLELISM.md](./CEO-AGENT-
- **Path:** `docs/OWNER-CHAT-DELIVERY-FORMAT.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **0. 并行一问一答（Must · 置顶）**: **Must 用两句话回答 Owner：**
- **1. 01–12 Agent 全表（Must · 不可只列「跑过的」）**: | ID | Agent | 状态 | 本任务用的能力 | 结果 | 与其它 Agent 并行？ |
- **2. 本次实际执行的步骤（时间线）**: ```text
- **3. HTML 结果（Must）**: - **URI：** `file://…/OWNER-XHS-FILTER-DELIVERABLE-<YYYY-MM-DD>.html#owner-latest`
- **4. 禁止**: - 只弹 HTML 不附 **01–12 全表 + 并行说明**


---

## L2 正文

# Owner · Cursor 会话交付格式（Must · 2026-10-30）

> **每次弹出 HTML / 交付结果**（含 `refresh-owner-notify-html` · `open-owner-xhs-deliverable-html`）时，**同一条 Cursor 回复 Must 含下列四块**。  
> 并行说明：[CEO-AGENT-ROSTER-AND-PARALLELISM.md](./CEO-AGENT-ROSTER-AND-PARALLELISM.md)

## 0. 并行一问一答（Must · 置顶）

**Must 用两句话回答 Owner：**

1. **是否调用了全部 12 个 Agent？** → 默认 **否**；列出 `invoked N/12`。  
2. **是否全员能力并行才出现这个 HTML？** → 默认 **否**；主链 **串行** CEO→GM→CEO（`parallelism.mode = sequential_ceo_gm_chain`）。

全表见下节 **01–12 roster**。

## 1. 01–12 Agent 全表（Must · 不可只列「跑过的」）

| ID | Agent | 状态 | 本任务用的能力 | 结果 | 与其它 Agent 并行？ |
|----|-------|------|----------------|------|---------------------|
| 00 | … | invoked / **skipped** | … | PASS/FAIL/— | **否**（串行链） |
| 01 | … | … | … | … | 否 |
| … | … | … | … | … | … |
| 12 | … | … | … | … | 否 |

**权威 JSON：** `content/evolution/00-manager/ceo-inbox/CEO-RUN-MANIFEST-latest.json` → `roster[]` + `parallelism`

**Agent 若无跑 full execution：** 仍 Must 按 [CEO-AGENT-ROSTER-AND-PARALLELISM.md](./CEO-AGENT-ROSTER-AND-PARALLELISM.md) 填全表（skipped 也要写）。

## 2. 本次实际执行的步骤（时间线）

```text
1. recover → 2. router → 3. six-case → 4. triple-eval → 5. stress×2 → 6. autopilot → 7. HTML open
```

来自 manifest `steps[]`。

## 3. HTML 结果（Must）

- **URI：** `file://…/OWNER-XHS-FILTER-DELIVERABLE-<YYYY-MM-DD>.html#owner-latest`
- **Must：** `open-owner-xhs-deliverable-html.sh` + 可用时 `open_resource` 同一 URI

## 4. 禁止

- 只弹 HTML 不附 **01–12 全表 + 并行说明**  
- 暗示「所有 Agent 都跑了/都并行」而不写 invoked 数  
- 只写「已跑 autopilot」