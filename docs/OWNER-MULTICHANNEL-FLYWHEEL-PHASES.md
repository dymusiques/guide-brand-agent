# 多平台飞轮 · 阶段 0 / 1 / 2（你最该记的一句口令）

真源：`integration/handoff/owner-multichannel-flywheel-phase.json`

## 你现在：阶段 0（积攒）

| 做 | 不做 |
|----|------|
| 小红书 Drive 导表 · LinkedIn/Medium inbox 填发帖数据 | **全链路写稿**（除非你下口令） |
| **每周**收 LinkedIn + Medium **选题** 5–10 条（Automation） | **SEO 三平台互链** |
| 偶尔 chat 讨论选题 | Agent **不替**你点各平台发送 |

积攒要攒多久？**没有固定日历终点**——用下面两条同时理解：

1. **建议门槛**（Agent 每周自检并告诉你）：  
   - LinkedIn、Medium 各 **≥2 次**发帖数据已 ingest  
   - 小红书 analytics **freshness PASS**  
   - 至少在阶段 0 过 **2 个自然周**、且你 **勾选过 ≥1 个选题**  
   → 满足后会在选题文末提示：**可以说「进入写稿阶段」**。

2. **真 trigger（以你为准）**：随时一句 **`进入写稿阶段`** 或 **`派活给 CEO` + 具体选题** → 机械层按 **阶段 1** 跑满链（evaluate · 交付包 · 互链准备）。

自检命令：

```bash
cd ~/Desktop/danying-brand-agent
python3 scripts/check-owner-flywheel-phase.py
```

## 阶段 1 · 写稿战役

- Owner：**派活给 CEO** + goal（或勾选后的选题）  
- Agent：各平台 **交付包**（简报 + 架构 + 完整文稿 + 为什么）  
- 小红书仍走现有 Brief/HTML；LinkedIn/Medium → `content/deliverables/*/*-pack.md`

## 阶段 2 · SEO 互链（写稿时再接）

- Owner 口令：**开启跨平台互链** / **三平台 SEO**  
- 或单篇写稿时 Agent **主动问**要不要在交付包里上 Medium↔LinkedIn↔小红书链接  
- 阶段 0 你可以一直说「先不要」

## 与现有每周选题 Automation 的关系

| Automation | 侧重 |
|------------|------|
| 周日 11:00 · 每周选题包 | 跨平台（含小红书）· evaluate 闭环 |
| **周日 12:00 · LinkedIn + Medium 选题** | **仅**领英 + Medium · 阶段 0 主用 · 指令见 [OWNER-WEEKLY-LI-MEDIUM-TOPIC-AUTOMATION-INSTRUCTIONS.md](./OWNER-WEEKLY-LI-MEDIUM-TOPIC-AUTOMATION-INSTRUCTIONS.md) |

阶段 0：**只勾选、只积攒；不勾选不写稿。**