# M0 / P0-1 Literature & Novelty Review

**Role:** R1 — Literature & Theory Scholar  
**Date:** 2026-09-03  
**Evidence cutoff:** 2026-09-03  
**Scope:** RQ-001–RQ-004；术语；第一批核心阅读  
**Status:** R1 REVIEW COMPLETE；等待 R4 validity review 与 R0 决议  

> 本文是定向 literature/novelty review，不是系统综述或 meta-analysis。它不包含项目实验结果，不授权架构或代码实现。文中严格区分 PAPER EVIDENCE、INTERPRETATION、HYPOTHESIS 与 IDEA。

## 1. Executive verdict

| RQ | R1 verdict | 是否已被充分回答 | 核心问题 |
|---|---|---|---|
| RQ-001 Planning value boundary | **NARROW** | 否；但相邻问题已高度拥挤 | “planning”与 ReAct 并非互斥；task conditions 过多且相互混杂；ADAPT 已直接研究 task complexity × model capability × as-needed planning |
| RQ-002 Dynamic replanning and recovery | **MERGE → RQ-001** | 否；但当前表述与已有 adaptive planning / tool-failure work 高度重叠 | ReAct 本身会依据 observation 调整行动；必须把 explicit plan revision 与 retry、repair、next-action reasoning 分开 |
| RQ-003 Reflection policy | **NARROW** | 否 | “selective”与“trace-grounded”本身不足以构成 novelty；应分解 trigger、diagnosis、correction，并排除 oracle leakage 与 cross-episode memory |
| RQ-004 Explanatory failure model | **MERGE → RQ-001 / RQ-003 analysis layer** | 描述性 taxonomy 已有大量工作；本项目的交互解释尚未被回答 | generic taxonomy 缺乏新意；trace association 不能自动支持 causal explanation；独立 RQ 会扩大 scope |

**INTERPRETATION:** M0 最稳妥的结果不是接受四个并列 RQ，而是冻结两个核心 RQ：一个研究 explicit planning / adaptive replanning 的边界，一个研究 evidence-grounded reflection policy；failure analysis 是两者共同的预注册解释层。

**HYPOTHESIS:** 如果项目能够在同一 task family 内控制 model、tool、prompt information、termination 与 inference budget，最可能形成可辩护贡献的不是“某机制平均更好”，而是机制效果随 dependency structure、failure observability 和 model capability 改变的、可复现的 interaction boundary。

## 2. 先解决概念重叠

### 2.1 PAPER EVIDENCE

