# 图片与交叉引用索引

以下编号对应 `thesis.tex` 的正文顺序。实验图采用PDF矢量文件，框图由TikZ源文件编译。修改图片内容时，可直接替换对应资源；图题与正文引用保留在表中的章节文件。

图1-1为研究背景的灾后道路观测示意图，约148 mm宽、88 mm高，采用黑白灰绘制观测无人机、局部视野、建筑遮挡、道路积水、空中中继与地面接收中心。实线和虚线箭头分别表示信息回传与接收确认，下方说明资源、观测和交付三方面的限制；图中场景为应用示例。绘图源文件为 figures/common/scenario.tex，预览为 output/pdf/background-scenario.png。当前编排位于正文第2页，与背景文字同页。

结构框架图约148 mm宽、145 mm高；无人机与通信场景示意图保留自然比例。原图1-2与图1-3已合并为图1-2，采用黑白矩形布局。论文题目为“通信资源受限下多无人机协同观测任务可靠完成方法研究”，明确通信资源约束、多无人机协同观测场景及任务可靠完成的目标；三个完整研究题目均交代约束、目标与方法，由 thesis-meta.tex 统一配置，并用于章节、目录、绪论及框图。上方说明应用示例、共同问题与总体目标，随后首先呈现研究一，下方从左至右排列研究二和研究三。各项分别说明问题、目标、方法与创新点。研究一联合确定下一跳和对应链路的发射功率，兼顾能量约束下的聚合吞吐量与网络寿命；研究二在通信预算内选择有助于观测判断的消息；研究三在不完备反馈下兼顾按时正确完成率与能耗。研究一至研究二的虚线标注传输速率与发送耗能，反向虚线说明消息数量与长度形成转发负载；研究二至研究三的实线传递候选消息及长度；研究一至研究三的实线标注“LEADR 的速率与能耗模型”，用于计算发送时间与能耗。虚线表示传输条件与负载的联系，实线表示候选消息与链路计算模型的使用关系。

图4-1与图5-2为可编辑场景示意图。更早的本地备份不随仓库分发；当前稿的批注与验收记录见 [PROGRESS.md](PROGRESS.md)。

