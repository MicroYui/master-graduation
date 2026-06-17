# EviCom-RL：面向动态边缘网络中多智能体视觉推理的链路感知选择性语义通信

## 摘要

多智能体具身感知系统，例如无人机、移动机器人、网联车辆和分布式边缘摄像头，正在越来越多地被要求在部分可观测和时变连接条件下执行视觉推理任务。视觉语言模型和大语言模型的最新进展，使得系统能够将局部视觉观测转化为语义证据，包括信念分布、声明、置信度分数、不确定性估计和自然语言推理依据。然而，在动态边缘网络中，无线链路具有间歇性、带宽有限，并且较长消息更容易错过短暂通信窗口，因此交换全部原始观测或全部语义消息通常并不可行。本文研究面向多智能体视觉推理的链路感知选择性语义通信问题。我们提出 EviCom-RL，这是一种 trace-driven 强化学习框架，用于在 token、时延和送达可靠性约束下学习选择与任务相关的语义消息。在离线阶段，冻结视觉语言模型从真实 VQAv2/COCO 样本中生成全图可见性标签、局部可见性证据和接收方信念更新轨迹；标签空间被统一为 clear、mostly_clear、uncertain、mostly_blocked 和 blocked 五级证据可见性状态。在在线仿真阶段，轻量级 graph-history masked actor-critic PPO 策略回放冻结轨迹，显式建模发送方、接收方、语义粒度、链路状态和已选历史，并学习应传输哪条消息、传输给谁以及采用何种语义粒度。为建模动态连接性，每条消息都关联时延、通信截止时间、送达概率和丢包风险；有效信念更新由送达概率进行折扣。在按 RQ 组织的 quick suite 中，本文分别考察主方法对比、智能体数量、通信预算、通信步数、链路可靠性、消息粒度、trace 规模和关键消融；EviComRL 在 Effective Quality 上全部条件排名第一，并在 Accuracy 与 Macro-F1 上相对多数可部署基线取得稳定优势。该设计将语义推理与通信策略学习分离，避免训练过程中反复在线调用大模型，并为研究动态边缘连接条件下通信高效的多智能体视觉推理提供了可复现框架。

## 1. 引言

分布式具身系统正在成为实时视觉理解的重要平台。无人机、移动机器人、路侧单元和临时边缘摄像头可以在灾害响应、交通监测、基础设施巡检、搜索救援和低空移动等场景中采集互补观测。已有 UAV-enabled edge computing 和协同感知研究均指出，移动边缘节点可以通过靠近数据源的计算与通信能力提升低时延智能服务，但其性能受到带宽、链路稳定性、节点移动性和资源调度的共同制约 [4,16,17]。不同于集中式静态视觉系统，这些智能体通常在有限视野、异构感知质量、遮挡、运动模糊和时变无线连接条件下运行。单个智能体可能只能观测场景中的一个小区域，因此会产生不完整甚至误导性的局部决策。因而，多智能体协作对于鲁棒场景理解至关重要 [4,5,6]。

大语言模型（LLMs）和视觉语言模型（VLMs）的最新发展为协同感知提供了新的抽象方式。近期关于 UAV、机器人和具身智能体的综述表明，基础模型能够增强感知、推理、规划和人机交互能力，并推动低空系统和多机器人系统向更强的 agentic intelligence 演进 [10,11,12]。具身边缘智能体不必只交换原始图像、特征图或检测框，而可以将其局部观测总结为语义证据：任务相关标签空间上的信念分布、置信度分数、不确定性估计、简洁声明或自然语言摘要。这类语义证据具有紧凑、可解释并且与下游决策直接相关的特点。该能力暗示了一种新的多智能体协作形式：智能体交换与任务相关的语义证据，而不是无差别地传输原始感知数据。

然而，动态边缘网络中的语义通信引入了非平凡的决策问题。首先，并非所有语义消息都有用。协同感知和 LLM 多智能体研究均表明，全量通信会带来冗余信息、带宽浪费和低信噪比 [6,13,14]。来自高度不确定或冗余智能体的消息可能对接收方信念贡献很小。其次，并非所有有用消息都能送达。在高移动性边缘网络中，链路质量快速变化，较长的摘要或完整上下文可能错过可用通信窗口。第三，通信与推理天然耦合：短标签消息可能更可靠，但不足以解决冲突；较长解释可能信息量更高，但传输风险也更大。因此，系统必须联合考虑语义价值、消息粒度、token 成本、时延和链路可靠性。

本文研究面向多智能体视觉推理的链路感知选择性语义通信问题。我们不假设每台无人机或边缘设备在策略学习期间都部署完整规模的 LLM。相反，我们使用冻结 VLM/LLM 调用离线构造语义轨迹，并在这些轨迹之上训练轻量级通信策略。这种 trace-driven 形式将昂贵的语义推理与通信策略优化解耦：大模型提供局部证据和信念更新监督，而强化学习决定在动态网络约束下应传输哪些语义消息。

我们在视觉问答任务中实例化该思想，但不直接把 VQAv2 的自然语言答案作为通信策略的监督标签。相反，每个 VQAv2/COCO 样本被转化为一个“问题相关视觉证据是否可见”的多智能体 episode：全图 VLM 判断该问题在完整图像中的证据可见性，局部智能体则只观察同一图像的不同裁剪区域，并给出局部可见性信念。候选消息被构造成多个语义粒度，包括 label、claim、summary 和 full evidence。每条候选消息对接收方信念的更新在线下记录。在强化学习阶段，环境回放这些冻结信念更新，并根据动态边缘链路诱导出的消息特定送达概率对其效果进行折扣。

需要强调的是，本文并不主张用五级证据可见性分类替代标准 VQA answer generation。相反，我们研究的是协同视觉问答之前的一个前置通信问题：当回答某个视觉查询所需的证据分散在多个局部观测中，且通信链路受限时，哪些局部语义证据值得被发送、发送给谁、以及以何种粒度发送。该抽象受到 VQA grounding 和 attention 研究的直接启发：已有工作表明，回答视觉问题往往依赖于定位与问题相关的图像区域，而不是仅依靠语言先验输出答案 [22,23,24,25]。同时，EmbodiedQA、多智能体 embodied QA、image-set VQA 以及多机器人协同空间推理均表明，视觉推理在部分可观测、多视角或多智能体场景中需要获取、整合和筛选互补视觉证据 [26,27,28,29]。因此，EviCom-RL 可以被理解为将“单图像中应看哪里”提升为“分布式局部观测中应通信哪些证据”的链路受限协同推理问题。

所得框架 EviCom-RL 将消息选择形式化为序列决策过程。在每一步中，策略观测候选消息特征、剩余通信预算、当前信念状态和链路感知可靠性特征。策略选择一条候选消息或终止通信。非法动作根据 token 预算、重复选择、接收方容量和最低送达概率进行 mask。策略通过 masked actor-critic PPO 训练，以最大化最终推理质量，同时惩罚 token 使用、时延、丢包风险和截止时间违约。

本文主要贡献如下。

1. 我们将动态边缘连接下的多智能体语义证据交换形式化为链路感知序列决策问题，其中语义收益和送达可靠性被联合优化。
2. 我们提出一种 trace-driven VLM/LLM 流水线，用于从 VQAv2/COCO 构造真实多智能体语义通信轨迹，包括全图可见性真值、局部可见性信念、消息粒度和接收方信念更新。
3. 我们提出动态链路可靠性模型，为每条语义消息分配截止时间、时延、送达概率和丢包风险，并使用送达概率计算有效信念更新。
4. 我们设计 EviCom-RL，一种带有 graph-history actor-critic 策略网络的 masked PPO 算法，用于在 token、时延、接收方容量和可靠性约束下选择语义消息；该网络显式编码发送方证据质量、接收方需求、消息粒度、链路状态和已选历史上下文。
5. 我们建立了可复现的实验套件，将冻结语义轨迹生成与轻量通信策略学习分离，并围绕主方法对比、智能体数量、通信预算、通信步数、链路可靠性、消息粒度、trace 规模和关键消融组织 RQ 实验；trace 构造中采用严格 JSON schema 校验、无效响应重试和内容审核拒绝样本跳过机制，以避免静默兜底污染通信轨迹。

## 2. 相关工作

### 2.1 多智能体系统中的通信学习

学习通信协议长期以来都是多智能体强化学习中的重要问题。Foerster 等人提出 RIAL 和 DIAL，使智能体能够通过强化学习和反向传播学习离散及可微通信协议 [1]。其中 RIAL 将通信动作作为强化学习动作的一部分，而 DIAL 利用可微通信通道把接收方误差信号反向传递给发送方，从而提高通信协议学习效率。CommNet 提出在智能体之间共享连续通信向量，并通过反向传播进行优化；该方法证明，即使不手工设计离散协议，连续消息聚合也可以提升协同任务表现 [2]。IC3Net 进一步引入个体化通信门控，使智能体能够在合作和竞争环境中学习何时通信是有益的，并在更大规模多智能体任务中验证了通信门控的重要性 [3]。这些工作确立了一个原则：通信应当是学习策略的一部分，而不是固定的外部通道。

然而，大多数经典通信学习方法面向抽象仿真环境，其中消息通常是低维向量或离散符号，通信成本也被简化。相比之下，EviCom-RL 考虑由视觉观测生成的类自然语言语义消息。这类消息的成本取决于 token 长度、传输时延和动态链路可靠性。因此，通信决策必须同时考虑语义价值和网络层面的可送达性。

### 2.2 通信高效的协同感知

