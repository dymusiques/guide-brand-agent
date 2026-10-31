---
context_version: "2026-10-30-l012"
repo_path: "docs/BRIEF-AUTO-GATE-PIPELINE.md"
goal: "Brief 自动验收管线 · 无人值守（Must）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "5724074f76240f3a"
---

# Brief 自动验收管线 · 无人值守（Must）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner（2026-10-27）：** 交稿前流程必须 **自动** 跑完（redteam-pre · 本篇 L1×6 · evaluate · kernel 6）；**不要**等 Owner 回复「请 evaluate」；FAIL 时 **CEO 自动打回**，Owner 不参与 verify。  
> **Owner（2026-10-28）：*
- **Path:** `docs/BRIEF-AUTO-GATE-PIPELINE.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **一条命令（全仓 Brief）**: ```bash
- **单篇 · Cursor Agent（推荐 · 进化闭环）**: ```bash
- **单篇 · 无人值守多轮（仅当轮间有外部改稿器）**: ```bash
- **步骤（机器 Must）**: | # | 动作 | 脚本 |
- **接入点（已接）**: - `manager-ceo-owner-gate.sh` → `evaluate-xhs-brief-complete.py`
- **Cursor Agent（Must）**: 见 `.cursor/rules/danying-manager-auto.mdc`：**禁止**等 Owner 说 evaluate；改 Brief 后 **同会话自动**跑 auto-gate-l…
- **Owner 仅**: gold / 发布 / 战略裁决 / Gate 3 轮仍 FAIL 的升级 — 见 [CEO-AUTO-QA-LOOP.md](./CEO-AUTO-QA-LOOP.md)


---

## L2 正文

# Brief 自动验收管线 · 无人值守（Must）

> **Owner（2026-10-27）：** 交稿前流程必须 **自动** 跑完（redteam-pre · 本篇 L1×6 · evaluate · kernel 6）；**不要**等 Owner 回复「请 evaluate」；FAIL 时 **CEO 自动打回**，Owner 不参与 verify。  
> **Owner（2026-10-28）：** 另 Must [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](./OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) — pitfalls · 三镜头 · **多轮 gap 直到 READY**（**L1 PASS ≠ 闭合**）。

## 一条命令（全仓 Brief）

```bash
bash scripts/manager-xhs-briefs-auto-pipeline.sh
```

## 单篇 · Cursor Agent（推荐 · 进化闭环）

```bash
bash scripts/manager-brief-evolution-until-gap.sh --brief content/xiaohongshu/<file>.md
```

- **exit 0** READY · **exit 42** NEEDS_WORK → **Must 读 EVOLUTION-GAP + CEO-REROUTE 实质性改稿再跑**（默认最多 6 轮 · 勿问 Owner）  
- 仅跑机器一轮：`bash scripts/manager-ceo-gate-one-round.sh --brief …` 后 **Must** `python scripts/analyze-brief-evolution-gap.py --brief …`  
- 队列：`content/evolution/00-manager/ceo-inbox/ceo-action-needed.md`  
- 矩阵：[WORKFLOW-AUTOMATION-MATRIX.md](./WORKFLOW-AUTOMATION-MATRIX.md)

## 单篇 · 无人值守多轮（仅当轮间有外部改稿器）

```bash
bash scripts/manager-ceo-auto-gate-loop.sh --brief content/xiaohongshu/<file>.md
```

默认最多 3 轮；**Brief 未变则 exit 42**（不空转）。盲重试：`CEO_GATE_BRUTE_FORCE=1`。

## 步骤（机器 Must）

| # | 动作 | 脚本 |
|---|------|------|
| 0 | 搜坑 MD（Agent Must · 无则不可写 Brief） | [BRIEF-PITFALLS-RESEARCH-SOP.md](../content/xiaohongshu/BRIEF-PITFALLS-RESEARCH-SOP.md) |
| 1 | 补全 redteam-pre（无则 AUTO 生成） | `ensure-redteam-pre.py --all` |
| 2 | **重对抗**（类似文/大 V/其它 IP 对打/FULL-DRILL/融合/L2–L3） | **`run-xhs-brief-adversarial-challenge.py --all`** |
| 3 | 本篇 L1-1…L1-6 + Gemini evaluate（**须 challenge 文件 schema PASS**） | `evaluate-xhs-brief-complete.py --brief …` |
| 4 | kernel 6 回归（批量时末步一次） | `verify-xhs-topic.sh` |
| 5 | FAIL → CEO-REROUTE + 补 redteam/challenge | `ceo-auto-fix-brief.py` |
| 6 | 交 Owner 前 | `manager-ceo-auto-gate-loop.sh` 或 Gate 内嵌 |

## 接入点（已接）

- `manager-ceo-owner-gate.sh` → `evaluate-xhs-brief-complete.py`
- `manager-autopilot.sh` → `manager-xhs-briefs-auto-pipeline.sh`
- `background-goal-evolution-cycle.sh` → ensure-redteam + complete（DEEP 时含 kernel 6）
- `ceo-xhs-ip-filter-batch.py` 收尾 → auto pipeline
- `verify-xhs-content-dir.sh` → 委托 auto pipeline（有 key 时）

## Cursor Agent（Must）

见 `.cursor/rules/danying-manager-auto.mdc`：**禁止**等 Owner 说 evaluate；改 Brief 后 **同会话自动**跑 auto-gate-loop；Gate FAIL **自动**读 CEO-REROUTE 改稿，**勿**把 FAIL 稿交 Owner。

## Owner 仅

gold / 发布 / 战略裁决 / Gate 3 轮仍 FAIL 的升级 — 见 [CEO-AUTO-QA-LOOP.md](./CEO-AUTO-QA-LOOP.md)