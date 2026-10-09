# Data Analytics 集成 Prompt

1. 读 `DATA-NEEDS.md`；Owner 导出 CSV → `content/analytics/inbox/` → `bash scripts/analytics-fetch.sh`。
2. 跑 `bash scripts/analytics-pipeline.sh`（试跑加 `--demo`）；读 `content/analytics/derived/next-topics-*.md` + `summary-*.json`。
3. 结合 `integration/IMPORTANT.md` + IP Brief 写 **简短复盘**；**不编造** 未导入的平台数据。
4. 将 **3 条 subject 建议** 交给 **04-xhs-topic-manager** 写 Brief → `evaluate --brief` → Manager `manager-workflow-verify.sh`。
5. **禁止** 用历史数据反改 kernel 6 case；若需改规则 → 05-kernel + Owner。
