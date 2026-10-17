# 03 Marketing Strategy · 集成

**成功目标：** `G-MARKETING-CAMPAIGN` · `G-STRONG-LINK`

1. Campaign / 渠道 Brief → `content/marketing/`（README 模板）。
2. **静态 lint：** `python scripts/lint-strategic-doc.py --kind marketing --file <doc.md>`
3. **Gemini 审阅：** `python scripts/evaluate-marketing-campaign.py --file <doc.md>`
4. **部门验收：** `bash scripts/verify-marketing-campaign.sh`
5. **矩阵：** `bash scripts/verify-agent-matrix.sh --agent 03`
6. 与 **04** 并列：campaign 定稿与 XHS Brief 均须各自 evaluate；**00** 用 Release 档 `verify-all`
