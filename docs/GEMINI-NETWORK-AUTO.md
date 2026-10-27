# Gemini 网络 · 全自动默认策略（Owner：全局 VPN · 3213 可选）

> **2026-10-27 Owner 前提：** 平时 **全局 VPN**；可能偶发掉线；`.env` 可保留 `GEMINI_HTTP_PROXY` 备忘，**不必** 为每次 verify 手动开关。

## 推荐方式（已写入代码 · 不用你二选一）

**智能回退（默认）：**

1. 若 `GEMINI_HTTP_PROXY` / 3213 **端口在听** → 走本地代理（与 SETUP 一致）。  
2. 若写了 3213 但 **未开** → **自动改直连**，走系统网络（= 你的全局 VPN）。  
3. VPN 掉线 → Gemini 仍会 FAIL；Agent 在 Gate/autopilot 里报错，**不** 甩给 Owner 手跑 verify。

实现：`kernels/xiaohongshu/config/gemini_config.py` · `configure_gemini_network()`。

## 和全自动 workflow 的关系

| 命令 | 需要 Gemini 通 |
|------|----------------|
| `manager-autopilot.sh` | 是（verify-goals） |
| `evaluate-xhs-topic.py` / Brief Gate | 是 |
| `verify-xhs-topic.sh` | 是（6 case） |
| `manager-ceo-owner-gate.sh --integration-only` | 否 |

**Owner 仍只做：** 发帖 + CSV inbox（见 AUTOPILOT.md）。

## 可选增强（非必须）

- 以后若 **不用** 3213：`.env` 里注释 `GEMINI_HTTP_PROXY` 即可；行为仍是 VPN 直连。  
- 若 VPN 常掉：在 VPN 客户端开 **断线重连**；Agent 无法在 VPN 断时 magic 恢复 Google API。

## 相关

- `.env.example` · [SETUP.md](../SETUP.md)  
- [VERIFY-TIERS.md](./VERIFY-TIERS.md) · `SKIP_GEMINI=1`（CI 档不烧 Gemini）
