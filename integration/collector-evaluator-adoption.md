---
context_version: "2026-10-30-l012"
repo_path: "integration/collector-evaluator-adoption.md"
goal: "Collector + Evaluator · 集成 adoption"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "73553333515458c2"
---

# Collector + Evaluator · 集成 adoption

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner 需求（2026-10-27）：** **CEO（00）+ 部门总经理（01–09 二级 Manager）** 公司层级；各部门 **Collector + v0→vN + Evaluator + GM-REPORT→CEO**。见 [docs/IP-MANAGEMENT-HIERARCHY.md](../docs/IP-MANAGEMEN
- **Path:** `integration/collector-evaluator-adoption.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **分层（不替代 00 步序）**: ```text
- **路径约定（Git 真相源）**: ```text
- **脚本（集成层 · 非 kernel）**: | 脚本 | 作用 |
- **各 Agent 范围（收集什么）**: | Agent | slug 前缀 | 典型 artifact | gold 从哪来 |
- **改集成时**: 1. 各 `agents/<nn>-*/INTEGRATION-PROMPT.md` 已链到 [`agents/_shared/COLLECTOR-EVALUATOR.md`](../agents/_…
- **验收**: ```bash


---

## L2 正文

# Collector + Evaluator · 集成 adoption

> **Owner 需求（2026-10-27）：** **CEO（00）+ 部门总经理（01–09 二级 Manager）** 公司层级；各部门 **Collector + v0→vN + Evaluator + GM-REPORT→CEO**。见 [docs/IP-MANAGEMENT-HIERARCHY.md](../docs/IP-MANAGEMENT-HIERARCHY.md)。

## 分层（不替代 00 步序）

```text
Owner 输入
  → Collector（intake 落盘 + manifest）
  → Agent 产出 v0
  → Evaluator（纠正稿 + evaluate-edit-distance.py）
  → v1…vN（CEO Gate FAIL → CEO-REROUTE → GM 自验；见 CEO-AUTO-QA-LOOP.md）
  → reference/gold.md（标准答案）
  → metrics.jsonl（每版距离；可算均值）
```

**双螺旋（内部）：** 成果变好 + intake/gold 基线抬高；**LLM/内部提示词**在 Manager's Loop 进化，**同样随意的 Owner 输入**越译越准；**内部 Gate** 更稳 — **Owner 输入方式不变**。见 [OWNER-INPUT-PRINCIPLES.md](../docs/OWNER-INPUT-PRINCIPLES.md) · [COLLECTOR-EVALUATOR-PIPELINE.md §双螺旋](../docs/COLLECTOR-EVALUATOR-PIPELINE.md#双螺旋基线升高--标准升高)。

## 路径约定（Git 真相源）

```text
content/evolution/<agent-slot>/<artifact-slug>/
  intake/           # Owner 喂入，只追加
  manifest.json     # 机器可读索引
  versions/v0.md
  versions/v1.md
  versions/vN-corrected.md   # 可选：Evaluator 当轮纠正
  reference/gold.md          # 标准答案（Owner 定）
  metrics.jsonl              # 每行一版指标
```

**agent-slot 示例：** `00-manager` · `01-personal-ip` · `04-xhs` · `09-analytics`

## 脚本（集成层 · 非 kernel）

| 脚本 | 作用 |
|------|------|
| `scripts/collector-intake.py` | 收集者：追加 intake + 更新 manifest |
| `scripts/evaluate-edit-distance.py` | Evaluator 度量：Levenshtein + 归一化 + 写 metrics |
| `scripts/evolution-metrics-summary.py` | 读 metrics.jsonl 输出平均编辑距离等 |

## 各 Agent 范围（收集什么）

| Agent | slug 前缀 | 典型 artifact | gold 从哪来 |
|-------|-----------|---------------|-------------|
| 00 | `00-manager` | 派活计划、CEO 摘要 | Owner 确认的计划 / playbook 锚句 |
| 01 | `01-personal-ip` | Pitch、IP 修订 | `ip-positioning-brief` 定稿句 |
| 02 | `02-business-brand` | SWOT 稿 | evaluate 通过后 commit 版 |
| 03 | `03-marketing` | 触达/campaign 段 | discovery-phase 定稿 |
| 04 | `04-xhs` | Brief/口播/packages | aligned Brief 或 Owner 审阅定稿 |
| 05 | — | **不产文案**；metrics 可挂 Brief 进化 | 同 04 gold |
| 06 | `06-pipeline` | 批量检报告 | 规范 checklist |
| 07 | `07-visual` | 封面字/ brief 块 | brand kit 通过稿 |
| 08 | `08-platform` | sync 摘要 | Git 定稿 md |
| 09 | `09-analytics` | next-topics 建议 | Owner 确认选题 |

## 改集成时

1. 各 `agents/<nn>-*/INTEGRATION-PROMPT.md` 已链到 [`agents/_shared/COLLECTOR-EVALUATOR.md`](../agents/_shared/COLLECTOR-EVALUATOR.md)  
2. `AUTO-WORKFLOW.md` 步 **0c** Collector · **3b** Evolution metrics（Brief 可选）  
3. 新能力只改本文 + 脚本，**不改** `kernels/xiaohongshu/line2/` 除非 05 专项  

## 验收

```bash
python scripts/collector-intake.py --agent 04 --slug _selftest --text "test" --dry-run
python scripts/evaluate-edit-distance.py --candidate content/evolution/_template/versions/v0.md --reference content/evolution/_template/reference/gold.md --label v0
bash scripts/verify-collector-evaluator.sh
```