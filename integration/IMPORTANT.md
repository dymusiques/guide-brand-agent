# IMPORTANT · Manager / 集成层必读（<!-- important -->）

集成 Agent **只读本文件 + 各 agent 的 INTEGRATION-PROMPT**，**不复制** classifier docstring 全文。

## Owner 目标（P 层）

- **强链接** 客户：品牌（**跨行业 open**）、艺术家、教育、AI×数字藏品创新者 —— 非 vanity 流量。
- **质量涨粉：** 约 1700 → 5000 → 10000（小红书为主渠道之一）。
- **不是家居号：** 不主攻家居/建材；富森美类案例仅历史一笔，不作系列默认。

## 黑盒核心（勿在集成层改规则）

- `kernels/xiaohongshu/line2/is_xhs_growth_aligned.py`
- 验收：`bash scripts/verify-xhs-topic.sh`（**6 Gemini case**）

## 集成调用（胶水）

- 单条：`python scripts/evaluate-xhs-topic.py --brief content/xiaohongshu/<file>.md`
- 批量：`bash scripts/verify-xhs-content-dir.sh`
- IP 真相：`content/personal-ip/ip-positioning-brief-2026-10-05.md`

## 红线

- 未 `aligned: true` → 不 sync Drive；不只 Drive 不 commit。
- 集成层 **不写算法层 prompt**；失败时先区分：集成路径 / Brief 内容 / kernel。
