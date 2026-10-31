---
context_version: "2026-10-30-l012"
repo_path: "docs/IP-MANAGEMENT-HIERARCHY.md"
goal: "IP 打造 · 管理层级（CEO → 部门总经理）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "5bd1d716e3beb891"
---

# IP 打造 · 管理层级（CEO → 部门总经理）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** - **01–09 职能岗 = 部门总经理**（编制内，单会话顺序扮演）。  
- **Cursor Task** = 临时工，向 **CEO 或某 GM** 汇报调研，**不**替代 GM 的 v0/Evaluator 责任。
- **Path:** `docs/IP-MANAGEMENT-HIERARCHY.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > Owner 目标链路（2026-10-27）：**公司式三层** — 顶层 CEO、各部门 **二级 Manager（总经理）**、总经理兼 **Evaluator + 部…
- **章节锚点**: - **部门总经理编制表**: | 二级 Manager（总经理） | 原 Agent ID | 部门 | 部门产出（v0 典型） | 汇报 CEO 时带什么 |
- **和 Sub-Agent / Task 的关系**: - **01–09 职能岗 = 部门总经理**（编制内，单会话顺序扮演）。


---

## L2 正文

# IP 打造 · 管理层级（CEO → 部门总经理）

> Owner 目标链路（2026-10-27）：**公司式三层** — 顶层 CEO、各部门 **二级 Manager（总经理）**、总经理兼 **Evaluator + 部门管理**，**向上汇报** CEO。


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


## 工作流（一次 Owner 任务）

1. **Owner → CEO：** 给目标 + 资料（CEO Collector 登记）。  
2. **CEO → 某部门 GM：** 「部门 X 领任务 slug Y」+ 截止产出 v0。  
3. **GM：** Collector 补 intake → 出 **v0** → 部门 Evaluator 出纠正/v1 → 写 **metrics** → 填 **GM-REPORT** → **汇报 CEO**。  
4. **CEO：** 汇总 GM-REPORT → **`manager-ceo-owner-gate.sh`**；PASS 才交 Owner；FAIL → **CEO-REROUTE** → GM 再 evaluate（默认 ≤3 轮，**不让 Owner 逐条验**）。见 [CEO-AUTO-QA-LOOP.md](./CEO-AUTO-QA-LOOP.md)。  
5. **Owner：** 定 **gold**、发布、裁决；CEO 不代发；Agent 只呈 **OWNER-HANDOFF**（已 gate）。


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