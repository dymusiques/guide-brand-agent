---
context_version: "2026-10-30-l012"
repo_path: "agents/00-manager/CEO-DISPATCH-SOP.md"
goal: "CEO 派活 SOP · 模板"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "b5d023f420eb21eb"
---

# CEO 派活 SOP · 模板

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > 原则来源：[docs/CEO-MANAGER-OPERATING-STANDARDS.md](../../docs/CEO-MANAGER-OPERATING-STANDARDS.md)（Owner 五原则）。  
> 流程：Owner 口语目标 → **先落盘 dispatch（本模板）** → 派活 → 验收 → 记录。  
> 示范：`conten
- **Path:** `agents/00-manager/CEO-DISPATCH-SOP.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **0. 使用步骤**: **Owner 不必每次贴终端命令：** 在 Cursor 说「请 CEO 开始工作」即可 → 见 [CEO-OWNER-ONE-LINE-TRIGGERS.md](../../docs/CEO-OW…
- **GM → CEO · 六项 6-case（Must · 有 Brief 时）**: 跑 **`bash scripts/ceo-full-execution-pipeline.sh`**（内嵌 `ceo-six-case-battery` → `ceo-triple-eval-bas…
- **Manager 派活记录 · 字段（每轮 Must 输出）**: ```markdown
- **Manager 派活记录**: - 目标：（Owner 原话摘要）
- **Auto-gate / Recover 指针**: | 情形 | 动作 | 文档 |


---

## L2 正文

# CEO 派活 SOP · 模板

> 原则来源：[docs/CEO-MANAGER-OPERATING-STANDARDS.md](../../docs/CEO-MANAGER-OPERATING-STANDARDS.md)（Owner 五原则）。  
> 流程：Owner 口语目标 → **先落盘 dispatch（本模板）** → 派活 → 验收 → 记录。  
> 示范：`content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27-evening.md`  
> GM 评估改进环（Owner 图 ↔ 01–12 对照）：[docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md](../../docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md)  
> CEO 环 · 两轮串行迭代（consult SOP → … → analyze）：[CEO-DOUBLE-ITERATION-SOP.md](CEO-DOUBLE-ITERATION-SOP.md) · [docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md](../../docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md)

## 0. 使用步骤

**Owner 不必每次贴终端命令：** 在 Cursor 说「请 CEO 开始工作」即可 → 见 [CEO-OWNER-ONE-LINE-TRIGGERS.md](../../docs/CEO-OWNER-ONE-LINE-TRIGGERS.md) · 可选 `bash scripts/ceo-start-work.sh` 看状态。

1. 复制下方模板到 `content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-<YYYY-MM-DD>[-tag].md`
2. 填 North star / 战役题 / per-agent 表（**每行必须有终端验收命令**）
3. 全员派活 → `VERIFY_GOALS_SKIP_PLATFORM=0 bash scripts/run-ceo-ip-all-agents-campaign.sh`（截止交付另加 `run-ceo-deep-delivery-cycle.sh`；二者并行时用 lock / `SKIP_GEMINI`）
4. 收尾回填「结果」与 **Manager 派活记录**
5. 新增文档/脚本 → 更新 `rules/WORKSPACE.md` 索引


## GM → CEO · 六项 6-case（Must · 有 Brief 时）

跑 **`bash scripts/ceo-full-execution-pipeline.sh`**（内嵌 `ceo-six-case-battery` → `ceo-triple-eval-baseline-loop` → `ceo-double-stress` → autopilot）。  
细则：[CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md](../../docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md) · Cursor 回复：[OWNER-CHAT-DELIVERY-FORMAT.md](../../docs/OWNER-CHAT-DELIVERY-FORMAT.md)

## Manager 派活记录 · 字段（每轮 Must 输出）

```markdown
## Manager 派活记录
- 目标：（Owner 原话摘要）
- North star：（例：打造个人 IP）
- 当前步：0x · Agent 名称
- 终端：PASS/FAIL + 命令（含 failures 数 / PASS 篇数）
- Owner Gate：PASS/FAIL · 打回 n/3 · 交 Owner：是/否（routine PASS → **否**）· Owner 通知：`ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-<date>.html`
- 报告 / 日志：路径
- 新增资产：路径（文档/脚本/规则/索引）
- 未做：（未 commit / 未 sync Drive / 未发帖 / 数据未验证…）
- 下一步：…
```

## Auto-gate / Recover 指针

| 情形 | 动作 | 文档 |
|------|------|------|
| CEO 派活或改 Brief 后 | 全仓 `bash scripts/manager-xhs-briefs-auto-pipeline.sh`；单篇 `manager-ceo-auto-gate-loop.sh --brief …` | [BRIEF-AUTO-GATE-PIPELINE](../../docs/BRIEF-AUTO-GATE-PIPELINE.md) · [BRIEF-ADVERSARIAL-CHALLENGE](../_shared/BRIEF-ADVERSARIAL-CHALLENGE.md) |
| 交 Owner 前 | `bash scripts/manager-ceo-owner-gate.sh --brief …` | [CEO-AUTO-QA-LOOP](../../docs/CEO-AUTO-QA-LOOP.md) |
| Gate FAIL | 写 `CEO-REROUTE` → GM 同会话改 v(N+1) → 再 gate（≤3 轮）；**不**把 FAIL 稿交 Owner | 同上 |
| 截止交付 | `bash scripts/run-ceo-deep-delivery-cycle.sh`（禁止仅跑 `ceo-xhs-ip-filter-batch.py`） | [CEO-OWNER-DEADLINE-DELIVERY](../../docs/CEO-OWNER-DEADLINE-DELIVERY.md) |
| 中断 / 阻塞 / FAIL / 跑错 | **自动** `bash scripts/ceo-auto-recover-blocked.sh` → 读 `ceo-inbox/ceo-auto-recover-latest.md` → 按需 nohup 重跑；**勿问 Owner 要不要重跑** | [CEO-AUTO-RECOVER-AND-RETRY](../../docs/CEO-AUTO-RECOVER-AND-RETRY.md) |
| 交班 / 大改后 | `bash scripts/verify-handoff.sh` | [AGENT-TAKEOVER](../../docs/AGENT-TAKEOVER.md) |