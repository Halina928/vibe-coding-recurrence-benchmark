# P4 安全机制实验正式总结

> 实验：SusVibes 安全机制实验（48 组配方中的 P4 分工，9 组）
> 执行人：成亦旸（P4）
> 完成时间：2026-11-23
> 代码版本：`Halina928/vibe-coding-recurrence-benchmark` @ `cdae923` + Windows 兼容补丁
> 数据状态：**trial**（补丁未合入主线；正式数据需 P1 合入或 Linux 复跑）

---

## 摘要

本次实验在 SusVibes 的 8 个仓库级真实任务上，执行 P4 分工的 9 组安全机制配方（04/09/14/19/24/29/34/39/44），模型固定 `deepseek-chat`，`max_steps=60`，任务集固定 `data/tasks_8.json`。

最终完成 **9 组 × 8 任务 = 72 个 episode、72 条 prediction，空补丁 0 条**。全部产物已打包为 `R48_P4_成亦旸.zip`，并附 `RESULT_MANIFEST.md`、`SUMMARY.csv` 与 `windows_fixes.patch`。

FuncPass / SecPass 尚未在本机计算（缺少 SusVibes 评测依赖），按计划由 P5 统一评测；因此本报告只对**数据完整性与过程有效性**负责，不对机制优劣下结论。

---

## 1. 实验目标

回答 GROUP_BRIEF 中的问题：在“功能能修好、但安全测试过不了”的真实任务上，**不同安全机制组合能否提升 SecPass、同时不显著牺牲 FuncPass**。

P4 负责的 9 组覆盖了三类机制的不同组合：

| 配方 | M1 知识 | M2 检测 | M3 过程 |
|---|---|---|---|
| 04 | K1 通用 | L1 自审 | S 状态保持 |
| 09 | K1 通用 | P 程序分析 | F 反馈表示 |
| 14 | K1 通用 | E 执行验证 | C 修复循环 |
| 19 | K2 任务感知 | L1 自审 | A 安全验收 |
| 24 | K2 任务感知 | L2 独立审查 | S 状态保持 |
| 29 | K2 任务感知 | E 执行验证 | F 反馈表示 |
| 34 | K3 仓库感知 | L1 自审 | C 修复循环 |
| 39 | K3 仓库感知 | L2 独立审查 | A 安全验收 |
| 44 | K3 仓库感知 | P 程序分析 | S 状态保持 |

---

## 2. 实验设计

### 2.1 任务集

- `data/tasks_8.json`，8 个任务：
  `markdown-it-py`、`requests-kerberos`、`wagtail-5c7a`、`wagtail-bc96`、`aiohttp-session`、`plone-isurlinportal`、`jupyter-core`、`ceph`。
- 每个任务对应一个 Docker 镜像（`songwen6968/susvibes.x86_64.eval_*`），由 `stage0` 导出 `/project` 作为起点仓库。

### 2.2 预算与模型

- 模型：`deepseek-chat`（GROUP_BRIEF 铁律第 3 条；未加 `--model`，沿用 config 默认）
- `max_steps = 60`（未加 `--max-steps`）
- 单任务墙钟超时参数 `--task-timeout 1800`（Windows 上不生效，见 3.2）
- 每组输出：`predictions.jsonl`、`predictions_first.jsonl`、`<任务>/episode.json`、`<任务>/trace.jsonl`

### 2.3 执行口径

- 9 组全部使用 `--tasks-file data/tasks_8.json`，任务集完全一致；
- 每组独立输出目录，失败可 `--resume` 续跑；
- 不修改 `harness_sec/`、`configs/`、`data/tasks_8.json`（仅打 Windows 兼容补丁，见 3.2）。

---

## 3. 执行环境与过程

### 3.1 环境

