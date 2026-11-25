# 实验评测汇总

| 实验 | 评测范围 | 配方或实例 | FuncPass | SecPass | Joint | 报告与数据 |
| --- | --- | --- | ---: | ---: | ---: | --- |
| P1 | SusVibes · 10 配方 × 8 任务，另有无机制对照 | 21 / 31 / 26 | 7/8 / 6/8 / 5/8 | 各 2/8 | 各 2/8 | [报告](P1/REPORT.md) · [CSV](P1/results.csv) · [原始报告](P1/eval_reports/) |
| P2 | SusVibes · 10 配方 × 8 任务 | 22 / 27 / 32 / 17 | 6/8 / 6/8 / 5/8 / 4/8 | 各 2/8 | 各 2/8 | [报告](P2/REPORT.md) · [CSV](P2/results.csv) · [原始报告](P2/eval_reports/) |
| P3 | 模型审查和静态检测 | 暂无报告 | — | — | — | [分工记录](../docs/OWNERS.md) |
| P4 | SusVibes · 9 配方 × 7 任务，Windows 试验 | 39 / 19 / 24 / 29 | 5/7 / 4/7 / 3/7 / 2/7 | 各 1/7 | 各 1/7 | [报告](P4/REPORT.md) · [CSV](P4/results.csv) · [原始报告](P4/eval_reports/) |
| P5 | 原版合成库存函数 `reserve(count)`，9 项流程断言通过 | 05 G-L2-F、10 G-P-C、15 G-E-A、20 T-L1-S、25 T-P-F、30 T-E-C、35 R-L1-A、40 R-L2-S、45 R-E-F | — | — | — | [分工配方](../data/recipe_assignment.md) · [原版报告](../../../results/llm-security-review-2026-11-13/README.md) · [原始证据](../../../results/llm-security-review-2026-11-13/evidence.json) |

## 评测口径

- **指标** · FuncPass 为功能通过，SecPass 为安全通过，Joint 要求同一任务或实例同时满足两项。
- **配方** · P1、P2、P4 列出各组并列最高 Joint 的配方，分数按配方顺序展示。完整配方和逐任务记录见[主实验配方汇总](all_results.csv)及[逐任务长表](per_task.csv)。
- **范围** · P1、P2、P4 的分母是 SusVibes 仓库任务，均为单次种子运行。P1 无机制对照为功能 5/8、联合 0/8。P4 的 Wagtail 任务因评测容器卡住未出报告，分母为 7。[P4 环境与实验记录](P4/EXPERIMENT_REPORT.md)
- **P5 范围** · 2026-11-13 原版实验使用单一合成函数验证 9 个机制组合。运行用例覆盖 `1`、`10`、`0`、`11`、`True` 和字符串 `"3"`，7 次模型请求均返回 HTTP 200。原始记录提供 9 项脚本断言结果，仓库暂无对应的 SusVibes 主实验 FuncPass、SecPass 或 Joint。
