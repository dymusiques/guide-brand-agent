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

总览：[docs/DANYING-BRAND-AGENT-INTEGRATION.md](../docs/DANYING-BRAND-AGENT-INTEGRATION.md)

**Owner 给目标 → 自动 00 Manager：** [00-manager/AUTO-WORKFLOW.md](00-manager/AUTO-WORKFLOW.md)（`.cursor/rules/danying-manager-auto.mdc`）
