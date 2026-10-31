---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-AUTO-RECOVER-AND-RETRY.md"
goal: "CEO · 中断 / 阻塞 / FAIL 自动恢复与重试"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "20de01157a891916"
---

# CEO · 中断 / 阻塞 / FAIL 自动恢复与重试

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner 原则：** CEO、campaign、deep-delivery 任务若被中断、阻塞、FAIL 或跑错路径，**Agent Must 自动**检测 → 诊断 → 修脚本或环境 → 换策略重试，直到闭合或达上限。**Owner 不必重复下口令。**
- **Path:** `docs/CEO-AUTO-RECOVER-AND-RETRY.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **何时触发**: | 信号 | 检测方式 |
- **流程（Detect → Diagnose → Fix → Retry → Escalate）**: 1. **Detect** — 锁文件、进程表、`*ceo-inbox/*.log` 末行与关键字。
- **环境变量（recover 脚本）**: | 变量 | 默认 | 含义 |
- **产物**: - 每次 recover：`content/evolution/00-manager/ceo-inbox/ceo-auto-recover-latest.md`（动作、pid、是否启动 nohup）。
- **相关**: - [CEO-OWNER-DEADLINE-DELIVERY.md](./CEO-OWNER-DEADLINE-DELIVERY.md)


---

## L2 正文

# CEO · 中断 / 阻塞 / FAIL 自动恢复与重试

> **Owner 原则：** CEO、campaign、deep-delivery 任务若被中断、阻塞、FAIL 或跑错路径，**Agent Must 自动**检测 → 诊断 → 修脚本或环境 → 换策略重试，直到闭合或达上限。**Owner 不必重复下口令。**

## 何时触发

| 信号 | 检测方式 |
|------|----------|
| 深交付锁占死 | `/tmp/ceo-deep-delivery.lock` 内 pid 已不存在 |
| 重复深交付进程 | `pgrep -f run-ceo-deep-delivery-cycle` 多于 1 个 |
| 深交付 log 未闭合 | 末行无 `RESULT: PASS ceo-deep-delivery`；或含 `syntax error` / `RESULT: FAIL` |
| Campaign 断在 Agent 02 | 最新 campaign log 有 `Agent 02` 无 `Agent 03`，且无 `RESULT: PASS ceo-ip-all-agents-campaign` |
| 脚本 exit 2 | 另一实例持锁（先 recover 再重试） |

**入口命令（Agent · 无人值守）：**

```bash
bash scripts/ceo-auto-recover-blocked.sh
```

会话规则见 `.cursor/rules/danying-manager-auto.mdc` · `integration/IMPORTANT.md`。

## 流程（Detect → Diagnose → Fix → Retry → Escalate）

1. **Detect** — 锁文件、进程表、`*ceo-inbox/*.log` 末行与关键字。
2. **Diagnose** — 区分：stale lock、重复 pid、脚本语法/环境、Gemini 超时、与 deep 并行导致的 `SKIP_GEMINI` 预期行为。
3. **Fix** — 清 stale lock；**谨慎**合并重复 deep 进程（保留 lock pid 或最早父进程）；修 repo 内已知脚本 bug；`VERIFY_GOALS_SKIP_PLATFORM=1` 等 env 见下。
4. **Retry** — 默认最多 **3 轮** recover 循环（`CEO_AUTO_RECOVER_MAX_ROUNDS`，跨会话由 Agent 读 `ceo-auto-recover-latest.md` 续跑）。  
   - 深交付重跑：`VERIFY_GOALS_SKIP_PLATFORM=1 CEO_DEEP_ROUNDS=2 bash scripts/run-ceo-deep-delivery-cycle.sh`（勿与第二条 deep 并行）。  
   - Campaign 重跑：`bash scripts/run-ceo-ip-all-agents-campaign.sh`（deep 仍跑时自动 `SKIP_GEMINI=1`）。
5. **Escalate to Owner** — 仅当：已达 N 轮仍 FAIL、需 **gold/发布/裁决**；**不要**为「要不要重跑」问 Owner。**Google：** 先 `check-google-auth-for-agent.sh`；PASS 则 **勿**因 OAuth chat 打扰 Owner（见 OWNER-GOOGLE-GRANT-AGENT.md）。

## 环境变量（recover 脚本）

| 变量 | 默认 | 含义 |
|------|------|------|
| `CEO_AUTO_RECOVER_KILL_DUP_DEEP` | `1` | 发现多个 deep-delivery 时，保留 1 个并 SIGTERM 其余（见脚本注释） |
| `CEO_AUTO_RECOVER_MAX_ROUNDS` | `3` | 文档级上限；单次脚本执行各动作至多 1 次 |
| `CEO_AUTO_RECOVER_DRY_RUN` | `0` | `1` 只写报告不杀进程、不启动重跑 |
| `VERIFY_GOALS_SKIP_PLATFORM` | `1` | 重跑 deep 时跳过 Drive 平台读（M4） |
| `CEO_DEEP_ROUNDS` | `2` | 重跑 deep 轮次 |

## 产物

- 每次 recover：`content/evolution/00-manager/ceo-inbox/ceo-auto-recover-latest.md`（动作、pid、是否启动 nohup）。
- 深交付 / campaign 各自 `ceo-*-*.log` · `*.md` 报告不变。

## 相关

- [CEO-OWNER-DEADLINE-DELIVERY.md](./CEO-OWNER-DEADLINE-DELIVERY.md)
- [CEO-AUTO-QA-LOOP.md](./CEO-AUTO-QA-LOOP.md)
- `scripts/lib/ceo-deep-delivery-lock.sh`