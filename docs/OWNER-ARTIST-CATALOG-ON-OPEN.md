# Owner 打开对话 · Artist 对标一次性审阅（不每日提示）

> **Owner（2026-10-27）：** GM10 **每天**继续收集/分析 artist；**不要**每天提醒。  
> **Owner 打开本仓库对话时**，Agent **自动**对比目录，**一次性列全**待审条目，等 Owner 回复适合/不适合及原因。

## Agent Must（会话开头 · 有则做）

1. 跑或读最新：`content/ip-research/artist-intel-catalog.json`（daily trio 后 `merge-artist-intel-catalog.py` 会更新）
2. 读 `content/ip-research/artist-intel-review-state.json` 的 `last_owner_review_at` / `verdicts`
3. 若存在 **尚未 Owner 裁决** 的 catalog 条目 → **主动输出「Artist 对标待审清单」**（表格：日期、名字、composite、**DB/PLD/APO/CTD**、为何 evaluate、sources_note）
4. **不要**在 Owner 未开对话时发消息；**不要**每天 push「请审阅」

## Owner 怎么回复

- 「A 适合，因为…；B 不适合，因为…」→ Agent 更新 `verdicts` + 可选调整 `artist-watchlist.json` 权重/移除

## Watchlist 维护（Must）

- **新出现的、与 Owner 相关的 artist** → 必须加入 [`artist-watchlist.json`](../content/ip-research/artist-watchlist.json)，**每条至少 1 个可核查 `urls`**
- **P1/P2/P3** = Agent 建议优先级（见 [`content/ip-research/README.md`](../content/ip-research/README.md)），不是 kernel 字段

## 命令

```bash
python scripts/merge-artist-intel-catalog.py   # trio 已自动调用
```