| 项 | 值 |
|---|---|
| 操作系统 | Windows 11 build 26200 |
| 容器 | Docker Desktop 4.99.0（Linux 容器） |
| Python（无 bandit/pytest 的组） | 3.14.3 |
| Python（需要检测器的组） | 3.12.14（venv `C:\sv\venv312`） |
| bandit | 1.9.4（离线安装） |
| pytest | 9.2.0（离线安装） |
| 输出根目录 | `C:\sv\runs\R48`（短路径） |

### 3.2 遇到的问题与处理

| # | 问题 | 影响 | 处理 |
|---|---|---|---|
| 1 | Docker Hub 不可达 | 8 个任务镜像无法拉取 | 配置 5 个 registry mirror，全部拉取成功 |
| 2 | 中文 Windows 子进程 GBK 解码 | 单测失败、`patch_now` 为 None | 子进程强制 `encoding="utf-8"` |
| 3 | `shutil.rmtree` 删不掉只读 `.git` | dry-run/清理失败 | 删除前清只读位 |
| 4 | Windows 无 `SIGALRM` | 启动即崩 | 平台保护；Windows 无单任务超时 |
| 5 | 路径过长（MAX_PATH 260） | **第一批 48 条补丁全部为 0** | 输出改短路径 `C:\sv` + `core.longpaths=true`，整批重跑 |
| 6 | ceph 仓库含 1134 个 symlink | `docker cp` 报权限错误 | 改为 tar 流解包并跳过 symlink |
| 7 | PyPI 不可达 | 无法安装 bandit / pytest | 用 Docker 容器下载 Windows wheel，离线装入 venv |
| 8 | pytest 缺失导致 E 静默返回空 | 14/29 的 E 机制无效 | 安装 pytest，重跑 14/29 |

> 第 5 条导致第一批数据全部作废，已移至 `runs/R48_invalid_pathlength/` 留档，未混入最终结果。

### 3.3 执行时间线

| 阶段 | 内容 | 结果 |
|---|---|---|
| 环境 | Docker、镜像、SusVibes 数据 | 8/8 镜像，186 任务数据集 |
| 第一批 | 6 组（04/14/19/24/34/39） | 5/8 且补丁全 0，作废 |
| 修复 | 短路径 + 长路径 + symlink | 单任务补丁恢复非空 |
| 第二批 | 6 组重跑 | 6 组 8/8，补丁非空 |
| 第三批 | 09/44（bandit） | 8/8，补丁非空 |
| 第四批 | 29（重跑） | 8/8，补丁非空 |
| 第五批 | 14/29（补 pytest 重跑） | 8/8，E 生效 |

---

## 4. 结果

### 4.1 完成度

| 指标 | 数值 |
|---|---|
| 配方数 | 9 |
| 任务数 | 8 |
| episode 总数 | 72 |
| prediction 总数 | 72 |
| **空补丁数** | **0** |
| 补丁字符范围 | 741 – 384,319 |

### 4.2 分组统计

| 配方 | 任务 | 空补丁 | blocked | attempts | 补丁最小/最大 |
|---|---:|---:|---:|---:|---|
| 04 | 8/8 | 0 | 1 | 14 | 1,124 / 383,786 |
| 09 | 8/8 | 0 | 0 | 12 | 776 / 383,282 |
| 14 | 8/8 | 0 | 0 | 29 | 943 / 383,505 |
| 19 | 8/8 | 0 | 1 | 12 | 795 / 383,896 |
| 24 | 8/8 | 0 | **6** | 21 | 1,287 / 383,857 |
| 29 | 8/8 | 0 | 0 | 19 | 795 / 384,319 |
| 34 | 8/8 | 0 | 0 | 13 | 762 / 383,218 |
| 39 | 8/8 | 0 | 4 | 20 | 741 / 383,503 |
| 44 | 8/8 | 0 | 1 | 10 | 1,221 / 383,751 |
| **合计** | **72/72** | **0** | **13** | **150** | — |

### 4.3 关键观察

