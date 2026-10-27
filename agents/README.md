# agents · danying-brand-agent

所有目标任务 Agent 分角色目录（集成 prompt，非算法层）。

| 目录 | 角色 |
|------|------|
| `00-manager/` | 总 Manager · Manager's Loop |
| `01-personal-ip/` | IP & 战略 |
| `02-business-brand/` | 商业品牌 |
| `03-marketing-strategy/` | 营销 |
| `04-xhs-topic-manager/` | 小红书选题 |
| `05-xhs-kernel/` | Classifier 核心 → `kernels/xiaohongshu/` |
| `06-xhs-content-pipeline/` | Brief 批量管线 |
| `07-brand-visual/` | 视觉 |
| `08-platform-integration/` | gdocs/Drive/OAuth |
| `09-data-analytics/` | 小红书数据 → 下一选题 |
| `10-artist-benchmark/` | **日更** · Artist 对标 · timeline · 借鉴分 |
| `11-ip-daily-evaluator/` | **日更** · IP challenge · rollups 筛选 |
| `12-owner-daily-brief/` | **日更** · 汇总 → Owner daily brief |

总览：[docs/DANYING-BRAND-AGENT-INTEGRATION.md](../docs/DANYING-BRAND-AGENT-INTEGRATION.md)

**Owner 给目标 → 自动 00 Manager：** [00-manager/AUTO-WORKFLOW.md](00-manager/AUTO-WORKFLOW.md)（`.cursor/rules/danying-manager-auto.mdc`）

**全仓集成构建：** `bash scripts/verify-all.sh` · 每 Agent 融合验：`bash scripts/verify-agent-fused.sh --agent 04`（A matrix + B 05 + C 日更）· [docs/VERIFY-AGENT-FUSED.md](../docs/VERIFY-AGENT-FUSED.md) · 目标表：[integration/GOALS-REGISTRY.md](../integration/GOALS-REGISTRY.md)
