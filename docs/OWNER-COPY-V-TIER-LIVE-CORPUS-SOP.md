# V-Tier 高互动帖 · 滚动语料库 SOP

## 真源

| 文件 | 作用 |
|------|------|
| `integration/handoff/owner-copy-v-tier-live-corpus.json` | **当前**收录的高阅读/高赞/高评论 **单篇**帖文 |
| `content/evolution/00-manager/ceo-inbox/owner-copy-v-tier-corpus-log.jsonl` | 每次追加/当次写稿合并的 **可追溯日志** |
| `content/xiaohongshu/v-tier-attestations/<brief>.json` | 当次写稿引用了语料库哪些 id + **本次新扒**的帖 |

## 标准（Owner 定）

1. **不要**只盯某个大 V 的某一篇陈年爆款；每次写稿前要 **新搜** 各平台 **近期** 高互动帖（不同账号、不同篇）。
2. 收录的是 **帖子/文章 URL**，不是主页、不是搜索页。
3. 每条记录 Must 有：**平台 · 账号 · 粉丝约数 · 标题 · 互动数（赞/反应/clap + 评论）· captured_at · source · style_steal**。
4. 小红书优先 **`xiaohongshu.com/explore/`** 直链；若先通过报道/转引确认数据，当次 attestation 的 `session_fresh_posts` **Must** 补 explore 直链并 merge 进语料库。
5. **文化/艺术/审美向（Owner Must）：** 每次 attestation ≥1 条来自 [`owner-copy-v-tier-cultural-art-creators.json`](../integration/handoff/owner-copy-v-tier-cultural-art-creators.json)（谢胜子、天才女友GG/天才少女G、艺术审美类等）的 **高互动单篇**。

## 每次写稿（Agent）

```bash
# 1) 语料库是否够新、够多样
.venv/bin/python scripts/refresh-owner-copy-v-tier-live-corpus.py --verify-only

# 2) 自搜高互动帖 → 写入 patch.json → merge
.venv/bin/python scripts/refresh-owner-copy-v-tier-live-corpus.py --from-json /tmp/v-tier-patch.json

# 3) 写 attestation（含 corpus_entry_ids + session_fresh_posts ≥1 条新帖）
# 4) 写稿
.venv/bin/python scripts/verify-owner-copy-v-tier-attestation.py --brief content/xiaohongshu/xxx-brief.md --merge-corpus
```

`--merge-corpus`（默认开）：PASS 时把 `session_fresh_posts` 合并进 live corpus 并写 jsonl 日志。

## 互动门槛（JSON `engagement_floors`）

- 小红书：创作者约 **40 万粉+**，或单篇 **1 万赞+**（转引须标注 `engagement_verified_via`）
- LinkedIn：**2000+ reactions** 且创作者 **30 万粉+** 档
- Medium：**5000+ claps** 或同级别曝光例外

门槛是 **收录进语料库** 的线，不是自动证明你的成稿达标。
