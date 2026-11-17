# CEO 派活前预检（deep 锁 · 勿叠派活）

> Owner **不必**记 `ls /tmp/ceo-deep-delivery.lock`。说 **「派活给 CEO」** 时，Agent 在满链里**自动**跑本预检。

## 命令（Agent / 终端）

```bash
cd ~/Desktop/danying-brand-agent
python3 scripts/ceo-dispatch-preflight.py --json          # 只看状态
python3 scripts/ceo-dispatch-preflight.py --recover       # 强制 recover
python3 scripts/ceo-dispatch-preflight.py --for-full-stack  # 与满链 gate 相同
```

机械真源：`integration/handoff/ceo-dispatch-preflight-latest.json`

## 自动接入点

| 时机 | 行为 |
|------|------|
| `agent-owner-research-gate.py` · `ceo_full_stack_goal` | `preflight_for_full_stack()` → 再 `ceo_campaign_wait_for_deep` |
| `run_ceo_full_execution.py` · 满链 | 同上 |
| `ceo-start-work.sh` | 开头打印预检摘要（recover 仍走原脚本） |

## 预检做什么

1. **僵尸锁**：锁文件里 pid 已死 → 删除 `/tmp/ceo-deep-delivery.lock`
2. **是否在跑**：锁 pid 存活 **或** `pgrep run-ceo-deep-delivery-cycle`
3. **最近 deep 日志**：未 `RESULT: PASS` / 尾部的 FAIL → 标记 `should_run_recover`
4. **多个 deep 根进程** → 自动 `bash scripts/ceo-auto-recover-blocked.sh`（满链默认开启）
5. **deep 真在跑** → **不** recover（避免杀进行中的交付）；满链最多等 `CEO_CAMPAIGN_WAIT_DEEP_SEC`（默认 900s）

## Owner 习惯（人话）

| 情况 | 你做啥 |
|------|--------|
| 要大派活 | 直接说「派活给 CEO + goal」即可 |
| deep 在跑 | **别**第二条满链口令叠上去 |
| 经常等满 900s | 看 `ceo-dispatch-preflight-latest.json`；Agent 跑 `--recover` 或查 [CEO-AUTO-RECOVER-AND-RETRY.md](./CEO-AUTO-RECOVER-AND-RETRY.md) |

## 相关

- [OWNER-CEO-FULL-STACK-TRIGGER.md](./OWNER-CEO-FULL-STACK-TRIGGER.md)
- [CEO-AUTO-RECOVER-AND-RETRY.md](./CEO-AUTO-RECOVER-AND-RETRY.md)
- `scripts/lib/ceo-deep-delivery-lock.sh`