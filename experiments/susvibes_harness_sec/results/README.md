# 实验与评测结果（P1 / P2 / P4）

> 官方评测器：SusVibes（FuncPass / SecPass）；**Joint = 同一任务 FuncPass 且 SecPass**。
> 代码：`experiments/susvibes_harness_sec/`（上游 main 已合并到 `cdae923`）。

## 覆盖情况

| 组 | 负责配方 | 任务数 | 说明 |
|---|---|---|---|
| P1 | 01,06,11,16,21,26,31,36,41,46 | 8 | 完整 8 任务 |
| P2 | 02,07,12,17,22,27,32,37,42,47 | 8 | 完整 8 任务（新版代码） |
| P4 | 04,09,14,19,24,29,34,39,44 | 8 | **wagtail-5c7a 评测失败**（测试无 counts，按 fail 计入）；Windows 兼容补丁为 trial |

## 文件

| 路径 | 内容 |
|---|---|
| `results/P1/results.csv` | P1 汇总（Func/Sec/Joint、attempts、成本） |
| `results/P1/REPORT.md` | P1 分析报告 |
| `results/P2/results.csv` / `REPORT.md` | P2 汇总与分析 |
| `results/P4/results.csv` / `REPORT.md` | P4 汇总（n=7） |
| `results/P4/EXPERIMENT_REPORT.md` 等 | P4 原始实验说明、manifest、Windows 补丁 |
| `results/<组>/eval_reports/<配方>/<iid>.json` | 每个任务的官方 `report.json`（原始证据） |
| `results/all_results.csv` | 三组合并的汇总 |
| `results/per_task.csv` | 三组逐任务 func/sec/joint（长表，便于画图） |

## 重要说明

1. **P4 是 trial**：Windows 兼容补丁未合入主线；wagtail-5c7a 评测失败（测试无 counts），已按 fail 计入，n=8，可与 P1/P2 的 8 任务口径对比。
2. 原始 `predictions.jsonl` / `trace.jsonl` **未入库**（体积原因，P4 的 ceph patch 约 38 万字符）；需要时可从各组 zip/云盘获取。
3. 评测口径：P1/P2 为 8 任务，P4 为 7 任务；跨组比较请以 Joint 数和逐任务表为准。
4. 所有结果均为单 seed、方向性结论。
