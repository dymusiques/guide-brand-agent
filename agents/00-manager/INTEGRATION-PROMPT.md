# Manager 集成 Prompt（非算法层）

**任务入口（自动）：** [AUTO-WORKFLOW.md](./AUTO-WORKFLOW.md) — Owner 给目标即执行，无需口令。

1. 读 `integration/IMPORTANT.md` + AUTO-WORKFLOW 指挥链。
2. 拆任务到 `agents/<nn>-*/INTEGRATION-PROMPT.md`，**不**重写 classifier docstring。
3. 失败时沿 Loop：Analyze → Manual → Propose（只改集成/Brief/Skill）→ Observe → Re-run。
4. 必跑：`bash scripts/manager-workflow-verify.sh`（有 Brief 带路径）；改 kernel 加 `verify-xhs-topic`；交班 `verify-handoff`。
5. Owner 战略变更 → 派 **01-personal-ip** 改 Brief，再派 **04-xhs-topic-manager**。
