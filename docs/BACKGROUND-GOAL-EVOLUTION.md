# 后台目标链 · Baseline + Evaluator + 验收（Owner 只 setup 一次）

> **Owner（2026-10-27）：** 一条 CLI setup 后后台自转；**不要**日常「一键 autopilot」。  
> **频率：** **每天 1 次** · **09:00** · `Asia/Shanghai`（含 Gemini 6 case）。  
> **改频率：** Agent 见 [BACKGROUND-CYCLE-INTERVAL-TRIGGER.md](../integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md) — **须先问 Owner**。

---

## 「一轮 cycle」是什么意思？里面有什么？

**cycle** = 后台自动执行 **一次** `scripts/background-goal-evolution-cycle.sh`（约数分钟，视 Gemini/网络而定）。**不是** 30 分钟里一直占满 CPU；旧版曾每 30 分钟触发一次，**已改为每天一次**。

| 顺序 | 步骤 | 作用 |
|------|------|------|
| 1 | `verify-collector-evaluator` | Collector/Evaluator 脚本 smoke |
| 2 | `verify-xhs-content-intake` | 写稿数据栈文件在仓 |
| 3 | `verify-goals` | M4 · G-* 与 evaluate 钩子 |
| 4 | `verify-xhs-topic` **6 case** | 05 对齐 kernel（**每日** `GOAL_EVOLUTION_DEEP=1`） |
| 5 | `analytics-pipeline` | 有 CSV 用真数据，否则 demo 刷新 |
| 6 | `ceo-dispatch-refresh` | 09→04 派活块 |
| 7 | `manager-dashboard` | CEO 仪表盘 md |
| 8 | `evolution-rollups-all` | 全仓 `metrics.jsonl` 汇总 → baseline/距离趋势 |
| 9 | `agent-work-queue.md` | 缺 redteam-pre 的 Brief 等 · 给 Cursor CEO |
| 10 | SEO lint | 非阻塞 |
| 11 | **`run-daily-gm-trio.sh`** | GM10 Artist · GM11 IP eval · GM12 **Owner daily brief** |

产出：`ceo-inbox/background-cycle-latest.md` · `derived/background-cycle-latest.json` · `derived/evolution-rollups-latest.md`

**不自动做：** 写 Brief 正文、代发帖、Drive 覆盖、未 aligned commit。

---

## Owner 只做一次（改 schedule 后需重启 Launcher）

```bash
cd /path/to/danying-brand-agent
bash scripts/setup-background-goal-evolution.sh
```

**Terminal.app / iTerm2** 启动（或 **改 yaml 后重启**）：

```bash
cd vendor/process-launcher
../../.venv/bin/process-launcher start --config config/dba-brand-agent.yaml
# 或：cd 到 repo 根 && source .venv/bin/activate && cd vendor/process-launcher && process-launcher start ...
# 若已在跑：Owner 在 GUI 终端 Ctrl+C 停掉再 start
```

---

## 和 Cursor / CEO 的分工

```text
每日 cycle → verify + metrics + 队列 + dispatch
Cursor CEO → 读 agent-work-queue · 写 v0/vN · 红队 1c · Gate → Owner 只确认发布/gold
```

---

## 环境

- [GEMINI-NETWORK-AUTO.md](./GEMINI-NETWORK-AUTO.md)  
- [integration/process-launcher-adoption.md](../integration/process-launcher-adoption.md)  
- [OWNER-INPUT-PRINCIPLES.md](./OWNER-INPUT-PRINCIPLES.md)

---

## 维护脚本（非 Owner 日常）

| 脚本 | 用途 |
|------|------|
| `background-goal-evolution-cycle.sh` | 单次 cycle（Launcher 每日调） |
| `background-goal-evolution-loop.sh` | 旧 **interval** 模式；**默认不用** |
| `manager-autopilot.sh` | 与 cycle 同逻辑的单次 Debug |

---

## TRIGGER（改间隔 / 改验收强度）

**Must 问 Owner：** [integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md](../integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md)