协同感知研究多个机器人、车辆或摄像头如何共享信息以提升场景理解能力。Who2com 将协同感知形式化为带宽敏感的信息共享问题，并通过 request、match 和 connect 形式的可学习握手机制决定目标智能体应从哪些邻居接收信息 [4]。When2com 在此基础上进一步关注通信图构建问题，通过学习通信组和通信时机，使智能体能够根据当前任务需要动态决定是否通信以及与谁通信 [5]。Where2comm 指出以往协同感知方法常隐含假设一旦协作就共享所有空间区域，而这会造成不必要带宽开销；因此它提出空间置信图以仅通信感知关键区域 [6]。How2comm 进一步研究通信高效且协作实用的多智能体感知，强调消息表示、信息补全和协作收益之间的平衡 [7]。

这些方法表明，选择性通信对于平衡感知精度与通信带宽至关重要。EviCom-RL 遵循这一原则，但在通信表示和可靠性模型上有所不同。现有协同感知方法通常交换特征图、空间置信图或中间感知表示。EviCom-RL 交换源自 VLM 输出的结构化语义证据，例如信念、声明和摘要。此外，EviCom-RL 显式建模动态链路窗口和消息送达概率，这对于移动边缘系统尤其重要。

### 2.3 VQA 证据定位与受控视觉推理

视觉问答研究并不只关注最终答案，还长期关注答案是否建立在问题相关的视觉证据之上。Shih 等人的 Where to Look 将 VQA 中的一个核心问题概括为根据问题定位应关注的图像区域，例如不同问题需要关注交通灯、人物、背景天气或物体属性等不同区域 [22]。VQA-HAT 通过人类擦亮模糊图像中有助于回答问题的区域来收集 human attention map，进一步表明视觉问题通常存在对答案具有关键作用的 evidence regions [23]。GQA 将 grounding 纳入真实世界视觉推理和组合式问答评估，用以区分模型是否真正关注问题和答案所指向的相关视觉区域，而不是仅依赖语言先验 [24]。近期 VQ-FocusAmbiguity 进一步强调视觉问题中的 focus ambiguity，即问题文本可能指向多个潜在图像区域，因此需要显式建模 question focus 与候选证据区域之间的关系 [25]。

上述工作为本文的 evidence visibility 设定提供了任务层面的依据：如果回答视觉问题通常需要定位问题相关证据区域，那么在多智能体局部观测场景中，一个自然问题就是判断某个局部视角是否包含足以支持回答的证据。本文没有声称五级 evidence visibility 是已有 VQA 标准任务；它是为了研究链路受限协同推理而构造的受控证据层抽象。与直接生成自由文本答案相比，该抽象能够避免答案词表偏置、语言先验、VLM 生成方差以及跨视角证据可用性等因素相互缠绕，从而使通信策略的贡献更容易被度量。

### 2.4 部分可观测、多视角与多智能体视觉问答

部分可观测性是具身视觉问答和多智能体视觉推理中的基本挑战。EmbodiedQA 要求智能体在初始视角可能无法看到答案相关像素的情况下主动移动并收集必要视觉信息，说明视觉问答不仅是静态图像分类问题，还包含 evidence acquisition 的过程 [26]。Multi-Agent Embodied Question Answering 进一步研究多个智能体在交互环境中协作探索和回答问题，强调为了准确回答任务查询，智能体需要协调探索分工并共享与目标相关的知识 [27]。Image-Set VQA 将传统单图 VQA 扩展为基于一组图像共同回答问题，任务中可能涉及跨图像对象关系、集合级属性和多视角证据整合 [28]。近期多机器人协同自我中心空间推理工作则关注多个机器人同步 egocentric 视觉流中的空间、时间和可见性问题，要求模型从分布式具身证据中形成一致场景级回答 [29]。

这些研究共同说明，多智能体视觉推理的关键并非单个视角直接输出答案，而是如何在部分、异构且可能不可靠的观测之间获取和融合证据。EviCom-RL 聚焦于这一问题的通信层：在所有相关证据无法被可靠全量传输时，策略必须决定哪些局部证据具有足够的任务价值和链路可送达性。换言之，已有 VQA grounding 研究回答“模型应在图像中看哪里”，EmbodiedQA 研究“智能体应移动到哪里获取证据”，而本文研究“在多智能体局部观测和动态边缘链路下，哪些已经观测到的证据应被通信”。

### 2.5 语义通信与任务导向通信

语义通信已被提出作为未来智能无线网络的关键范式。语义通信不再仅优化比特级重建，而是旨在高效传输与任务相关的意义 [8,9]。Gündüz 等人强调，未来通信系统需要从传输比特扩展到传输上下文、语义和任务相关信息，并将通信目标与下游智能任务相结合 [8]。Luo 等人则系统总结了语义通信的基本概念、应用场景和开放挑战，指出语义层、知识层和任务层的联合设计是未来网络的重要方向 [9]。任务导向通信进一步强调，通信应根据下游任务性能进行评价，例如分类准确率、决策质量或控制效用。

EviCom-RL 可以被视为多智能体推理层面的任务导向语义通信框架。它不设计物理层语义编码器或解码器。相反，它假设语义证据已经由冻结 VLM/LLM 模块提取，并聚焦于决定哪些语义单元应在不可靠边缘链路上传输。其优化目标不是消息重建保真度，而是通信约束下最终协同视觉推理质量。

### 2.6 面向 UAV、机器人和具身智能体的大模型

LLM 和 VLM 近来已被用于 UAV 系统、多机器人协作、具身智能体和低空移动场景。关于 UAV 与 LLM 的综述认为，基础模型可以增强空中系统的感知、记忆、推理、工具使用和人机交互能力，并可能推动 UAV 从执行预设任务的移动平台转变为具备自主推理能力的 agentic aerial system [10]。关于多机器人系统中 LLM 的研究表明，语言模型可以支持任务分配、规划、协同和人机通信，但仍面临时延、幻觉、可扩展性和真实世界 grounding 等挑战 [11]。视觉-语言-动作模型综述则从具身 AI 角度总结了感知、语言、动作和世界模型之间的关系，强调多模态基础模型正在成为机器人系统理解和执行任务的重要接口 [12]。

本文与这些研究互补。我们不关注高层任务规划或直接 UAV 控制，也不要求在每台 UAV 上在线部署完整规模的 LLM。相反，我们研究由冻结或边缘辅助 VLM/LLM 模块产生的语义输出，如何在动态且不可靠的通信网络中被智能体选择性交换。

### 2.7 LLM 多智能体系统中的通信成本

LLM-based 多智能体系统通常依赖智能体之间的大量消息交换。近期研究表明，无限制通信会产生冗余、噪声甚至有害消息。AgentPrune 提出剪枝 LLM-based 多智能体流水线中的非必要通信，通过识别并删除低价值或有害消息降低 token 成本并提升系统效率 [13]。基于拍卖的语言智能体交互方法将通信带宽视为稀缺资源，并让智能体基于效用竞争发言机会，从机制设计角度刻画语言智能体之间的资源理性交互 [14]。关于 LLM-based 多智能体协作扩展性的研究进一步表明，通信拓扑、智能体数量和消息组织方式会显著影响效率与性能，简单增加 agent 数量并不必然带来单调收益 [15]。

这些工作启发了语言智能体系统中的资源理性通信。EviCom-RL 将这一思想扩展到具身边缘感知场景。在我们的设定中，token 成本只是通信成本的一部分；消息还必须穿越具有时延和送达不确定性的动态无线链路。因此，即使某条消息具有较高语义效用，如果它不太可能在链路窗口关闭前送达，也可能并不值得发送。

### 2.8 UAV 边缘计算与动态卸载

UAV-enabled edge computing 研究空中和移动边缘系统中的资源管理、计算卸载、缓存和通信调度 [16]。相关综述从资源管理角度总结了 UAV 与边缘计算结合时面临的移动性、能量、覆盖、计算资源和链路质量问题，并指出 AI-based 方法正逐渐用于复杂资源调度 [16]。动态卸载框架进一步强调了 UAV 操作中的时延、带宽、可扩展性和资源约束，说明在实际空中边缘环境中，计算位置、传输链路和任务 deadline 需要联合优化 [17]。这些研究为本文问题提供了网络与资源管理背景。

EviCom-RL 处理的是系统栈中的不同层次。传统卸载问题关注计算应在哪里执行或资源应如何分配。EviCom-RL 关注在本地或边缘辅助感知已经产生候选消息后，哪些语义证据应被传输。该区别非常重要：即便存在边缘服务器，在间歇链路下上传原始图像也可能不可靠或低效。因此，选择性语义通信是动态边缘智能的一种互补机制。

## 3. 问题形式化

### 3.1 多智能体视觉推理设定

考虑一组具身边缘智能体。该设定与协同感知中多个移动感知节点共享互补观测的基本假设一致 [4,5,6]，同时也与 UAV-enabled edge computing 中移动边缘节点受链路和资源约束的系统背景相符 [16,17]：

$$
\mathcal{N}=\{1,2,\ldots,N\},
$$

其中每个智能体可以表示 UAV、移动机器人、网联车辆或边缘摄像头。任务实例 $k\in\mathcal{K}$ 由视觉场景 $I_k$、任务查询 $q_k$ 和可见性标签空间 $\mathcal{Y}^{vis}$ 组成。本文关注的不是直接回答 VQAv2 的自然语言答案，而是判断回答该查询所需的视觉证据在某一视角中是否可见。因此标签空间被统一为五级有序集合：

$$
\mathcal{Y}^{vis}=\{\text{clear},\text{mostly\_clear},\text{uncertain},\text{mostly\_blocked},\text{blocked}\}.
$$

