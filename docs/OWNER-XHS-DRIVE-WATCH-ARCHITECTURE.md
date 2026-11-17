# Drive 变更 → 同步 · 架构（诚实边界）

## Cursor 没有「Google 直接打进来的官方 Webhook」

- **Cursor Automation** 只有 **定时 / 手动** 触发，**不能**像 Zapier 那样登记一个公网 URL 让 Google 随便 POST。
- 因此「通知 Cursor」在工程上 = **本机或云端 Agent 按时间表跑脚本**，或 **本机 process-launcher 收 localhost HTTP**。

## 推荐组合（本仓已实现 · 最 work）

| 层 | 做什么 |
|----|--------|
| **日检脚本** | `compare-owner-xhs-drive-listing.py` 刷新 listing → 比对 fingerprint → 变则 `--sync` + `ceo-action-needed.md` |
| **Cursor Automation #4** | 每天 10:00 跑上一条（见 `OWNER-XHS-DRIVE-WATCH-AUTOMATION-INSTRUCTIONS.md`） |

**不依赖邮件** · **不依赖公网 webhook** · Mac 关机日检会跳过，开机后次日补上。

## 进阶：Apps Script + 本机 Webhook（可选 · 非默认）

适合：**Mac 常开** 且 **process-launcher :7997 健康**。

```text
Google Apps Script（定时或手动）
  → POST http://127.0.0.1:7997/run
  → command: bash scripts/sync-owner-xhs-data-from-drive.sh
```

模板：`docs/google-apps-script/owner-xhs-drive-sync-launcher.gs.template`

**限制：**

- Apps Script **无法**直接 POST 到你电脑（除非 **公网隧道**，安全成本高）。
- 因此 **不能**实现「Google 云 → 直达 Cursor 云端 Agent」；只能 **Google 云 → 你家 Mac launcher**，或 **放弃实时、用日检 Automation**。

### Drive API `changes.watch`

同样需要 **HTTPS 公网 endpoint** 接 push；本仓 **未部署**。与 Apps Script 同属进阶，**日检 + Automation #4 是当前性价比最高路径**。

## 与选题/保洁 Automation 的关系

**完全独立** —— 只盯 `owner-xhs-data-drive.json` 文件夹，不跑选题包、不跑保洁。