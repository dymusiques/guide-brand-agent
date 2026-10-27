# IP 打造 · 管理层级（CEO → 部门总经理）

> Owner 目标链路（2026-10-27）：**公司式三层** — 顶层 CEO、各部门 **二级 Manager（总经理）**、总经理兼 **Evaluator + 部门管理**，**向上汇报** CEO。

---

## 一层图

```text
Owner（目标 · 资料 · 终审）
        │
        ▼
┌───────────────────────────────────────┐
│  00 · CEO / 总 Manager                 │
│  · 接 Owner 总目标 · 派活到各部门       │
│  · 收各部门总经理汇报 · 汇总 PASS/FAIL  │
│  · 自有 Collector（总目标/派活记录）    │
└───────────────────────────────────────┘
        │ 派任务 + 要汇报
        ▼
┌─────────────── 9 个部门总经理（二级 Manager）──────────────┐
│  每个 = 职能 Agent（01–09）+ 本部门 Must 能力：              │
│  ① Collector（吃尽 Owner 喂给该部门的资料）                  │
│  ② v0 → v1 → v2…（本部门产出进化）                          │
│  ③ 部门 Evaluator（纠正稿 + 对 gold 的编辑距离 · metrics）   │
│  ④ 部门管理（INTEGRATION-PROMPT · verify 6 case · G-*）    │
│  ⑤ 向上汇报 CEO（GM-REPORT · 见模板）                        │
└────────────────────────────────────────────────────────────┘
        │
        ▼
   Git 定稿 / Owner 发布（CEO 门控 commit · aligned）
```

**不是 9 个 CEO：** 只有 **00** 对 Owner 负总责；01–09 是 **总经理**，对 CEO 汇报，不对 Owner 抢总调度。

---

## 部门总经理编制表

| 二级 Manager（总经理） | 原 Agent ID | 部门 | 部门产出（v0 典型） | 汇报 CEO 时带什么 |
|------------------------|-------------|------|---------------------|-------------------|
| **IP 战略 GM** | 01 | personal-ip | Pitch、IP 修订、红线 | intake 数 · v 当前 · mean 编辑距离 · 与 Brief 是否一致 |
| **商业品牌 GM** | 02 | business-brand | SWOT、商业稿 | 同上 + evaluate-business-brand |
| **营销 GM** | 03 | marketing | 触达/campaign 段 | 同上 + evaluate-marketing-campaign |
| **小红书内容 GM** | 04 | xhs-topic-manager | Brief/口播/packages | 同上 + aligned + voice-qa |
| **对齐质检 GM** | 05 | xhs-kernel | 规则/6 case（无文案 v0） | kernel PASS · 对 04 进化链的 gate 结论 |
| **内容管线 GM** | 06 | xhs-content-pipeline | 目录批量检 | 批量 PASS/FAIL 清单 |
| **视觉 GM** | 07 | brand-visual | 封面/视觉块 | 与 kit 一致 · 封面 evolution |
| **平台 GM** | 08 | platform | Drive 同步摘要 | 同步范围 · 未越权写 Brief |
| **数据 GM** | 09 | data-analytics | next-topics、dispatch | CSV 口径 · 派活建议 · 无 CSV 标注 |

**04 的「Topic Manager」= 小红书内容部总经理**，不是第二个 CEO。

---

## 两条程序挂在哪一层

| 程序 | CEO（00） | 部门总经理（01–09） |
|------|-----------|---------------------|
| **Collector** | 收 Owner **总目标**、跨部门资料索引 | 收 Owner 喂给 **本部门** 的全部资料 → 本部门 `intake/` |
| **Evaluator（编辑距离）** | 可选：对 **派活计划/CEO 摘要** vs playbook 锚句 | **Must**：本部门每个 artifact 的 vN vs `reference/gold.md` → `metrics.jsonl` |
| **部门管理** | 步序、Manager's Loop、commit 门控 | 本部门 INTEGRATION-PROMPT、verify-agent-matrix、G-* |

**05 总经理：** 部门 Evaluator = **Gemini aligned gate** + 监督 04 进化是否先收敛再称定稿；**本人不产 v0 口播**。

---

## 工作流（一次 Owner 任务）

1. **Owner → CEO：** 给目标 + 资料（CEO Collector 登记）。  
2. **CEO → 某部门 GM：** 「部门 X 领任务 slug Y」+ 截止产出 v0。  
3. **GM：** Collector 补 intake → 出 **v0** → 部门 Evaluator 出纠正/v1 → 写 **metrics** → 填 **GM-REPORT** → **汇报 CEO**。  
4. **CEO：** 汇总 GM-REPORT → **`manager-ceo-owner-gate.sh`**；PASS 才交 Owner；FAIL → **CEO-REROUTE** → GM 再 evaluate（默认 ≤3 轮，**不让 Owner 逐条验**）。见 [CEO-AUTO-QA-LOOP.md](./CEO-AUTO-QA-LOOP.md)。  
5. **Owner：** 定 **gold**、发布、裁决；CEO 不代发；Agent 只呈 **OWNER-HANDOFF**（已 gate）。

---

## 文件与命令（与层级对应）

| 层级 | 路径 / 命令 |
|------|-------------|
| 部门 artifact | `content/evolution/<dept-slot>/<slug>/`（intake · versions · gold · metrics） |
| 部门汇报 CEO | `content/evolution/<dept-slot>/<slug>/GM-REPORT.md`（模板见下） |
| CEO 收件箱 | `content/evolution/00-manager/ceo-inbox/`（可选汇总） |
| Collector | `scripts/collector-intake.py --agent <dept-slot> ...` |
| 部门 Evaluator 度量 | `scripts/evaluate-edit-distance.py` + `evolution-metrics-summary.py` |
| CEO 验收链 | `manager-workflow-verify.sh` · **`manager-ceo-owner-gate.sh`（交 Owner 前）** · [CEO-AUTO-QA-LOOP.md](./CEO-AUTO-QA-LOOP.md) |

**规范细节：** [agents/_shared/COLLECTOR-EVALUATOR.md](../agents/_shared/COLLECTOR-EVALUATOR.md) · [COLLECTOR-EVALUATOR-PIPELINE.md](./COLLECTOR-EVALUATOR-PIPELINE.md)

---

## 部门总经理 · 向上汇报模板

复制到 `GM-REPORT.md`：

```markdown
# GM-REPORT · <部门名> · <slug>

- 汇报给：00 CEO
- 日期：
- 任务（CEO 派活摘要）：

## Collector
- intake 条数：
- 新 intake id：

## 版本
- 当前定稿候选：vN 路径
- gold 是否 Owner 已确认：是/否

## 部门 Evaluator（编辑距离）
- metrics.jsonl 路径
- mean(dist_corrected_ref) 或 mean(dist_candidate_ref)：
- 相对上一版距离是否下降：是/否/首版

## 部门管理
- verify / evaluate：（PASS/FAIL + 命令）
- G-*：
- 风险/需 CEO 裁决：

## 请求 CEO
- [ ] 进入 commit  - [ ] 打回改稿  - [ ] 需 Owner 确认 gold
```

---

## 和 Sub-Agent / Task 的关系

- **01–09 职能岗 = 部门总经理**（编制内，单会话顺序扮演）。  
- **Cursor Task** = 临时工，向 **CEO 或某 GM** 汇报调研，**不**替代 GM 的 v0/Evaluator 责任。

见 [IP-SUBAGENT-ROSTER.md](../content/personal-ip/IP-SUBAGENT-ROSTER.md)