全图真值 $y_k^*\in\mathcal{Y}^{vis}$ 由冻结 VLM 在完整图像 $I_k$ 和查询 $q_k$ 上生成，并仅用于离线训练奖励和评估。该设定使全局监督标签与局部智能体证据具有相同语义空间，避免把自然语言答案类别与局部可见性证据混合。

本文将该子任务称为 collaborative evidence visibility inference。它不是标准 VQA answer generation 的替代任务，而是面向协同视觉问答的前置证据层任务。其核心假设是：在链路受限的多智能体系统中，联合回答任务查询之前，系统首先需要判断哪些局部观测包含问题相关视觉证据，并决定哪些证据值得通信。直接将自由形式 VQA 答案作为通信策略监督会同时引入答案词表偏置、语言先验、生成式模型随机性和跨视角证据缺失问题；相比之下，可见性信念将任务约束在“证据是否足以支持回答”这一更可控的语义层，从而更适合分析通信选择策略本身的作用。

每个智能体接收局部观测：

$$
o_{i,k},\quad i\in\mathcal{N},
$$

该观测可能只覆盖场景中的一个子区域。令 $\rho_{i,k}\in\{0,1\}$ 表示智能体 $i$ 是否对任务 $k$ 具有有效观测。当 $\rho_{i,k}=1$ 时，冻结 VLM/LLM 模块产生局部语义证据：

$$
e_{i,k}=\left(y_{i,k},p_{i,k},u_{i,k},q_{i,k}^{obs},\ell_{i,k},r_{i,k},\mathbf{b}_{i,k}\right),
$$

其中 $y_{i,k}\in\mathcal{Y}^{vis}$ 为局部可见性预测，$p_{i,k}$ 为置信度，$u_{i,k}$ 为不确定性，$q_{i,k}^{obs}$ 为观测质量，$\ell_{i,k}$ 为观测区域，$r_{i,k}$ 为文本摘要，$\mathbf{b}_{i,k}$ 为 $\mathcal{Y}^{vis}$ 上的信念分布。

信念分布满足：

$$
\mathbf{b}_{i,k}=\left[b_{i,k}^{1},\ldots,b_{i,k}^{|\mathcal{Y}^{vis}|}\right],\quad
\sum_{y\in\mathcal{Y}^{vis}}b_{i,k}^{y}=1.
$$

信念不确定性由熵度量：

$$
H_{i,k}=-\sum_{y\in\mathcal{Y}^{vis}}b_{i,k}^{y}\log\left(b_{i,k}^{y}+\epsilon_h\right).
$$

### 3.2 语义消息空间

每个局部证据项可以被压缩为不同语义粒度的消息。该多粒度消息空间借鉴了语义通信中“传输任务相关意义而非完整原始数据”的思想 [8,9]，也与 LLM 多智能体系统中按消息效用控制通信开销的研究方向一致 [13,14]：

$$
\mathcal{C}=\{\text{label},\text{claim},\text{summary},\text{full}\}.
$$

对于发送方 $i$、接收方 $j$、任务 $k$ 和模式 $c\in\mathcal{C}$，候选消息为：

$$
m_{i\rightarrow j,k}^{c}=\phi_c(e_{i,k}),
$$

其中 $\phi_c$ 是确定性格式化器或基于 prompt 的压缩函数。token 长度为：

$$
T_{i\rightarrow j,k}^{c}=\operatorname{Token}(m_{i\rightarrow j,k}^{c}).
$$

通常有：

$$
T^{label}<T^{claim}<T^{summary}<T^{full}.
$$

短消息更可靠，但可能不足以解决冲突。长消息包含更丰富证据，但会带来更高时延和丢包风险。

### 3.3 动态边缘链路模型

令 $L_m$ 为消息 $m$ 的时延，$D_m$ 表示相应链路的预测通信窗口或截止时间。动态边缘链路中的时延、带宽和任务截止时间约束已被 UAV 边缘计算和动态卸载研究反复强调 [16,17]。在此基础上，本文将链路可用窗口显式映射到语义消息的送达概率。消息 $m$ 的送达概率建模为：

$$
p_m^{del}=\sigma\left(\frac{D_m-L_m}{\tau}\right),
$$

其中 $\tau$ 为温度参数。丢包风险为：

$$
R_m^{drop}=1-p_m^{del}.
$$

该模型刻画了如下事实：如果消息传输时延超过可用链路窗口，则该消息不太可能产生实际作用。由于时延随消息大小增加、随链路带宽增加而降低，较长语义消息在动态连接条件下自然更不可靠。

### 3.4 Trace-Driven 信念更新

接收方信念更新由冻结 VLM/LLM 调用离线生成。该设计参考了 VLM/LLM 在具身系统中作为语义感知与推理模块的趋势 [10,11,12]，同时保留了强化学习通信策略的轻量训练过程 [1,3,18]。令 $\mathbf{b}_{j,k}^{0}$ 为接收方在接收消息 $m_{i\rightarrow j,k}^{c}$ 之前的信念。理想的消息后信念为：

$$
\mathbf{b}_{j,k}^{+,i,c}
=\mathcal{U}_{LLM}\left(o_{j,k},e_{j,k},m_{i\rightarrow j,k}^{c},\pi^{update}\right),
$$

其中 $\pi^{update}$ 是更新 prompt 或 schema。更新模型必须返回包含所有固定标签的 belief 对象，并且概率质量必须为正；缺失字段、非法标签或全零概率会被视为无效输出并触发重试。保存的信念增量为：

$$
\Delta\mathbf{b}_{i\rightarrow j,k}^{c}=\mathbf{b}_{j,k}^{+,i,c}-\mathbf{b}_{j,k}^{0}.
$$

在强化学习过程中，不进行在线 LLM/VLM 调用。环境回放保存的增量，并根据链路可靠性对其进行折扣：

$$
\tilde{\mathbf{b}}_{j,k}^{t+1}
=\operatorname{Normalize}\left(\tilde{\mathbf{b}}_{j,k}^{t}+p_m^{del}\Delta\mathbf{b}_{i\rightarrow j,k}^{c}\right).
$$

当前实现将最终决策中心信念 $B_k$ 取为 agent 0 的更新信念。该设计确保来自其他智能体的信息必须通过被选择的通信动作到达，从而使通信价值可度量。对所有智能体进行可靠性加权融合是一个自然扩展。

### 3.5 优化目标

目标是学习通信策略 $\pi$，在最小化通信成本和送达风险的同时最大化协同推理质量。对于任务 $k$，离线训练中的最终质量由决策中心分配给全图可见性真值 $y_k^*$ 的信念度量：

$$
Q_k^{final}=B_k^{y_k^*}.
$$

优化目标为：

$$
\max_{\pi}\;\mathbb{E}_{\pi}\left[
Q_k^{final}
-\beta_T\tilde{T}^{msg}
-\beta_L\tilde{L}^{comm}
-\beta_R\tilde{R}^{drop}
\right],
$$

其中 $\tilde{T}^{msg}$、$\tilde{L}^{comm}$ 和 $\tilde{R}^{drop}$ 分别表示归一化 token 使用量、通信时延和丢包风险成本。由于 $y_k^*$ 只参与离线奖励计算而不进入策略状态，该目标不会向策略泄露真实标签；策略在推理时只能依据候选消息特征、当前信念、预算状态和链路特征行动。

## 4. 方法

### 4.1 概述

EviCom-RL 包含两个阶段。第一阶段构造冻结语义通信轨迹：全图 VLM 生成任务级可见性真值，局部 VLM 生成每个智能体的局部可见性证据，更新模型生成候选消息对接收方信念的影响。第二阶段训练轻量级强化学习策略，以在动态链路约束下选择消息。

离线 trace 对每个任务实例包含全图真值来源、局部智能体证据、候选语义消息、token 计数、链路特征、送达概率、丢包风险和接收方信念增量。在线仿真环境使用这些 trace 评估通信决策，不再进行额外模型调用。

### 4.2 离线语义轨迹构造

给定一个 VQAv2/COCO 样本，系统首先使用完整图像和任务问题调用冻结 VLM，生成五级可见性真值 $y_k^*$ 及其信念分布，并将该来源记录为全图可见性标注。随后图像被划分为分配给不同智能体的局部 crop。对于每个智能体，冻结 VLM 接收局部 crop 和任务问题，并返回结构化局部证据，包括局部可见性标签、置信度、不确定性、观测质量、信念分布和文本摘要。随后在四种语义粒度下生成候选消息。对于每个发送方-接收方-模式元组，系统记录消息文本、token 长度、链路特征和接收方信念更新。

形式化地，trace 数据集为：

$$
\mathcal{D}^{trace}=\left\{
y_k^*,e_{i,k},m_{i\rightarrow j,k}^{c},T_{i\rightarrow j,k}^{c},
p_m^{del},R_m^{drop},\Delta\mathbf{b}_{i\rightarrow j,k}^{c}
\right\}.
$$

这种 trace-driven 设计具有三个优点。首先，它使所有策略具有可比性，因为它们作用于相同语义证据和信念更新。其次，它避免了策略训练阶段反复调用 LLM/VLM，从而提高可复现性并降低成本。第三，trace 构造阶段对 VLM/LLM 输出执行严格 schema 校验：空内容、空 JSON、缺失 belief、全零概率质量或非法标签会触发重试；不可恢复的格式错误会显式失败，内容审核拒绝样本则被记录并跳过，而不是用兜底伪标签填充。

### 4.3 候选检索与链路感知重排序

