第4章图表使用 `graduation_second_question` 中已完成的最终实验：

`outputs/rq_suite/fixed5_v2_features_20260715_152059/`

主设置为3000条轨迹、80轮训练、随机种子0，增量折扣指数为0.5。三次重复的可靠性特征对照来自 `outputs/diag/clean/G0_nofeat.csv` 和 `G1_feat.csv`，单独统计均值及样本标准差。

| 文件 | 内容 |
|---|---|
| workflow.tex | 冻结轨迹与选择性通信流程 |
| network.tex | 41维候选、11维全局状态及结构化策略网络 |
| main_accuracy.pdf | 主设置准确率 |
| quality_cost.pdf | 有效信念质量与每任务平均通信量（token） |
| training_curve.pdf | 主设置80轮训练回报 |
| agent_count.pdf | 3、6、9个局部视角 |
| budget.pdf | 60、120、180、240 token预算 |
| max_steps.pdf | 4、8、12步上限 |
| link_profile.pdf | 良好、中等、较差链路 |
| message_modes.pdf | 标签至全部消息模式 |
| trace_scale.pdf | 500、1000、2000条轨迹 |
| ablation.pdf | 最新完整实验中的模块对照 |
| reliability.pdf | 可靠性特征的三次重复对照 |

所有实验图均提供PDF矢量文件和PNG预览，中文使用宋体，英文及数字使用Times New Roman。`source_data/` 保存绘图读取的CSV与训练回报文件。`render_figures.py` 仅重新排版既有数据，不启动模型或实验；编译论文不需要运行该脚本。

图表中的“每任务平均通信量”先对单个任务所选消息的 token 数求和，再对任务取平均，对应原数据字段 `avg_tokens`（可靠性特征对照中为 `avg_tok`），不是单条消息的平均长度。原始字段名称和实验数值保持不变。

独立重绘时，在安装了 `matplotlib`、`numpy` 及上述字体的 Python 环境中运行：

```bash
python figures/rq2/render_figures.py
```

脚本优先读取本目录已打包的 `source_data/`，完整源码包不依赖外部实验仓库。只有本地数据文件缺失时，才从 `--study` 指定的完整实验目录补齐；未指定时使用相邻 `graduation_second_question` 仓库中的上述实验目录。可靠性对照的补齐路径为该仓库 `outputs/diag/clean/`。如仅需更新部分图，可通过 `--figures quality_cost reliability` 等名称选择输出。
