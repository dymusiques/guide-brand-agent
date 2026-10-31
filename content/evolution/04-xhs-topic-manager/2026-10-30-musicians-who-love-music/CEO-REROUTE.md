# CEO-REROUTE · 2026-10-30-musicians-who-love-music · round 1

- at: 2026-10-31T09:01:34
- brief: `content/xiaohongshu/2026-10-30-musicians-who-love-music-brief.md`

## FAIL 项（自动检测）

- gate failed — inspect verify-logs JSON

## Prompt Change 提案（GM/AI 必填 · 改稿前填写）

- 改什么：（文件路径 + 段落）
- 一句 diff：
- 依据（FAIL / verify-logs）：
- 预期哪条 gate 变绿：
- 风险：

## GM Must（无人值守下一轮）

1. 完成上节 **提案** 再改 classifier JSON / 正文 / INTEGRATION-PROMPT
2. `python scripts/ensure-redteam-pre.py --brief …`（若 redteam 缺）
3. `python scripts/evaluate-xhs-brief-complete.py --brief …`
4. PASS 后更新 Brief Verify log · **GM-REPORT 本轮分析结论**

**Owner 不参与 verify。**