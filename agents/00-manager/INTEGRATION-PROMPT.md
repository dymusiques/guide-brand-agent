# Manager 集成 Prompt（非算法层）

1. 读 `integration/IMPORTANT.md`。
2. 拆任务到 `agents/<nn>-*/`，**不**重写 classifier docstring。
3. 失败时沿 Loop：Analyze → Manual → Propose（只改集成/Brief/Skill）→ Observe → Re-run。
4. 必跑：有 Brief 则 `verify-xhs-content-dir`；改 kernel 则 `verify-xhs-topic`；交班 `verify-handoff`。
5. Owner 战略变更 → 派 **01-personal-ip** 改 Brief，再派 **04-xhs-topic-manager**。
