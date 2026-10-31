---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md"
goal: "六项 6-case · GM 完工 → Senior Manager（CEO）复核（Must · 2026-10-30）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "74ab2c9953d7a638"
---

# 六项 6-case · GM 完工 → Senior Manager（CEO）复核（Must · 2026-10-30）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner 口语「六项 disc test」= 本仓六项 6-case 基准**（非 MBTI DISC）。全部 **PASS** 后，各 **GM 交 GM-REPORT**，**CEO（00）** 复核，再 **Owner HTML**。
- **Path:** `docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **1. 六项 6-case（顺序 · 脚本强制）**: | # | 名称 | 脚本 | 谁负责 |
- **2. GM → CEO 指挥链（单会话 · 顺序扮演）**: ```text
- **3. 三重 evaluate + 距 baseline/gold**: **Must**（有 brief 时 · Python 编排）：
- **4. 双重压测（stress ×2）**: **Must**（工作流测试稿 READY 或 Owner 指定压测）：
- **5. Python 总入口（含上文全部）**: ```bash
- **6. Cursor 交 Owner（Must · 见 OWNER-CHAT-DELIVERY-FORMAT.md）**: - 表格式列出 **调用了哪些 Agent / 能力 / 脚本**
- **7. Commit / push**: - **READY + routine：** AUTO-WORKFLOW 步 5 · Owner 未禁止 → **Must git commit** 定稿路径


---

## L2 正文

# 六项 6-case · GM 完工 → Senior Manager（CEO）复核（Must · 2026-10-30）

> **Owner 口语「六项 disc test」= 本仓六项 6-case 基准**（非 MBTI DISC）。全部 **PASS** 后，各 **GM 交 GM-REPORT**，**CEO（00）** 复核，再 **Owner HTML**。

## 1. 六项 6-case（顺序 · 脚本强制）

| # | 名称 | 脚本 | 谁负责 |
|---|------|------|--------|
| 1 | **集成 6-case** | `bash scripts/verify-integration.sh` | 08 / 集成 |
| 2 | **01 IP 函数壳** | `python scripts/evaluate_personal_ip.py --check` | 01 GM |
| 3 | **GM fused 6（01）** | `bash scripts/verify-agent-fused.sh --agent 01` | 01 GM |
| 4 | **GM fused 6（04）** | `bash scripts/verify-agent-fused.sh --agent 04` | 04 GM |
| 5 | **GM fused 6（05）** | `bash scripts/verify-agent-fused.sh --agent 05` | 05 GM |
| 6 | **本篇 L1×6 + Kernel 6 回归** | `evaluate-xhs-brief-complete.py --brief …` + `verify-xhs-topic.sh` | 04/05 |

有 `--brief` 时 **Must 跑齐 1–6**；无 brief 时跑 1–5 + HTML refresh。

## 2. GM → CEO 指挥链（单会话 · 顺序扮演）

```text
Owner 目标 → intake/collector
  → 01 IP（边界/KPI）
  → 04 Topic（pitfalls · 长稿 · redteam）
  → 05 Kernel（6-case 回归 · 不改 kernel 除非专项）
  → 04 GM-REPORT（六项 + metrics）
  → CEO：triple-eval · double-stress · owner-gate · HTML
  → Owner：浏览器 HTML（#owner-latest）
```

**GM-REPORT 模板：** [`content/evolution/_template/GM-REPORT.md`](../content/evolution/_template/GM-REPORT.md)  
**CEO 派活记录：** [`agents/00-manager/CEO-DISPATCH-SOP.md`](../agents/00-manager/CEO-DISPATCH-SOP.md) + `CEO-RUN-MANIFEST-latest.md`

## 3. 三重 evaluate + 距 baseline/gold

**Must**（有 brief 时 · Python 编排）：

```bash
bash scripts/ceo-triple-eval-baseline-loop.sh --brief content/xiaohongshu/<file>-brief.md
```

- **轮 1–3：** 每轮 `manager-ceo-gate-one-round.sh` → **`verify-xhs-clever-advocate.sh`**（长稿 ≥4 反方 · Clever）→ `analyze-brief-evolution-gap.py` →（有 gold）`evaluate-edit-distance.py` → 追加 `metrics.jsonl`
- **退出：** READY 且 gold/longform 达标 → 0；**42** → Agent 同会话改稿再跑 full execution；未 READY 且轮次用尽 → 1
- **可观察性：** 每轮写入 `EVOLUTION-GAP-latest.md` · `CEO-RUN-MANIFEST-latest.json` 的 `eval_rounds[]`

## 4. 双重压测（stress ×2）

**Must**（工作流测试稿 READY 或 Owner 指定压测）：

| 次 | 脚本 | 含义 |
|----|------|------|
| 压测 0 | `bash scripts/verify-xhs-clever-advocate.sh --brief …` | Clever 多立场反方（长稿 Must） |
| 压测 1 | `python scripts/run-xhs-brief-adversarial-challenge.py --brief …` | 对抗/schema 压测（含 Clever 表） |
| 压测 2 | `bash scripts/ceo-workflow-test-round2-finish.sh` 或第二次 adversarial（`CEO_STRESS_PASS=2`） | campaign/round2 或重对抗 |

编排：`bash scripts/ceo-double-stress.sh --brief …`

## 5. Python 总入口（含上文全部）

```bash
bash scripts/ceo-full-execution-pipeline.sh --goal "<Owner 原话>" --brief … --no-discovery-auto
```

实现：`scripts/run_ceo_full_execution.py` · 机器清单：`integration/handoff/ceo-full-execution-cycle.json`

## 6. Cursor 交 Owner（Must · 见 OWNER-CHAT-DELIVERY-FORMAT.md）

- 表格式列出 **调用了哪些 Agent / 能力 / 脚本**
- **逐步时间线**
- **HTML 绝对路径 + file:// 链接**（并 `open-owner-xhs-deliverable-html.sh`）
- 附 `CEO-RUN-MANIFEST-latest.json` 摘要

## 7. Commit / push

- **READY + routine：** AUTO-WORKFLOW 步 5 · Owner 未禁止 → **Must git commit** 定稿路径  
- **push / 双推：** **仅** Owner 明确要求时；写入规则，**不**默认 push