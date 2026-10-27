# verify-all 档位（公司审计标准）

| 档位 | 命令 | 含义 |
|------|------|------|
| **CI** | `VERIFY_TIER=ci bash scripts/verify-all.sh` | 胶水 + 矩阵 + platform + analytics demo；**不**烧 Gemini |
| **Release** | `VERIFY_TIER=release bash scripts/verify-all.sh` | CI 项 + **05 XHS Gemini 6** + **02/03 strategic Gemini 6** |
| **Release 严** | 上式 + `VERIFY_STRICT_BRIEFS=1` | 且所有 `content/xiaohongshu/*-brief.md` 须 aligned |
| **Release 战略严** | 上式 + `VERIFY_STRICT_STRATEGIC=1` | 且 `content/business-brand/*.md`、`content/marketing/*.md`（除 README）须 lint + evaluate |

环境变量等价：`SKIP_GEMINI=1` ≈ CI 档。

定稿单条：

```bash
bash scripts/verify-all.sh --brief content/xiaohongshu/foo-brief.md
python scripts/evaluate-business-brand.py --file content/business-brand/your-doc.md
python scripts/evaluate-marketing-campaign.py --file content/marketing/your-campaign.md
```

## Gemini 6 case 与 M4 分工

Module 3 课纲里的 **Gemini 6 case** = 各 kernel 下 `test_*_aligned.py` / `test_is_xhs_growth_aligned.py` 的 **6 个固定用例**（改 classifier / 战略 doc 规则后回归）。与 **M4**（`bash scripts/verify-goals.sh` · 按 `G-*` hook 快检 Owner 目标）不是同一层：**M4 不跑整包 kernel 6 case**，避免 autopilot 因 API 波动打断日常链。

| 层级 | 是什么 | Gemini 6 case |
| --- | --- | --- |
| **1 · 05 / 03 / 02 部门 verify 脚本** | kernel / classifier **回归**（Module 3 课纲）；人工改 kernel 后单跑 | ✅ 有 key 时：`verify-xhs-topic.sh` → `test_is_xhs_growth_aligned.py`；`verify-business-brand.sh` / `verify-marketing-campaign.sh` → 各 `test_*_aligned.py`（**各 6 用例**；02/03 前先 lint README scaffold） |
| **2 · Agent 矩阵** | `verify-agent-matrix.sh`：Goal registry **6** + **10×6 集成 glue**（路径、函数壳、`--check`、Goal 挂载、test 文件存在性等） | ❌ **不**在矩阵里批量调 Gemini API；glue 只验脚本/测试模块 **在仓**。整包 6 case 走第 1 层部门脚本 |
| **3 · verify-all（Release / CI）** | `bash scripts/verify-all.sh`；`VERIFY_TIER=ci` 默认 `SKIP_GEMINI=1` | **Release**（默认 tier）：有 key 时串跑第 1 层三个部门 Gemini 套件；无 key 则 SKIP。**CI** 档：胶水 + 矩阵 + M4 + platform 等，**不**烧 Gemini 6 |
| **4 · M4 + manager-autopilot** | `verify-goals.sh` → `test_goals_verify.py` 按 `verify_hooks.json` 验 **G-\***（交付物标记、discovery Brief、lint、单文件 `evaluate-*` 等）；[AUTOPILOT.md](AUTOPILOT.md) 日常链 **必跑 M4** | ❌ **不**调用 `verify-xhs-topic.sh` / `verify-business-brand.sh` / `verify-marketing-campaign.sh` 整包 6 case；无 key 时 `skip_without_gemini` 的 evaluate 可 SKIP。`AUTOPILOT_FULL=1` 仅附加 **CI 档** verify-all（仍不烧 Gemini 6） |

**何时跑哪条：** 改 `kernels/xiaohongshu/line2/` 或 XHS classifier → `verify-xhs-topic.sh`；改 `kernels/strategic_docs/` → 02/03 部门脚本；换机 / 交班 / 发版 → `VERIFY_TIER=release bash scripts/verify-all.sh`；日常 autopilot → `manager-autopilot.sh`（M4 即可）。

## 小红书声音 · L2（无 Gemini）

| 层 | 命令 | 何时 |
|----|------|------|
| **L2 视频/声音 QA** | `bash scripts/verify-xhs-voice-qa.sh content/xiaohongshu/*video-round1*.md` | Round 1 落盘后 · 改 VOICE-ANCHOR / 04 禁词表后 |
| **L1 IP evaluate** | `evaluate-xhs-topic.py --brief` | Brief 定稿 · 轨 2 认知期 |

L2 **不替代** L1；视频 Round 1 **只要求 L2 PASS**。
