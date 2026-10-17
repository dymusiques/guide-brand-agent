# 营销触达 → 小红书 · 术语（小白向）

## 04 是谁？

**04 = 小红书选题 Agent（Topic Manager）**  
职责：根据 IP 和触达计划，**写「笔记施工单」**，不是直接发小红书。

## Brief 是什么？

**Brief = 一篇 Markdown 施工单**，路径形如：

`content/xiaohongshu/2026-10-20-某主题-brief.md`

里面通常有：

- 笔记标题、钩子、正文要点、封面说明  
- 一块 **classifier JSON**（给 AI 审阅用）

**触达计划**（`content/marketing/`）回答「这一阶段推什么、给谁、私信什么」；  
**Brief** 回答「**这一篇** 笔记具体怎么写」。

## evaluate 是什么？

**evaluate = 用 Gemini 自动审这篇 Brief 是否对齐你的目标**（IP、强链接、不单品类绑定等）。

常用命令：

```bash
python scripts/evaluate-xhs-topic.py --brief content/xiaohongshu/你的文件-brief.md
```

终端里若 JSON 显示 **`"aligned": true`** 且退出成功 → 这篇可以当 **定稿方向**；  
**`aligned: false`** → 改 Brief 再 evaluate，**未过不算定稿**。

## 和触达计划的关系

```
触达计划（03 · marketing md）
    → 04 写 Brief
    → evaluate --brief
    → 你或团队按 Brief 发笔记
```

触达计划本身的审阅用：

```bash
python scripts/evaluate-marketing-campaign.py --file content/marketing/2026-10-brand-discovery-phase.md
```
