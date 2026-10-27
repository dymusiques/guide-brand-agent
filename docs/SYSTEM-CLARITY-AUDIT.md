# 系统清晰度审计 · danying-brand-agent

> **直觉校验：** 你的「有点乱」**部分成立** —— 不是架构散了，而是 **层叠多、历史队列并存、工具箱刚扩容**。  
> **交互地图：** [agent-ecosystem-map.html](./agent-ecosystem-map.html)（点节点看能力）· 原 CEO 闭环图：[workflow-mindmap.html](./workflow-mindmap.html)

**评级说明**

| 等级 | 含义 |
|------|------|
| 🟢 清晰 | 单一入口、规则互斥明确，Agent 不易走错 |
| 🟡 轻度凌乱 | 能跑，但要多读 1–2 份 MD 或存在并行「真相源」 |
| 🟠 中度凌乱 | 文档/队列/工具多，无索引易误用 |
| 🔴 重度凌乱 | 双 CEO、矛盾指令、验收缺口（**本仓当前无**） |

---

## 逐步审计表

| # | 步骤 / 环节 | 凌乱？ | 等级 | 说明（为何会有感觉） | Agent 防乱锚点 |
|---|-------------|--------|------|----------------------|----------------|
| 1 | 每会话读 SOUL / USER / integrations / WORKSPACE | 否 | 🟢 | 固定四件套，AGENTS.md 写死 | 不要跳过直接 grep |
| 2 | Owner 目标任务 → 自动 00 Manager | 否 | 🟢 | `danying-manager-auto.mdc` + AUTO-WORKFLOW | 纯解释可不跑 verify |
| 3 | **CEO 唯一性**（00 vs autopilot vs Launcher vs CLI） | 否 | 🟢 | EXTENSION-POINTS §0 写明「只留一套主路径」 | Launcher/CLI **默认不启** |
| 4 | 指挥链步序 0 → 0a → **2a** → 0b → 1 → … | **略** | 🟡 | 步号 **非连续**（2a 在 2 前），新 Agent 要扫表 | AUTO-WORKFLOW 表 = 唯一步序 |
| 5 | **0a 数据栈**（Excel/PDF/MANIFEST） | **略** | 🟡 | 文件多、路径深；换机要 raw/xlsx | `verify-xhs-content-intake.sh` + XHS-DATA-LAYER |
| 6 | **2a 视频迭代**（Round1–3 · 轨1） | **略** | 🟡 | 与旧「单 Brief 模板」并存；L2 禁词另层 | XHS-VIDEO-ITERATION + VOICE-ANCHOR |
| 7 | 04 写 Brief / packages | **略** | 🟡 | **两套队列**：discovery `*-brief.md` vs pivot `*-packages.md` | Owner 当前主 truth：**pivot A/B/C/E** |
| 8 | 03 evaluate + 05 kernel aligned | 否 | 🟢 | 硬门：`aligned: true` | manager-workflow-verify |
| 9 | 06 批量 Brief verify | 否 | 🟢 | 目录级 PASS/FAIL | verify-xhs-content-dir |
| 10 | Git 定稿 vs Drive 可选 | 否 | 🟢 | HANDOFF-COMPLETENESS | 未 aligned 不称定稿 |
| 11 | 09 → derived → 派 04 | 否 | 🟢 | ceo-dispatch 单文件 | 不建第二派活文件 |
| 12 | Owner App 发帖 | 否 | 🟢 | 刻意非自动化 | CONTENT-DELIVERY |
| 13 | **rules/skills vs .cursor/skills vs vendor** | **略** | 🟡 | 三层路由；INDEX 变长 | INDEX 只路由；Brief 走 xiaohongshu |
| 14 | **IP 13 工具 submodule** | **略** | 🟠 | 已全装；易误以为都要跑 | ip-content-skills-adoption **触发条件** |
| 15 | verify 脚本族（handoff / manager / voice / intake / ip-env） | **略** | 🟡 | 多个 bash；场景不同 | check.md + 各 adoption 写「何时跑」 |
| 16 | 并行 Task / Survey | 否 | 🟢 | 明文 **不替代** 04 写 Brief | tmp/ 不进定稿 |
| 17 | Phase 2 B站 / Insta360 | **略** | 🟡 | 渠道增多；与 XHS 主渠道并列文档 | bilibili-inst360 + 仍 Owner 手发 |
| 18 | Hub（danying-apps）vs 本仓 | **略** | 🟡 | 克隆/verify 路由跨 repo | INDEX.md · VERIFY-MAP |
| 19 | 思维导图 vs 本审计 vs 多 adoption | **略** | 🟡 | 文档多但 **分工不同** | 本表 + agent-ecosystem-map |
| 20 | 未 commit 的大量 content 草稿 | **是（工作区）** | 🟠 | Git 与「脑中主队列」可能不一致 | 定稿后 commit；pivot 包为当前主交付 |

---

## 总结判断

| 问题 | 答案 |
|------|------|
| **整体是不是「坏掉/不可维护」？** | **否。** 有单一 CEO（00）、硬验收门、EXTENSION-POINTS 默认栈。 |
| **你的直觉「有点乱」主要来自哪？** | ① 视频迭代 + 声音锚定 **叠** 在 Brief 管线之上；② **pivot 包** 与旧 discovery brief **并存**；③ **13 个 IP 工具** 刚 vendor；④ 步号 0a/2a/0b **非直觉数字**。 |
| **算不算混乱到 Agent 必迷路？** | **默认写小红书不会** —— 若 Agent 遵守「主路径 = Manager + 04 + evaluate」。**会乱** 的情况：把 IP CLI 当每步必跑、或混用两套选题队列。 |
| **优先的三条收敛（可选）** | 1）在 `published-notes-index` 或 README 标 **唯一「当前发队列」**；2）旧 workflow-test 队列显式标 deprecated；3）INDEX 顶部保留 **主路径 5 行**（已有 EXTENSION-POINTS，可再链到 map）。 |

---

## 相关文件

- [WORKFLOW-CEO-ARCHITECTURE.md](./WORKFLOW-CEO-ARCHITECTURE.md)
- [agent-ecosystem-map.html](./agent-ecosystem-map.html)
- [workflow-mindmap.html](./workflow-mindmap.html)
