# Owner 成功标准 · 指标地图（Agent Must 读）

> **结论：** 对 Agent，**越具体越好**——但只能把 **可客观核对** 的项做成数字；**文笔像不像大 V** 不能伪造自动分，改用 **Rubric 自评 + 证据链 + Owner 一票**。  
> **Rubric JSON：** [`integration/handoff/owner-copy-success-rubric.json`](../integration/handoff/owner-copy-success-rubric.json)

## 为什么不是「全部一个总分」？

| 若全数字化 | 问题 |
|------------|------|
| 自动 NLP「像大 V」 | 假 PASS，和你终审冲突 |
| 只有 Owner 说好 | Agent 无自检尺，交付模糊 |
| **推荐：三层** | 机器硬门槛 + Rubric 软分数（须举证）+ Owner Gate |

## 三层成功（FluteBuddy 宣传 · IP 生态链 · 共用）

### L1 · 机器硬门槛（PASS/FAIL，有明确数）

| ID | 标准 | 数值/条件 | 验收 |
|----|------|-----------|------|
| L1-01 | 进化四维度 | 各 **≥80**/100 | `evolve-platform-hits.py` |
| L1-02 | Attestation 条数 | **≥3** 帖、**≥3** creator、**≥1** fresh、**≥1** 文化审美向 | `verify-owner-copy-v-tier-attestation.py` |
| L1-03 | Attestation 时效 | **≤30** 天（Brief 新改则刷新） | 同上 |
| L1-04 | 人话/脚手架 | 长稿 **≥80** 汉字等 | `verify-owner-copy-human-readable.py` |
| L1-05 | 小红书禁词 | 脚本 **PASS** | `xhs-copy-grep-banned.sh` |
| L1-06 | 长稿篇幅（XHS Brief） | **3000–5000** 字 | `OWNER-LONGFORM-XHS-SPEC.md` + extract |
| L1-07 | Clever 对抗（Brief） | **≥4** 反方等 | gap / clever verify |
| L1-08 | Evolution 闭合 | **READY** | `EVOLUTION-GAP-latest.md` |
| L1-09 | 进化轮次 | 默认 **≤6** 轮 | `CEO_EVOLUTION_MAX_ROUNDS` |
| L1-10 | 语料互动门槛 | 见 `engagement_floors`（如 LI **2000+** reactions） | corpus validate |

**L1 全 PASS** = Agent **可以** 交 Owner 审文笔，**不等于** 可以发布。

### L2 · Rubric 自评（有分数，Must 填证据；Agent 会话内）

每项 **0–100**，**加权**见 JSON；**低于项内 `min_score` → 禁止称定稿**，须改稿再评。

| 维度 | 含义 | min 示例 |
|------|------|----------|
| R-文化判断 | 现象/审美/艺术上下文，非 KPI 小标题 | 75 |
| R-私人叙事 | 具体场景/对话/态度，非手册体 | 75 |
| R-大 V 节奏 | 段长、钩子、一句一画面（对照 attestation URL） | 70 |
| R-轨一致 | IP：生活≥专业感；FB：家庭场景非 SaaS 列表 | 75 |
| R-露出合规 | 单篇 FluteBuddy/IP 产品露出 **≤30%** 篇幅体感 | 80 |
| R-三平台口吻 | 按 PLATFORM-HIT 口吻维对照 | 80 |

落盘：`content/xiaohongshu/rubric-scores/<brief-stem>.json`（与 attestation 同 stem）。

**L2 加权总分 ≥ `overall_min`（默认 80）** = Agent 自检「值得交 Owner」。

### L3 · Owner Gate（无数值替代）

| ID | 标准 | 谁定 |
|----|------|------|
| L3-01 | 文笔是否真到大 V / 文化审美档 | **Owner** |
| L3-02 | 是否发布到平台 | **Owner** |
| L3-03 | 业务结果（涨粉、waitlist、私信） | **Owner** + 日后 CSV/后台 |

**唯一「宣传成功」：** L1 PASS + L2 ≥ 线 + **L3-01 你口头/书面 OK**。

## 规划数字（不自动验收每篇）

| 项 | 数 | 用途 |
|----|-----|------|
| IP 维度配比 | 22/18/15/18/12/8/7 % | 选题规划，非单篇计分 |
| 周更 | XHS 2–3、LI 1–2 | 运营节奏 |
| P0 家庭 | 40 等 | FluteBuddy 战略，非 brand agent 自动判定 |

## Agent 交付前最小命令链

```bash
bash scripts/verify-owner-copy-v-tier-mandate.sh
.venv/bin/python scripts/verify-owner-copy-v-tier-attestation.py --brief <brief>
.venv/bin/python scripts/verify-owner-copy-human-readable.py --brief <brief>
.venv/bin/python scripts/score-owner-copy-success-rubric.py --brief <brief>   # L2
# 有 Brief 时再加 evolution / xhs-copy / delivery sh
```

## 与本仓定位

- **本仓成功** = 宣传/IP/产品 **叙事** 过关（L1+L2+L3-01）。  
- **FluteBuddy 产品成功**（准不准、稳不稳）= **flute-practice-buddy** 仓，不在此表 L3 自动验。
