# 每周选题包 · 5–10 主题（跨平台）

真源：`integration/handoff/owner-owner-triggers.json` · `weekly_topic_pack`

## 目标

每周 **5–10** 个「主题包」（非仅小红书标题）：观点 + IP 契合 + 热点检索方向 + 建议平台（小红书 / LinkedIn / Medium），Owner 自选后发。

## 机械入口

```bash
cd ~/Desktop/danying-brand-agent
python3 scripts/owner-weekly-topic-pack.py
```

## 输入

| 来源 | 用途 |
|------|------|
| IP Brief | 观点与边界 |
| `analytics-pipeline` / `next-topics-*.md` | 数据支柱 |
| `owner-pending-videos-eval-*` | **evaluate baseline** · 避免重复待发题 |
| `chat-sparks/*.md` | 聊天/网上启发 |
| Gemini（有 Key） | 扩写到 5–10 条 |

## 输出

- `content/strategy/weekly-topic-pack/weekly-topic-pack-<date>.md`
- `integration/handoff/owner-weekly-topic-pack-latest.json`（Layer C · ignore）

## Cursor Automation

- **每周日 11:00 GMT+8** · `0 11 * * 0`
- 名称：`品牌仓 · 每周选题包`
- 指令见 `docs/OWNER-WORKSPACE-HYGIENE.md` 同目录下 Automation 草稿

Automation 内 Agent **Must**：

1. 跑 `owner-weekly-topic-pack.py`
2. Web 检索补强每条 `hot_search_hint`（Google 趋势/新闻，注明日期）
3. 中文交付 5–10 条；Owner 回「派活给 CEO」才进满链

## 与「派活给 CEO」

选题选定后 → Owner 说 **派活给 CEO** → 见 [OWNER-CEO-FULL-STACK-TRIGGER.md](./OWNER-CEO-FULL-STACK-TRIGGER.md)