| 图号 | 图题 | 题注所在文件 | 图片或绘图源文件 | LaTeX 标签 |
|---|---|---|---|---|
| 1-1 | 灾后道路观测中的无人机协同与信息回传示意 | [chapters/01_introduction.tex](chapters/01_introduction.tex) | [scenario.tex](figures/common/scenario.tex) | `fig:intro:scenario` |
| 1-2 | 本文整体研究框架 | [chapters/01_introduction.tex](chapters/01_introduction.tex) | [research-framework.tex](figures/common/research-framework.tex) | `fig:intro:framework` |
| 2-1 | 一次发送尝试中的数据事件与反馈事件 | [chapters/02_foundations.tex](chapters/02_foundations.tex) | [timeline.tex](figures/common/timeline.tex) | `fig:base:timeline` |
| 2-2 | 局部观测消息的生成、传输与任务判断 | [chapters/02_foundations.tex](chapters/02_foundations.tex) | [semantic-pipeline.tex](figures/common/semantic-pipeline.tex) | `fig:base:semantic-pipeline` |
| 2-3 | 任务类别与消息接收状态的概率表示 | [chapters/02_foundations.tex](chapters/02_foundations.tex) | [belief-types.tex](figures/common/belief-types.tex) | `fig:base:beliefs` |
| 3-1 | 无人机集群中的多跳通信与能量感知路由场景 | [chapters/03_leadr.tex](chapters/03_leadr.tex) | [scenario.pdf](figures/rq1/scenario.pdf) | `rq1:fig:scenario` |
| 3-2 | 不同无人机数量下的路由性能比较 | [chapters/03_leadr.tex](chapters/03_leadr.tex) | [num_a.pdf](figures/rq1/num_a.pdf)<br>[num_b.pdf](figures/rq1/num_b.pdf)<br>[num_c.pdf](figures/rq1/num_c.pdf)<br>[num_d.pdf](figures/rq1/num_d.pdf) | `rq1:fig:size` |
| 3-3 | 不同通信范围下的路由性能比较 | [chapters/03_leadr.tex](chapters/03_leadr.tex) | [com_a.pdf](figures/rq1/com_a.pdf)<br>[com_b.pdf](figures/rq1/com_b.pdf)<br>[com_c.pdf](figures/rq1/com_c.pdf)<br>[com_d.pdf](figures/rq1/com_d.pdf) | `rq1:fig:range` |
| 3-4 | 不同平均飞行速度下的路由性能比较 | [chapters/03_leadr.tex](chapters/03_leadr.tex) | [speed_a.pdf](figures/rq1/speed_a.pdf)<br>[speed_b.pdf](figures/rq1/speed_b.pdf)<br>[speed_c.pdf](figures/rq1/speed_c.pdf)<br>[speed_d.pdf](figures/rq1/speed_d.pdf) | `rq1:fig:speed` |
| 4-1 | 多视角观测与多粒度语义证据选择示意 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [observation-scenario.tex](figures/rq2/observation-scenario.tex) | `rq2:fig:observation` |
| 4-2 | 观测数据生成与消息选择流程 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [workflow.tex](figures/rq2/workflow.tex) | `rq2:fig:workflow` |
| 4-3 | 消息选择的策略网络结构 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [network.tex](figures/rq2/network.tex) | `rq2:fig:network` |
| 4-4 | 基准配置下的有效信念质量与每任务平均通信量 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [quality_cost.pdf](figures/rq2/quality_cost.pdf) | `rq2:fig:tradeoff` |
| 4-5 | 不同局部视角数量下的质量与通信开销 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [agent_count.pdf](figures/rq2/agent_count.pdf) | `rq2:fig:agents` |
| 4-6 | 不同通信预算下的性能变化 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [budget.pdf](figures/rq2/budget.pdf) | `rq2:fig:budget` |
| 4-7 | 不同链路条件下的推理质量与成本 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [link_profile.pdf](figures/rq2/link_profile.pdf) | `rq2:fig:links` |
| 5-1 | 语义可靠交付的逻辑结构与反馈关系 | [chapters/05_cbfc.tex](chapters/05_cbfc.tex) | [system.tex](figures/rq3/system.tex) | `rq3:fig:system` |
| 5-2 | 语义数据送达与累计确认不同步的通信示意 | [chapters/rq3/model.tex](chapters/rq3/model.tex) | [delivery-scenario.tex](figures/rq3/delivery-scenario.tex) | `rq3:fig:delivery-scene` |
| 5-3 | C-BFC 的整体计算流程 | [chapters/rq3/method.tex](chapters/rq3/method.tex) | [controller.tex](figures/rq3/controller.tex) | `rq3:fig:controller` |
| 5-4 | 速率波动强度变化下的性能比较 | [chapters/rq3/experiments.tex](chapters/rq3/experiments.tex) | [01_fading_compact.pdf](figures/rq3/01_fading_compact.pdf) | `rq3:fig:fading` |
| 5-5 | 反馈平均额外时延变化下的性能比较 | [chapters/rq3/experiments.tex](chapters/rq3/experiments.tex) | [02_feedback_compact.pdf](figures/rq3/02_feedback_compact.pdf) | `rq3:fig:feedback` |
| 5-6 | 任务截止时间变化下的性能比较 | [chapters/rq3/experiments.tex](chapters/rq3/experiments.tex) | [03_deadline_compact.pdf](figures/rq3/03_deadline_compact.pdf) | `rq3:fig:deadline` |
| 5-7 | 每节点初始发送能量变化下的性能比较 | [chapters/rq3/experiments.tex](chapters/rq3/experiments.tex) | [04_energy_compact.pdf](figures/rq3/04_energy_compact.pdf) | `rq3:fig:energy` |
| 5-8 | 不同反馈丢失率下的组件比较 | [chapters/rq3/experiments.tex](chapters/rq3/experiments.tex) | [05_ablation_compact.pdf](figures/rq3/05_ablation_compact.pdf) | `rq3:fig:ablation` |

## 本次精简与保留资源

2026-10-27 修订后，正文共24幅编号图。第4章保留总体质量与通信代价、视角数量、通信预算和链路条件四组结果图；分类结果、关键消融及可靠性重复实验以表格呈现。以下7张图及其PNG、数据和绘图代码继续保留，只是不再被正文引用：

- main_accuracy.pdf：与总体比较表重复。
- training_curve.pdf：单次训练的回报曲线。
- max_steps.pdf：通信步数参数对照。
- message_modes.pdf：消息粒度对照，主要结果与限制保留在正文。
- trace_scale.pdf：不同数据子集规模对照。
- ablation.pdf：由消融结果表呈现相同数值。
- reliability.pdf：由三次重复实验表呈现均值与标准差。

第5章的5张四联图使用 *_compact.pdf，保留原坐标、曲线、误差棒与图例，仅缩小子图间和边缘空白；正文显示宽度为0.90倍行宽。原PDF和PNG均保留。运行 scripts/compact_rq3_figures.py 可从原图重新生成紧凑版本。

上述本地备份属于修订历史；当前版本及后续修改由 Git 记录。

2026-10-30 将图4-4至图4-7重新排为较扁的矢量图，四联图减少纵向空白并仅在下排保留横轴标题，同等显示宽度下高度约减少17%—27%。CSV数据、曲线数值和未引用的7张结果图保持不变；重绘入口为 figures/rq2/render_figures.py。框架图同步明确研究三使用 LEADR 的速率与能耗模型；历史批注处理情况见 PROGRESS.md。

2026-11-03 根据文字批注修改框架图及第2章示意图，明确共同约束、各研究的具体问题、方法和输入联系；图4-2将观测数据生成、候选筛选与策略训练改为直接说明功能的文字。各实验结果图的曲线、数值和版式保持原样。验收记录见 output/review-comments-20261103.html。
