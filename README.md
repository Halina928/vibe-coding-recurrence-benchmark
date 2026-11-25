# Vibe Coding Recurrence Benchmark

这个仓库研究 AI 辅助代码修改中的安全回归，以及安全审查、验收门禁和修复循环对代码交付的影响。仓库包含多轮回归基准、SusVibes 主实验和张永基的九项合成流程验证。

## 最新评测

| 实验 | 评测范围 | 结果 | 报告 |
| --- | --- | --- | --- |
| 张永基九项实验 | 9 个自定义合成流程实例 | 功能 9/9，安全 9/9，联合 9/9 | [逐项结果](experiments/susvibes_harness_sec/docs/RESULTS_ZHANG_YONGJI_2026-11-13.md) |
| P1 | 10 个配方 × 8 个目标任务，另有对照 | 最高 Joint 2/8 | [P1 报告](experiments/susvibes_harness_sec/results/P1/REPORT.md) |
| P2 | 10 个配方 × 8 个目标任务 | 最高 Joint 2/8 | [P2 报告](experiments/susvibes_harness_sec/results/P2/REPORT.md) |
| P3 | [M2 检测分工](experiments/susvibes_harness_sec/docs/OWNERS.md) | 主分支暂无独立评分报告 | — |
| P4 | 9 个配方 × 7 个目标任务，Windows 试验 | 最高 Joint 1/7 | [P4 报告](experiments/susvibes_harness_sec/results/P4/REPORT.md) |

[完整汇总与统计口径](experiments/susvibes_harness_sec/results/README.md)

## 项目架构

| 实验线 | 运行与配置 | 结果 |
| --- | --- | --- |
| 多轮安全回归 | [cases/](cases/) 定义场景和测试，[harness/](harness/) 负责模型调用与逐轮评测，[run_experiments.py](run_experiments.py) 提供批量入口 | [results/](results/) 保存逐轮结果，[workspaces/](workspaces/) 保存代码快照，[scripts/](scripts/) 提供汇总和绘图 |
| SusVibes 主实验 | [机制层](experiments/susvibes_harness_sec/harness_sec/) 通过配方编排知识输入、质量检测和反馈控制，调用上游评测器 | [主实验报告及评测数据](experiments/susvibes_harness_sec/results/) |
| 张永基合成流程验证 | [实验脚本](results/llm-security-review-2026-11-13/run_experiments.py) 使用合成库存函数验证九个机制组合，再用 SusVibes 上游引擎逐项评分 | [DeepSeek 调用证据](results/llm-security-review-2026-11-13/evidence.json) · [九项评分 CSV](results/llm-security-review-2026-11-13/susvibes-workflows-2026-11-25/scores.csv) |

主实验中，[配方配置](experiments/susvibes_harness_sec/harness_sec/configs/) 选择要启用的机制，[编排器](experiments/susvibes_harness_sec/harness_sec/orchestrator.py) 依次运行知识输入、代理生成、质量检查和反馈控制，[评测入口](experiments/susvibes_harness_sec/harness_sec/evaluate.py) 将生成的补丁交给上游评测器。[机制层架构与调用链](experiments/susvibes_harness_sec/docs/ARCHITECTURE.md)

多轮回归基准的历史记录适合分析个别场景的逐轮变化。比较模型整体表现还需要匹配场景覆盖和重复次数。判断旧入口是否回归时，需要确认同一检查在此前轮次已通过。

## 运行入口

- 多轮回归的配置、测试和结果解释见 [配置与测试](docs/TESTING.md)。离线功能测试无需模型服务。
- SusVibes 主实验的 Docker、上游仓库和模型服务配置见 [实验手册](experiments/susvibes_harness_sec/docs/RUNBOOK.md)。
- 九项合成流程的原始证据、复跑方式及评分范围见 [个人实验报告](experiments/susvibes_harness_sec/docs/RESULTS_ZHANG_YONGJI_2026-11-13.md)。
