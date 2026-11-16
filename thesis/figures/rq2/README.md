第4章图表使用 `graduation_second_question` 中已完成的最终实验：

`outputs/rq_suite/fixed5_v2_features_20260715_152059/`

基准配置为3000条轨迹、80轮训练、随机种子0，增量折扣指数为0.5。三次重复的可靠性特征对照来自 `outputs/diag/clean/G0_nofeat.csv` 和 `G1_feat.csv`，单独统计均值及样本标准差。

| 文件 | 内容 |
|---|---|
| workflow.tex | 观测数据生成与消息选择流程 |
| network.tex | 41维候选、11维全局状态及结构化策略网络 |
| main_accuracy.pdf | 基准配置准确率 |
| quality_cost.pdf | 有效信念质量与每任务平均通信量（token） |
| training_curve.pdf | 基准配置80轮训练回报 |
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

2026-10-27 精简正文后，结果图中仅 quality_cost.pdf、agent_count.pdf、budget.pdf 和 link_profile.pdf 仍在正文引用。其余7张结果图保留在本目录，分类比较、关键消融与可靠性重复实验改由表格呈现；训练过程、最大步数和轨迹规模曲线暂不展示。消息粒度对照的主要数值和适用限制仍在正文说明。所有已记录实验数据保持原样。

2026-10-30 将上述四张图重新排为较扁的版式：quality_cost 的画布为6.45×2.50英寸，三张四联图为6.45×3.30英寸，并缩小子图间距。相同显示宽度下，最终PDF高度分别约减少17%和27%；图中文字使用SimSun与Times New Roman，曲线和源数据不变。仅重绘这四张图可在论文根目录执行：

```powershell
python figures/rq2/render_figures.py --figures quality_cost agent_count budget link_profile
```

部分重绘仅更新选中的PDF与PNG；仅在选中ablation或重绘全部图时生成消融汇总表。此处使用已有汇总数据；编译论文无需重绘。
