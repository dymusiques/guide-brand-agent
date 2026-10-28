# Brief 自动验收管线 · 无人值守（Must）

> **Owner（2026-10-27）：** 交稿前流程必须 **自动** 跑完（redteam-pre · 本篇 L1×6 · evaluate · kernel 6）；**不要**等 Owner 回复「请 evaluate」；FAIL 时 **CEO 自动打回**，Owner 不参与 verify。

## 一条命令（全仓 Brief）

```bash
bash scripts/manager-xhs-briefs-auto-pipeline.sh
```

## 单篇（含打回循环 · 默认 3 轮）

```bash
bash scripts/manager-ceo-auto-gate-loop.sh --brief content/xiaohongshu/<file>.md
```

## 步骤（机器 Must）

| # | 动作 | 脚本 |
|---|------|------|
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
