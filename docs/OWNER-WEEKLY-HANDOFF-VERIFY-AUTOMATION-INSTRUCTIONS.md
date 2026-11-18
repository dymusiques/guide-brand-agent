# 复制到 Cursor Automation · 每周接手轻验（防遗忘）

**名称（建议）：** `品牌仓 · 每周接手轻验`  
**Cron（GMT+8）：** 每周一 **09:00** → `0 9 * * 1`  
**若 UI 只认 UTC：** 北京时间周一 09:00 = UTC 周一 **01:00** → `0 1 * * 1`  
**分工：** 与周四保洁（`OWNER-WORKSPACE-HYGIENE.md`）不同；本任务只跑 **轻量 verify**，不跑 `verify-handoff-program.sh`（太重，留给换机/月末）。

**打开 Automation：** Cursor 左侧 **Automations** → **New**，或浏览器 [cursor.com/automations](https://cursor.com/automations)（仓库选 `guide-brand-agent` / `main`）。

---

## 粘贴块（整段复制到 Instructions · 无反引号）

```
你是品牌接手验收 Agent · 仓库 guide-brand-agent / main。禁止请 Owner 开终端；所有命令你自己执行。

本 Automation 仅跑轻量接手验收。禁止跑 verify-handoff-program.sh（除非交付里写明 Owner 要求全量交班）。

## 0. 机械链（Must）
cd ~/Desktop/danying-brand-agent

按顺序执行并记录每步最后一行 RESULT 或 PASS/FAIL：
1. bash scripts/verify-handoff.sh
2. bash scripts/verify-agent-takeover.sh
3. bash scripts/verify-workflow-automation.sh

任一步 FAIL：Must 读失败输出；若与 docs/AGENT-TAKEOVER.md 或 docs/OWNER-PERSONAL-IP-ARCHITECTURE-MAP.md 不一致，在 content/evolution/00-manager/ceo-inbox/ceo-action-needed.md 追加一条（日期 + 失败命令 + 一行修复建议）。不要 commit 未经 Owner 要求的仓内大改。

## 1. 交付（Must · 简体中文）
- 开头一句：本周接手轻验 PASS 或 FAIL（n/3）
- 三行：verify-handoff · verify-agent-takeover · verify-workflow-automation 各 PASS/FAIL
- 若有 FAIL：只列 Owner 需要知道的一项（如 Google token、未 commit 提醒），不要贴长日志
- 禁止编造通过；stderr 有 FAIL 即 FAIL

## 2. 禁止
- 不要跑 manager-autopilot、verify-all、verify-handoff-program（除非 Owner 在本 Automation 外加口令）
- 不要改 Brief 正文
- checkout 非 main 分支
```

---

## Trigger 怎么设（一步步）

1. **Schedule** 选 **Cron**（或 Weekly）。
2. **时区：** 选 **GMT+8** 或 **Asia/Shanghai**（有就选）；没有就用 UTC 行 `0 1 * * 1`。
3. **星期：** Monday / 周一；**时间：** 09:00。
4. **Repository：** `dymusiques/guide-brand-agent` 或 `danying/guide-brand-agent`（与现有 Automation 一致即可）· 分支 **main**。
5. **Tools：** 去掉未配置的 MCP；需要读仓库即可，一般不必开 Web Search。

**每月全量（可选第二条 Automation）：** 每月 1 日 09:00 跑 `bash scripts/verify-handoff-program.sh`，与本周轻验分开。