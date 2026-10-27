# Data Analytics 集成 Prompt

> **Collector + Evaluator（Must）：** [../_shared/COLLECTOR-EVALUATOR.md](../_shared/COLLECTOR-EVALUATOR.md) · slot `09-analytics` · CSV/Owner _feed 进 intake；next-topics v0→vN

0. **与 04 叠加：** 复盘/选题建议须可被 [XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md) 引用（MANIFEST + snapshot + strategy + PDF 研究 MD）。

1. 读 `DATA-NEEDS.md`；Owner 导出 CSV/xlsx → inbox 或 `raw/xiaohongshu/` → `bash scripts/analytics-fetch.sh`。
2. 跑 `bash scripts/analytics-pipeline.sh`（试跑加 `--demo`）；读 `content/analytics/derived/next-topics-*.md` + `summary-*.json`。
3. 结合 `integration/IMPORTANT.md` + IP Brief 写 **简短复盘**；**不编造** 未导入的平台数据。
4. 将 **3 条 subject 建议** 交给 **04-xhs-topic-manager** 写 Brief → `evaluate --brief` → Manager `manager-workflow-verify.sh`。
5. **禁止** 用历史数据反改 kernel 6 case；若需改规则 → 05-kernel + Owner。
