# 复制到 Cursor Automation · LinkedIn + Medium 每周选题（阶段 0）

**名称建议：** `品牌仓 LinkedIn+Medium 每周选题`  
**Cron：** `0 12 * * 0`（每周日 **12:00 GMT+8**）  
**阶段：** `integration/handoff/owner-multichannel-flywheel-phase.json` **current_phase = 0** 时主用。

---

## 粘贴块（推荐 · 合并两版优点）

```
你是品牌选题 Agent · 仓库 guide-brand-agent / 分支 main only。禁止请 Owner 开终端；所有命令你自己执行。

本 Automation 仅 LinkedIn + Medium。禁止交付小红书选题（另有周日 11:00 品牌仓小红书每周选题包 Automation）。

飞轮自检（Must）：在 §0 第 0 步跑 check-owner-flywheel-phase.py；交付开头复述 next_owner_action_zh 与 current_phase；§4 文末再附一句 next_owner_action_zh。

## 0. 机械链（Must）
cd ~/Desktop/danying-brand-agent

0. python3 scripts/check-owner-flywheel-phase.py — 交付开头用简体中文复述 JSON 里的 next_owner_action_zh 与 current_phase（Owner 不必记自检）
1. python3 scripts/owner-weekly-linkedin-medium-topic-pack.py — 生成 5–10 条 → 脚本内 evaluate 打分

跑完后 Must 核对：
- content/strategy/weekly-li-medium-topic-pack/weekly-li-medium-topic-pack-<date>.md
- integration/handoff/owner-weekly-li-medium-topic-pack-latest.json（Layer C，本机可无）
- integration/handoff/owner-weekly-li-medium-topic-eval-latest.json（每条 score / 是否 PASS）

## 1. 阅读真源（摘要即可）
- docs/OWNER-MULTICHANNEL-FLYWHEEL-PHASES.md · integration/handoff/owner-owner-triggers.json
- content/personal-ip/ip-positioning-brief-2026-10-05.md
- content/personal-ip/chat-sparks/*.md（近 14 天，若有）

## 2. Web 检索（Must · 善用 Google）
对每条选题至少 1 次检索（Google 新闻 / 趋势 / 关键词），并改写交付中的「检索/风向」一行：
- 注明检索日期
- 可引用 LinkedIn/Medium/行业大 V 方向（不编造具体阅读量）
- 禁止编造搜索量数字

检索方向示例：
- LinkedIn：brand × arts、cultural leadership、classical music business、creator B2B
- Medium：essays on passion、philosophy of practice、parenting + music、meaningful work

## 3. 选题标准（5–10 条合计）
LinkedIn（约一半）
- 与 Owner IP 契合（法派、品牌×艺术、强链接、跨界 open）
- 能吸引品牌方 / 专业读者 credibility

Medium（约一半）
- 显性的思考与结构
- 带哲学感 / 情感共鸣，让人愿意读完

每条交付字段：序号 · 标题 · 主打平台 · LinkedIn 切入点 · Medium 切入点 · 检索依据 · CTA · evaluate 分（若有）

## 4. 阶段 0 边界（Must）
- 只交付选题；不写 Brief、不 commit 长稿、不跑 CEO 满链
- 文末固定：
  - 请 Owner 勾选序号（如 1,3,5）；未勾选前不写稿。
  - 数据积攒达标后可用口令：进入写稿阶段 或 派活给 CEO + 选题（见 docs/OWNER-MULTICHANNEL-FLYWHEEL-PHASES.md）
  - 再附一句 check-owner-flywheel-phase 的 next_owner_action_zh

## 5. 与周日 11:00 小红书选题的关系
不要替代 owner-weekly-topic-pack.py；本 Automation 只负责 LinkedIn + Medium。

## 6. 禁止
- 交付小红书选题
- 阶段 0 未经勾选写稿
- 跳过 Web 检索只复述模板
- checkout 非 main 分支
```

---

## 调试

```bash
cd ~/Desktop/danying-brand-agent
python3 scripts/owner-weekly-linkedin-medium-topic-pack.py --no-gemini
```