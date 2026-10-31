---
context_version: "2026-10-30-l012"
repo_path: "agents/_shared/BRIEF-ADVERSARIAL-CHALLENGE.md"
goal: "Brief 重对抗 · 全 GM 必跑（Owner 2026-10-27 · 2026-10-28 扩）"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "e4c26124489f0da6"
---

# Brief 重对抗 · 全 GM 必跑（Owner 2026-10-27 · 2026-10-28 扩）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **CEO 派任何写 Brief / 交 Owner 任务时，下属 GM 不得跳过。** Owner **不必**重复叮嘱。  
> **总纲（Must 先读）：** [docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../../docs/OWNER-XHS-ADVERSARIAL-AND-EVO
- **Path:** `agents/_shared/BRIEF-ADVERSARIAL-CHALLENGE.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **写前（Must · 在 redteam-pre 之前或同时）**: 1. [BRIEF-PITFALLS-RESEARCH-SOP.md](../../content/xiaohongshu/BRIEF-PITFALLS-RESEARCH-SOP.md) → `res…
- **三层对抗（由浅到深）**: | 层 | 产物 | 脚本 |
- **谁 Must 跑**: | GM | 何时 |
- **一条命令（全仓）**: ```bash
- **写后 · 多轮进化（Must · 勿问 Owner）**: ```bash
- **文档**: - [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../../docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MA…


---

## L2 正文

# Brief 重对抗 · 全 GM 必跑（Owner 2026-10-27 · 2026-10-28 扩）

> **CEO 派任何写 Brief / 交 Owner 任务时，下属 GM 不得跳过。** Owner **不必**重复叮嘱。  
> **总纲（Must 先读）：** [docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../../docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) — 搜坑 · 三镜头 · L2–L3 · 多轮 gap 直到 READY。

## 写前（Must · 在 redteam-pre 之前或同时）

1. [BRIEF-PITFALLS-RESEARCH-SOP.md](../../content/xiaohongshu/BRIEF-PITFALLS-RESEARCH-SOP.md) → `research/<slug>-pitfalls.md`（WebSearch ≥3）  
2. [BRIEF-THREE-LENS-SOP.md](../../content/xiaohongshu/BRIEF-THREE-LENS-SOP.md) → 进 **正文**  
3. [BRIEF-REDTEAM-PRE.md](../../content/xiaohongshu/BRIEF-REDTEAM-PRE.md) → ≥1 条 **L2–L3**（X2/X11 等）

## 三层对抗（由浅到深）

| 层 | 产物 | 脚本 |
|----|------|------|
| 轻 · redteam-pre | `content/xiaohongshu/redteam/<slug>-pre.md` | `ensure-redteam-pre.py` |
| **重 · 外部+对打+FULL-DRILL** | `content/xiaohongshu/challenge/<slug>-challenge.md` + HTML | **`run-xhs-brief-adversarial-challenge.py`** |
| 机器 · L1×6 + evaluate + kernel 6 | verify-logs JSON | `evaluate-xhs-brief-complete.py` |

## 谁 Must 跑

| GM | 何时 |
|----|------|
| **00 CEO** | 派活后 · 交 Owner 前 · `manager-xhs-briefs-auto-pipeline.sh` 或单篇 auto-gate-loop |
| **04 xhs-topic** | 写/改 Brief 后 **同轮** 跑 adversarial + complete |
| **01 personal-ip** | 读 challenge 节「融合 / 01 攻击」；FAIL 则驳方向回 04 |
| **09 analytics** | 读 challenge 节「类似低点击 / 数据 moment」 |
| **11 ip-daily-eval** | 日更 rollup 检查 `challenge/` 是否齐全 |
| **10/12** | 见 [SUBAGENT-DAILY-KIT.md](./SUBAGENT-DAILY-KIT.md) · challenge 步 = 本重对抗 + challenge-log |

## 一条命令（全仓）

```bash
bash scripts/manager-xhs-briefs-auto-pipeline.sh
```

## 写后 · 多轮进化（Must · 勿问 Owner）

```bash
bash scripts/manager-brief-evolution-until-gap.sh --brief content/xiaohongshu/<slug>-brief.md
```

- 每轮后读 `content/evolution/04-xhs-topic-manager/<slug>/EVOLUTION-GAP-latest.md`  
- **READY** 前禁止当定稿 / 筛选示范

## 文档

- [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../../docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md)
- [BRIEF-AUTO-GATE-PIPELINE.md](../../docs/BRIEF-AUTO-GATE-PIPELINE.md)
- [2026-10-27-ip-adversarial-red-team.md](../../content/personal-ip/2026-10-27-ip-adversarial-red-team.md)