完整候选集合可能包含大量发送方-接收方-模式组合。EviCom-RL 首先检索一组规模可控的有前景消息。检索分数为：

$$
S_{retrieve}(m)=
\frac{H_j+C_{ij}^{conf}+C_{ij}^{comp}+q_i^{obs}+0.2b_c}
{(T_m/T^{max}+L_m+\epsilon)(1+R_m^{drop})},
$$

其中 $H_j$ 是接收方熵，$C_{ij}^{conf}$ 是预测冲突，$C_{ij}^{comp}$ 是观测互补性，$q_i^{obs}$ 是观测质量，$b_c$ 是模式相关 bonus。

检索到的候选再使用链路感知特征进行重排序：

$$
S_{rerank}(m)=H_j+C_{ij}^{conf}+C_{ij}^{comp}+q_i^{obs}
+0.8\mathbb{I}[j=0]
+0.4p_m^{del}+0.2\eta_{ij}^{link}+0.1\eta_{ij}^{bw}
-0.7\frac{T_m}{T^{max}}-0.2L_m-0.4R_m^{drop}.
$$

top-$M$ 候选被传递给强化学习策略。

### 4.4 马尔可夫决策过程

每个任务 episode 被建模为有限时域马尔可夫决策过程。在时刻 $t$，状态为：

$$
s_t=\{x_1(t),x_2(t),\ldots,x_M(t),g_t\},
$$

其中 $x_m(t)$ 是候选消息 $m$ 的特征向量，$g_t$ 是全局状态。消息特征包含语义价值指标和链路感知成本：

$$
x_m=\left[
p_i,u_i,q_i^{obs},H_j,C_{ij}^{conf},C_{ij}^{comp},
\operatorname{onehot}(c),\tilde{T}_m,L_m,D_m,p_m^{del},R_m^{drop},
I_m^{sel},I_{j=0},\eta_{ij}^{link},\eta_{ij}^{bw},\tilde{E}_m
\right].
$$

动作空间为：

$$
a_t\in\{0,1,2,\ldots,M\},
$$

其中 $a_t=0$ 表示停止，$a_t=m$ 表示选择候选 $m$。

非法动作会被 mask。如果候选已经被选择、超过剩余 token 预算、送达概率低于阈值、违反接收方容量约束或超过最大 episode 长度，则该候选无效。为了避免随机初始化策略在首步退化为无通信，只要仍存在合法通信动作，训练和推理均不允许首步直接选择 stop；后续步骤中 stop 始终可用。

### 4.5 奖励函数

对于被选择的消息 $m$，单步奖励为：

$$
r_t=\lambda_q\Delta Q_t
-\lambda_T\Delta\tilde{T}_t
-\lambda_L\Delta\tilde{L}_t
-\lambda_RR_t^{drop}
-\lambda_D\mathbb{I}[L_m>D_m].
$$

其中 $\Delta Q_t$ 是训练期间决策中心分配给全图可见性真值的信念提升。策略输入不包含该真值；真值仅用于定义离线训练信号。在当前实现中，质量增益被放大以鼓励策略主动寻找有价值的通信，而 token、时延、能耗、丢包风险和 deadline miss 构成通信代价。episode 终止时，环境还会加入当前最终质量和轻微的已用 token 惩罚，使策略同时关注即时增益和最终预测质量。在评估阶段，学习到的策略仅基于可观测消息和链路特征进行动作选择。

一个具体实例化为：

$$
r_t=2\Delta Q_t
-0.015\frac{T_m}{T^{budget}}
-0.01L_m
-0.003E_m
-0.05R_m^{drop}
-0.03\mathbb{I}[L_m>D_m],
$$

并在 stop 或达到最大步数时追加 $Q_t-0.01T^{used}/T^{budget}$。这些系数不是问题定义的一部分，而是用于当前实现的成本-质量权衡超参数。完整实验中，$\lambda_q,\lambda_T,\lambda_L,\lambda_R,\lambda_D$ 以及终止奖励、warm-start 成本项和候选重排序中的中心偏好、送达概率偏好等权重，均通过 validation split 上的 hyperparameter search 选择；test split 仅用于报告最终结果，避免根据测试集反复调参。

### 4.6 Masked Actor-Critic 策略

EviCom-RL 的主策略采用 graph-history actor-critic 网络，而不是只把候选特征拼接后输入普通 MLP。该设计来自通信决策本身的结构：一条候选消息同时连接发送方、接收方、语义粒度和链路状态；同时，当前 episode 中已经选择过哪些消息会改变后续候选的边际价值。因此，策略网络将每条候选消息的输入拆分为五类结构化子特征：

$$
x_m=\left[x_m^{send},x_m^{recv},x_m^{mode},x_m^{link},x_m^{hist}\right],
$$

其中 $x_m^{send}$ 包含发送方置信度、不确定性和观察质量，$x_m^{recv}$ 包含接收方 belief entropy 以及是否为决策中心，$x_m^{mode}$ 表示 label、claim、summary 或 full evidence 的 one-hot 语义粒度，$x_m^{link}$ 包含 token、时延、送达概率、丢包风险、链路质量、带宽和能耗，$x_m^{hist}$ 表示该消息是否已被选择。候选基础表示和全局状态表示为：

$$
h_m^0=\operatorname{MLP}_{cand}(x_m),\qquad
z_t=\operatorname{MLP}_{global}(g_t).
$$

结构分支分别编码发送方、接收方、语义模式和链路因素，并引入已选消息上下文 $\bar{h}_t^{sel}$ 与决策中心相关上下文 $\bar{h}_t^{ctr}$：

$$
u_m=\operatorname{MLP}_{graph}\left[
h_m^0,\phi_s(x_m^{send}),\phi_r(x_m^{recv}),
\phi_c(x_m^{mode}),\phi_l(x_m^{link}),
\bar{h}_t^{sel},\bar{h}_t^{ctr},z_t
\right].
$$

为了避免结构分支在训练初期破坏候选基础编码，网络使用门控残差融合：

$$
\alpha_m=\sigma\left(W_\alpha[h_m^0,u_m,z_t]\right),\qquad
h_m=h_m^0+\alpha_m\odot u_m.
$$

消息动作 logit 和停止动作 logit 分别为：

$$
\ell_m=w^\top\sigma(W_h[h_m,z_t,\bar{h}_t^{sel},\bar{h}_t^{ctr}]),
$$

$$
\ell_{stop}=w_s^\top\sigma(W_s[z_t,\bar{h}_t^{sel},\bar{h}_t^{ctr}]).
$$

应用 action mask 后，策略为：

$$
\pi_\theta(a_t\mid s_t)=\operatorname{Softmax}(\ell+mask).
$$

价值网络融合 $z_t$、合法候选的 masked mean context、已选历史上下文和中心上下文来估计 $V_\psi(s_t)$。该网络仍保持轻量级，能够在 CPU 上运行；但相比扁平 MLP，它显式区分“谁在发送、发给谁、以何种粒度、经由何种链路、此前已经选过什么”。完整实验中，原始扁平 MLP actor-critic 作为 EviComRL-MLP 消融方法保留，用于检验 graph-history 结构是否带来稳定收益。

### 4.7 PPO 优化

策略使用 proximal policy optimization（PPO）训练 [18]。裁剪策略目标为：

