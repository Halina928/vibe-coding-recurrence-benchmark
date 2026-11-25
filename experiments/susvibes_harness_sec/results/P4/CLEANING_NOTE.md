# P4 数据清洗说明

原始 P4 predictions 在 Windows 上生成，包含两类环境伪影：

1. `old mode/new mode`：132 个文件的可执行位从 100755 变 100644（含 `runtests.py`），导致 5c7a 测试无法运行；
2. ceph 的 1134 个 symlink 被记录为 `+++ /dev/null` 删除。

清洗脚本逻辑（见 `scripts/` 或本次处理）：删除 mode 行、删除 `+++ /dev/null` 文件块、保留真实代码 hunk。
清洗后重新评测 wagtail-5c7a 与 ceph，其余 6 个任务沿用原报告。
