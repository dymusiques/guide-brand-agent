# Brief 重对抗 · 全 GM 必跑（Owner 2026-10-27）

> **CEO 派任何写 Brief / 交 Owner 任务时，下属 GM 不得跳过。** Owner **不必**重复叮嘱。

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

## 文档

- [BRIEF-AUTO-GATE-PIPELINE.md](../../docs/BRIEF-AUTO-GATE-PIPELINE.md)
- [2026-10-27-ip-adversarial-red-team.md](../../content/personal-ip/2026-10-27-ip-adversarial-red-team.md)
