# CEO 自动纠错 · Owner 门控（默认不让 Owner 逐条验）

> **Owner 要求（2026-10-27）：** 按目标 **自动产出** → **CEO 自动验收/纠错** → 不过则 **打回部门 GM 再 evaluate**；**不要**每轮都让 Owner 跑 verify。**交给 Owner 的任何交付物，Agent 必须先自验一遍**；只有需要 Owner 决策时才来确认。

> **Owner 输入（2026-10-27）：** 怎么说都行 — **内部** Gate/提示词/Evaluator 负责抬高质量；**不** 要求 Owner 公式化 prompt。见 [OWNER-INPUT-PRINCIPLES.md](./OWNER-INPUT-PRINCIPLES.md)。

---

## 原则（Must）

| 谁 | 做什么 | 不做什么 |
|----|--------|----------|
| **部门 GM（01–09）** | Collector → v0 → 部门 Evaluator（纠正 + 编辑距离）→ 本部门 verify/evaluate → **GM-REPORT** | 不把「请 Owner 帮忙验 aligned」当默认出口 |
| **CEO（00）** | 收 GM-REPORT → 跑 **Owner Gate**（脚本 + 对照目标/G-*）→ PASS 才 **交 Owner**；FAIL **打回 GM**（CEO-REROUTE） | 不把未 gate 的稿/ Brief 当「定稿候选」呈现给 Owner |
| **Owner** | **确认** gold、发布、范围变更、不可逆操作 | **默认不负责** 逐步跑 `evaluate` / matrix verify |

**会话内「自动纠错」：** Gate FAIL 时，Agent **同会话** 扮演 GM 改稿 → 再跑 gate，直到 PASS 或触达 **打回上限**（见下）。不要求 Owner 说「再验一次」。

---

## 闭环（Produce → CEO Gate → Owner 或 Reroute）

```text
Owner 目标 + 资料
    → CEO 派 GM（slug · G-* · 验收命令清单）
    → GM：v0 → Evaluator → GM-REPORT（自报 PASS 前须本部门命令全绿）
    → CEO：bash scripts/manager-ceo-owner-gate.sh …
         ├─ PASS → Owner 交接包（短确认清单，见 OWNER-HANDOFF 模板）
         └─ FAIL → CEO-REROUTE.md → GM 改 v(N+1) → 再 GM-REPORT → 再 Gate（循环）
    → 达上限仍 FAIL → 只向 Owner 报 **阻塞项 + 已跑命令输出**（仍不甩未验稿）
```

**打回上限（默认）：** `CEO_GATE_MAX_ROUNDS=3`（Agent 自计轮次；第 4 轮仍 FAIL 才 escalation）。可在 Owner 当轮指定覆盖。

---

## Owner Gate（机器验收 · **仅 Agent 跑，Owner 无步骤**）

**Gate** = 交给 Owner 之前的 **内部质检**（aligned、Brief 规范、可选 voice-qa 等）。标准可在内部越收越严；**Owner 仍只需自然说话 + 看结果确认**。

**有 Brief 定稿 / 交 Owner 看正文前，Agent Must：**

```bash
bash scripts/manager-ceo-owner-gate.sh --brief content/xiaohongshu/<file>.md
# 内嵌 manager-ceo-auto-gate-loop.sh（redteam + L1×6 + evaluate + kernel 6 · ≤3 轮）
```

**无人值守全仓 Brief：** `bash scripts/manager-xhs-briefs-auto-pipeline.sh` — 见 [BRIEF-AUTO-GATE-PIPELINE.md](./BRIEF-AUTO-GATE-PIPELINE.md)

**可选叠加：**

```bash
# 视频 Round1
bash scripts/manager-ceo-owner-gate.sh --brief … --voice content/xiaohongshu/<round1>.md

# 进化链（有 gold 时）
bash scripts/manager-ceo-owner-gate.sh --brief … \
  --evolution content/evolution/04-xhs/<slug>
```

Gate **PASS** 才会在 `content/evolution/00-manager/ceo-inbox/` 写入 `gate-latest.md`（含时间戳与命令清单）。

**与 autopilot 关系：** `manager-autopilot.sh` = 日常链/09 派活；**交 Owner 前** 仍须对 **当次交付** 跑 `manager-ceo-owner-gate.sh`（Brief 路径），二者不互相替代。

---

## CEO 打回 GM（CEO-REROUTE）

Gate 或 GM-REPORT 与终端不一致时，CEO 在同 slug 目录写（或更新）：

`content/evolution/<dept-slot>/<slug>/CEO-REROUTE.md`

模板：[`content/evolution/_template/CEO-REROUTE.md`](../content/evolution/_template/CEO-REROUTE.md)

GM **Must：** 读 REROUTE → 出 v(N+1) → 重跑 REROUTE 里列出的命令 → 更新 GM-REPORT → 通知 CEO 复 gate。

---

## 何时才找 Owner「确认」

仅以下情况 **允许** 打断 Owner 做验证；其余 **Agent 自验**：

| 需 Owner 确认 | 不需 Owner（CEO/GM 自验） |
|---------------|---------------------------|
| 定 **gold** / 改战略红线 / 发布上线 | `evaluate-xhs-topic` aligned |
| 合作范围、单品类绑定、对外承诺 | `verify-xhs-voice-qa`、SEO lint |
| 不可逆：Drive 覆盖、发信、代发 | `manager-workflow-verify`、`verify-agent-matrix` |
| Gate 3 轮仍 FAIL 的 **裁决**（改 Brief vs 改 Skill vs 05 kernel） | 编辑距离、metrics 汇总 |

Owner 交接包模板：[`content/evolution/_template/OWNER-HANDOFF.md`](../content/evolution/_template/OWNER-HANDOFF.md)

---

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
