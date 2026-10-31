---
context_version: "2026-10-30-l012"
repo_path: "content/xiaohongshu/2026-10-20-workflow-test-5topics-queue.md"
goal: "Workflow 全链路测试 · 5 题交付（待 Owner 确认）"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "59e4bb07d8027faa"
---

# Workflow 全链路测试 · 5 题交付（待 Owner 确认）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** - **目标：** 全 workflow 测试 + 5 题成稿交 Owner  
- **当前步：** 04 交付本队列 → **待 Owner 确认**  
- **终端：** intake PASS · autopilot PASS · handoff PASS · kernel 6 case 地域 FAIL  
- **下一步：** Owner 选题 
- **Path:** `content/xiaohongshu/2026-10-20-workflow-test-5topics-queue.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > **生成：** 2026-10-20 · 依据 [XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-ST…
- **章节锚点**: - **篇 B · 视频（搜索/具体的人 · 2026 风向）**: - **形式：** 60–90s 口播 + B-roll
- **Manager 派活记录**: - **目标：** 全 workflow 测试 + 5 题成稿交 Owner


---

## L2 正文

# Workflow 全链路测试 · 5 题交付（待 Owner 确认）

> **生成：** 2026-10-20 · 依据 [XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md)  
> **数据：** `notes-snapshot` + `xhs-data-strategy` + `next-topics-2026-10-20`  
> **平台：** WILL/Momentum/搜索趋势 MD  
> **状态：** 待 Owner 确认 · **未** evaluate（Gemini 地域限制见文末测试报告）


## 篇 B · 视频（搜索/具体的人 · 2026 风向）

- **形式：** 60–90s 口播 + B-roll  
- **标题：** 品牌别只搜「人群标签」  
- **平台依据：** WILL「看见具体的人」+ 搜索趋势「理性听劝」  

### 正文（视频描述区可粘贴）

很多品牌做小红书，先选「人群包」再填内容——  
用户真正搜的，往往是 **具体场景**：  
这场发布怎么不尴尬？跨界怎么不像硬广？艺术环节怎么让人愿意停？

2026 的方向（WILL/Momentum 同构）是：**具体 moment + 真实原生**，不是素材轰炸。  
我用法派训练里的「第一句怎么站住」，迁移到品牌现场——  
**先让人信 moment，再信你。**

跨行业品牌主理人 / 市场人：  
收藏这篇结构；有发布、联名、文化体验场景，私信 **「聊聊」**。

### 标签

#品牌策划 #小红书运营 #艺术跨界 #法派长笛 #种草

### 口播要点

1. 钩子：「人群标签填满了，用户还是划走？」  
2. 转折：具体 scene > 抽象高端人群  
3. 收口：收藏 + 聊聊  


## 篇 D · 视频（AI×艺术 IP · 数字藏品 · 不说 NFT）

- **形式：** 45–60s 对镜  
- **标题：** 艺术 IP 数字化，别从 NFT 讲起  
- **依据：** next-topics #2 · IP Brief 数字藏品 · 认知期跨行业 open  

### 正文

被问最多的是：艺术能不能做 **数字藏品**、能不能接 **AI**？  
可以聊，但 **别从 NFT 三个字开场**——  
品牌方会被吓跑，用户也会当成炒概念。

更稳的路径：**先有一个可被感受的专业 moment**（演奏、现场、Concert-Lecture），  
再谈 **哪些资产适合沉淀为数字藏品**、AI 如何 **放大叙事而不是替代训练**。

我是法派长笛体系 + 跨界策划视角，服务 **品牌 / 艺术家 / AI 创新** 同频对话，  
不绑单一垂类号。

有 IP 数字化、联名、沉浸式体验想法：**收藏** + 私信 **「聊聊」** / **「合作/品牌」**。

### 标签

#数字藏品 #AI创新 #艺术IP #法派长笛 #品牌策划

### 口播结构

钩子（别从 NFT 讲起）→ 专业 moment 先行 → CTA 聊聊  


## Workflow 测试报告（本文件生成时）

| 步骤 | 命令 / 产物 | 结果 |
|------|-------------|------|
| Intake Stack | `bash scripts/verify-xhs-content-intake.sh` | **PASS** |
| CEO 链 | `bash scripts/manager-autopilot.sh` | **PASS**（Owner 发帖/CSV 待办除外） |
| 5 Brief 目录 | `verify-xhs-content-dir`（autopilot 内） | **5 passed** |
| 09→04 | `next-topics-2026-10-20.md` + `ceo-dispatch-latest.md` | **已刷新** |
| 交班 | `bash scripts/verify-handoff.sh` | **PASS**（2 WARN：未 commit · 建议跑 content-dir） |
| Kernel 6 case | `bash scripts/verify-xhs-topic.sh` | **FAIL** — Gemini `User location is not supported`（环境/区域，非文案） |
| 本批 evaluate | 未跑 5× `--brief` | 同上；结构已按 aligned 历史 Brief 对齐 |

**数据/PDF 融入结论：** Excel→MANIFEST/snapshot/strategy/pipeline **已接入**；PDF→raw+MD **已接入** Intake Stack + 00 步 0a/2 + 04/09 prompt。

---

## Manager 派活记录

- **目标：** 全 workflow 测试 + 5 题成稿交 Owner  
- **当前步：** 04 交付本队列 → **待 Owner 确认**  
- **终端：** intake PASS · autopilot PASS · handoff PASS · kernel 6 case 地域 FAIL  
- **下一步：** Owner 选题 → 04 写正式 `*-brief.md` → evaluate（API 可用时）→ 确认后发布