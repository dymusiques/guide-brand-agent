# Owner · Git 提交分层与噪音提醒（Agent Must）

> **Owner 约定（2026-11-07）：** 战略 baseline **可以**进 Git 当备份；但这类文件**会持续小改**。  
> **Agent 在帮 Owner commit 前 Must** 读本页 + `integration/handoff/owner-git-commit-policy.json`，并按类型 **口头提醒** Owner 是否有噪音、是否应拆 commit / 排除 runtime。

## 三层（不要混在一个 commit 里除非 Owner 明确要求）

| 层 | 典型路径 | 是否进 Git | 噪音风险 | Agent 提醒话术 |
|----|----------|------------|----------|----------------|
| **A · 规则/脚本包** | `docs/CEO-*`, `integration/handoff/owner-*-track.json`, `scripts/verify-*`, `.cursor/rules` | ✅ 应 commit | 低 | 「规则包：改完即 commit，新机必 pull。」 |
| **B · 战略 baseline** | `*-strategy.md`, `flutebuddy-xhs-videos.json`, `content/xiaohongshu/*-brief.md`, `drafts/`, `intake/*-2026-*` | ✅ Owner 要备份时 commit | **高**（小改频繁） | 「这是 baseline 快照；之后每次改 brief/JSON 都会产生 diff。建议：只 stage 本次审定文件，或等冻结再 commit。」 |
| **C · 运行时** | `CEO-RUN-MANIFEST-latest.*`, `OWNER-XHS-FILTER-DELIVERABLE-*`, `daily-gm-summary-*`, `background-cycle-*`, `corpus-screens/`, `ceo-drive-catalog-live.json`, `*-latest.json`（context 解析） | ❌ 默认不 commit | 极高 | 「这些是 pipeline 输出，应本地/Drive 保留；clone 后脚本再生。」 |

### Layer C · research-gate handoff（永不进 Git）

- **`integration/handoff/owner-research-gate-latest.json`** 以及 **`integration/handoff/owner-*-latest.json`** = 每次 `research-gate` / `content-session` / hydrate 等**跑完才写**的快照，不是仓库真理源。
- **Must not commit**：即使本地 `status=PASS`，进 Git 也会让新 Agent / 新机器误认「不用真跑 gate」。
- **Clone 后没有这些文件是正常的** → 按合同跑 `agent-owner-research-gate.py` 或 `agent-workflow.py brand research-gate` 再生；`.gitignore` 已拦 re-add。
- **Mechanical 真源**（应 commit）：`integration/handoff/agent-owner-research-gate-contract.json`、`agent-gate-layer-union.json` — 只描述管子，不存某次 PASS 结果。

## B 层：baseline 快照命名建议

- Commit message 含 **`baseline`** 或 **`snapshot YYYY-MM-DD`**，便于以后 `git log` 区分规则 vs 内容。
- **HTML 交付页**（`OWNER-*-DELIVERABLE-*.html`）默认 **不** 跟 brief 同 commit（可 `build-*.py` 重建）；Owner 若要「当时长什么样」再单独 snapshot commit。

## Agent 工作流（Must）

1. Owner 说「commit baseline / 战略定稿 / 规则包」→ 跑 `git status`，按上表 **分类列出** staged / 未 staged。
2. **Must 提醒** 若 staged 含 B+C 混合，或 C 误入。
3. **Must 对 Owner 说出下面整句（原话，不可省略）** — Owner 靠这句话记得要筛噪音：

   > **「这次 commit 可能会有噪音（尤其是 brief / 战略 JSON / 交付 HTML 小改）。建议你先跟我一起检查一遍 git status，把 runtime 和不想进历史的文件从 stage 里拿掉。」**

4. 仅当 Owner 确认（或已明确「就 commit baseline」）再 `git commit`。
5. **每一次** 再 commit B 类、规则包或整包时：**重复第 3 步整句**，不要假设 Owner 已记得。

## 相关

- [HANDOFF-COMPLETENESS.md](./HANDOFF-COMPLETENESS.md) L0 Git 真相源  
- [AGENT-TAKEOVER.md](./AGENT-TAKEOVER.md)
