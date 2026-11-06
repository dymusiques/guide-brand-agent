# 文案标准 · 文化 / 艺术 / 审美向大 V（Owner 定 · 双线 Must）

> **机器可读：** [`integration/handoff/owner-copy-v-tier-cultural-art-creators.json`](../integration/handoff/owner-copy-v-tier-cultural-art-creators.json)  
> **总标准：** [`OWNER-COPY-V-TIER-400K-MANDATE.md`](./OWNER-COPY-V-TIER-400K-MANDATE.md)

## Owner 要什么

你点名的类型：**谢胜子**、**天才少女 G**（仓库映射为 **天才女友 GG · 时尚社会学**）这类——

- 有 **文化判断**（现象、身份、传统、行业不是干货清单）
- 有 **艺术 / 审美语感**（画面、器物、声音、空间，不是 KPI 小标题）
- 有 **高互动帖的文笔**（几十万粉档、单篇高赞/高评/高 clap）

**FluteBuddy 产品轨** 与 **张丹瀛 IP 生态链轨** **同一标准**：  
可以讲产品、讲练琴，但读起来要像这类大 V 的 **高互动文章/笔记**，不能像 SaaS 说明书或品牌手册。

## 对标池（持续扩充）

| 账号 | 约粉丝 | 属性 |
|------|--------|------|
| 谢胜子极致进化学 | 20万+ | 认知·态度·关系（Owner 喜） |
| 天才女友 GG（天才少女G） | 32万+ | 时尚社会学·审美争议·文化 |
| 何水晶 | 88万+ | 画家·艺术过程 |
| 画画的玉玉卿 | 100万+ | 国风·文物拟人·审美传播 |
| 天才职业故事 | 151万+ | 人文·职业叙事 |
| 闫不闲 | 55万+ | 审美手工·情绪价值 |
| 晨子看书 | 56万+ | 阅读·文化 |

LinkedIn / Medium 仍用 Lara、Justin、Martha 等，但 **Must 带一句文化/审美判断**，见 JSON `cross_platform_same_standard`。

## 每次写稿怎么验

1. 滚动语料库 + **至少 1 条**来自上池（或带 `cultural_art_aesthetic` tag）的 **高互动单篇**（见 attestation）。  
2. `verify-owner-copy-v-tier-attestation.py` **FAIL** 若全文对标里没有文化/艺术/审美向帖。  
3. **Owner review** 终审文笔是否真到该档。

## 昵称说明

Owner 说的 **「天才少女G」** → 当前数据最匹配的是 **天才女友 GG**（`tiancainvyou_gg` · 时尚社会学）。若你指的是别的号，说一声我们改 `owner_aliases`。
