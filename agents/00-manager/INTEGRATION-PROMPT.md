# Manager 集成 Prompt（非算法层）

**任务入口（自动）：** [AUTO-WORKFLOW.md](./AUTO-WORKFLOW.md) — Owner 给目标即执行，无需口令。

1. 读 `integration/IMPORTANT.md` + AUTO-WORKFLOW 指挥链。
2. 拆任务到 `agents/<nn>-*/INTEGRATION-PROMPT.md`，**不**重写 classifier docstring。
3. 失败时沿 Loop：Analyze → Manual → Propose（只改集成/Brief/Skill）→ Observe → Re-run。
4. 每轮派活前 / Owner 问进度：`bash scripts/manager-dashboard.sh`；交班 / 大改后：`bash scripts/verify-all.sh`；Brief 定稿：`manager-workflow-verify.sh <brief>`。
5. Owner 目标 ID 见 `integration/GOALS-REGISTRY.md`，派活时标注 `G-*`。
6. Owner 战略变更 → 派 **01-personal-ip** 改 Brief，再派 **04-xhs-topic-manager**。
