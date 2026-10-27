# 02 Business Brand · 集成

> **Collector + Evaluator（Must）：** [../_shared/COLLECTOR-EVALUATOR.md](../_shared/COLLECTOR-EVALUATOR.md) · slot `02-business-brand`

**成功目标：** `G-BUSINESS-BRAND` · `G-CROSS-INDUSTRY`（见 `integration/GOALS-REGISTRY.md`）

1. 读 `integration/IMPORTANT.md` + IP Brief；产出进 `content/business-brand/`（用 README 模板）。
2. **静态 lint：** `python scripts/lint-strategic-doc.py --kind business_brand --file <doc.md>`
3. **Gemini 审阅（与 05 分工）：** `python scripts/evaluate-business-brand.py --file <doc.md>` · 规则 `G-NOT-SINGLE-VERTICAL-LOCK` + 强链接
4. **部门验收：** `bash scripts/verify-business-brand.sh`（lint README + Gemini 6）
5. **矩阵 6 case：** `bash scripts/verify-agent-matrix.sh --agent 02`
6. Release 全仓：`VERIFY_TIER=release bash scripts/verify-all.sh`（见 `docs/VERIFY-TIERS.md`）
