# 对抗进化环 · 新 Agent 进门就执行

Owner 不必再说第二遍。写作、三平台成稿、爆款对标，都走这一环。没有 Brief，不是跳过的理由。

入口：`bash scripts/ceo-full-execution-pipeline.sh --goal "<Owner 原话>"`  
执行：`scripts/run_ceo_full_execution.py` 在目标含「写 / 笔记 / 口播 / 成稿 / LinkedIn / Medium / 艺术家 / 爆款」时调用 `scripts/evolve-platform-hits.py`。  
分数线：[`PLATFORM-HIT-STANDARDS.md`](./PLATFORM-HIT-STANDARDS.md)。脚本里的 `ANGLE_BAR = 80` 与爆款本地规则是过线依据。禁止把文档或脚本里的线改低来收工。

## 要做的事

1. **换角度对抗，炸出舒适区。** 同一篇稿分三席，每席只攻击一件事：
   - **01** 写作标准：像不像本人在说话。场景抽掉之后观点还在，这一席不过。
   - **04** 切入视角：换一个切口，现稿还站不站得住。
   - **00 CEO / Senior Manager** 反方读者：挑正文最没接住的一条。
2. **不要模糊，不要偷懒。** 改稿要接住具体反对。补一句金句、把攻击贴进「反方」小标题，算没改。
3. **不要降低 baseline。** 角度线 80，爆款分 75，且爆款本地规则要过。80 比 75 高，是因为角度席在炸舒适区，爆款分只核对平台写法。不许用爆款分代替角度线。两条线都不是平台官方分数，来历见 [`PLATFORM-HIT-STANDARDS.md`](./PLATFORM-HIT-STANDARDS.md) 的「为什么是 80 和 75」。
4. **先压测，再进化。** 第一轮打分就是 baseline。先记下距离，再改。
5. **循环。** 尝试 → 测量和成功线的距离 → 提高 baseline → 再 evolution → 再测量。默认最多 6 轮（`CEO_EVOLUTION_MAX_ROUNDS`）。距离 = 各席不足 80 的分数相加，0 才算角度这关过。
6. **角度过了，再对爆款线。** 各平台标准不同。领英、小红书、Medium 分开对标，标准写在 `PLATFORM-HIT-STANDARDS.md`，由 `evolve-platform-hits.py` 强制执行。新的平台研究要写回这份标准，再改脚本里的检查。禁止用一个笼统的「爆款」同时放过三个平台。
7. **自动跑完。** 不要问 Owner 要不要对抗、要不要进化、要不要再测一轮。exit 42 = 同一会话改稿再跑。轮次用尽仍未过，继续改，仍然不要把线改低。

## 命令

```bash
bash scripts/ceo-full-execution-pipeline.sh --goal "<Owner 原话>"
```

有 Brief 时加上 `--brief content/xiaohongshu/<file>-brief.md`。这时还要跑 Brief 自己的 triple-eval 和 double-stress。那两步不替代上面的三席对抗。

只复查三平台成稿：

```bash
.venv/bin/python scripts/evolve-platform-hits.py \
  --dir content/evolution/00-manager/ceo-inbox/<成稿目录> \
  --goal "<Owner 原话>"
```

流水线禁止加 `--judge-only`。那一档只测量，不进化。

## 什么叫过

同时成立：

- 三席距离 = 0（每席 ≥ 80）
- 该平台本地爆款规则通过
- Gemini 爆款分 ≥ 75

爆款分是潜力线，不是播放量。发布、拍摄、出镜仍由 Owner 做。

## 上次为什么没跑进 go-through

2026-11-03 那次 `ceo-full-execution-pipeline.sh` 没有 `--brief`。Brief 专用的 triple-eval、Clever、double-stress 被脚本直接跳过，autopilot 还带了 `--skip-evolution`。三平台对抗当时还不在这条入口里，所以那次 go-through 没有换角度，也没有量距离。之后单独打的爆款分，不能当作对抗已经跑过。

现在入口已接到 `evolve-platform-hits.py`。没有 Brief 时，日志会写明：Brief 环被跳过，三平台对抗环没有被跳过。exit 42 时 go-through 停在 NEEDS_WORK，不得报 PASS。
