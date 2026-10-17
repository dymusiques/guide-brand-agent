# Owner 目标注册表（Goal Registry）

机器可读：`integration/goals/registry.json`  
Hook 映射：`integration/goals/verify_hooks.json`  
验收：`python integration/tests/test_goals_registry.py`（注册表结构 6 case）· **M4** `bash scripts/verify-goals.sh`（按 G-* 跑 hook，**非** kernel Gemini 6 case 整包 — 见 [docs/VERIFY-TIERS.md](../docs/VERIFY-TIERS.md#gemini-6-case-与-m4-分工)）

| ID | 目标 | 负责 Agent | 自动断言 |
|----|------|------------|----------|
| G-STRONG-LINK | 强链接、非 vanity | 00/01/04/05 | evaluate + Gemini 6 |
| G-QUALITY-GROWTH | 1700→5000→10k | 09/04 | **否**（CSV/Owner；不进 classifier） |
| G-NOT-SINGLE-VERTICAL-LOCK | 不单品类绑定；全品类可合作 | 01/02/03/04/05 | IP Brief + kernel（家居仅为曾误绑示例） |
| G-CROSS-INDUSTRY | 跨行业 open | 01/02/04 | IP Brief |
| G-BRIEF-ALIGNED-GATE | aligned 才定稿 | 00/04/06 | evaluate exit 0 |
| G-ANALYTICS-EVIDENCE | 有数才复盘 | 09/00 | analytics-pipeline |
| G-PLATFORM-SYNC | gdocs/Drive/Git | 08 | verify-integration 6 |
| G-BRAND-VISUAL | 封面与 kit | 07 | agent 07 verify 6 |
| G-MARKETING-CAMPAIGN | campaign Brief | 03 | M4：lint + evaluate 触达计划稿；整包 Gemini 6 → `verify-marketing-campaign.sh` |
| G-BUSINESS-BRAND | 商业品牌文档 | 02 | M4：lint + evaluate 当前 SWOT 稿；整包 Gemini 6 → `verify-business-brand.sh` |

**00 Manager** 读本表 + `integration/IMPORTANT.md`，派活时标注关联 `G-*`；**不**把粉丝 KPI 写进 kernel 6 case。