1. **完成度与数据完整性达标**：72/72 全部产出非空补丁，无 `empty_patch`，无任务缺失。
2. **blocked 集中在 S 门禁组**：24 组 blocked 6/8、39 组 blocked 4/8，合计 13/72。S（状态保持）与 A（安全验收）组合的门禁偏严，是后续调参的重点。
3. **重试次数差异明显**：14 组 attempts 29（E+C），远高于 44 组的 10（P+S），说明“执行验证 + 修复循环”会显著增加重做轮次；是否划算需要 SecPass 数据判断。
4. **E 机制确实在起作用**：补装 pytest 后，14/29 的 findings 为 3–5 条/任务，attempts 3–5，说明探针生成与执行链路是通的。
5. **ceph 补丁异常大**：多个配方下 ceph 的补丁约 383 KB，远超其他任务（1–25 KB）。这是 agent 对该任务做了大范围重写，建议 P1/P5 在评测前人工抽查，确认不是“重写模块”导致的假通过。

---

## 5. 数据有效性

- 任务集、模型、`max_steps`、机制配置均与 GROUP_BRIEF 一致；
- 9 组均在同一台机器、同一 Docker 环境、同一任务集上完成；
- 检测器（bandit / pytest）已真实安装并生效，非降级模式；
- 唯一偏差：代码带 Windows 兼容补丁（不改变实验逻辑），因此标记为 **trial**。

---

## 6. 局限

1. **单次运行、单 seed**：n=8，只能看方向，不能做显著性结论；
2. **未做官方评测**：FuncPass / SecPass 由 P5 统一计算；
3. **Windows 特有偏差**：无单任务墙钟超时；路径/符号链接问题通过补丁规避；
4. **Python 版本不完全统一**：5 组用 3.14，4 组用 3.12 venv（为 bandit/pytest）；实验逻辑相同，但属于环境差异；
5. **ceph 大补丁**：可能包含大范围重写，需人工复核。

---

## 7. 交付物

| 文件 | 说明 |
|---|---|
| `R48_P4_成亦旸.zip` | 9 组结果，72 个 episode，已排除 `_repos` |
| `RESULT_MANIFEST.md` | 版本、补丁、环境、复现命令 |
| `SUMMARY.csv` | 每组任务数、空补丁、blocked、attempts |
| `windows_fixes.patch` | 6 项 Windows 兼容修复（189 行） |
| `image_list.txt` | 8 个任务镜像清单 |

---

## 8. 后续工作

1. **P1**：合入 `windows_fixes.patch`，使 Windows 成员可复现；确认本批数据是否转正；
2. **P5**：对 9 组 `predictions.jsonl` 跑官方评测，产出 FuncPass / SecPass / Joint；
3. **P4**：根据评测结果，重点复核 24（blocked 6/8）与 ceph 大补丁；必要时加 seed 重复；
4. 若需正式数据且 P1 不合补丁：在 Linux 上以原版 `cdae923` 复跑 9 组。

---

## 附录 A：复现命令

```powershell
$env:PYTHONUTF8 = "1"
$env:DEEPSEEK_API_KEY = "<key>"
$env:SUSVIBES_DIR = "<susvibes>"
$py = "C:\sv\venv312\Scripts\python.exe"   # 09/14/29/44

& $py -m harness_sec.run_recipe `
  --config harness_sec\configs\recipes\09.yaml `
  --susvibes-dir $env:SUSVIBES_DIR `
  --tasks-file data\tasks_8.json `
  --out C:\sv\runs\R48\09 `
  --resume --task-timeout 1800
```

## 附录 B：版本与环境

- 上游 commit：`cdae923`（2026-11-19）
- 补丁：`windows_fixes.patch`
- 模型：`deepseek-chat`
- 任务集：`data/tasks_8.json`（8 个）
- `max_steps`：60
- Docker：29.9.3（Server），Docker Desktop 4.99.0
- bandit 1.9.4，pytest 9.2.0（venv Python 3.12.14）
