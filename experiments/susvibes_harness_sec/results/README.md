# 实验结果汇总

## SusVibes 主实验

按各报告的任务分母和配方统计。FuncPass 表示功能通过，SecPass 表示安全通过，Joint 要求同一任务同时通过功能和安全检查。

| 分组 | 实验规模 | Joint 最高的配方 | 同一配方的 FuncPass / SecPass / Joint | 报告 |
| --- | --- | --- | --- | --- |
| P1 | 10 配方 × 8 任务，另有无机制对照 | 21、31、26 | 21 为 7/8、2/8、2/8；31 为 6/8、2/8、2/8；26 为 5/8、2/8、2/8 | [报告及逐任务矩阵](P1/REPORT.md) |
| P2 | 10 配方 × 8 任务 | 22、27、32、17 | 22 和 27 为 6/8、2/8、2/8；32 为 5/8、2/8、2/8；17 为 4/8、2/8、2/8 | [报告及逐任务矩阵](P2/REPORT.md) |
| P3 | M2 模型审查和静态检测分工 | — | 主分支暂无独立评分报告 | [分工记录](../docs/OWNERS.md) |
| P4 | 9 配方 × 7 任务 | 39、19、24、29 | 39 为 5/7、1/7、1/7；19 为 4/7、1/7、1/7；24 为 3/7、1/7、1/7；29 为 2/7、1/7、1/7 | [评测报告](P4/REPORT.md) · [完整实验记录](P4/EXPERIMENT_REPORT.md) |

P1 的无机制对照为功能 5/8、联合 0/8。P1 和 P2 的报告均为单次种子运行。P4 使用 Windows 兼容试验环境，缺少因评测容器卡住而未产出报告的 Wagtail 任务，故分母为 7。这些结果按各自环境和样本解释。

### 主实验数据文件

- [三组合并的配方汇总](all_results.csv)和[逐任务 FuncPass、SecPass、Joint 长表](per_task.csv)
- 逐组 CSV 与官方每任务报告：[P1](P1/results.csv) · [P1 原始报告](P1/eval_reports/) · [P2](P2/results.csv) · [P2 原始报告](P2/eval_reports/) · [P4](P4/results.csv) · [P4 原始报告](P4/eval_reports/)

仓库归档了评测报告与统计表。原始预测和运行轨迹保存在各组实验归档中。

## 张永基九项合成流程实验

9 个实例分别评估审查、自审状态、AST 检查、门禁、反馈或修复循环。功能通过 **9/9**，安全通过 **9/9**，联合通过 **9/9**。SusVibes 上游评测引擎运行了自定义合成任务，模型审查使用此前 DeepSeek 实际调用记录，执行类用例重新运行。主实验的分母是仓库任务，个人实验的分母是流程实例，两组分数应按各自口径解读。

[个人实验逐项说明](../docs/RESULTS_ZHANG_YONGJI_2026-11-13.md) · [评分 CSV](../../../results/llm-security-review-2026-11-13/susvibes-workflows-2026-11-25/scores.csv) · [评测器汇总 JSON](../../../results/llm-security-review-2026-11-13/susvibes-workflows-2026-11-25/summary.json) · [当次 DeepSeek 记录](../../../results/llm-security-review-2026-11-13/susvibes-workflows-2026-11-25/deepseek-evidence.json)
