# 聊天启发 · Chat Sparks

Owner 从对话或网上摘的 **观点种子**，供选题/Brief/CEO 派活引用（非定稿正文）。

## 何时写入

- Owner 说：**归到聊天启发** / **记入启发** / **记进启发** / **spark**
- Agent 从对话提炼 **一句主张 + 来源（chat | url）+ 日期**

```bash
python3 scripts/owner-chat-spark-append.py --title "标题" --claim "主张一句" --source chat
# 网上摘抄：--source url --source-ref "https://..."
```

## 文件约定

- 一条一文件：`YYYY-MM-DD-<slug>.md`
- 模板见 `_TEMPLATE.md`

## 与架构关系

- **不代替** `content/xiaohongshu/*-brief.md`
- 每周选题脚本 `owner-weekly-topic-pack.py` **可读** 本目录作额外输入
- 定稿进 Brief 前仍过 gate / evaluate