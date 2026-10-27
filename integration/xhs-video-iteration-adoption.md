# 集成 · 小红书视频迭代 + 声音锚定

> **胶水层路由：** 00 Manager 步 **2a**（视频 Round 1–3）→ 本文件 + `content/xiaohongshu/XHS-VIDEO-ITERATION.md`  
> **不改 kernel**；L1 仍用 `evaluate-xhs-topic.py`；L2 用 `verify-xhs-voice-qa.sh`。

## 何时走本链路

Owner 要：**视频标题/封面备选 · 像本人 · 迭代点选** → **Must** 本链路，**Skip** 旧「5 题一次性长正文测试队列」模式。

## Manager 步序（插入 AUTO-WORKFLOW 步 2a）

1. `verify-xhs-content-intake.sh`（L0）  
2. 读 `VOICE-ANCHOR.md` + `voice-anchor-sources.json` + `cv-source-2026-09-15.md`  
3. 产出 Round 1 MD → `verify-xhs-voice-qa.sh`（L2）  
4. Owner 点选 → Round 2  
5. （可选）Brief + evaluate（L1）

## Drive

- CV：`fileId=13vh69eCf_OaVY0DT9gj7AYifeq_wjmCt482cExcjf0k` → Git `content/personal-ip/cv-source-2026-09-15.md`  
- 小红书风向 PDF：已有 `content/marketing/research/xhs-platform-research-index.md`（Intake #5）

## 04 INTEGRATION-PROMPT

硬规则与禁词表已写入 `agents/04-xhs-topic-manager/INTEGRATION-PROMPT.md` §视频迭代 / §L2 QA。
