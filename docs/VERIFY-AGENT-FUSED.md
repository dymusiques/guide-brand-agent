# verify-agent-fused · A + B + C 融合

**Owner 确认策略（勿回退成「每岗第二个 Gemini kernel」）：**

- **A** · 00–09 集成 matrix glue（`verify-agent-matrix.sh`）
- **B** · **仅 Brief → 05** Gemini 6 case（04/05 深融合）
- **C** · 10 schema+1 次 Gemini · 11/12 **本地 6 case + challenge/hygiene/gold**（无 05 克隆）
- **共用** · `shared_gold.py`（reference/gold）· `shared_traps.py`（X1–X12 · GM11 daily）

一条命令按岗跑齐三层（见下表）。

```bash
bash scripts/verify-agent-fused.sh --agent 04          # A + B（有 key 时 05 Gemini 6）
bash scripts/verify-agent-fused.sh --agent 11 --with-artifacts
bash scripts/verify-agent-fused.sh --agent all-daily --with-artifacts   # 10+11+12 L1
bash scripts/verify-agent-fused.sh --agent all-09      # 仅 matrix 00-09
SKIP_GEMINI=1 bash scripts/verify-agent-fused.sh --agent 05   # A only（B 跳过）
```

| 层 | 00–09 | 10 | 11 | 12 |
|----|-------|----|----|-----|
| **A** matrix 6 glue | ✅ | — | — | — |
| **B** 05 Gemini 6 | 04/05 挂接 | — | — | — |
| **C** L1 六 case + hygiene | — | schema JSON | eval+challenge+gold | brief 结构 |

**Daily cycle 已接入：** `run-daily-gm-trio.sh` 末尾 → `verify-daily-gm-trio.sh` → `all-daily --with-artifacts`（**仅本地 Python**，不增 Gemini）。

**未默认接入 daily：** `all-09` 全 matrix、04/05 的 **B 层 Gemini**（与 `background-goal-evolution-cycle.sh` 中 `GOAL_EVOLUTION_DEEP=1` 才跑 `verify-xhs-topic` 一致）。

## 成本与改 daily 幅度

| 改动 | daily 增量 | Gemini | 说明 |
|------|------------|--------|------|
| **本次：11/12 L1 + fused + trio verify** | **+约 1–3 秒** | **0** | 6 个本地 case × 2 + artifact 读盘 |
| 若 daily 加 `all-09` matrix | +约 5–30 秒 | 0 | 仅 glue |
| 若 daily 对 01–09 各跑 B 层 Gemini | +数分钟 | **+数十次/天** | 不推荐；保持 05 单点 |
| 若 daily 默认 `verify-agent-fused --agent 04`（含 B） | +15–30 秒 | +6 | 与 `GOAL_EVOLUTION_DEEP=1` 等价 |

交班 / Release：`VERIFY_TIER=release bash scripts/verify-all.sh` 仍为主 capstone；单岗深检用本脚本。