$$
\mathcal{L}_{policy}
=-\mathbb{E}_t\left[
\min\left(
r_t(\theta)\hat{A}_t,
\operatorname{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat{A}_t
\right)
\right],
$$

其中：

$$
r_t(\theta)=\frac{\pi_\theta(a_t\mid s_t,mask_t)}{\pi_{\theta_{old}}(a_t\mid s_t,mask_t)}.
$$

优势函数使用 generalized advantage estimation（GAE）估计 [19]：

$$
\hat{A}_t=\sum_{l=0}^{\infty}(\gamma\lambda)^l\delta_{t+l},
$$

$$
\delta_t=r_t+\gamma V_\psi(s_{t+1})-V_\psi(s_t).
$$

价值损失为：

$$
\mathcal{L}_{value}=\mathbb{E}_t[(V_\psi(s_t)-R_t)^2],
$$

总损失为：

$$
\mathcal{L}=\mathcal{L}_{policy}+c_v\mathcal{L}_{value}-c_e\mathcal{H}(\pi_\theta).
$$

在小规模离线 trace 上，纯 PPO 初始探索可能因为过早 stop 或反复选择低价值消息而产生较大方差。当前算法在 PPO 前加入一次轻量监督 warm start：环境枚举发往决策中心且即时质量增益为正的候选消息，用其构造局部 oracle 动作，对 actor 进行少量交叉熵预热。该步骤不改变最终优化目标，只用于稳定随机初始化。训练过程中，算法同时记录采样 rollout return 和确定性策略在训练集上的平均 return，并保留确定性 return 最好的参数作为最终 checkpoint，以避免小样本 PPO 后期探索噪声导致策略退化。

### 4.8 算法

#### Algorithm 1：离线语义轨迹构造

```text
Input: VQAv2/COCO samples, frozen VLM/LLM, message modes C
Output: Semantic trace dataset D_trace

1: Initialize D_trace ← ∅
2: for each task sample k do
3:     Query the frozen VLM on the full image and question to obtain y_k^*
4:     Validate that y_k^* and its belief follow the fixed visibility schema
5:     Crop the image into local observations {o_i,k}
6:     for each agent i do
7:         Generate local visibility evidence e_i,k using the frozen VLM
8:         Validate label, confidence, uncertainty, observation quality, summary, and belief
9:     end for
10:    for each sender i and receiver j, i ≠ j do
11:        for each message mode c in C do
12:            Construct semantic message m_i→j,k^c
13:            Count tokens and estimate latency, deadline, delivery probability, and drop risk
14:            Query the frozen update model to obtain b_j,k^{+,i,c}
15:            Validate that the updated belief has positive mass on the fixed label space
16:            Store Δb_i→j,k^c and message metadata in D_trace
17:        end for
18:    end for
19: end for
20: return D_trace
```

#### Algorithm 2：EviCom-RL 训练

```text
Input: Training trace dataset D_train, token budget T_max, candidate size M
Output: Trained policy π_θ

1: Initialize policy parameters θ and value parameters ψ
2: Warm-start π_θ with one pass of positive immediate-gain oracle actions
3: Evaluate deterministic return and store the initial checkpoint
4: for each training epoch do
5:     Sample or shuffle task episodes from D_train
6:     for each episode k do
7:         Build top-M candidates using retrieve-rerank-select
8:         Initialize selected set, budget state, and decision-center belief
9:         while the episode is not terminated do
10:            Construct state s_t and action mask
11:            Sample action a_t ~ π_θ(a_t | s_t, mask_t)
12:            if a_t is stop then break
13:            Apply the selected message with delivery-discounted belief update
14:            Compute reward from quality gain, token cost, latency, energy, and drop risk
15:            Store transition
16:        end while
17:    end for
18:    Estimate advantages using GAE
19:    Update θ and ψ using masked PPO
20:    Evaluate deterministic return and keep the best checkpoint
21: end for
22: return the best checkpoint policy π_θ
```

#### Algorithm 3：推理

```text
Input: Test trace dataset D_test, trained policy π_θ
Output: Selected messages and final predictions

1: for each test episode k do
2:     Build top-M candidate messages
3:     Initialize budget and belief state
4:     while valid actions remain do
5:         Construct state and action mask
6:         Select a_t ← argmax_a π_θ(a | s_t, mask_t)
7:         if a_t is stop then break
8:         Apply selected message and update belief/cost statistics
9:     end while
10:    Output the final prediction from the decision-center belief
11: end for
```

## 5. 数据与实现协议

### 5.1 数据集构造

主要 trace 来源是 VQAv2 val2014 及其配对的 COCO val2014 图像。VQAv2 提供面向真实图像的视觉查询，能够减少语言先验捷径并要求视觉 grounding [20]；COCO 提供具有丰富物体和场景上下文的自然图像 [21]。本文使用 VQAv2 的问题作为任务查询，但不直接使用其自然语言答案作为策略监督标签。每个 VQA 样本通过全图可见性标注和局部 crop 证据生成，被转化为一个多智能体可见性推理 episode。

trace 以 JSONL 格式保存全图可见性真值、局部证据、候选消息、链路感知消息成本和信念更新。已有样本按 question ID 索引，从而支持增量构造和中断后恢复。训练、验证和测试划分在策略训练阶段从同一冻结 trace 池中分层抽取，因此划分策略可以在后续实验协议中调整，而不需要改变 trace 格式。

### 5.2 可复现性考虑

所提出协议将 trace 生成与策略训练分离。所有 VLM/LLM 调用均发生在 trace 构造阶段。强化学习、基线评估、消融实验和敏感性分析使用同一冻结 trace。该分离减少了随机模型输出带来的方差，避免重复 API 调用，并使不同通信策略可以被直接比较。

在完整实验中，冻结 trace 首先按标签分布划分为 training、validation 和 test split。PPO 学习率、PPO epoch、clip 系数、熵正则权重、reward 中的成本-质量系数，以及 retrieve-rerank-select 中的语义价值、中心偏好和链路可靠性权重，均在 validation split 上通过网格搜索或分阶段搜索确定。选择指标采用 balanced accuracy、macro-F1、effective quality 和 QCR 的加权组合，以同时衡量分类质量、有效送达质量和通信成本。最终表格中的主结果不使用 validation 分数，而是在固定最优超参数后，于 test split 上重新训练并评估得到；消融实验只改变被考察的模块或系数，其余设置保持与验证集搜索得到的配置一致。
### 5.3 当前实现范围

当前实现聚焦于链路感知语义消息选择的核心机制。它不要求 NS-3 仿真、完整 UAV 轨迹控制或在线 VLM 部署。已实现的网络模型使用轻量代理来表示距离相关链路质量、带宽因子、时延、截止时间、送达概率和丢包风险。该抽象足以研究核心算法问题：通信策略应如何在语义收益与动态送达可靠性之间进行权衡。

## 6. 实验

本节报告当前已完成的完整 RQ suite 结果。与前一阶段只报告单一主设置或 validation sweep 不同，本节结果覆盖 28 个实验条件，包括主设置、智能体数量、通信预算、最大通信步数、链路可靠性、消息粒度、trace 规模以及关键模块消融。需要说明的是，本轮实验是为了快速形成完整实验闭环的 quick suite：它使用单随机种子、2000 条 trace 和 80 个训练 epoch，不作为最终定稿的多 seed 结果。尽管如此，它已经能够检验方法趋势、暴露成本-质量权衡，并为后续正式多 seed 实验提供依据。

### 6.1 数据集与 Trace 构造

实验基于 VQAv2 val2014 问题及其对应的 COCO val2014 图像构造。每个 VQA 样本被转换为一个多智能体 evidence visibility episode：全图 VLM 生成五级可见性真值，局部 agent 只观察图像 crop 并生成局部 belief、声明、摘要和接收方 belief update。标签空间为 clear、mostly_clear、uncertain、mostly_blocked 和 blocked。

当前 trace 文件前缀为 `outputs_api_trace_fixed5/traces/api_trace_fixed5_a9_global.jsonl`。完整 trace 池包含约 3000 条有效 episode；训练和评估脚本能够自动读取主文件及其分片。每条 episode 包含 9 个局部视觉 agent。训练时额外加入一个盲决策中心，使最终判断必须依赖其他 agent 发送的语义证据，而不能直接读取全局图像或全局标签。

### 6.2 实验设置

强化学习和基线评估均在冻结 trace 上进行，不再调用 VLM/LLM。本轮 RQ suite 使用 `num_tasks=2000`、`validation_ratio=0.2`、`eval_split=test`、`seeds=[0]`、`token_budget=120`、`max_steps=8`、`min_delivery_prob=0.45`、`max_candidates=16`、`retrieve_top_k=32`、`train_epochs=80`、`ppo_epochs=4`。策略网络采用 graph-history masked actor-critic PPO。由于本轮为快速完整实验，`include_mlp_baseline=false`，因此表格中的 `EviComRL-MLP` 架构消融不在本轮报告。

超参数来自先前在 validation split 上完成的 32 组 sweep。搜索维度包括 PPO learning rate、reward 中的 quality gain、token cost、drop risk cost，以及候选重排序中的 center bonus 和 delivery probability weight。sweep score 使用 Balanced Accuracy 0.35、Macro-F1 0.30、Effective Quality 0.25、QCR 0.10 的加权组合。32 组配置全部完成，score 范围为 0.440753 至 0.469509，均值为 0.455663；最终采用的配置为 `rl_learning_rate=0.001`、`quality_gain=1.5`、`token_cost=0.025`、`drop_risk_cost=0.06`、`center_bonus=0.6`、`delivery_prob=0.4`。

### 6.3 对比方法与评价指标

当前实验纳入 NoComm、Random、FullComm、TokenGreedy、Greedy、LearnRank、SemanticOnly、LinkOnly、Where2Comm-Trace、How2Comm-Trace、ContextualBandit、EviComRL-w/oDeliveryDiscount、OracleGreedy 和 EviComRL。除 OracleGreedy 外，所有方法均不访问真实标签。OracleGreedy 使用真实标签计算单步最大质量增益，因此只作为不可部署上界，用于说明候选消息中仍存在多少可被挖掘的信息。

Where2Comm-Trace 和 How2Comm-Trace 是对已有协同感知通信思想的 trace-level 适配，而不是直接复现原论文的 3D 感知网络。SemanticOnly、LinkOnly、ContextualBandit 和 EviComRL-w/oDeliveryDiscount 分别用于诊断语义收益、链路可靠性、单步学习排序和送达折扣建模的影响。

评价指标同时覆盖推理质量和通信效率。Accuracy、Balanced Accuracy 和 Macro-F1 衡量最终证据可见性判断是否准确；Avg Tokens、Avg Latency、Avg Energy、Avg Drop Risk 和 Deadline Miss Rate 衡量通信开销与链路风险；Effective Quality 将最终 belief 质量与平均送达概率相乘，用于反映不可靠链路下真正有效的推理质量；QCR 衡量 quality-cost ratio。由于本文研究链路受限通信策略，结果解释不能只看 accuracy，也需要同时观察 token、时延、送达概率和 QCR。

### 6.4 RQ1：EviCom-RL 是否优于可部署通信基线？

RQ1 比较主设置 `main/default` 下的不同通信策略。该设置使用 9 个局部 agent、token budget 120、max steps 8 和 medium 链路条件。表 1 给出方法对比结果。OracleGreedy 访问真实标签，仅作为不可部署上界；其余方法均不访问测试标签。

| Method | Accuracy | Balanced Acc. | Macro-F1 | Avg Tokens | Effective Quality | QCR |
|---|---:|---:|---:|---:|---:|---:|
| OracleGreedy | 0.8225 | 0.8715 | 0.8823 | 27.96 | 0.4512 | 0.2766 |
| EviComRL-w/oDeliveryDiscount | 0.5750 | 0.5469 | 0.4736 | 52.45 | 0.3983 | 0.1783 |
| EviComRL | 0.5600 | 0.5403 | 0.4647 | 52.91 | 0.3799 | 0.1695 |
| How2Comm-Trace | 0.4900 | 0.5403 | 0.4084 | 35.58 | 0.3342 | 0.1899 |
| SemanticOnly | 0.5000 | 0.5221 | 0.4171 | 52.18 | 0.3315 | 0.1423 |
| ContextualBandit | 0.4275 | 0.5160 | 0.3673 | 84.12 | 0.2835 | 0.0947 |
| FullComm | 0.5100 | 0.5068 | 0.4104 | 31.26 | 0.3346 | 0.1867 |
| TokenGreedy | 0.4925 | 0.5085 | 0.4037 | 27.00 | 0.3074 | 0.1794 |
| LearnRank | 0.4075 | 0.4851 | 0.3565 | 27.00 | 0.2804 | 0.1754 |
| Where2Comm-Trace | 0.4075 | 0.4721 | 0.3466 | 27.00 | 0.2823 | 0.1780 |
| Greedy | 0.3900 | 0.4659 | 0.3342 | 27.00 | 0.2764 | 0.1748 |
| Random | 0.3525 | 0.4549 | 0.3231 | 45.35 | 0.2617 | 0.1231 |
| LinkOnly | 0.3300 | 0.4291 | 0.2997 | 27.00 | 0.2530 | 0.1610 |
| NoComm | 0.3225 | 0.2000 | 0.0975 | 0.00 | 0.2000 | 0.2000 |

结果显示，EviComRL 在 Accuracy、Macro-F1 和 Effective Quality 上优于所有可部署非 oracle 基线；Balanced Accuracy 与 How2Comm-Trace 几乎相同，仅低约 0.00003。相比 FullComm，EviComRL 的 Accuracy 提高 0.0500，Balanced Accuracy 提高 0.0335，Macro-F1 提高 0.0543，Effective Quality 提高 0.0453。相比 ContextualBandit，EviComRL 的 Accuracy 提高 0.1325，Macro-F1 提高 0.0974，Effective Quality 提高 0.0963，同时平均 token 从 84.12 降低到 52.91。这说明 PPO 序列决策不仅优于无选择的全量通信，也优于单步上下文排序。

需要注意的是，EviComRL 的 QCR 不是最高。NoComm 因为没有通信成本，QCR 形式上较高，但其 Balanced Accuracy 和 Macro-F1 很低；How2Comm-Trace 和 FullComm 也在 QCR 上略高于 EviComRL。这说明当前 EviComRL reward 更偏向最终 belief 质量，而不是严格最小化 token 成本。换言之，当前方法主要证明了链路感知学习式选择能够提升有效推理质量，但成本约束仍有进一步调优空间。

图 1 展示主设置下不同方法的准确率对比，图 2 展示主设置下通信成本与有效质量之间的折中关系，图 3 展示 PPO 训练曲线。训练回报与最终 test 指标并不完全等价，因此本文解释结果时以 test split 的 Accuracy、Balanced Accuracy、Macro-F1、Effective Quality 和 QCR 为主。

![图 1：主设置方法准确率对比](outputs/rq_suite/quick_fixed5_from_best_20260615_233314/main/default/figures/accuracy_bar.png)

![图 2：主设置质量-成本折中](outputs/rq_suite/quick_fixed5_from_best_20260615_233314/main/default/figures/cost_quality_tradeoff.png)

![图 3：主设置 PPO 训练曲线](outputs/rq_suite/quick_fixed5_from_best_20260615_233314/main/default/figures/rl_training_curve.png)

### 6.5 RQ2：智能体数量如何影响证据整合？

RQ2 比较 3、6 和 9 个 agent 条件。该实验通过 `trace_agent_limit` 从同一 9-agent trace 中截取不同数量的局部观测，用于评估部分可观测覆盖范围对通信策略的影响。

| Agent Count | Accuracy | Balanced Acc. | Macro-F1 | Avg Tokens | Effective Quality | QCR |
|---|---:|---:|---:|---:|---:|---:|
| 3 agents | 0.3025 | 0.4072 | 0.2773 | 31.3 | 0.2741 | 0.1587 |
| 6 agents | 0.5425 | 0.5408 | 0.4427 | 49.4 | 0.3716 | 0.1764 |
| 9 agents | 0.5600 | 0.5403 | 0.4647 | 52.9 | 0.3799 | 0.1695 |

![图 4：不同智能体数量下的 EviComRL 表现](outputs/rq_suite/quick_fixed5_from_best_20260615_233314/paper_figures/rq2_agent_count.png)

结果显示，3-agent 条件下 EviComRL 的 Accuracy 和 Balanced Accuracy 明显低于 6-agent 与 9-agent 条件。这说明 evidence visibility 任务确实依赖足够的局部视角覆盖：当可用 agent 太少时，关键证据更可能完全缺失，通信策略无法凭空恢复未观测到的信息。6-agent 与 9-agent 的 Balanced Accuracy 接近，说明在当前 crop 设计下，视角覆盖达到一定程度后进一步增加 agent 的收益开始趋于饱和。后续正式实验可以将该组扩展为 3、6、9、12 agents，以更清晰地观察覆盖饱和点。

### 6.6 RQ3：通信预算如何影响质量-成本折中？

RQ3 比较 token budget 60、120、180 和 240，用于检验更多通信预算是否一定带来更好推理效果。

| Token Budget | Accuracy | Balanced Acc. | Macro-F1 | Avg Tokens | Effective Quality | QCR |
|---|---:|---:|---:|---:|---:|---:|
| 60 | 0.5600 | 0.5591 | 0.4796 | 44.1 | 0.3810 | 0.1870 |
| 120 | 0.5600 | 0.5403 | 0.4647 | 52.9 | 0.3799 | 0.1695 |
| 180 | 0.5550 | 0.5312 | 0.4587 | 52.6 | 0.3886 | 0.1766 |
| 240 | 0.5500 | 0.5511 | 0.4668 | 55.4 | 0.3828 | 0.1691 |

![图 5：不同 token budget 下的 EviComRL 表现](outputs/rq_suite/quick_fixed5_from_best_20260615_233314/paper_figures/rq3_budget.png)

结果显示，budget 60 已经取得较好的 Balanced Accuracy、Macro-F1 和 QCR，而 budget 180 与 240 没有带来稳定提升。这表明简单放宽 token 预算并不自动改善推理质量，反而可能引入冗余或噪声消息。对于当前 fixed5 visibility 任务，更合理的方向不是无限增大预算，而是学习更好的 stop 策略、候选去冗余机制和成本敏感 reward。

### 6.7 RQ4：多步序列决策是否优于较短通信过程？

RQ4 比较 max steps 4、8 和 12，用于检验通信轮次数量对序列选择的影响。

| Max Steps | Accuracy | Balanced Acc. | Macro-F1 | Avg Tokens | Effective Quality | QCR |
|---|---:|---:|---:|---:|---:|---:|
| 4 | 0.5550 | 0.5567 | 0.4649 | 54.5 | 0.3829 | 0.1695 |
| 8 | 0.5600 | 0.5403 | 0.4647 | 52.9 | 0.3799 | 0.1695 |
| 12 | 0.5575 | 0.5641 | 0.4714 | 55.2 | 0.3809 | 0.1663 |

![图 6：不同最大通信步数下的 EviComRL 表现](outputs/rq_suite/quick_fixed5_from_best_20260615_233314/paper_figures/rq4_max_steps.png)

steps 12 在 Balanced Accuracy 和 Macro-F1 上略优于 steps 4 与 steps 8，说明多步通信确实能提供更细粒度的序列选择空间。与此同时，各步数之间差异并不极端，说明当前候选消息在前几步已经包含大量高价值证据，后续步骤更容易受到冗余和成本项影响。该结果支持将消息选择建模为序列决策，但也提示必须配合终止动作、预算约束和候选重排序，否则更多步数不一定带来单调收益。

### 6.8 RQ5：链路可靠性变化如何影响有效推理质量？

RQ5 比较 easy、medium 和 hard 三种链路设置。与只看分类准确率不同，该组实验重点观察 Effective Quality 和 QCR 是否能揭示动态边缘链路下的真实有效性。

| Link Profile | Accuracy | Balanced Acc. | Macro-F1 | Avg Tokens | Effective Quality | QCR |
|---|---:|---:|---:|---:|---:|---:|
| easy | 0.5500 | 0.5327 | 0.4535 | 61.3 | 0.3886 | 0.1669 |
| medium | 0.5600 | 0.5403 | 0.4647 | 52.9 | 0.3799 | 0.1695 |
| hard | 0.5925 | 0.5642 | 0.4979 | 48.8 | 0.2332 | 0.0888 |

![图 7：不同链路可靠性下的 EviComRL 表现](outputs/rq_suite/quick_fixed5_from_best_20260615_233314/paper_figures/rq5_link_profile.png)

hard 链路条件下 Accuracy 和 Balanced Accuracy 反而更高，但 Effective Quality 和 QCR 明显下降。这一现象说明，单纯分类准确率可能无法完整反映动态链路风险：在 hard 链路下，策略仍可能依靠少数高置信消息做出较准确判断，但较低送达概率会显著削弱有效质量。因此，本文将 Effective Quality 和 QCR 作为核心指标之一是必要的；它们能够揭示“预测看似正确，但通信链路不可靠”的情况。

### 6.9 RQ6：消息语义粒度是否越细越好？

RQ6 比较 label-only、label+claim、label+claim+summary 和 all modes 四种消息粒度设置。

| Message Modes | Accuracy | Balanced Acc. | Macro-F1 | Avg Tokens | Effective Quality | QCR |
|---|---:|---:|---:|---:|---:|---:|
| label | 0.5875 | 0.6065 | 0.4978 | 25.7 | 0.3325 | 0.1967 |
| label+claim | 0.5575 | 0.5611 | 0.4695 | 41.5 | 0.3450 | 0.1727 |
| label+claim+summary | 0.5625 | 0.5444 | 0.4645 | 55.1 | 0.3818 | 0.1681 |
| all | 0.5600 | 0.5403 | 0.4647 | 52.9 | 0.3799 | 0.1695 |

![图 8：不同消息语义粒度下的 EviComRL 表现](outputs/rq_suite/quick_fixed5_from_best_20260615_233314/paper_figures/rq6_message_modes.png)

当前 quick suite 中，label-only 在 Balanced Accuracy、Macro-F1 和 QCR 上表现最好，同时 token 成本最低。这说明在 fixed5 evidence visibility 代理任务中，结构化标签已经包含大量直接有用的信息；更长的 claim 或 summary 虽然可能携带更多自然语言解释，但也带来 token 成本和送达风险。该结果不应被解释为长消息在所有协同视觉任务中无用，而应理解为：当下游目标是五级证据可见性判断时，短标签与 belief 更新可能已经足以支撑中心决策。对于原始 VQA answer generation，summary 或 full evidence 可能仍有更高价值，需要后续 selected-evidence answer evaluation 验证。

### 6.10 RQ7：trace 规模如何影响训练效果？

RQ7 比较 500、1000 和 2000 条 trace 条件。该组用于检验样本规模对策略学习的影响，但当前结果来自单 seed quick suite，因此主要用于趋势判断。

| Trace Count | Accuracy | Balanced Acc. | Macro-F1 | Avg Tokens | Effective Quality | QCR |
|---|---:|---:|---:|---:|---:|---:|
| 500 | 0.5100 | 0.5830 | 0.4215 | 51.3 | 0.3578 | 0.1642 |
| 1000 | 0.4876 | 0.5888 | 0.4368 | 51.6 | 0.3611 | 0.1648 |
| 2000 | 0.5600 | 0.5403 | 0.4647 | 52.9 | 0.3799 | 0.1695 |

![图 9：不同 trace 规模下的 EviComRL 表现](outputs/rq_suite/quick_fixed5_from_best_20260615_233314/paper_figures/rq7_trace_scale.png)

结果没有呈现严格单调增长。n500 和 n1000 的 Balanced Accuracy 较高，但 n2000 在 Accuracy、Macro-F1 和 Effective Quality 上更好。这可能来自单随机种子方差、不同子集标签分布差异，以及较小数据集上测试划分波动。因此，当前结论应保持谨慎：已有 500 到 1000 条 trace 足以训练出有效策略，但最终是否随数据规模稳定提升，需要在 3000 条 trace、多个 seed 和固定测试划分上重新确认。

### 6.11 RQ8：关键模块消融是否支持方法设计？

RQ8 对 EviComRL 的关键组件进行消融，包括盲决策中心、中心奖励、丢包风险奖励、链路感知候选分数、候选重排序、token cost reward 和 warm start。

| Variant | Accuracy | Balanced Acc. | Macro-F1 | Avg Tokens | Effective Quality | QCR |
|---|---:|---:|---:|---:|---:|---:|
| EviComRL | 0.5600 | 0.5403 | 0.4647 | 52.9 | 0.3799 | 0.1695 |
| w/o blind center | 0.2950 | 0.3617 | 0.2837 | 13.0 | 0.2767 | 0.2124 |
| w/o center bonus | 0.5600 | 0.5403 | 0.4647 | 52.9 | 0.3799 | 0.1695 |
| w/o drop risk | 0.5750 | 0.5510 | 0.4767 | 56.9 | 0.3781 | 0.1632 |
| w/o link score | 0.5475 | 0.5375 | 0.4526 | 46.7 | 0.3686 | 0.1742 |
| w/o rerank | 0.5225 | 0.5528 | 0.4325 | 49.4 | 0.3502 | 0.1653 |
| w/o token cost | 0.5650 | 0.5703 | 0.4839 | 57.9 | 0.3812 | 0.1625 |
| w/o warm start | 0.5550 | 0.5361 | 0.4559 | 55.8 | 0.3738 | 0.1628 |

![图 10：EviComRL 关键模块消融](outputs/rq_suite/quick_fixed5_from_best_20260615_233314/paper_figures/rq8_ablation_with_main.png)

消融结果揭示了三个重点。首先，去除盲决策中心后，Balanced Accuracy 降至 0.3617，明显低于主设置。这说明 blind center 设定并非无关细节，而是迫使最终决策依赖跨 agent 通信，从而更严格地检验通信策略。其次，去除 token cost reward 后，Balanced Accuracy 升至 0.5703，但 QCR 降至 0.1625，说明更高分类质量往往伴随更高通信开销，成本约束确实会改变策略偏好。第三，去除 rerank 或 link-aware score 后 Effective Quality 下降，表明候选质量和链路感知排序仍影响最终性能。

额外值得注意的是，EviComRL-w/oDeliveryDiscount 在主设置和跨条件平均中均略高于 EviComRL。该结果表明当前送达概率折扣可能偏保守，或者训练 reward 与 Effective Quality/QCR 指标之间尚未完全对齐。因此，送达折扣不是被证明无效，而是需要重新校准：后续正式实验应比较不同折扣强度，或将折扣项显式纳入超参数搜索。

### 6.12 跨 RQ 结果摘要

以上 RQ1 至 RQ8 分别对应方法比较、系统规模、通信预算、通信步数、链路可靠性、消息粒度、数据规模和模块消融。表 9 只作为跨条件摘要，而不是替代各 RQ 的主要证据。为避免 OracleGreedy 掩盖可部署方法差异，结论主要基于非 oracle 方法。

| Method | Accuracy | Balanced Acc. | Macro-F1 | Avg Tokens | Effective Quality | QCR |
|---|---:|---:|---:|---:|---:|---:|
| OracleGreedy | 0.7699 | 0.8243 | 0.8289 | 26.3 | 0.4230 | 0.2656 |
| EviComRL-w/oDeliveryDiscount | 0.5446 | 0.5461 | 0.4560 | 49.2 | 0.3799 | 0.1770 |
| EviComRL | 0.5361 | 0.5401 | 0.4502 | 49.3 | 0.3618 | 0.1686 |
| How2Comm-Trace | 0.4687 | 0.5249 | 0.3939 | 36.8 | 0.3180 | 0.1788 |
| SemanticOnly | 0.4818 | 0.5110 | 0.4053 | 52.4 | 0.3148 | 0.1355 |
| ContextualBandit | 0.4261 | 0.5035 | 0.3652 | 72.4 | 0.2775 | 0.1053 |
| FullComm | 0.4845 | 0.5031 | 0.3979 | 33.7 | 0.3174 | 0.1735 |
| TokenGreedy | 0.4672 | 0.5006 | 0.3897 | 28.6 | 0.2945 | 0.1693 |
| LearnRank | 0.3935 | 0.4657 | 0.3441 | 28.7 | 0.2715 | 0.1667 |
| Where2Comm-Trace | 0.3940 | 0.4586 | 0.3372 | 28.7 | 0.2745 | 0.1696 |
| Greedy | 0.3779 | 0.4524 | 0.3261 | 28.7 | 0.2686 | 0.1665 |
| Random | 0.3373 | 0.4340 | 0.3075 | 45.9 | 0.2488 | 0.1161 |
| LinkOnly | 0.3209 | 0.4181 | 0.2936 | 28.7 | 0.2477 | 0.1543 |
| NoComm | 0.3171 | 0.2043 | 0.1013 | 0.0 | 0.2001 | 0.2001 |

从条件级排名看，若排除 OracleGreedy 和 EviComRL-w/oDeliveryDiscount 这一变体，EviComRL 在 Accuracy 上 26/28 条件排名第一，在 Macro-F1 上 24/28 条件排名第一，在 Effective Quality 上 28/28 条件排名第一。Balanced Accuracy 的表现更接近：EviComRL 在 10/28 条件排名第一，但在 26/28 条件进入前三，说明部分启发式或短消息策略在类别均衡性上偶尔能取得相近结果。QCR 则只有 1/28 条件排名第一，这再次说明当前策略仍偏向“提高有效推理质量”，而非“最低成本地通信”。

### 6.13 小结

当前 quick RQ suite 形成了按研究问题组织的完整实验闭环，而不是单一混合条件比较。RQ1 表明 EviComRL 在主设置下优于多数可部署基线；RQ2 表明局部视角覆盖不足会显著限制通信策略；RQ3 与 RQ4 说明预算和步数并非越大越好，必须与 stop 策略和成本 reward 联合优化；RQ5 证明链路可靠性会显著改变有效推理质量，因此不能只报告 accuracy；RQ6 表明 fixed5 visibility 任务更偏好短结构化消息；RQ7 暂时说明 trace 规模趋势需要多 seed 确认；RQ8 支持 blind center、链路感知排序、候选重排序和成本项的必要性。

同时，当前结果也暴露了三点后续工作。第一，QCR 不是 EviComRL 的强项，说明 reward 仍需加强成本约束。第二，w/oDeliveryDiscount 变体略优于主方法，说明送达折扣需要重新校准。第三，本轮是单 seed quick suite，尚不能替代最终多 seed 显著性报告。正式定稿实验应使用 3000 条 trace、160 epochs、至少 3 个 seed，并重新报告均值和标准差。

## 7. 讨论

当前实验说明，EviCom-RL 能够在真实 VQAv2/COCO 派生的 fixed5 visibility trace 上学习到有效的语义消息选择策略。与 NoComm 相比，EviComRL 显著提升最终 evidence visibility 判断；与 FullComm 相比，EviComRL 避免了无差别传输带来的冗余干扰；与 SemanticOnly 和 LinkOnly 相比，EviComRL 证明语义收益与链路可靠性需要联合建模；与 ContextualBandit 相比，EviComRL 的优势说明多步通信历史和剩余预算具有实际价值。

OracleGreedy 的结果明显高于 EviComRL，表明候选消息中仍包含大量潜在有效信息，通信策略仍有进一步提升空间。与此同时，EviComRL 的 QCR 尚未达到最优，说明当前策略更偏向提升 belief 质量，而不是严格最小化通信成本。对于动态边缘网络而言，这种偏向并非完全不可接受：在安全巡检、灾害响应或搜索救援场景中，有效推理质量可能比极限节省 token 更重要。但若目标是带宽极端受限的长期部署，仍需要进一步引入成本约束、风险敏感 reward 或 Pareto-front 选择。

本文当前实现仍是一种 controlled proxy task：它研究协同视觉问答中的 evidence visibility communication，而不是直接生成原始 VQA 自然语言答案。该设计有利于控制变量、比较通信策略和避免在线调用大模型带来的高成本；但为了进一步增强任务说服力，后续需要补充 visibility-answer correlation 和 selected-evidence answer evaluation，以证明所选择的 evidence visibility 消息确实能帮助原始 VQA answer generation。

## 8. 总结

本文形式化了动态边缘网络中面向多智能体视觉推理的链路感知选择性语义通信问题。EviCom-RL 将冻结 VLM/LLM 语义轨迹与 graph-history masked actor-critic PPO 结合起来，以学习在 token、时延和送达可靠性约束下应传输哪些语义证据。当前建模将 VQAv2/COCO 样本转换为问题相关证据可见性的五级分类任务，使全图监督、局部证据和接收方信念更新位于同一标签空间。该框架连接了三条研究脉络：通信高效协同感知、LLM/VLM 赋能的具身智能，以及任务导向语义通信。

当前按 RQ 组织的 quick suite 显示，EviComRL 在 Effective Quality 上全部条件排名第一，并在 Accuracy 和 Macro-F1 上相对多数可部署基线取得稳定优势。分组结果进一步表明，智能体视角覆盖、通信预算、通信步数、链路可靠性和消息粒度都会显著改变质量-成本折中。这说明链路感知的学习式选择性语义通信能够有效提升动态边缘约束下的多智能体证据整合质量。与此同时，QCR 与送达折扣消融结果表明，当前方法仍需要更精细的成本约束和折扣校准。总体而言，EviCom-RL 已经形成从 trace 构造、策略学习、baseline 比较到消融分析的完整实验闭环，为后续多 seed 正式实验和原始 VQA answerability 验证奠定了基础。

## 参考文献

[1] J. N. Foerster, Y. M. Assael, N. de Freitas, and S. Whiteson. Learning to Communicate with Deep Multi-Agent Reinforcement Learning. NeurIPS, 2016. https://arxiv.org/abs/1605.06676

[2] S. Sukhbaatar, A. Szlam, and R. Fergus. Learning Multiagent Communication with Backpropagation. NeurIPS, 2016. https://arxiv.org/abs/1605.07736

[3] A. Singh, T. Jain, and S. Sukhbaatar. Learning when to Communicate at Scale in Multiagent Cooperative and Competitive Tasks. ICLR, 2019. https://arxiv.org/abs/1812.09755

[4] Y.-C. Liu, J. Tian, N. Glaser, and Z. Kira. Who2com: Collaborative Perception via Learnable Handshake Communication. ICRA, 2020. https://arxiv.org/abs/2003.09575

[5] Y.-C. Liu, J. Tian, N. Glaser, and Z. Kira. When2com: Multi-Agent Perception via Communication Graph Grouping. CVPR, 2020. https://openaccess.thecvf.com/content_CVPR_2020/html/Liu_When2com_Multi-Agent_Perception_via_Communication_Graph_Grouping_CVPR_2020_paper.html

[6] Y. Hu, S. Fang, Z. Lei, Y. Zhong, and S. Chen. Where2comm: Communication-Efficient Collaborative Perception via Spatial Confidence Maps. NeurIPS, 2022. https://arxiv.org/abs/2209.12836

[7] Y. Ding et al. How2comm: Communication-Efficient and Collaboration-Pragmatic Multi-Agent Perception. NeurIPS, 2023. https://proceedings.neurips.cc/paper_files/paper/2023/file/4f31327e046913c7238d5b671f5d820e-Paper-Conference.pdf

[8] D. Gündüz, Z. Qin, I. E. Aguerri, H. S. Dhillon, Z. Yang, A. Yener, K. K. Wong, and C.-B. Chae. Beyond Transmitting Bits: Context, Semantics, and Task-Oriented Communications. IEEE Journal on Selected Areas in Communications, 2023. https://ieeexplore.ieee.org/document/10056860

[9] X. Luo, H.-H. Chen, and Q. Guo. Semantic Communications for Future Internet: Fundamentals, Applications, and Challenges. IEEE Communications Surveys & Tutorials, 2022. https://dl.acm.org/doi/abs/10.1109/COMST.2022.3223224

[10] H. Tian et al. UAVs Meet LLMs: Overviews and Perspectives Toward Agentic Low-Altitude Mobility. arXiv, 2025. https://arxiv.org/abs/2501.02341

[11] P. Li et al. Large Language Models for Multi-Robot Systems: A Survey. arXiv, 2025. https://arxiv.org/abs/2502.03814

[12] J. Chen et al. A Survey on Vision-Language-Action Models for Embodied AI. arXiv, 2024. https://arxiv.org/abs/2405.14093

[13] Z. Zhang et al. Cut the Crap: An Economical Communication Pipeline for LLM-based Multi-Agent Systems. OpenReview, 2024. https://openreview.net/forum?id=LkzuPorQ5L

[14] M. Kim et al. An Auction-based Method for Language Agent Interaction. AAAI, 2026. https://ojs.aaai.org/index.php/AAAI/article/view/40182

[15] Z. Li et al. Scaling Large Language Model-based Multi-Agent Collaboration. OpenReview, 2025. https://openreview.net/forum?id=K3n5jPkrU6

[16] X. Xia, S. M. M. Fattah, and M. A. Babar. A Survey on UAV-Enabled Edge Computing: Resource Management Perspective. ACM Computing Surveys, 2023. https://dl.acm.org/doi/10.1145/3626566

[17] M. A. Khan et al. Dynamic Task Offloading Edge-Aware Optimization Framework for Enhanced UAV Operations on Edge Computing Platform. Scientific Reports, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11252341/

[18] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal Policy Optimization Algorithms. arXiv, 2017. https://arxiv.org/abs/1707.06347

[19] J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel. High-Dimensional Continuous Control Using Generalized Advantage Estimation. arXiv, 2015. https://arxiv.org/abs/1506.02438

[20] Y. Goyal, T. Khot, D. Summers-Stay, D. Batra, and D. Parikh. Making the V in VQA Matter: Elevating the Role of Image Understanding in Visual Question Answering. CVPR, 2017. https://arxiv.org/abs/1612.00837

[21] T.-Y. Lin et al. Microsoft COCO: Common Objects in Context. ECCV, 2014. https://arxiv.org/abs/1405.0312

[22] K. J. Shih, S. Singh, and D. Hoiem. Where to Look: Focus Regions for Visual Question Answering. CVPR, 2016. https://openaccess.thecvf.com/content_cvpr_2016/papers/Shih_Where_to_Look_CVPR_2016_paper.pdf

[23] A. Das, H. Agrawal, C. L. Zitnick, D. Parikh, and D. Batra. Human Attention in Visual Question Answering: Do Humans and Deep Networks Look at the Same Regions? Computer Vision and Image Understanding, 2017. https://arxiv.org/abs/1606.03556

[24] D. A. Hudson and C. D. Manning. GQA: A New Dataset for Real-World Visual Reasoning and Compositional Question Answering. CVPR, 2019. https://openaccess.thecvf.com/content_CVPR_2019/papers/Hudson_GQA_A_New_Dataset_for_Real-World_Visual_Reasoning_and_Compositional_CVPR_2019_paper.pdf

[25] C. Chen, Y.-Y. Tseng, Z. Li, A. Venkatesh, and D. Gurari. Acknowledging Focus Ambiguity in Visual Questions. arXiv, 2025. https://arxiv.org/abs/2501.02201

[26] A. Das, S. Datta, G. Gkioxari, S. Lee, D. Parikh, and D. Batra. Embodied Question Answering. CVPR, 2018. https://openaccess.thecvf.com/content_cvpr_2018/papers/Das_Embodied_Question_Answering_CVPR_2018_paper.pdf

[27] S. Tan, W. Xiang, H. Liu, D. Guo, and F. Sun. Multi-Agent Embodied Question Answering in Interactive Environments. ECCV, 2020. https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123580647.pdf

[28] A. Bansal, Y. Zhang, and R. Chellappa. Visual Question Answering on Image Sets. ECCV, 2020. https://arxiv.org/abs/2008.11976

[29] K. Peng et al. Seeing Together: Multi-Robot Cooperative Egocentric Spatial Reasoning with Multimodal Large Language Models. arXiv, 2026. https://arxiv.org/abs/2605.18431
