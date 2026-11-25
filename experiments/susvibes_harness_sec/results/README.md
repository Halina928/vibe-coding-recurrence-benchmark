# P1–P5 实验评测汇总

按分工编号归档。P1、P2、P4、P5 目录包含主实验报告和逐任务数据；P5 同时保留历史合成流程实验与逐项证据。P3 目录记录归档状态。

| 实验 | 评测范围 | 配方或实例 | FuncPass | SecPass | Joint | 报告与数据 |
| --- | --- | --- | ---: | ---: | ---: | --- |
| P1 | SusVibes · 10 配方 × 8 任务，另有无机制对照 | 21 / 31 / 26 | 7/8 / 6/8 / 5/8 | 各 2/8 | 各 2/8 | [报告](P1/REPORT.md) · [CSV](P1/results.csv) · [原始报告](P1/eval_reports/) |
| P2 | SusVibes · 10 配方 × 8 任务 | 22 / 27 / 32 / 17 | 6/8 / 6/8 / 5/8 / 4/8 | 各 2/8 | 各 2/8 | [报告](P2/REPORT.md) · [CSV](P2/results.csv) · [原始报告](P2/eval_reports/) |
| P3 | 模型审查和静态检测 | 暂无报告 | — | — | — | [归档状态](P3/REPORT.md) |
| P4 | SusVibes · 9 配方 × 7 任务，Windows 试验 | 39 / 19 / 24 / 29 | 5/7 / 4/7 / 3/7 / 2/7 | 各 1/7 | 各 1/7 | [报告](P4/REPORT.md) · [CSV](P4/results.csv) · [原始报告](P4/eval_reports/) |
| P5 | SusVibes · 9 配方 × 8 任务 | 25 | 5/8 | 4/8 | 4/8 | [报告](P5/REPORT.md) · [实验报告](P5/EXPERIMENT_REPORT.md) · [CSV](P5/results.csv) · [原始报告](P5/eval_reports/) |

## 评测口径

- **指标** · FuncPass 为功能通过，SecPass 为安全通过，Joint 要求同一任务或实例同时满足两项。
- **配方** · P1、P2、P4、P5 列出各组并列或最高 Joint 的配方，分数按配方顺序展示（P5 配方 `25` 唯一最高 4/8，次高 `30` 为 2/8，`05` / `20` / `40` 为 1/8）。完整配方和逐任务记录见[主实验配方汇总](all_results.csv)及[逐任务长表](per_task.csv)。
- **范围** · P1、P2、P4、P5 的分母是 SusVibes 仓库任务，均为单次种子运行。P1 无机制对照为功能 5/8、联合 0/8。P4 的 Wagtail 任务因评测容器卡住未出报告，分母为 7。[P4 环境与实验记录](P4/EXPERIMENT_REPORT.md)
- **P5 归档状态** · 全部 9 个配方 × 8 个仓库任务（72 项）已完成单次运行与官方 SusVibes 评测（均 `eval_status=tested`，无容器失败或缺失），另保留 2026-11-13 与 2026-11-25 历史合成流程检查作为独立记录。[配方分配](../data/recipe_assignment.md) · [任务清单](../data/tasks_8.json) · [历史记录](P5/REPORT.md)