- ReAct 将 reasoning trace 与 action 交错生成；作者明确说 reasoning trace 可用于诱导、追踪和更新行动计划，并处理异常。因此 ReAct 不是“完全无计划”的 agent。[Yao et al., ICLR 2023](https://arxiv.org/abs/2210.03629)
- ADAPT 明确区分 iterative executor（ReAct）与 plan-and-execute，并把其 planning 定义为日常意义上的“为复杂任务设计 subtask list”，不是 classical AI planning。它在 executor 失败时才继续分解，并报告效果随任务复杂度与 executor 能力变化；但主要结果因成本限制只做了单次运行。[Prasad et al., Findings of NAACL 2024](https://aclanthology.org/2024.findings-naacl.264/)
- PlanGenLLMs 总结出 LLM planning 研究已覆盖多个领域，但方法高度 task-specific，评价标准仍缺乏一致性；其六个评价维度包括 completeness、executability、optimality、representation、generalization 与 efficiency。[Wei et al., ACL 2025](https://aclanthology.org/2025.acl-long.958/)
- Reflexion 把环境给出的 binary/scalar feedback 转成语言反馈，并把它加入后续 episode 的上下文；这同时引入 reflection、feedback 与 episodic memory，而不是一个纯粹的“额外思考步骤”。[Shinn et al., NeurIPS 2023](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)

### 2.2 INTERPRETATION

当前四个 RQ 的 treatment 并不天然正交：

1. ReAct 可以进行隐式、局部、逐步的计划更新；
2. replanning 需要以一个可识别的旧 plan 为前提；
3. reflection 可以输出新 plan，因此可能同时构成 replanning；
4. Reflexion 又把 reflection 与跨 episode memory 捆绑。

因此，若不先操作化，实验标签会把 prompt wording、额外 test-time compute、feedback、memory 与真实策略差异混在一起。

## 3. M0 建议操作定义

以下全部是 **IDEA — proposed project definitions**，不是声称学术界已有唯一共识。

### 3.1 Planning

**IDEA:** `planning` 是在执行其覆盖的第一个外部动作之前，生成一个可记录的 prospective plan artifact。该 artifact 至少包含两个未来 subgoal/action unit 及其顺序或依赖关系，并被后续 executor 明确读取。

- 包含：一次性 subgoal list、带依赖的 task graph、partial-order plan。
- 不包含：普通 chain-of-thought；只选择下一步 action；事后对已发生轨迹的总结。
- 必须另行记录：plan granularity、representation、生成时可见信息、是否允许工具反馈、planner 与 executor 是否同一 model。
- 本项目首轮的 planning 应限定为 **colloquial task-decomposition planning**，不得与 classical planning 的 soundness、completeness 或 optimality 混称。

### 3.2 Replanning

**IDEA:** `replanning` 是在至少一个外部 action/observation 已发生后，因新证据表明原 plan 的前提、可执行性或预期进展失效，而显式修改、替换或重新排序旧 plan 的未执行部分；必须留下 `old plan → trigger evidence → new plan` 的可审计记录。

- 不包含：原样重试同一 tool call；只修正一个参数；ReAct 常规的下一动作选择；没有旧 plan artifact 的“重新想一遍”。
- local repair 只有在改变未来 plan commitment 时才算 replanning。
- trigger 必须预先分类为 explicit error、silent/wrong result、incomplete observation、state change 或 constraint revelation。

### 3.3 Reflection

**IDEA:** `reflection` 是一次与常规 action selection 分离的 meta-level inference：它读取指定 trace evidence 与 feedback，输出 `(diagnosis, corrective guidance)` 中至少一项，并且该输出被下一次行动或重试显式使用。

- 不包含：普通 ReAct Thought；无 trace 证据的“再想想”；只复述错误消息；直接重试。
- 必须分别标记：intrinsic/self feedback、environment feedback、deterministic verifier、human/oracle feedback。
- 必须分别标记：same-episode correction 与 cross-episode learning。首三个月建议只研究 same-episode，避免把 reflection 与 memory 混合。

### 3.4 Recovery

**IDEA:** 对预先声明为 recoverable 的干预实例，在扰动发生后，agent 于同一总预算和所有硬约束内仍达到任务 ground truth，称为 recovery。

- `end-to-end recovery rate = recovered / all recoverable injected cases`。
- `conditional recovery rate = recovered / detected recoverable cases`；必须与 detection rate 同时报，避免只在检测成功样本上制造高恢复率。
- 不得把第一次 tool call 失败后原样成功重试，自动等同于 strategy-level recovery；应单列 transient retry recovery。
- irrecoverable、ambiguous 与 engineering/harness failure 不进入 recovery 分母，但必须报告数量与判定规则。

### 3.5 ReAct baseline

**IDEA:** `ReAct baseline` 是同一 backbone model 在 `Thought → Action → Observation` 交错循环中逐步选择动作；它可依据 observations 调整下一动作，但没有：

1. 独立的 ex-ante plan artifact；
2. 独立 planner call；
3. 显式 replan event；
4. 专用 reflection pass；
5. 跨 episode reflective memory。

同 model、tool schema/access、task information、demonstration count、termination、temperature/decoding、最大 wall-clock / tool / LLM-call / token budget 必须一致或透明报告。因为 ReAct 本身能局部适应，项目不得把它描述为“不能规划、不能处理异常”的 straw baseline。

### 3.6 为完成 P0-1 还应冻结的两个术语

**IDEA — task success:** 由环境状态或确定性 verifier 判定所有目标约束均满足；LLM 自述完成不算成功。若任务允许 partial credit，必须预先定义 subgoal 权重，并与 binary success 分开报告。

**IDEA — fair baseline:** 除目标 runtime intervention 外，模型、可见信息、工具、初始状态、提示示例、停止规则和采样协议一致；同时报告 `equal maximum budget` 和 `actual resources consumed`。仅令复杂策略拥有更多调用再比较 raw success，不构成公平因果比较；但强行让所有方法实际消耗相同 tokens 也可能不自然，因此 success-at-budget curve 优于单点 equalization。

## 4. RQ-001 — Planning value boundary

### 4.1 学术界已经知道什么？— PAPER EVIDENCE

- ReAct 证明交错 reasoning/action 可优于只 reasoning 或只 acting 的若干基线，并允许 observation 驱动的计划更新；该论文不回答 separate explicit plan 相对 ReAct 的普遍价值边界。[Yao et al., ICLR 2023](https://arxiv.org/abs/2210.03629)
- Plan-and-Solve 在非交互式 reasoning datasets 上先规划再求解，报告相对 Zero-shot-CoT 的提升；它不能直接支持 tool-using agent 的结论。[Wang et al., ACL 2023](https://aclanthology.org/2023.acl-long.147/)
- LLM+P 显示纯 LLM 在形式化长程 planning 问题上常不能产生可行 plan，而把自然语言转换为 PDDL 并调用 classical planner 可显著改善正确/最优 planning；但其 intervention 同时加入了符号模型与外部搜索器。[Liu et al., 2023](https://arxiv.org/abs/2304.11477)
- ReWOO 把 reasoning/planning 与 observations 解耦，报告更低 token 消耗、HotpotQA 上的性能提升及 tool-failure robustness；它同时改变 prompt/context 结构与执行方式。[Xu et al., 2023](https://arxiv.org/abs/2305.18323)
- ADAPT 是最直接的 novelty collision：它比较 ReAct、static plan-and-execute、retry、Reflexion 与按需层级分解，在 ALFWorld、WebShop、TextCraft 上报告最高达 28.3、27、33 个百分点的 absolute gain，并分析 task complexity 与 executor capability；但主要结果是单次运行，且“comparable calls”不等于完全相同的实际 token/latency/cost。[Prasad et al., Findings of NAACL 2024](https://aclanthology.org/2024.findings-naacl.264/)

### 4.2 是否已被充分回答？— INTERPRETATION

没有。已有论文支持“某些 explicit/adaptive planning 设计在某些 benchmark 上有效”，但没有建立跨 task family、model capability、budget 与 uncertainty regime 的稳定边界。与此同时，当前 RQ 与 ADAPT 的问题设置非常接近，不能仅凭“测试 planning 何时有效”主张新颖。

### 4.3 表述问题— INTERPRETATION

- `task dependency depth`、`horizon` 与 `difficulty` 很可能共变，无法区分是哪一因素产生 interaction。
- `uncertainty` 同时可指 partial observability、stochastic transition、tool unreliability 或未知 constraint，过宽。
- `explicit planning` 可指 subtask list、formal planning、search 或 planner-executor separation，处理混杂。
- success、efficiency、latency、cost 全部并列会导致多重 primary outcomes；R4 需指定一个 primary outcome 与一个 resource-adjusted primary comparison。

### 4.4 R1 verdict— INTERPRETATION

**NARROW**。

### 4.5 建议改写— IDEA

> 在固定 task family、model、tool access、prompt information、termination 与预算协议下，显式 ex-ante subgoal plan 相对 ReAct baseline 的成功率与 resource-normalized efficiency，是否随预注册的 dependency depth 改变？该 interaction 在 fully observed、stationary 环境中是否可重复？

首轮只操纵 dependency depth；把 partial observability、tool failure 与 environmental change 留给合并后的 adaptive/replanning 子问题。

### 4.6 Novelty warning— INTERPRETATION

- “planning 帮助复杂任务”不是新 claim；ADAPT 已明确连接 task complexity、executor capability 与按需 planning。
- “我们的 planning 比 ReAct 高 X%”最多是 benchmark result，不自动是 research contribution。
- 可辩护 novelty 必须来自：更干净的 factor isolation、budget-response curve、负效应边界、跨模型复现，或能预测 treatment heterogeneity 的预注册变量。

## 5. RQ-002 — Dynamic replanning and recovery

### 5.1 学术界已经知道什么？— PAPER EVIDENCE

- ReAct 的原始定义已经允许 reasoning trace 更新 action plan 和处理 exceptions，所以“dynamic response to observations”并非 replanning 方法独有。[Yao et al., ICLR 2023](https://arxiv.org/abs/2210.03629)
- ADAPT 在 executor 检测失败后按需重新分解复杂 subtask，并优于 static plan-and-execute 与 retry baselines；这是 failure-triggered adaptive planning 的直接先例。[Prasad et al., Findings of NAACL 2024](https://aclanthology.org/2024.findings-naacl.264/)
- Tools Fail 区分显式报错与返回看似正常但错误的 silent tool failure，并在受控 calculator 和 embodied planning 环境中研究检测与恢复。[Sun et al., EMNLP 2024](https://aclanthology.org/2024.emnlp-main.790/)
- AdaPlanBench 专门测试 world/user constraints 渐进揭示时的 adaptive planning/replanning；307 个 household tasks、10 个模型中最好 accuracy 为 67.75%，且 constraint 累积时性能下降。[Liu et al., 2026 preprint](https://arxiv.org/abs/2606.05622)
- CostBench 已在 travel-planning domain 中加入 tool failure、cost change 等动态 blocking event，专门评价 cost-optimal planning 与 adaptation。[Liu et al., ACL 2026](https://aclanthology.org/2026.acl-long.584/)

### 5.2 是否已被充分回答？— INTERPRETATION

没有统一答案；failure observability、recoverability、timing、task domain 与 budget 会改变结论。但“在 tool failure / environmental change 下加 replanning 并看 recovery”已是明确的现有研究线，当前宽表述缺乏足够区别。

### 5.3 表述问题— INTERPRETATION

- 与 RQ-001 的 boundary question 是同一因果结构的动态环境分支。
- 将 tool failure、incomplete observation、environmental change 混为一个变量会掩盖 detection 难度和 ground-truth 差异。
- `replanning availability/trigger` 把两个不同 treatment 合并：能否 replan，以及何时触发。
- ReAct 若可自然调整，必须证明显式 plan revision 的增量效果，而不是比较“适应”与“不适应”。

### 5.4 R1 verdict— INTERPRETATION

**MERGE → RQ-001**，作为第二阶段 adaptive-planning 子问题，不作为独立核心 RQ。

### 5.5 建议合并后的子问题— IDEA

> 对已经生成 explicit plan 的任务，在预先声明为 recoverable 的扰动下，typed replanning 相对 budget-matched static plan、ReAct 与 retry control 是否提高 end-to-end recovery；该效应是否随 failure observability 与 failure timing 改变？

首轮只选一种可复现 perturbation family，并至少分开 explicit error 与 silent wrong-result；environmental state change 可留到后续 replication。

### 5.6 Novelty warning— INTERPRETATION

- “遇到失败后重新规划”不是 novel mechanism。
- 把 retry、argument repair 或普通 next-action reasoning 重命名为 replanning 会造成 nominal novelty。
- 若 replanning 得到额外 oracle failure label、更多环境信息或更多 calls，其恢复提升不能归因于 replanning 本身。

## 6. RQ-003 — Reflection policy

### 6.1 学术界已经知道什么？— PAPER EVIDENCE

- Reflexion 在 sequential decision-making、coding 与 reasoning 上报告显著提升，但其主要机制使用 evaluator feedback、跨 trial verbal reflection 和 episodic memory；这不是纯 same-episode reflection treatment。[Shinn et al., NeurIPS 2023](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
- 纯 intrinsic self-correction 在 reasoning 上经常不能改善，甚至会把正确答案改错。[Huang et al., 2023](https://arxiv.org/abs/2310.01798)
- TACL critical survey 指出：prompted LLM 在没有可靠外部反馈时通常没有被证明能成功 self-correct；可靠外部反馈或大规模 fine-tuning 改变结论，并且部分已有比较会因不公平设置高估 self-correction。[Kamoi et al., TACL 2024](https://aclanthology.org/2024.tacl-1.78/)
- BIG-Bench Mistake 研究把 mistake finding 与 correction 分开，发现模型难在定位错误，但给出 ground-truth error location 后更能修正。[Tyen et al., 2023](https://arxiv.org/abs/2311.08516)
- BenchTrace 将 detection、localization、diagnosis 分开测量；Qwen3-32B 与 GPT-4.1 的端到端 reflection pass rate 均低于 30%，diagnosis 是主要瓶颈，并观察到遗忘与跨 context negative transfer。[Huang et al., 2026 preprint](https://arxiv.org/abs/2605.29225)

### 6.2 是否已被充分回答？— INTERPRETATION

没有。是否反思有效高度依赖 feedback quality、错误是否可检测、是否允许 oracle signal、模型能力和评价预算。现有证据足以否定“reflection 一般有效”，但尚未回答在受控 tool-use traces 上，非 oracle selective trigger 能否以更低 false-intervention / cost 获得净收益。

### 6.3 表述问题— INTERPRETATION

- `selective` 没有说明选择器看到什么；若使用 ground-truth failure 或 task score，会产生 oracle leakage。
- `trace-grounded` 没有说明允许使用 observation、error code、verifier result 还是 gold diagnosis。
- `corrected-failure rate` 可能只统计成功触发的样本，忽略 missed detections。
- Reflexion 式跨 episode memory 与当前 M3 前 memory-out-of-scope 冲突。

### 6.4 R1 verdict— INTERPRETATION

**NARROW**。

### 6.5 建议改写— IDEA

> 在 same-episode tool-use 中，仅使用预先允许的 trace-observable signals、且不访问 gold outcome/failure labels 的 selective reflection，能否相对 no-reflection、always-reflect 和 budget-matched extra-attempt control 提高 end-to-end correction，并降低 repeated mistake；其净收益如何由 trigger、diagnosis 与 correction 三阶段的错误分解解释？

### 6.6 Novelty warning— INTERPRETATION

- “反思错误并重试”已有大量先例；“selective”或“trace-grounded”两个形容词本身不构成 novelty。
- 反思若读取 deterministic verifier / error message，claim 应是 external-feedback-assisted correction，不是 intrinsic self-reflection。
- 额外一次推理优于 no-reflection 可能只是 test-time compute effect；必须有 budget-matched extra-attempt 或 alternative-compute control。
- 一个更好的 trigger 可能来自更强 judge，而非 reflection policy；selector model capability 必须纳入控制。

## 7. RQ-004 — Explanatory failure model

### 7.1 学术界已经知道什么？— PAPER EVIDENCE

- AgentBench 在八种环境中评价 agents，并把常见失败关联到 long-term reasoning、decision-making 与 instruction-following 等能力缺口。[Liu et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html)
- AgentBoard 指出只看 final success 无法解释过程，提出 fine-grained progress rate 与多维分析工具。[Ma et al., NeurIPS 2024 Datasets & Benchmarks](https://proceedings.neurips.cc/paper_files/paper/2024/hash/877b40688e330a0e2a3fc24084208dfa-Abstract-Datasets_and_Benchmarks_Track.html)
- AgentDebug 提出覆盖 planning、action、reflection、memory 与 system operations 的模块化 taxonomy，并建立 ALFWorld、GAIA、WebShop 的 annotated failure trajectories；它还研究关键错误检测与 targeted feedback recovery。当前应按 preprint / workshop-level evidence 对待，不作为定论。[Zhu et al., arXiv 2025](https://arxiv.org/abs/2509.25370)
- Butterfly Effects in Toolchains 已针对 parameter filling 建立五类 failure taxonomy，并用 15 种 input perturbation 研究输入来源与 failure category 的关系。[Xiong et al., Findings of EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.907/)
- BenchTrace 用 step range 定位 failure instance，并把 detection、localization、diagnosis 拆开；其 FAR 的人工/LLM 验证只有 81.8% accuracy、Cohen's κ=0.538，说明连 failure-derived metric 本身也有显著标注不确定性。[Huang et al., 2026 preprint](https://arxiv.org/abs/2605.29225)

### 7.2 是否已被充分回答？— INTERPRETATION

generic failure taxonomy 与 trace-based diagnosis 已经是拥挤方向；创建另一套类别表没有明显新颖性。尚未被回答的是：在本项目的受控 interventions 下，预注册的 trace events 是否能稳定区分 strategy effect、model capability 与 task stratum，并对未见运行提供额外预测价值。

### 7.3 表述问题— INTERPRETATION

- `explain` 容易被误读为 causal explanation；观察到某 failure category 与最终失败相关，只是 association。
- `哪些失败可被检测和恢复` 同时包含 taxonomy、detector evaluation 与 intervention evaluation，范围过大。
- taxonomy 若在看过所有实验结果后迭代，容易 hindsight overfitting；若完全预定义，又可能 trace coverage 不足。
- model failure、policy/runtime failure、tool/environment failure 与 harness/engineering bug 必须分层，否则 category frequency 不可解释。

### 7.4 R1 verdict— INTERPRETATION

**MERGE → RQ-001 / RQ-003 analysis layer**。不在 M0 激活为独立 novelty RQ。

### 7.5 建议作为预注册分析问题— IDEA

> 哪些预注册的 trace-observable event 与 planning/replanning/reflection treatment effect 的异质性相关，并能在 held-out runs 上对 final failure 或 recovery 提供超过 task difficulty、model 与 aggregate progress 的增量预测？

建议使用两层标签：`locus`（model/policy、runtime、tool/environment、harness）→ `mechanism`（例如 wrong tool、invalid argument、missed contradiction、stale plan、loop、premature termination），保留 `unknown/ambiguous`，并区分 first error、proximate cause 与 terminal symptom。

### 7.6 Novelty warning— INTERPRETATION

- 新 taxonomy 不是自动贡献；必须证明 reviewer reliability、coverage、跨 task portability 或 predictive/detection value。
- post-hoc trace narrative 不能证明“为什么”策略有效；因果解释需要 intervention、mediation assumptions 或至少明确降级为 descriptive mechanism evidence。
- 若 RQ-004 继续独立存在，会很容易扩张为通用 observability/debugging 项目，偏离当前最小 single-agent runtime 主线。

## 8. 建议冻结后的 Research Identity 与 RQ set

### 8.1 Research Identity v1 候选— IDEA

> 在固定模型、工具、任务信息与推理预算协议下，本项目研究显式前瞻计划，以及由可观察失败触发的重规划或反思，如何随任务依赖结构与失败可观察性改变单代理工具任务的成功、恢复与效率。

### 8.2 候选 active RQs— IDEA

1. **RQ-A — Explicit planning boundary:** 显式 ex-ante subgoal plan 相对 ReAct 的效果是否随 dependency depth 改变；在 budget-response curve 上何时收益转负？
2. **RQ-B — Evidence-grounded correction policy:** 在非 oracle trace signals 下，selective same-episode reflection 何时相对 no/always/budget-matched extra attempt 产生正的 end-to-end correction 净收益？

Replanning 是 RQ-A 的动态扰动子问题；failure model 是 RQ-A/RQ-B 的共同解释与质量控制层。

**INTERPRETATION:** 该收缩保留了初始化文件的核心 thesis，同时把四个机制名词收束为两个可区分的 treatment family。是否采用仍由 R0 决定，并且必须等待 R4 的 measurability/validity 审查。

## 9. 当前允许与不允许的 claims

### 9.1 PAPER EVIDENCE — 可表述

- “既有研究在特定 benchmarks 上报告 explicit/adaptive planning 或 reflection 的收益。”
- “既有研究也报告 intrinsic self-correction 的失败、错误检测瓶颈、negative transfer 与动态 constraint 下的明显性能缺口。”
- “现有 planning 与 agent evaluation 文献的任务、表示和评价标准高度异质。”

### 9.2 INTERPRETATION — 必须带限定

- “现有证据尚未形成可跨 task/model/budget 泛化的 planning 或 reflection 价值边界。”
- “本项目最可能的差异化在严格受控的 interaction boundary 与负结果，而不是新增一个 agent 模块。”

### 9.3 HYPOTHESIS — 尚待项目实验

- 高 dependency depth 可能提高 explicit planning 的边际价值，但 partial observability 或 stale assumptions 可能使 static plan 有害。
- selective reflection 的主要瓶颈可能是 failure detection/diagnosis，而不是生成修复动作。
- 更强模型可能缩小某些 runtime strategy 的收益，也可能提高其利用高质量 plan/feedback 的能力。

### 9.4 当前禁止

- “Planning 在复杂任务上更好。”
- “Dynamic replanning 能提高 recovery。”
- “Selective reflection 比 always/no reflection 更可靠或更省成本。”
- “我们提出了新的 failure taxonomy / explanatory model。”
- 任何因果、跨模型、跨任务、普遍性或 novelty claim。

## 10. 第一批核心论文（最多 5 篇）

| 顺序 | Paper | Priority | Reading Mode | 为什么现在读 | 必须掌握 |
|---|---|---|---|---|---|
| 1 | [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) | MUST READ | **DEEP READ → RECONSTRUCT** | 定义公平 baseline；避免把 ReAct 错当“无 planning” | loop 语义、prompt/traces、benchmarks、ablations、何时 reason、已承认的 failure/limitations |
| 2 | [ADAPT: As-Needed Decomposition and Planning with Language Models](https://aclanthology.org/2024.findings-naacl.264/) | MUST READ | **DEEP READ** | 与 RQ-001/002 最接近的 novelty collision | planning 定义、failure trigger、planner/executor、baseline fairness、complexity stratification、single-run 限制 |
| 3 | [Reflexion: Language Agents with Verbal Reinforcement Learning](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html) | MUST READ | **DEEP READ → RECONSTRUCT** | 澄清 reflection 实际绑定了 evaluator、feedback、retry 与 memory | actor/evaluator/self-reflection、trigger、feedback source、跨 trial memory、ablations、failure cases |
| 4 | [When Can LLMs Actually Correct Their Own Mistakes?](https://aclanthology.org/2024.tacl-1.78/) | MUST READ | **DEEP READ** | 为 RQ-003 提供负证据与公平性 checklist | intrinsic vs external feedback、self-correction research questions、unfair comparisons、成功条件 |
| 5 | [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370) | MUST READ FOR COLLISION CHECK | **STANDARD READ；taxonomy/annotation/evaluation 章节定向 DEEP** | RQ-004 的直接 novelty collision | taxonomy construction、first/root error、annotation protocol、detection metrics、recovery intervention；同时牢记其 preprint/workshop-level status |

**INTERPRETATION — 阅读顺序理由:** 先把 baseline 读准，再读最接近的 planning collision；随后读 reflection 原始正结果和 critical survey 的负/方法学证据；最后才读 failure taxonomy，避免先发明类别、再把所有 traces 塞入类别。

**IDEA — 暂不列入首批但应作为第二批:** Tools Fail、AgentBoard、PlanGenLLMs、AdaPlanBench、BenchTrace。Plan-and-Solve、LLM+P、ReWOO 可作为 related-work references，不应直接当作本项目 tool-agent 因果结论。

## 11. R1 final recommendation to R0

**INTERPRETATION:** 不建议按原文 ACCEPT 任何一个 RQ。建议 R0：

1. `RQ-001 = NARROW`；
2. `RQ-002 = MERGE into narrowed RQ-001`；
3. `RQ-003 = NARROW`；
4. `RQ-004 = MERGE as analysis layer, not active standalone RQ`；
5. 只有在 R4 证明 manipulation、budget protocol、ground truth 与 repetition 可行后，激活两个核心 RQ；
6. 在 M0 决议中明确：项目不以“提出 planning/replanning/reflection/taxonomy”为 novelty，而以可复现的 boundary、negative result 与机制分解作为可能贡献；这仍是 HYPOTHESIS，不是 FINDING。

---

# ROLE UPDATE

**ROLE-LOG-ID:** ROLE-20260903-R1-001  
**Role:** R1 — Literature & Theory Scholar  
**Date:** 2026-09-03  
**Task:** M0 / P0-1 Literature & Novelty Review for RQ-001–RQ-004  
**Context:** RQ-001–RQ-004 均为 CANDIDATE；M0 被 R1/R4 reviews 阻塞；M0 前禁止架构冻结与实现。  
**What Was Done:** 审查四个 candidate RQs；核对 foundational、direct-collision、critical/negative、benchmark 与 failure-taxonomy literature；给出术语操作定义、RQ disposition、novelty warnings、allowed/prohibited claims 与首批五篇阅读顺序。  
**What Changed:** R1 建议从四个并列 candidate RQs 收缩为两个核心 RQs；RQ-002 并入 RQ-001 的动态扰动子问题；RQ-004 降为跨 RQ 的预注册解释层。该变化是 PROPOSED，尚非 DECISION。  
**Evidence:** ReAct (ICLR 2023)；Reflexion (NeurIPS 2023)；ADAPT (Findings NAACL 2024)；Kamoi et al. self-correction survey (TACL 2024)；Tools Fail (EMNLP 2024)；AgentBoard (NeurIPS 2024 D&B)；PlanGenLLMs (ACL 2025)；AgentDebug (2025 preprint / 2026 workshop-level)；AdaPlanBench 与 BenchTrace (2026 preprints)；CostBench (ACL 2026)。  
**Files Affected:** `PROJECT_DOCS/ROLE_DELIVERABLES/R1_M0_LITERATURE_NOVELTY_REVIEW.md`（新增 R1 handoff artifact，后由 R6 分类归档）；未修改 R6-owned Project Memory。  
**Research Questions Affected:** RQ-001 NARROW；RQ-002 MERGE→RQ-001；RQ-003 NARROW；RQ-004 MERGE→analysis layer。  
**Architecture Impact:** NONE AUTHORIZED；仅提出未来 treatment 必须可分离、trace-observable 的研究要求，不包含模块或接口设计。  
**Experiment Impact:** 为 R4 提供 factors/baselines/confounds 输入：ReAct 非 straw baseline；typed failures；detection 与 recovery 分母；budget-matched extra-attempt control；success-at-budget；same-episode reflection；taxonomy reliability。  
**New Risks:** ADAPT / adaptive-planning novelty collision；reflection 与 memory/feedback/test-time-compute 混杂；ReAct 与 replanning 不可区分；oracle trigger leakage；failure taxonomy hindsight overfitting；preprint evidence 可靠性低于正式同行评议论文。  
**Recommended Next Step:** R4 对两个收缩后 RQ 完成 measurability/validity review；随后 R0 记录 ACCEPT/MERGE/NARROW 决议、Research Identity v1 与 active RQ set；R6 将 paper evidence 与本 ROLE UPDATE 归档至 06_LITERATURE、03_RESEARCH_QUESTIONS、09_ROLE_LOG。  
**Need Handoff:** YES — R4（可测量性/validity/budget protocol）、R0（最终 freeze decision）、R6（归档）。
