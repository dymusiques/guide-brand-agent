# Owner 文案过关 · 2000+ 对标档

Machine-readable：`integration/handoff/owner-copy-benchmarks-tier2.json`

## 三层标准（不要混）

| 层 | 用途 | 文件 |
|----|------|------|
| **V-Tier（文笔 · 双线 Must）** | 模仿 **40–50 万粉级**大 V 用词/语法/节奏 + 生态链陈列；FluteBuddy 与 IP 同标准 | [`OWNER-COPY-V-TIER-400K-MANDATE.md`](./OWNER-COPY-V-TIER-400K-MANDATE.md) · `owner-copy-v-tier-400k.json` |
| **Tier2（Owner 过关）** | 单篇约 **2000+** 互动档结构与口气 | `owner-copy-benchmarks-tier2.json` |
| **Tier1（CEO 对抗顶线）** | 换角度仍站得住 · 10k clap / 1k LI / 4w 赞 | `docs/angle-benchmarks.json` |

过关 = **先过人话门禁** → **V-Tier 文笔对照（大 V 深扒）** → Tier2 **结构与口气** → Tier1 对抗（有 Brief / 三平台成稿时）→ **Owner review 终稿**。

## Tier2 范文在教什么

- **Martha Eason（Medium · 演奏者发社媒）**：先写羞怯与矛盾，再写一年实验；不是行业黑话。
- **Flavie Halais（The Riff · 音乐人平台陷阱）**：长文但有论点、有研究、有出路。
- **SauceFromVeli（艺术家当 CEO）**：明确「这篇写给谁」，短段。
- **elle luna（Should/Must）**：高 clap 的叙事节奏（Tier1 已收录，Tier2 仍作结构老师）。
- **邓雨柔 / 织忆经纬（小红书引述 4 万赞）**：一件作品 + 具体记忆，不是「认知期 1234」。
- **Suzanne K.（LinkedIn 歌剧转型）**：拆「LinkedIn 假光滑」，技能迁移写具体。

## 仓库内反模式（Must 禁止当 Owner 首读）

1. `## L1 任务` / `## 章节锚点` / `context_version` 出现在弹层「正文」。
2. classifier 的 `"body"` 一行摘要冒充 3000 字长稿。
3. 工作流测试稿里 **动线 / 人在场 / RT60** 堆满首屏（测试管线可以，Owner 弹层不行）。
4. 无 Brief 任务仍弹 **FILTER** 页。

## 命令

```bash
.venv/bin/python scripts/verify-owner-copy-human-readable.py \
  --brief content/xiaohongshu/2026-10-30-musicians-who-love-music-brief.md
```

FAIL → 改 **drafts/*-longform.md** 或 Brief 链接，不是改 HTML 皮肤。

## 与 evolve-platform-hits 的关系

`evolve-platform-hits.py` 仍按 [PLATFORM-HIT-STANDARDS.md](./PLATFORM-HIT-STANDARDS.md) 打四维度；**不会**自动读 Tier2 JSON。Agent 写稿前 **Must 读** Tier2 + 人话 verify，再跑 evolution。
