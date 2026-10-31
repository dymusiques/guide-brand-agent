---
context_version: "2026-10-30-l012"
repo_path: "docs/COLLECTOR-EVALUATOR-PIPELINE.md"
goal: "Collector + Evaluator · Owner 怎么用"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "45cb5de5b3e4fb11"
---

# Collector + Evaluator · Owner 怎么用

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 1. **收集者（Collector）** — 你喂的语音转写、md、chat 片段、表格，**全部进 intake**，Agent 必须基于 **manifest 里全部 intake** 再写 v0。  
2. **Evaluator** — 每轮产出 **纠正稿** + 与 **gold 标准答案** 的 **编辑距离**，记入 `metrics.js
- **Path:** `docs/COLLECTOR-EVALUATOR-PIPELINE.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **你要的两层能力（全 Agent + CEO 都有）**: 1. **收集者（Collector）** — 你喂的语音转写、md、chat 片段、表格，**全部进 intake**，Agent 必须基于 **manifest 里全部 intake** 再写 v…
- **一次完整循环（以篇 E 口播为例 · Agent 04）**: ```bash
- **CEO（00）同样**: ```bash
- **双螺旋：基线升高 · 标准升高**: **Owner 原则（2026-10-27）：** 迭代让 **单篇成果** 慢慢变好，并让 **自己的基线**（素材 + gold）越抬越高；**无论你用多口语、多碎片的说法**，系统在基线抬高后应…
- **与小红书 aligned 的关系**: - **进化距离** = 你离「心中定稿」多近（可量化）。
- **规范全文**: [agents/_shared/COLLECTOR-EVALUATOR.md](../agents/_shared/COLLECTOR-EVALUATOR.md) · [integration/col…


---

## L2 正文

# Collector + Evaluator · Owner 怎么用

## 你要的两层能力（全 Agent + CEO 都有）

1. **收集者（Collector）** — 你喂的语音转写、md、chat 片段、表格，**全部进 intake**，Agent 必须基于 **manifest 里全部 intake** 再写 v0。  
2. **Evaluator** — 每轮产出 **纠正稿** + 与 **gold 标准答案** 的 **编辑距离**，记入 `metrics.jsonl`；v0→v1→v2 进化，可看 **平均距离是否下降**。

## 一次完整循环（以篇 E 口播为例 · Agent 04）

```bash
# 1) 收集者：登记你刚说的原话
python scripts/collector-intake.py --agent 04-xhs --slug pivot-E \
  --file content/xiaohongshu/owner-source-pivot-E-paris-chengdu-2026-10-21.md \
  --note "Owner 2026-10-27 审美增补"

# 2) Agent 写 v0 → 保存
# content/evolution/04-xhs/pivot-E/versions/v0.md

# 3) Evaluator 纠正 → v0-corrected 或直接 v1.md

# 4) 你定标准答案（或 aligned Brief 摘录）
# content/evolution/04-xhs/pivot-E/reference/gold.md

# 5) 编辑距离
python scripts/evaluate-edit-distance.py \
  --candidate content/evolution/04-xhs/pivot-E/versions/v1.md \
  --reference content/evolution/04-xhs/pivot-E/reference/gold.md \
  --corrected content/evolution/04-xhs/pivot-E/versions/v1-corrected.md \
  --label v1 \
  --append content/evolution/04-xhs/pivot-E/metrics.jsonl

# 6) 平均距离
python scripts/evolution-metrics-summary.py content/evolution/04-xhs/pivot-E/metrics.jsonl
```

## CEO（00）同样

```bash
python scripts/collector-intake.py --agent 00-manager --slug 2026-10-27-redteam --text "Owner: 跑红队+进化指标"
# v0 = 派活计划 md → 与 reference/gold.md（playbook 锚句）算距离
```

## 双螺旋：基线升高 · 标准升高

**Owner 原则（2026-10-27）：** 迭代让 **单篇成果** 慢慢变好，并让 **自己的基线**（素材 + gold）越抬越高；**无论你用多口语、多碎片的说法**，系统在基线抬高后应 **内化** 成最好效果 — **不要求** 你说「evaluate 过的提示词」。见 [OWNER-INPUT-PRINCIPLES.md](./OWNER-INPUT-PRINCIPLES.md)。

| 什么在升高 | 怎么升高（**内部**；Owner 输入方式不变） |
|------------|------------------------------------------|
| **素材基线（intake）** | Owner 随意喂文案、数据、原话 → manifest 更全 → 下一版 v0 起点更高 |
| **标准基线（gold / playbook）** | 定稿、aligned Brief、IP 锚句升格为 `reference/gold.md` → Evaluator 靶心抬高 |
| **LLM + 内部提示词** | Agent 用 Skill / INTEGRATION-PROMPT / Brief（Owner **不写**）；Manager's Loop 迭代集成层 → 同样随意的 Owner 话 **越译越准** |
| **内部质检（Gate）** | 交 Owner 前脚本自检（aligned 等）**越跑越稳** — **不** 提高 Owner 使用门槛 |
| **可量化** | 有 gold：编辑距离↓；无 gold：内部 gate 通过率↑（Owner 不跑命令） |

**不是魔法：** 基线需持续 intake / gold / 内部迭代；**Agent** 在 CEO→GM 打回环里改稿并重跑 **内部 gate**，不把未验稿交给 Owner。

## 与小红书 aligned 的关系

- **进化距离** = 你离「心中定稿」多近（可量化）。  
- **evaluate-xhs-topic** = IP/强链接规则 gate。  
- 建议：**gold** = 你认可的终稿；aligned 通过后再把 gold 同步进 `reference/gold.md`。

## 规范全文

[agents/_shared/COLLECTOR-EVALUATOR.md](../agents/_shared/COLLECTOR-EVALUATOR.md) · [integration/collector-evaluator-adoption.md](../integration/collector-evaluator-adoption.md)