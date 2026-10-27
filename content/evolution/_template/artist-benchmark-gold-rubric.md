# Artist 对标 · Evaluator 靶心（gold rubric · DB/PLD/APO/CTD）

**禁用 SWOT 作对外对标表**；使用四指标（`kernels/daily-gm/benchmark_framework.py`）：

| ID | 名称 | 问什么 |
|----|------|--------|
| **DB** | Directional Benchmarking | 其 career/内容 **战略方向** 是否与 Owner（法派×跨界×强链接×不绑单品类×AI 可选）**同向** |
| **PLD** | Pixel-Level Deconstruction | 封面/标题/钩子/栏目/CTA/日周更 **能否像素级拆解** 并迁移到 Owner 执行 |
| **APO** | Audience Persona Overlap | 受众是否与 Owner（品牌/艺术/教育/AI）**重叠**，且非纯 vanity |
| **CTD** | Core Topic Density | 核心题是否 **集中** 于专业+跨界+叙事，而非垂直锁号/跑题 |

- 必须含：**benchmark_metrics**（四指标各 score+rationale）· **borrow_score**（加权合成）· **why_evaluate** · **alignment_points**（≥3）· **timeline**（≥3）
- 必须对照 Owner IP Brief · 禁止捏造合同/收入
- 批量筛查：`python scripts/screen-artist-watchlist.py`
