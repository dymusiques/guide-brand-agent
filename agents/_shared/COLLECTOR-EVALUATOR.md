# 收集者 + Evaluator · 管理层级（CEO + 部门总经理）

> **组织：** [docs/IP-MANAGEMENT-HIERARCHY.md](../../docs/IP-MANAGEMENT-HIERARCHY.md) — **00 = CEO**；**01–09 = 部门总经理（二级 Manager）**，兼 Collector + 部门 Evaluator + 部门管理，**GM-REPORT 汇报 CEO**。  
> ** adoption：** [integration/collector-evaluator-adoption.md](../../integration/collector-evaluator-adoption.md)  
> **Owner 说明：** [docs/COLLECTOR-EVALUATOR-PIPELINE.md](../../docs/COLLECTOR-EVALUATOR-PIPELINE.md)

## 两个程序（每个 Agent 产出都要走）

### 1 · Collector（收集者）

**职责：** 吸收 Owner 当轮及历史喂入的 **一切资料**，再生成输出；不丢、不编造未入库内容。

| 动作 | 命令 / 路径 |
|------|-------------|
| 登记 Owner 输入 | `python scripts/collector-intake.py --agent <NN> --slug <artifact> --stdin` 或 `--file <path>` |
| 登记目录 | `content/evolution/<agent>-<name>/<slug>/intake/` |
| 索引 | 同目录 `manifest.json`（intake 列表 + 版本链） |

**Agent 写 v0 前 Must：** 读该 slug 下 **全部** `intake/*` + 本域真相源（如 04 另读 Intake Stack）。

### 2 · Evaluator（进化评估 · 编辑距离）

**职责：** 对当前版本文本做 **纠正稿**（写入下一版或 `versions/*-corrected.md`），并相对 **标准答案 reference** 计算 **编辑距离**。

| 动作 | 命令 |
|------|------|
| 度量 + 追加 metrics | `python scripts/evaluate-edit-distance.py --candidate versions/vN.md --reference reference/gold.md [--corrected versions/vN-corrected.md] --label vN --append metrics.jsonl` |

**版本命名：**

- **v0** — 首次综合 intake 后的产出（最初版本）  
- **v1, v2, …** — Evaluator/改稿进化；**纠正稿**可命名为 `vN-corrected.md`，下一版为 `v(N+1).md`  
- **reference/gold.md** — Owner 或已对齐定稿（标准答案）；未设 gold 时只存 candidate 链，不造假距离  

**汇总指标：** 对 `metrics.jsonl` 取 `dist_corrected_ref`（或 `dist_candidate_ref`）**平均值** = 该 artifact 进化收敛度。

**Owner 原则 · 基线与标准一起升高（内部内化）：** 随意输入 → Collector/intake；定稿 → gold；**内部** Skill/集成 prompt 迭代 → 同样口语输入 **译得更准**；**内部 Gate** 交 Owner 前自检。**不要求** Owner 说 evaluate 级提示词。见 [OWNER-INPUT-PRINCIPLES.md](../../docs/OWNER-INPUT-PRINCIPLES.md) · [COLLECTOR-EVALUATOR-PIPELINE.md §双螺旋](../../docs/COLLECTOR-EVALUATOR-PIPELINE.md#双螺旋基线升高--标准升高)。

## 与现有 gate 的关系

| 层 | 工具 | 测什么 |
|----|------|--------|
| **IP 进化（本文件）** | `evaluate-edit-distance.py` | 文本 ↔ gold **编辑距离**、版本链 |
| **小红书 aligned（05）** | `evaluate-xhs-topic.py` | Gemini 规则 yes/no |
| **声音 L2（04/2a）** | `verify-xhs-voice-qa.sh` | 禁词/像本人 |

Brief 定稿：**两者可并存** — 先 evolution 收敛，再 `aligned: true`（或 gold = aligned 定稿）。

## CEO（00）vs 部门总经理（01–09）

| 角色 | Collector | Evaluator + v0→vN | 管理 | 汇报 |
|------|-----------|-------------------|------|------|
| **CEO** | Owner 总目标、跨部门索引 | Gate + 打回 GM（[CEO-AUTO-QA-LOOP.md](../../docs/CEO-AUTO-QA-LOOP.md)） | 派活、步序、commit 门控、收 GM 报告 | → Owner（仅 gate PASS + 确认项） |
| **部门 GM** | **本部门全部 intake** | **Must**：本 slug 的 v0…vN + metrics | 本部门 INTEGRATION + verify | **GM-REPORT → CEO** |

CEO **不绕过 GM** 直接产部门 v0（除非 Owner 明确「CEO 代笔」单轮例外）。

**GM 汇报文件：** `content/evolution/<dept-slot>/<slug>/GM-REPORT.md`（模板见 IP-MANAGEMENT-HIERARCHY.md）
