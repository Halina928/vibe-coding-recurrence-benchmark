# P4 实验结果说明（R48，9 组全量）

## 交付内容

- 配方：`04 / 09 / 14 / 19 / 24 / 29 / 34 / 39 / 44`（P4 全部 9 组）
- 任务集：`data/tasks_8.json`（8 个任务，全部 8/8）
- 模型：`deepseek-chat`（GROUP_BRIEF 铁律第 3 条）
- `max_steps`：60（未加 `--max-steps`）
- 合计：**72 个 episode、72 条 prediction、0 条空补丁**
- 每组产物：`predictions.jsonl`、`predictions_first.jsonl`、`<任务>/episode.json`、`<任务>/trace.jsonl`
- 已排除 `_repos/`

## 代码版本

- 上游：`Halina928/vibe-coding-recurrence-benchmark` @ `cdae923`（2026-11-19）
- 本地补丁：`windows_fixes.patch`，**未合入主线**
- 因此这批结果按 trial 处理；P1 合入补丁后可作正式数据

## Windows 兼容补丁（不改实验逻辑）

| # | 文件 | 内容 | 原因 |
|---|---|---|---|
| 1 | `sandbox.py`、`e_exec.py`、`p_sast.py` | 子进程输出强制 UTF-8 | 中文 Windows 默认 GBK |
| 2 | `sandbox.py`、`run_recipe.py` | 删除 git 仓库前清只读位 | Windows `.git/objects` 只读 |
| 3 | `run_recipe.py` | `SIGALRM` 平台保护 | Windows 无该信号 |
| 4 | `sandbox.py` | `docker cp` 失败时改用 tar 流解包并跳过 symlink | ceph 仓库含 1134 个 symlink，普通用户无创建权限 |
| 5 | `run_recipe.py` | `--resume` 在导出仓库之前判断 | 避免重复导出 |
| 6 | 机器配置 | `git config --global core.longpaths true` | Windows MAX_PATH 260，路径过深会让 `git diff` 为空 |

> 第 4、6 条是关键：不加时所有 `model_patch` 都是 0 字符（第一批数据已作废，见 `runs/R48_invalid_pathlength`）。

## 检测器环境（重要）

本机无法访问 PyPI，因此用 Docker 容器下载 Windows wheel，离线安装到独立 venv：

- venv：`C:\sv\venv312`（Python 3.12.14）
- 安装：`bandit 1.9.4`、`pytest 9.2.0`
- wheel 来源：`python:3.12-slim` 容器，`pip download --platform win_amd64 --python-version 3.12`
- 运行：
  - `09 / 14 / 29 / 44` 使用 `C:\sv\venv312\Scripts\python.exe`
  - `04 / 19 / 24 / 34 / 39` 使用系统 Python 3.14

> 14 和 29 曾因缺 pytest 导致 E 静默返回空，已用 venv 重跑；最终数据 E 的 findings 为 3–5 条/任务。

## 运行环境

- Windows 11（build 26200）
- Docker Desktop 4.99.0，Linux 容器
- 8 个任务镜像：`songwen6968/susvibes.x86_64.eval_*`（见 `image_list.txt`）
- 输出根目录：`C:\sv\runs\R48`（短路径，规避 MAX_PATH）

## 复现命令（单组）

```powershell
$env:PYTHONUTF8 = "1"
$env:DEEPSEEK_API_KEY = "<key>"
$env:SUSVIBES_DIR = "<susvibes>"
$py = "C:\sv\venv312\Scripts\python.exe"   # 需要 bandit/pytest 的组

& $py -m harness_sec.run_recipe `
  --config harness_sec\configs\recipes\09.yaml `
  --susvibes-dir $env:SUSVIBES_DIR `
  --tasks-file data\tasks_8.json `
  --out C:\sv\runs\R48\09 `
  --resume --task-timeout 1800
```

## 结果摘要

- 9 组 × 8 任务 = 72 条 prediction，**全部非空**
- `ceph`、`wagtail-5c7a` 多数配方 `blocked=True`（A 门禁拦截，符合预期）
- 官方评测（FuncPass/SecPass）未在本机执行：需要 SusVibes 的 Python 依赖，本机 PyPI 不通；建议由 P5 统一评测

## 备注

- 单次运行、单 seed；n=8 只能看方向
- `runs/R48_invalid_pathlength/` 是第一批无效结果（路径长度导致补丁全空），仅留档
