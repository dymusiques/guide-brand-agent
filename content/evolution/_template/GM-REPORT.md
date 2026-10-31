---
context_version: "2026-10-30-l012"
repo_path: "content/evolution/_template/GM-REPORT.md"
goal: "GM-REPORT · <部门名> · <slug>"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "e0b9e3c8e6a5f2d0"
---

# GM-REPORT · <部门名> · <slug>

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** - 汇报给：00 CEO
- 日期：
- 任务（CEO 派活摘要）：
- **Path:** `content/evolution/_template/GM-REPORT.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **Collector**: - intake 条数：
- **版本**: - 当前定稿候选：versions/vN.md
- **部门 Evaluator**: - metrics.jsonl：
- **六项 6-case 基准（Must · 交 CEO 前）**: | # | 层 | 命令 | 结果 |
- **部门管理**: - verify / evaluate：（PASS/FAIL + 命令）
- **本轮分析结论（PASS/FAIL 均写 · 可观察性）**: - （AI/GM 必填：哪项变好/变差 · 为什么 · 下一轮改什么 · 是否改 prompt/SOP）
- **请求 CEO**: - [ ] 可 commit / 定稿


---

## L2 正文

# GM-REPORT · <部门名> · <slug>

- 汇报给：00 CEO
- 日期：
- 任务（CEO 派活摘要）：

## Collector

- intake 条数：
- 新 intake id：

## 版本

- 当前定稿候选：versions/vN.md
- gold（reference/gold.md）Owner 已确认：是 / 否

## 部门 Evaluator

- metrics.jsonl：
- mean 编辑距离（dist_corrected_ref 或 dist_candidate_ref）：
- 较上一版是否下降：是 / 否 / 首版

## 六项 6-case 基准（Must · 交 CEO 前）

| # | 层 | 命令 | 结果 |
|---|-----|------|------|
| 1 | 集成 6 | `verify-integration.sh` | |
| 2 | 01 壳 | `evaluate_personal_ip.py --check` | |
| 3–5 | fused 01/04/05 | `verify-agent-fused.sh --agent NN` | |
| 6 | 本篇 L1+kernel | `evaluate-xhs-brief-complete.py` + `verify-xhs-topic.sh` | |

## 部门管理

- verify / evaluate：（PASS/FAIL + 命令）
- triple-eval 轮次 / norm_dist：（见 EVOLUTION-GAP · metrics.jsonl）
- G-*：
- 风险 / 需 CEO 裁决：

## 本轮分析结论（PASS/FAIL 均写 · 可观察性）

- （AI/GM 必填：哪项变好/变差 · 为什么 · 下一轮改什么 · 是否改 prompt/SOP）

## 请求 CEO

- [ ] 可 commit / 定稿
- [ ] 打回改稿
- [ ] 需 Owner 确认 gold