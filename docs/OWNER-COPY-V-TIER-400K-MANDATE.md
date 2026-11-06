# Owner 文案 · 40–50 万粉大 V 文笔档（V-Tier）

> **机器可读（新 Agent 先读 JSON）：** [`integration/handoff/owner-copy-v-tier-400k.json`](../integration/handoff/owner-copy-v-tier-400k.json)  
> **双线 workflow：** [`OWNER-DUAL-TRACK-COPY-WORKFLOW.md`](./OWNER-DUAL-TRACK-COPY-WORKFLOW.md)  
> **与 Tier2 关系：** [`OWNER-COPY-BENCHMARKS-TIER2.md`](./OWNER-COPY-BENCHMARKS-TIER2.md)

## 这条标准是什么

Owner 要求：**FluteBuddy 产品轨** 与 **张丹瀛个人 IP 生态链轨** 的所有对外宣传文案，文笔必须接近 **Medium / LinkedIn / 小红书上约 40 万–50 万粉丝（或同级别曝光）大 V** 的写法——**行业相关或完全无关都可以**，学的是 **用词、语法、节奏、私人感与生态链呈现方式**，不是抄人设。

**Owner 偏好类型（Must 对标）：** [**文化 · 艺术 · 审美向大 V**](./OWNER-COPY-V-TIER-CULTURAL-ART-STANDARD.md)（如 **谢胜子**、**天才少女G / 天才女友GG**、何水晶、画画的玉玉卿等）的 **高互动单篇** 文笔；双线宣传 **都必须** 达到这一档，见 `owner-copy-v-tier-cultural-art-creators.json`。

**脚本不会自动替你「变成大 V」**；Agent Must 深扒对标、写稿时对照，Owner **Must review 终稿文笔**（设计如此，非 bug）。

**诚实说明（Must）：** [`OWNER-COPY-V-TIER-MEASUREMENT-HONESTY.md`](./OWNER-COPY-V-TIER-MEASUREMENT-HONESTY.md) — 什么叫能验、什么叫不能验。

## 三层标准（勿混）

| 层 | 门槛 | 文件 | 何时用 |
|----|------|------|--------|
| **人话门禁** | 禁 Agent 脚手架 / 摘要冒充正文 | `verify-owner-copy-human-readable.py` | 每篇 Brief / longform |
| **Tier2** | 单篇约 2000+ 互动档结构与口气 | `owner-copy-benchmarks-tier2.json` | 写稿前读 + 对照 |
| **V-Tier（本档）** | 40–50 万粉级 **文笔与生态链陈列** | `owner-copy-v-tier-400k.json` + `owner-ip-benchmark-creators.json` | **A/B 双线凡写文案 Must** |

## Agent 写稿前 Must（V-Tier）

1. **写前**打开对标作品 → 落盘 attestation（见 MEASUREMENT-HONESTY）→ `verify-owner-copy-v-tier-attestation.py` **PASS**。
2. 读 `owner-copy-v-tier-400k.json` 里 **本轨**（`flutebuddy` / `personal_ip`）的 `style_checklist`。
3. 自搜并更新（至少每季度）对标账号：小红书 / LinkedIn / Medium 各 ≥2 个 **followers_approx ≥ 400000**（或文档列出的同级别曝光例外）。
4. 写前填 mental checklist：**一句一画面 · 具体名词 · 第一人称态度 · 段短可扫 · 生态链怎么「列给人看」**（见 JSON `ecosystem_display_patterns`）。
5. 写后顺序：`xhs-copy-grep-banned`（小红书）→ `verify-owner-copy-human-readable` → `evolve-platform-hits.py`（四维度 ≥80）→ **交 Owner review**。

## 生态链 vs 文笔

- **生态链内容**（生活/关系/故事 + 专业托底）：见 IP 战略与 `owner-ip-ecosystem-content.json`。
- **大 V 怎么罗列自己的矩阵/栏目**：深扒 `owner-ip-benchmark-creators.json`，HTML `#benchmarks`。
- **FluteBuddy** 同样用 V-Tier 文笔；产品信息 ≤ 叙事，不写成 SaaS 说明书。

## 验收命令

```bash
bash scripts/verify-owner-copy-v-tier-mandate.sh
.venv/bin/python scripts/verify-owner-copy-human-readable.py --brief content/xiaohongshu/<slug>-brief.md
```
