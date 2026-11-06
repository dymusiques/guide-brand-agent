# V-Tier 衡量 · 诚实说明（Owner / 新 Agent Must 读）

## 不能直接「确定」已是 40–50 万粉文笔

本仓 **没有** NLP 模型、没有爬取全量帖子、也没有和某大 V 原文做自动相似度打分。  
因此 **任何脚本 PASS ≠ 文笔已等于大 V**。

| 检查项 | 实际在验什么 |
|--------|----------------|
| `verify-owner-copy-v-tier-mandate.sh` | 标准 **文档/JSON 存在** |
| `verify-owner-copy-human-readable.py` | **不是 Agent 脚手架**、长度底线 |
| `evolve-platform-hits.py` | 仓库内 **四维度规则分**（角度/爆款/口吻/引用），**不读**大 V 原文 |
| **Owner review** | 唯一权威：**像不像大 V、能不能发** |

「40–50 万粉」指的是 **对标人选的粉丝量级/曝光量级**（见 `owner-ip-benchmark-creators.json`），用来约束 Agent **该看谁**；不是自动认证成稿等级。

## 写前 Must：滚动高互动语料 + 当次 attestation

**语料库（持续更新）：** `integration/handoff/owner-copy-v-tier-live-corpus.json`  
**SOP：** [`OWNER-COPY-V-TIER-LIVE-CORPUS-SOP.md`](./OWNER-COPY-V-TIER-LIVE-CORPUS-SOP.md)  
**审计日志：** `content/evolution/00-manager/ceo-inbox/owner-copy-v-tier-corpus-log.jsonl`

每次为 **FluteBuddy / 个人 IP** 写稿 **前**：

1. 自搜 **不同大 V、不同篇** 的 **高赞/高评/高 clap** 帖（非主页）；merge 进 live corpus（`refresh-owner-copy-v-tier-live-corpus.py --from-json`）。
2. 写 attestation：`corpus_entry_ids`（从库中引用）+ **`session_fresh_posts` ≥1 条本次新扒**（含互动数、URL、style_steal）。
3. 落盘：`content/xiaohongshu/v-tier-attestations/<brief 文件名>.json`。
4. 跑门禁（delivery 前，默认 merge 新帖进语料库）：

```bash
.venv/bin/python scripts/verify-owner-copy-v-tier-attestation.py --brief content/xiaohongshu/<slug>-brief.md
```

**FAIL** = 没有 attestation、没有当次新帖、creator<3、缺平台、互动/URL 不达标、过期 → **视为未做对比**。

Discovery 测试 Brief 默认 **SKIP** attestation；双线产品/IP Brief **不 SKIP**。

## 与 Owner review 的分工

- **Attestation PASS**：证明 Agent **这次写之前**翻过对标作品（可审计）。
- **Evolution ≥80**：证明稿子在 **仓库规则** 下过线。
- **Rubric L2**（[`OWNER-SUCCESS-METRICS-MAP.md`](./OWNER-SUCCESS-METRICS-MAP.md)）：Agent **自填 0–100 + 证据**；加权 **≥80** 才可交 Owner；**不是**自动 NLP 分。
- **Owner PASS**：证明 **文笔** 真的到大 V 档。

缺一不可，且 **只有 Owner 是文笔终审**。

## 对 Agent：为什么要三层而不是「一个总分」？

**越具体越好**——但只能把 **可核对** 的做成数字。假自动「文笔分」会骗过流程、骗不过你。  
因此：**L1 硬数字 + L2 Rubric（须举证）+ L3 你定** = 当前最优折中；见指标地图。
