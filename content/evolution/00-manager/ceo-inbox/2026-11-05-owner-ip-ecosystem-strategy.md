# 张丹瀛 · 个人 IP 生态链 · 三平台方针（CEO · Drive 背书）

- **轨 ID：** `personal_ip_ecosystem` · 配置 `integration/handoff/owner-ip-track.json`
- **与 FluteBuddy 关系：** **两条 goal 轨，同一 CEO 主链**；内容 **产品 ≤30%**，人格与多维切面为主
- **Drive screen：** `corpus-screens/张丹瀛-个人IP-生态链-多维度-影响力-小红书-LinkedIn-Medium-法派长笛-听见/` · **434** reference · hydrate **8**
- **可视化交付：** `OWNER-IP-ECOSYSTEM-DELIVERABLE-<date>.html` · 内容真源 `owner-ip-ecosystem-content.json`

---

## 一、要让读者看见什么（真实生态链）

**不要高大上品牌手册。** 读者要先感到：这是一个**有生活、有态度、有故事**的人，然后才信你的专业。

| 层 | 写什么 |
|----|--------|
| **生活 · 家庭** | 晚饭、练琴以外、旅途、独居/家人对话（可 anonymize） |
| **感情 · 关系** | 边界、感谢、失望、不灌鸡汤 |
| **工作 · 社会** | 行业里见到的真事 + 一句你的判断 |
| **法派长笛 / 听见** | 专业可核对，但不端架子 |
| **品牌现场 / AI / FluteBuddy** | 故事化案例；产品 ≤30% |

**对标博主库（深扒）：** `integration/handoff/owner-ip-benchmark-creators.json` · HTML `#benchmarks`  
**Owner 文笔类型（Must · 双线）：** [`OWNER-COPY-V-TIER-CULTURAL-ART-STANDARD.md`](../../../docs/OWNER-COPY-V-TIER-CULTURAL-ART-STANDARD.md) — 谢胜子、天才少女G/天才女友GG、艺术审美向高互动帖。  
例：LinkedIn Lara / Justin；Medium Martha；小红书 何水晶、玉玉卿、闫不闲等见 `owner-copy-v-tier-cultural-art-creators.json`。

**人即品牌：** 案例可以换，名字始终是张丹瀛 / Danying。

---

## 二、三平台分工

| 平台 | 形态 | 频率 | 过关线 |
|------|------|------|--------|
| **小红书** | 多角度笔记/口播 + 听见摘要 | 周 2–3 | V-Tier 大 V 文笔 + Tier2 · `verify-owner-copy-human-readable` · Owner review |
| **LinkedIn** | 第一人称职业叙事 · 检索 `linkedin-sources.json` | 周 1–2 | `evolve-platform-hits` · 600–1800 字 |
| **Medium** | 长文一个观点 | 月 1–2 | 5–7 分钟读完 · 四维度 ≥80 |

Starter 标题见 `owner-ip-ecosystem-content.json` → HTML `#platforms`。

---

## 三、Drive 优先 hydrate（Owner 可点开）

见 JSON `drive_hydrate` · INDEX 同目录。

---

## 四、全自动 workflow（本轨）

```bash
bash scripts/open-owner-ip-ecosystem-deliverable-html.sh
# 或 CEO 全量（goal 含 个人IP/生态链/张丹瀛…）：
bash scripts/ceo-full-execution-pipeline.sh --goal "张丹瀛 个人IP 生态链 三平台" --no-discovery-auto
```

**不弹** `OWNER-XHS-FILTER-DELIVERABLE`（见 `docs/CEO-OWNER-HTML-ROUTING.md`）。
