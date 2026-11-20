# Cursor Automation 索引（品牌仓）

各自 **独立** Cron · 互不可替代。  
**HTML + Chrome 统一标准：** [OWNER-AUTOMATION-HTML-CHROME-STANDARD.md](./OWNER-AUTOMATION-HTML-CHROME-STANDARD.md)

**Must：** Automation **Runtime = This Computer**（本机），否则无法 `open -a "Google Chrome"`。

**分支：** `guide-brand-agent` / `main` · [OWNER-CURSOR-AUTOMATION-BRANCH-PIN.md](./OWNER-CURSOR-AUTOMATION-BRANCH-PIN.md)

**Cron 时区：** UI 若按 UTC 填写，见各文档；或用界面选 GMT+8。

| # | 名称 | Cron (GMT+8) | slug | Instructions |
|---|------|--------------|------|--------------|
| 1 | 品牌仓小红书每周选题包 | 周日 11:00 | `weekly-topic-xhs` | [OWNER-WEEKLY-TOPIC-AUTOMATION-INSTRUCTIONS.md](./OWNER-WEEKLY-TOPIC-AUTOMATION-INSTRUCTIONS.md) |
| 1b | LinkedIn+Medium 每周选题 | 周日 12:00 | `weekly-topic-li-medium` | [OWNER-WEEKLY-LI-MEDIUM-TOPIC-AUTOMATION-INSTRUCTIONS.md](./OWNER-WEEKLY-LI-MEDIUM-TOPIC-AUTOMATION-INSTRUCTIONS.md) |
| 2 | 品牌仓 · 每周保洁提醒 | 周四 11:00 | `workspace-hygiene` | [OWNER-WORKSPACE-HYGIENE-AUTOMATION-INSTRUCTIONS.md](./OWNER-WORKSPACE-HYGIENE-AUTOMATION-INSTRUCTIONS.md) |
| 2b | 每周接手轻验 | 周一 09:00 | `weekly-handoff-verify` | [OWNER-WEEKLY-HANDOFF-VERIFY-AUTOMATION-INSTRUCTIONS.md](./OWNER-WEEKLY-HANDOFF-VERIFY-AUTOMATION-INSTRUCTIONS.md) |
| 3 | 小红书导表提醒 | 周三+周日 20:30 | `xhs-export-reminder` | [OWNER-XHS-EXPORT-REMINDER-AUTOMATION-INSTRUCTIONS.md](./OWNER-XHS-EXPORT-REMINDER-AUTOMATION-INSTRUCTIONS.md) |
| 4 | Drive 日检 · 小红书数据 | 每天 10:30 | `xhs-drive-watch` | [OWNER-XHS-DRIVE-WATCH-AUTOMATION-INSTRUCTIONS.md](./OWNER-XHS-DRIVE-WATCH-AUTOMATION-INSTRUCTIONS.md) |
| 5 | 每日 AI 资讯简报 | 每天 08:00 | `daily-ai-intel` | [OWNER-DAILY-AI-INTEL-AUTOMATION-INSTRUCTIONS.md](./OWNER-DAILY-AI-INTEL-AUTOMATION-INSTRUCTIONS.md) |

HTML 输出目录：`content/evolution/00-manager/ceo-inbox/automation-runs/OWNER-AUTOMATION-<slug>-<date>.html`

---

**另：** 本机 `process-launcher` 09:00 → `background-goal-evolution-cycle`（**非** Cursor Automation；若也要 HTML，需单独加脚本调用，未纳入上表）。

**更新 Cursor UI：** 每条 Automation 的 Instructions → **整段替换**为对应 md 文件内「粘贴块」；保存后试跑 **Run once** 看 Chrome 是否弹出。