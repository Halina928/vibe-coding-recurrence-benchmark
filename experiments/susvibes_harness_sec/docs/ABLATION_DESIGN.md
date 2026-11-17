# 机制归因实验设计（修正版）：不只围绕 K2

> 背景：最初的 3 个消融（`k1_e_a`、`k2_a`、`k2_e_f`）都以 **31 = K2+E+A** 为参照，
> 只能回答"31 里换掉 K2/E/A 会怎样"，**不能**回答"M2 家族其他策略重不重要"、"M3 其他等级重不重要"。
> 本文件给出更完整的归因设计。

## 三层实验，回答不同问题

| 层 | 内容 | 回答 |
|---|---|---|
| **8 臂**（000–111） | M1/M2/M3 开/关（M1 开=k2，M2 开=[l2,p]，M3 开=[f,c,a]） | 哪一层"开"总体有用（粗粒度主效应） |
| **48 组**（recipes/01–48） | k1/k2/k3 × l1/l2/p/e × F/C/A/S（**没有 none**） | 非空策略的哪种组合最好（主实验） |
| **归因实验**（本文件） | **留一法 + 单家族**：固定其他两层，只变一层 | 具体哪个策略/等级在起作用（细粒度） |

## 修正后的归因设计（以 31 = K2+E+A 为参照）

| 组 | 配置 | 相对 31 | 回答 |
|---|---|---|---|
| **M1 家族** | `k1_e_a`（已有） | K2→K1 | 通用知识 vs 任务卡 |
| | **`m1_k3_e_a`**（新增） | K2→K3 | 任务卡 vs 仓库知识 |
| **M2 家族** | `k2_a`（已有，=无检测器） | E→none | 完全不要检测行不行 |
| | **`m2_k2_l1_a`**（新增） | E→L1 | 自审够不够 |
| | `k2_l2_a`（已有，2 任务） | E→L2 | 独立审查 vs 执行探针 |
| | **`m2_k2_p_a`**（新增） | E→P | 规则扫描够不够 |
| **M3 家族** | **`m3_k2_e_none`**（新增） | A→none | 不要门禁/反馈行不行 |
| | `k2_e_f`（已有，=F） | A→F | 只反馈不门禁 |
| | **`m3_k2_e_c`**（新增） | A→C | 只循环 |
| | **`m3_k2_e_s`**（新增） | A→S | 加契约 |
| **单家族** | **`sing_k2`**（新增） | 只有 K2 | 知识卡单独够不够 |
| | **`sing_m2_e`**（新增） | 只有 E | 检测单独够不够 |
| | **`sing_m3_a`**（新增） | 只有 A | 门禁单独够不够 |

（`31` 自身 = K2+E+A，作参照；`k1_e_a`、`k2_a`、`k2_e_f`、`k2_l2_a` 复用已有配置。）

## 运行方式

```bash
# 8 个目标任务
for c in m1_k3_e_a m2_k2_l1_a m2_k2_p_a m3_k2_e_none m3_k2_e_c m3_k2_e_s sing_k2 sing_m2_e sing_m3_a; do
  $PY -m harness_sec.run_recipe --config harness_sec/configs/ablation_full/$c.yaml \\
    --susvibes-dir "$SUSVIBES_DIR" --tasks-file data/tasks_8.json \\
    --out runs/ablation_full/$c --resume --task-timeout 1800
done

$PY -m harness_sec.evaluate --arms-root runs/ablation_full \\
  --susvibes-dir "$SUSVIBES_DIR" --max-workers 1 --local-images --no-rescue \\
  --csv runs/ablation_full/results.csv
```

## 结论边界（写论文时必须说明）

- 当前数据只能说："**在这 8 个任务、这组参照下**，K2 卡是关键，E/A 非必需"；
- **不能**说"M2 家族无用"或"M3 家族无用"——那需要跑完上表的 M2/M3 家族（尤其是 `sing_m2_e`、`sing_m3_a`）；
- 8 个任务样本小，结论需在更多任务/48 组上复核。
