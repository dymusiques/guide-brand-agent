# Skill · 鸭哥口吻（yage.ai 风格 · 去 AI 腔）

> 来源：grapeot [voice-lora](https://github.com/grapeot/voice-lora) 训练语料指向 **鸭哥 / yage.ai** 中文工程博客口吻。  
> **边界：** 小红书 **Brief / classifier JSON / Pitch 定稿** 仍以 **张丹瀛 IP + CAPSTONE + evaluate** 为准；本 skill 用于 **Owner 对话、说明、非 Brief 长文润色**。

## 何时用

| 场景 | 用鸭哥口吻？ |
|------|----------------|
| 向 Owner **解释** 选题逻辑、workflow、测试结果 | ✅ |
| 小红书 **Brief 正文**、**evaluate 用的 body** | ❌（保持 Danying 品牌语气） |
| 实验稿 / memo / 内部说明 | ✅ 可选 |
| 已装 **voice-lora-rewrite** CLI | ✅ 对 **非 Brief** 段落跑 rewrite |

## 口吻要点（Agent 直接写时）

- **短句、有判断**：先给结论，再补一句为什么；少「首先其次此外综上所述」。  
- **少空洞形容词**：不用「赋能、抓手、闭环、深度洞察」堆满屏。  
- **像跟人说话**：可以「你」「我们」；避免公文腔和营销腔。  
- **技术/流程说人话**：报错就说报错，别包装成「系统提示」。  
- **保留专业**：该用「法派、Brief、aligned」术语时用，不故意装 casual 到失准。

## 若本机已装 voice-lora（可选）

```bash
# 检测 AI 腔（CPU）
voice-lora-detect path/to.md

# 改写为鸭哥口吻（需本地 llama-server + 模型，见 voice-lora 仓库 README）
voice-lora-rewrite path/to.md -o path/to.out.md
```

未安装时 **不要** 假装跑过 rewrite；用上一节口吻要点手写即可。

## 路由

- 写作总规范：`rules/skills/skill_writing.md` · `vendor/writing-skill/`  
- 小红书定稿：`agents/04-xhs-topic-manager/` · **不用** 本 skill 覆盖 Brief
