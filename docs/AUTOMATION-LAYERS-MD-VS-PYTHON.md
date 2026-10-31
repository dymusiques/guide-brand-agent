---
context_version: "2026-10-30-l012"
repo_path: "docs/AUTOMATION-LAYERS-MD-VS-PYTHON.md"
goal: "自动化分层 · MD/Prompt/Skill vs 函数壳 vs Python（Owner 确认 · 2026-10-30）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "53a4f9073d86ec6e"
---

# 自动化分层 · MD/Prompt/Skill vs 函数壳 vs Python（Owner 确认 · 2026-10-30）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > 另一 Agent 说的 **「IP 定位 = MD + Prompt + Skill，在 Playbook 文档管理/人定标准里，不要求函数壳」** —— **对「写什么、怎么交互」这一层** 是对的。  
> 本仓 **同时** 还有 **「跑验收、串联无人值守」** 一层；两层 **适用范围不同**，不是二选一。
- **Path:** `docs/AUTOMATION-LAYERS-MD-VS-PYTHON.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **2. 全自动化是否「必须写一个 Python 才能做完」？**: **不必唯一 Python，但集成层几乎必有 Python（或等价脚本）。**
- **4. Python 总入口（从零起的「一条命令」）**: ```bash


---

## L2 正文

# 自动化分层 · MD/Prompt/Skill vs 函数壳 vs Python（Owner 确认 · 2026-10-30）

> 另一 Agent 说的 **「IP 定位 = MD + Prompt + Skill，在 Playbook 文档管理/人定标准里，不要求函数壳」** —— **对「写什么、怎么交互」这一层** 是对的。  
> 本仓 **同时** 还有 **「跑验收、串联无人值守」** 一层；两层 **适用范围不同**，不是二选一。


## 2. 全自动化是否「必须写一个 Python 才能做完」？

**不必唯一 Python，但集成层几乎必有 Python（或等价脚本）。**

| 组件 | 典型形态 | 本仓 |
|------|----------|------|
| 编排（CEO 一条链） | bash **或** Python 调 subprocess | `manager-ceo-xhs-owner-delivery.sh` · **`run_ceo_xhs_autopilot.py`**（Python 总入口） |
| 判定 / 对抗 / metrics | **Python** | `evaluate-xhs-brief-complete.py` · `run-xhs-brief-adversarial-challenge.py` · … |
| 定时无人值守 | bash + process-launcher | `background-goal-evolution-cycle.sh` |
| **改 Brief 正文** | **Cursor Agent / Owner** | 脚本 **不会** 自动写稿（设计如此） |

结论：**整条「无人值守验收 + HTML + campaign」** 需要 **Python + bash 组合**；**不是**「只能有一个 .py 文件」，但 **没有 Python 就做不完** 对抗/evaluate/编辑距离/HTML 生成这些集成能力。


## 4. Python 总入口（从零起的「一条命令」）

```bash
.venv/bin/python scripts/run_ceo_xhs_autopilot.py
.venv/bin/python scripts/run_ceo_xhs_autopilot.py --round2
.venv/bin/python scripts/evaluate_personal_ip.py --check
```

见 [`CEO-XHS-OWNER-DELIVERY-AUTOPILOT.md`](./CEO-XHS-OWNER-DELIVERY-AUTOPILOT.md) · [`integration/handoff/ceo-xhs-delivery-cycle.json`](../integration/handoff/ceo-xhs-delivery-cycle.json)