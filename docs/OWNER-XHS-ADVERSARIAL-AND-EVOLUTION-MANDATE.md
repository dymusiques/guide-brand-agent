---
context_version: "2026-10-30-l012"
repo_path: "docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md"
goal: "Owner 固定 · 小红书对抗生成 + 多轮压测（Must · 2026-10-28）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "937d26ea3eda6d85"
---

# Owner 固定 · 小红书对抗生成 + 多轮压测（Must · 2026-10-28）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner 原话（摘要）：** 不要正确废话；先定方向 → 上网搜坑 → 打 **极难自动纠** 的 L2–L3 对抗；第一轮测完 **自动 analyze 当 baseline**，**勿问 Owner** 直接进第二轮及后续轮，用 **与终极目标/轮间演进** 的 **距离** 驱动改稿，直到结果足够好。  
> **适用范围：** 凡本仓 **
- **Path:** `docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **§2 · 自动多轮 evaluation 与压测（无人确认）**
- **§4 · Manager 派活记录 · 额外必报字段**: - **搜坑：** pitfalls 路径 · 回应了几条


---

## L2 正文

# Owner 固定 · 小红书对抗生成 + 多轮压测（Must · 2026-10-28）

> **Owner 原话（摘要）：** 不要正确废话；先定方向 → 上网搜坑 → 打 **极难自动纠** 的 L2–L3 对抗；第一轮测完 **自动 analyze 当 baseline**，**勿问 Owner** 直接进第二轮及后续轮，用 **与终极目标/轮间演进** 的 **距离** 驱动改稿，直到结果足够好。  
> **适用范围：** 凡本仓 **小红书 Brief / 笔记定稿 / 筛选交付 / 工作流测试稿**；**认知期 Discovery 01–04 与测试稿须同案例线**（见 `content/xiaohongshu/DISCOVERY-SERIES-UNIFIED-NARRATIVE.md`）。其它 GM 任务 **类比** [MANAGER-EVAL-IMPROVEMENT-LOOP.md](./MANAGER-EVAL-IMPROVEMENT-LOOP.md)。

**铁律：** **L1 / aligned PASS ≠ Owner 满意。** 未满足本文 **§2 闭环** 前，**不得**把稿当「可筛选示范」或 routine 交 Owner。


## §2 · 自动多轮 evaluation 与压测（无人确认）

### 2.1 闭环定义（「足够好」）

同时满足：

1. **机器 gate PASS**（complete + kernel 6）  
2. **fusion 全 ✅**（或 challenge 无 ⚠️ 待加强）  
3. **有 `reference/gold.md` 时：** `norm_dist_candidate_ref` ≤ **`CEO_GOLD_NORM_MAX`**（默认 **0.45**）或 EVOLUTION-GAP 写明 Owner  spec 已满足三镜头  
4. **`research/<slug>-pitfalls.md` 存在** 且 Brief 至少回应其中 **2 条** 坑  
5. **`EVOLUTION-GAP-latest.md` 状态 = `READY`**

未满足 → **同会话继续轮次**，**勿问 Owner**。

### 2.2 轮次流程（Agent Must · 单会话）

```text
轮 1：gate-one-round → analyze-brief-evolution-gap.py（baseline）
轮 2+：读 EVOLUTION-GAP + CEO-REROUTE + challenge L2–L3 → 实质性改稿（非禁词补丁）
      → gate-one-round → analyze（记录与 baseline / 与 gold / 与上轮 的距离）
直到 READY 或 轮次 = CEO_EVOLUTION_MAX_ROUNDS（默认 6）
```

**命令（单篇）：**

```bash
bash scripts/manager-brief-evolution-until-gap.sh --brief content/xiaohongshu/<slug>-brief.md
```

- **exit 0** · READY  
- **exit 42** · 须改稿后再跑（Brief 未变或 gap 未闭合）  
- **exit 1** · 达 max 轮仍未 READY → 交 Owner 裁决（**交 Owner：是**）

**工作流测试稿** 在 §2 闭环 **之后** 仍 Must：`bash scripts/ceo-workflow-test-round2-finish.sh`（01–12 campaign 压测 · 勿问 Owner）· [CEO-WORKFLOW-TEST-SOP.md](./CEO-WORKFLOW-TEST-SOP.md)。

### 2.3 距离 / 差距（Must 落盘）

| 度量 | 工具 | 用途 |
|------|------|------|
| 与 gold | `evaluate-edit-distance.py` → `metrics.jsonl` | 终极目标距离 |
| 与上轮正文 | `versions/vN-*.md` + 编辑距离 | 轮间演进 |
| 与 baseline verify | `verify-logs/*-complete-*.json` 对比 | 哪条 L1/adversarial 变了 |
| 综合 | `analyze-brief-evolution-gap.py` | `EVOLUTION-GAP-latest.md` + **READY/NEEDS_WORK** |

每轮 **Analyze（Must 写进 EVOLUTION-GAP 或 ITERATION-LOG）：** 变好/变差项 · 距 gold 还差什么 · 下一轮只改什么（1–3 条）。

### 2.4 与双轮 SOP 关系

- **语义改稿多轮：** 本文 §2 + `manager-brief-evolution-until-gap.sh`  
- **改 INTEGRATION / prompt 的双轮：** [CEO-DOUBLE-ITERATION-SOP.md](../agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md)  
- 二者 **可串联**：Brief 先 §2 READY，再 double-iteration 改集成。


## §4 · Manager 派活记录 · 额外必报字段

- **搜坑：** pitfalls 路径 · 回应了几条  
- **对抗：** 本篇 L2–L3 编号 · fusion 是否全 ✅  
- **进化：** 轮次 n/N · **READY/NEEDS_WORK** · norm_dist（有 gold 时）  
- **压测：** 是否已跑 campaign 第二轮（测试稿）