# 图片与交叉引用索引

以下编号对应 `thesis.tex` 的正文顺序。实验图采用PDF矢量文件，框图由TikZ源文件编译。修改图片内容时，可直接替换对应资源；图题与正文引用保留在表中的章节文件。

| 图号 | 图题 | 题注所在文件 | 图片或绘图源文件 | LaTeX 标签 |
|---|---|---|---|---|
| 1-1 | 资源受限无人机网络中的数据回传与语义协同场景 | [chapters/01_introduction.tex](chapters/01_introduction.tex) | [scenario.tex](figures/common/scenario.tex) | `fig:intro:scenario` |
| 1-2 | 本文主要研究内容 | [chapters/01_introduction.tex](chapters/01_introduction.tex) | [research-chain.tex](figures/common/research-chain.tex) | `fig:intro:chain` |
| 1-3 | 本文整体研究方案 | [chapters/01_introduction.tex](chapters/01_introduction.tex) | [research-framework.tex](figures/common/research-framework.tex) | `fig:intro:framework` |
| 2-1 | 一次发送尝试中的数据事件与反馈事件 | [chapters/02_foundations.tex](chapters/02_foundations.tex) | [timeline.tex](figures/common/timeline.tex) | `fig:base:timeline` |
| 2-2 | 语义证据从局部形成到接收端使用的过程 | [chapters/02_foundations.tex](chapters/02_foundations.tex) | [semantic-pipeline.tex](figures/common/semantic-pipeline.tex) | `fig:base:semantic-pipeline` |
| 2-3 | 语义类别信念与接收状态信念的区别 | [chapters/02_foundations.tex](chapters/02_foundations.tex) | [belief-types.tex](figures/common/belief-types.tex) | `fig:base:beliefs` |
| 3-1 | 无人机集群中的多跳通信与能量感知路由场景 | [chapters/03_leadr.tex](chapters/03_leadr.tex) | [scenario.pdf](figures/rq1/scenario.pdf) | `rq1:fig:scenario` |
| 3-2 | 不同无人机数量下的路由性能比较 | [chapters/03_leadr.tex](chapters/03_leadr.tex) | [num_a.pdf](figures/rq1/num_a.pdf)<br>[num_b.pdf](figures/rq1/num_b.pdf)<br>[num_c.pdf](figures/rq1/num_c.pdf)<br>[num_d.pdf](figures/rq1/num_d.pdf) | `rq1:fig:size` |
| 3-3 | 不同通信范围下的路由性能比较 | [chapters/03_leadr.tex](chapters/03_leadr.tex) | [com_a.pdf](figures/rq1/com_a.pdf)<br>[com_b.pdf](figures/rq1/com_b.pdf)<br>[com_c.pdf](figures/rq1/com_c.pdf)<br>[com_d.pdf](figures/rq1/com_d.pdf) | `rq1:fig:range` |
| 3-4 | 不同平均飞行速度下的路由性能比较 | [chapters/03_leadr.tex](chapters/03_leadr.tex) | [speed_a.pdf](figures/rq1/speed_a.pdf)<br>[speed_b.pdf](figures/rq1/speed_b.pdf)<br>[speed_c.pdf](figures/rq1/speed_c.pdf)<br>[speed_d.pdf](figures/rq1/speed_d.pdf) | `rq1:fig:speed` |
| 4-1 | 冻结语义轨迹与选择性通信策略的整体流程 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [workflow.tex](figures/rq2/workflow.tex) | `rq2:fig:workflow` |
| 4-2 | 可靠性与历史感知的掩码策略网络 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [network.tex](figures/rq2/network.tex) | `rq2:fig:network` |
| 4-3 | 主设置下的证据可见性分类准确率 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [main_accuracy.pdf](figures/rq2/main_accuracy.pdf) | `rq2:fig:accuracy` |
| 4-4 | 主设置下的有效信念质量与每任务平均通信量 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [quality_cost.pdf](figures/rq2/quality_cost.pdf) | `rq2:fig:tradeoff` |
| 4-5 | 主设置下 PPO 的训练回报变化 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [training_curve.pdf](figures/rq2/training_curve.pdf) | `rq2:fig:training` |
| 4-6 | 不同局部视角数量下的质量与通信开销 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [agent_count.pdf](figures/rq2/agent_count.pdf) | `rq2:fig:agents` |
| 4-7 | 不同通信预算下的性能变化 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [budget.pdf](figures/rq2/budget.pdf) | `rq2:fig:budget` |
| 4-8 | 最大通信步数对策略性能的影响 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [max_steps.pdf](figures/rq2/max_steps.pdf) | `rq2:fig:steps` |
| 4-9 | 不同链路条件下的推理质量与成本 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [link_profile.pdf](figures/rq2/link_profile.pdf) | `rq2:fig:links` |
| 4-10 | 可用语义消息模式对策略性能的影响 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [message_modes.pdf](figures/rq2/message_modes.pdf) | `rq2:fig:modes` |
| 4-11 | 不同语义轨迹规模下的策略表现 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [trace_scale.pdf](figures/rq2/trace_scale.pdf) | `rq2:fig:scale` |
| 4-12 | 主要组成部分的消融结果 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [ablation.pdf](figures/rq2/ablation.pdf) | `rq2:fig:ablation` |
| 4-13 | 可靠性特征对分类质量和每任务平均通信量的影响 | [chapters/04_evicom.tex](chapters/04_evicom.tex) | [reliability.pdf](figures/rq2/reliability.pdf) | `rq2:fig:reliability` |
| 5-1 | 语义可靠交付的逻辑结构与反馈关系 | [chapters/05_cbfc.tex](chapters/05_cbfc.tex) | [system.tex](figures/rq3/system.tex) | `rq3:fig:system` |
| 5-2 | C-BFC 的整体计算流程 | [chapters/rq3/method.tex](chapters/rq3/method.tex) | [controller.tex](figures/rq3/controller.tex) | `rq3:fig:controller` |
| 5-3 | 速率波动强度变化下的性能比较 | [chapters/rq3/experiments.tex](chapters/rq3/experiments.tex) | [01_fading.pdf](figures/rq3/01_fading.pdf) | `rq3:fig:fading` |
| 5-4 | 反馈平均额外时延变化下的性能比较 | [chapters/rq3/experiments.tex](chapters/rq3/experiments.tex) | [02_feedback.pdf](figures/rq3/02_feedback.pdf) | `rq3:fig:feedback` |
| 5-5 | 任务截止时间变化下的性能比较 | [chapters/rq3/experiments.tex](chapters/rq3/experiments.tex) | [03_deadline.pdf](figures/rq3/03_deadline.pdf) | `rq3:fig:deadline` |
| 5-6 | 每节点初始发送能量变化下的性能比较 | [chapters/rq3/experiments.tex](chapters/rq3/experiments.tex) | [04_energy.pdf](figures/rq3/04_energy.pdf) | `rq3:fig:energy` |
| 5-7 | 不同反馈丢失率下的组件比较 | [chapters/rq3/experiments.tex](chapters/rq3/experiments.tex) | [05_ablation.pdf](figures/rq3/05_ablation.pdf) | `rq3:fig:ablation` |
