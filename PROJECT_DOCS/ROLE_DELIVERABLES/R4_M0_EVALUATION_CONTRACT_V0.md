# R4 M0 / P0-1–P0-2 Evaluation Contract v0 草案

**Role:** R4 — Benchmark & Experiment Scientist  
**Date:** 2026-09-21  
**Status:** DRAFT / PROPOSED；供 R0 决议，不把任何候选 RQ 标记为 ACCEPTED。  
**Scope:** 仅研究设计审查；不创建 benchmark、不写 runner、不冻结架构、不产生实验结果。

## 0. 审查结论与边界

本审查以 `PROJECT_DOCS/GOVERNANCE/Project Instructions.md` 的 R4 职责、`PROJECT_MEMORY/03_RESEARCH_QUESTIONS.md` 的候选定义，以及 R1 的 M0 文献/新颖性审查为输入。当前没有 EXPERIMENT RESULT 或 FINDING。以下均为 **DECISION PROPOSAL / HYPOTHESIS / DESIGN ASSUMPTION**，须由 R0 接受后才可进入冻结 Research Contract。

建议把研究主线收缩为两个可执行 treatment family：

1. **显式前瞻计划边界：** fixed task family 中 explicit ex-ante subgoal plan 相对 ReAct 的增量效果；首轮只操纵 dependency depth。
2. **证据约束的动态纠错：** 在可复现、可恢复的扰动下，显式 plan revision 或 same-episode selective reflection 的增量效果；先分清 ordinary observation-driven adaptation、retry/repair 与 dynamic replanning/reflection。

ReAct 必须作为有 observation-driven adaptation、隐式 online/local planning 的真实 baseline。任何 “no planning baseline” 表述都不合格。

## 1. RQ-by-RQ measurability / validity verdict

| 候选 RQ | 可测量性 | 可证伪性 | 三个月可行性 | 主要 baseline | 变量/metrics 是否可闭合 | 最大风险 | R4 disposition proposal |
|---|---|---|---|---|---|---|---|
| **RQ-001 Planning value boundary** | **可，但须收窄。** 用任务依赖图深度、固定 horizon 与可自动验证的 end state 操作化；treatment 是 explicit ex-ante plan vs ReAct，而非 planning vs no planning。 | **可。** 预注册 interaction 和 budget-adjusted effect；若深度×strategy 无稳定 interaction，或收益只在不公平 prompt/预算下出现，则否证 boundary 假设。 | **可行，前提是首轮只做 fully observed、stationary、单一 tool family、2 个模型层级以内。** | ReAct；同一模型/tool/prompt；必要时 static plan-and-execute 与 execution-only control。 | 可闭合，但须指定一个主要成功结局和一个资源归一化比较。 | 任务“需要规划”的循环定义；planner 得到更多信息/调用；计划文本质量被误当最终效用；ReAct straw-man 化。 | **NARROW**（沿用 R1 建议，尚非 R0 决议）。 |
| **RQ-002 Dynamic replanning and recovery** | **单独不可接受；合并后可测量。** 需预注册一种 perturbation family、failure timing、observability、recoverability，并明确 revision 与 retry/repair 的操作定义。 | **可，作为 RQ-001 的第二阶段子问题。** 若 budget-matched 后 revision 无 recovery 增量，或与 ReAct/repair 无差异，则否证。 | **单独做宽范围不可行；合并后可行。** 只先做一种 typed tool failure 或可验证环境扰动。 | ReAct；static plan；retry/argument-repair control；dynamic plan revision。 | recovery denominator、failure injection 与额外推理预算必须固定。 | ReAct 的 observation adaptation 被误判为无 replanning；把 retry/repair/next-action reasoning 重命名为 replanning；oracle failure label 泄漏。 | **MERGE → RQ-001**，作为后续 adaptive-planning 子问题。 |
| **RQ-003 Reflection policy** | **可，但须收窄。** 定义 same-episode、trace-grounded、非 oracle 的 signal；分解 trigger、diagnosis、correction。跨 episode memory 不纳入首轮。 | **可。** selective 必须胜过 no-reflection、always-reflect 和 budget-matched extra-attempt，且净收益超过 false intervention 与资源成本；否则否证。 | **可行但资源紧张。** 首轮限于已存在的可审计 tool traces 与一种 verifier/error signal；不做通用 self-correction。 | no reflection；always reflection；budget-matched extra attempt；可选 retry/repair。 | 可闭合，前提是 corrected-failure 以所有 eligible failures 为分母，而非仅触发样本。 | trigger 使用 gold outcome/failure label；额外 call effect；反思读取了更强反馈；正确答案被改错；选择器与 actor 能力混杂。 | **NARROW**；作为独立 candidate 是否激活须由 R0 在成本审查后决定。 |
| **RQ-004 Explanatory failure model** | **作为独立 RQ 不宜测量。** 作为预注册 analysis layer 可测：两层标签、盲法双标注、unknown/ambiguous、held-out predictive value。 | **可作为分析层否证。** 若 reviewer agreement、coverage 或 held-out 增量预测未达阈值，放弃“解释模型”主张。 | **分析层可行；建立新通用 taxonomy 不可行。** | aggregate success/difficulty/model baseline；独立标签质量 control。 | 需要把 descriptive association 与 causal explanation 分开。 | hindsight taxonomy；first error / proximate cause / terminal symptom 混淆；工程、tool、environment、model failure 混层；标签本身不可靠。 | **MERGE → RQ-001 / RQ-003 analysis layer**，不作为独立 active novelty RQ。 |

以上 disposition 是 R4 建议，不改变 `03_RESEARCH_QUESTIONS.md` 中的 CANDIDATE 状态。

## 2. 推荐 task unit 与 difficulty strata

### 2.1 Task unit

最小 task unit 是一次独立、可重放的 **single-agent tool-use episode**，包含：固定任务实例、版本化初始 state、用户信息、tool registry/schema、model/prompt 配置、预算、随机 seed、完整 event trace、自动 verifier 输出。一个 episode 只能有一个主要 end-state 判定；重试是同一 episode 的策略行为，不得把成功重试另算一个样本。

任务必须有可执行 ground truth：唯一或等价的 end-state predicate；若存在多个合法解，验证器检查状态约束而不是字符串相等。每个 task 必须标记是否可恢复、扰动类型和预期 difficulty；不得用 agent 自己生成的 plan 作为 gold。

### 2.2 分层

建议先使用 L1–L4，冻结后再考虑 L5–L7：

- **L1 single-tool:** 一个 tool call，验证 argument 与 end state；作 sanity/control，不作为 planning 主要证据。
- **L2 sequential tools:** 固定顺序的 2–3 calls；测试基本 tool selection/argument，不声称需要显式 planning。
- **L3 dependency:** 2–5 个有明确前置依赖的 calls；以 dependency graph depth（如 1/2/3/4+）作为首轮主要难度 factor。
- **L4 planning:** 至少两条合法执行路径、非平凡子目标依赖，但 state fully observed、stationary；用于 RQ-001 的核心比较。
- **后续 L5 uncertainty / L6 tool failure / L7 dynamic environment:** 仅在 RQ-001 首轮 manipulation 和预算协议通过 pilot 后启用；RQ-002 先选一个 typed、可重放的 L6 扰动。

不建议在 M0 直接激活 L8 long horizon、开放世界或多工具异构 benchmark；它们会把 task difficulty、coverage、latency 与 architecture complexity 同时推高。

## 3. Baseline matrix

| Baseline / treatment | 作用 | 必须固定或报告 |
|---|---|---|
| **ReAct** | 主比较 baseline；允许 Thought/Action/Observation 闭环和 observation-driven adaptation/隐式局部 planning。 | 与 treatment 同 model、tool、prompt information、termination、budget；不得删掉其 observation 适应能力。 |
| **Explicit ex-ante plan + executor** | RQ-001 treatment；计划在执行前生成，计划不能读取未来 observation。 | plan schema、planner calls/tokens、是否允许 revise（首轮否）必须预注册。 |
| **Static plan-and-execute** | RQ-002 control；区分初始计划价值与 revision 价值。 | 同样初始信息与 plan budget；失败后只允许预注册 retry/repair。 |
| **Retry / argument-repair control** | RQ-002/RQ-003 control；隔离“再试一次/修参数”与重规划。 | retry 次数、触发 signal、每次 call budget、是否改变 plan 必须相同。 |
| **No reflection** | RQ-003 control；保持普通执行策略。 | 相同 initial prompt/tool/termination；不能因禁用 reflection 而偷减必需的 recovery call。 |
| **Always reflection** | RQ-003 control；检验 selective 的选择价值。 | 反思点、可见 trace、反思 token/call 上限固定。 |
| **Budget-matched extra attempt** | test-time compute control；隔离“多一次推理”效应。 | 总 calls/tokens/latency/cost envelope 与 reflection treatment 尽可能匹配。 |
| **Execution-only / minimal sanity control** | 可选，检查任务是否其实不需要 planning。 | 不用于把 ReAct 叫“无 planning”；只作为 diagnostic。 |

首轮至少需要 ReAct、explicit plan、static plan（若进入 RQ-002）、no/always/selective reflection（若进入 RQ-003）及对应 budget control；不应把所有 baseline 同时铺开。

## 4. Independent / dependent variables

### 4.1 Independent variables

核心 treatment：runtime strategy（ReAct；explicit ex-ante plan；static plan；typed dynamic revision；no/always/selective reflection）。

预注册 task factors：dependency depth、horizon、合法路径数、failure timing、failure observability（显式 error vs silent wrong-result，仅在 RQ-002 阶段）、recoverability。模型 capability 作为 block/随机效应或预注册 moderator，不应与 strategy 混淆。可选 second-stage factors：prompt version、tool family、seed；不得在结果后挑选。

### 4.2 Primary metrics

为避免多重 primary outcomes，建议每个核心 comparison 只指定：

- **RQ-001 primary outcome：episode-level end-state success**（二元，按预注册 verifier 判定）。主要检验是 strategy × dependency-depth interaction；同时报告 absolute success difference。
- **RQ-002 primary outcome：eligible-failure recovery success**（分母为所有预注入且 ground-truth 可恢复的 failure episodes；未触发、误诊、超预算均算失败）。
- **RQ-003 primary outcome：end-to-end correction success**（所有预注入/观测到的 eligible failure 为分母，成功恢复且最终 end state 正确才算成功）。
- **RQ-004 analysis-layer primary quality gate：盲法标签 agreement**（建议 Cohen's kappa 或 Krippendorff's alpha，报告类别不平衡影响）；它不是项目的 agent success primary outcome。

**统一 resource-adjusted primary comparison：** 每个 treatment 与其公平 baseline 计算 `success per budget unit` 作为预先指定的资源校正比较（预算单位至少记录 model calls、input/output tokens、wall-clock latency、估计 cost；主报告可用固定 hard cap 下 success 与 budget-response curve，避免任意单一折算）。不要把 success、latency、cost 全部同时称 primary。

### 4.3 Secondary metrics

Task partial credit / progress；tool selection accuracy；argument validity/accuracy；first-error rate、repeated-error rate；steps/tool calls；tokens；wall-clock latency；API cost；retry count；termination reason；failure locus；false intervention rate（reflection 介入后原本可保持正确却变错或无必要消耗）；missed detection；diagnosis accuracy；recovery time；budget exhaustion。所有失败样本保留，不能只分析成功运行。

## 5. Repetition and variance assumptions

- 不接受 single-run 结论。每个 cell 至少 5 个独立 seeds 作为 pilot 下限；正式主比较建议每 cell 至少 10 个 seeds，且每个 seed 运行完整 task set 或预注册的 paired task assignment。
- task instance 是独立重复单位；同一 task 在不同策略间采用 paired/block 设计，seed 与 task order 预注册。若 LLM API 非确定，记录 request seed（若支持）并把响应随机性视为方差来源。
- 主报告使用 per-task paired differences、bootstrap 95% CI 或合适的 mixed-effects/logistic model；按 task、model、stratum 报告均值/中位数、分布和方差。成功率不应只报均值，不得用一个 lucky run。
- pilot 只用于估计 variance、检查 verifier 和成本，不得用于事后改写 hypothesis 或挑选 task。正式 sample size 需根据 pilot effect/variance 与最低实际重要差异（MCID）预注册；在没有 pilot 方差前，不宣称具有统计 power。
- 若任务量小或结果高度离散，明确标记为 exploratory；不把“未显著”解释为等价，除非做了预注册等效性/非劣性界限。

## 6. Fairness controls

以下在 strategy comparison 中必须相同或显式计价：

1. **Prompt demonstrations / information:** 完全相同的 demos、任务说明、tool descriptions、error messages；plan treatment 的额外结构只能是 strategy 操作，不得偷加 gold decomposition。
2. **Tool access:** 相同 registry、schema、权限、初始 state、返回格式、可见 observation；不得让某 treatment 获得额外 verifier 或未来 state。
3. **Model capability:** 同一 model checkpoint/version、temperature/top-p、context limits；跨模型只作 block/moderator，不能把 stronger model gain 归因于 architecture。
4. **Inference budget:** 预注册 max calls、total input/output tokens、wall-clock deadline、retry count；planner/reflection/revision calls 计入总预算。报告 hard-cap success 与 budget-response curve。
5. **Tokens / latency / cost:** 全部逐 episode 记录；成本按实际 token price/version 计算并冻结价格表，延迟区分 model time、tool time、queue time；超时和预算耗尽是失败/右删失需预注册处理。
6. **Termination and stop rules:** 相同 end-state verifier、termination condition、max steps、invalid-action handling；不得为某策略放宽停止条件。
7. **Task allocation / order:** paired tasks、固定 task version、随机化执行顺序、隔离 rate limit/cache effects；失败 runs 不丢弃。
8. **Trace visibility:** ReAct 的 observation adaptation、reflection 的 signal、replanner 的 failure input 必须逐字段记录；gold outcome、hidden labels、未来 observation 不得进入 treatment prompt。
9. **Implementation parity:** 在 M0 不实现；冻结后需要先做 protocol-level equivalence review，确认差异来自 strategy 而非 parser、serialization、tool wrapper 或 harness bug。

## 7. Confounds, leakage, ambiguity, validity threats

### Confounds

- planner prompt 长度、计划生成 token 与 executor token 把 strategy effect 和 compute effect 混在一起；
- ReAct、retry、repair、dynamic revision 的行为边界未定义；
- model capability × strategy interaction 被误读为普遍 architecture effect；
- task family、tool schema、dependency depth 与 horizon 共线；
- tool latency、rate limits、cache、parallelism 造成伪 cost/latency effect；
- verifier 难度、answer format、termination policy 偏向某策略；
- reflection trigger、diagnosis、correction 三阶段被压成单一 treatment；
- failure injection 改变了任务难度或信息量，而非只改变 recoverability。

### Leakage

- 使用 gold failure label、gold error location、最终 success 或隐藏 environment state 触发 selective reflection/replanning；
- explicit plan 读取未来 observations、完整 solution 或 benchmark metadata；
- task IDs、tool names、error strings 暗示 strata 或正确路径；
- demos 只展示某一种策略可用的 decomposition；
- 失败注入器暴露“这是实验扰动”的额外 signal；
- 用结果后人工筛选 “可恢复” episodes；
- RQ-004 标签者看到 strategy、model 或 outcome 后产生确认偏差。

### Ambiguity / validity threats

- “planning”未写明 ex-ante、scope、允许 revise 与预算；
- “replanning”未写明 plan representation 是否真正改变、何时触发、是否仅 retry/repair；
- “reflection”未写明 signal vocabulary、可见 trace、是否允许 verifier；
- partial success 与 end-state success 不一致；
- taxonomy 的 first error、proximate cause、terminal symptom 混淆；
- descriptive association 被写成 causal explanation；
- 任务覆盖不足导致外部有效性弱；
- 非确定 API、模型升级、价格变化破坏复现；
- benchmark 过度适配某一 prompt/model，损害跨模型有效性。

## 8. Leakage / ambiguity preflight checks

在任何正式 benchmark 或 runner 之前，R4 要求通过以下纸面检查：

1. 对每个 treatment 写出一页信息流图：每个输入字段标记为 public / trace-observable / hidden / gold；gold 只可进入 verifier，不能进入 policy。
2. 对同一 failure case，人工列出 ReAct next-action、retry/repair、dynamic revision、reflection 的最小行为差异；若两个 treatment 可产生相同 trace，不能声称机制已分离。
3. 由不参与设计的 reviewer 盲审任务：是否唯一/等价答案、是否真的需要 agent、是否能自动判定、是否泄漏 difficulty/strategy。
4. 使用 synthetic sanity tasks：L1 应不显示 planning advantage；已知不可恢复 failure 不进入 recovery denominator；无扰动 control 不得被当作 recovery success。
5. 预注册 excluded/ambiguous handling：verifier 不确定、环境污染、tool outage、schema bug、模型服务异常必须标记并报告，不能事后删样本。
6. 先做 protocol-only pilot 和 cost audit；pilot 只验证可执行性，不产正式 finding。

## 9. Falsification conditions

以下是可执行的预注册否证条件；满足任一项，需承认相应 hypothesis 未获支持，并把结果记录为 negative/null result：

- **RQ-001：** 在预注册 dependency-depth strata 和 budget cap 下，explicit plan 相对 ReAct 的 end-state success interaction CI 覆盖 0 且 effect 未达到 MCID；或任何名义收益在 token/latency/cost 对齐后消失；或收益仅在额外信息/不等 prompt 下出现。
- **RQ-002（合并子问题）：** 在 typed、可恢复扰动中，dynamic revision 相对 static + retry/repair + ReAct 的 recovery difference 未达 MCID，或 control for extra calls 后消失；若 revision 只修复了可由普通 observation-driven adaptation 完成的 case，也不支持“显式 replanning 增量”。
- **RQ-003：** selective reflection 不超过 no-reflection 与 always-reflect 的预注册非劣/优效界限；或 success 增益小于 false intervention、额外 tokens/latency/cost 的 MCID；或 signal 需要 gold label/oracle。
- **RQ-004 analysis layer：** 双标注 agreement 低于预注册最低阈值（建议先以 κ/α < 0.6 作为需修订信号，不是最终科学阈值）、unknown/ambiguous 比例过高、held-out prediction 不超过 difficulty + model + aggregate progress 的增量基线，或标签只能在看到结果后稳定构造。
- **全局：** control protocol 无法保证同等 prompt/tool/model/budget/termination；自动 verifier 与人工审计不一致；失败运行被系统性丢弃；成本/延迟记录不完整。此时实验不得升级为正式 claim。

MCID、等效性界限、最小 agreement 阈值必须在 R0 冻结前由 pilot/统计审查确定；本草案中的数值是起始建议，不是结果。

## 10. Rough cost envelope（设计期估算）

这是资源规划，不是实际支出；价格、模型和 API 版本未冻结，因此不能当作 EXPERIMENT RESULT。

| 阶段 | 规模假设 | 粗略调用量 | 粗略资源/成本 |
|---|---|---:|---|
| Protocol-only / verifier pilot | 30–60 tasks，2 strategies，2 models，3 seeds；不做大规模 benchmark | 约 360–720 episodes；每 episode 5–12 model calls | 约 2k–8k model calls；若平均 3k–8k tokens/episode，约 1–6M tokens；API 成本约 **US$20–200**，取决于 model mix |
| RQ-001 first formal cell | 80–120 tasks，2 strategies，2 model tiers，10 seeds，4 depth strata（paired） | 约 3,200–4,800 episodes；每 episode 4–10 calls | 约 15k–50k calls；约 15–80M tokens；API 成本约 **US$200–1,500**，另加运行/存储成本 |
| RQ-002 second-stage perturbation | 40–80 base tasks，4 strategies/controls，2 model tiers，5–10 seeds | 约 1,600–6,400 episodes | 约 10k–60k calls；约 10–100M tokens；约 **US$150–2,000** |
| RQ-003 narrowly scoped reflection | 40–80 failure tasks，4 policies，2 model tiers，5–10 seeds | 约 1,600–6,400 episodes | 约 10k–70k calls；约 10–120M tokens；约 **US$200–2,500** |
| RQ-004 annotation / audit | 正式 traces 的 10–20% 双标注，另加 held-out scoring | 不以 model calls 为主 | 人工/审核时间约 20–60 小时；若使用 judge，需另计且不能替代人工 agreement audit |

三个月内建议只承诺：protocol pilot → RQ-001 主比较 → 视成本与 validity gate 再选择 RQ-002 或 RQ-003 之一。若必须覆盖两者，应减少 model tiers/task breadth，而不是降低 repetition 或 budget accounting。成本上限的任何升级需由 R0 重新排序 P0/P1。

## 11. Recommended disposition and activation gates

### RQ-001 — **NARROW**

建议改写为：在固定 task family、model、tool access、prompt information、termination 与推理预算协议下，explicit ex-ante subgoal plan 相对 ReAct 的 end-state success 与 resource-normalized efficiency 是否随预注册 dependency depth 改变；该 interaction 在 fully observed、stationary 环境中是否可重复？

激活 gate：任务依赖深度可由独立标注/图结构重建；ReAct prompt 与 tool access 等价；plan tokens/calls 计入总预算；success verifier 通过 sanity audit；paired repeated protocol 可行。

### RQ-002 — **MERGE → RQ-001**

建议改写为 RQ-001 的第二阶段：对已生成 explicit plan 的任务，在预声明、可恢复的 typed perturbation 下，dynamic plan revision 相对 budget-matched static plan、ReAct 与 retry/repair control 是否提高 end-to-end recovery；效应是否随 failure observability/timing 改变？

激活 gate：只选一种扰动 family；failure injection 可重放；recoverability 有外部 ground truth；revision 改变 plan state 而非只改 argument/重试；extra inference budget 可公平计价。

### RQ-003 — **NARROW**

建议改写为：在 same-episode tool-use 中，仅使用预先允许且 trace-observable、不得访问 gold outcome/failure label 的 selective reflection，相对 no-reflection、always-reflect 与 budget-matched extra attempt，是否提高 end-to-end correction 并降低 repeated mistake；trigger、diagnosis、correction 的错误如何分解？

激活 gate：signal schema 冻结；cross-episode memory 排除；所有 eligible failures 纳入分母；false intervention 定义可自动/盲审；reflection 与 extra-attempt 的 calls/tokens/cost 可对齐。

### RQ-004 — **MERGE → analysis layer**

仅保留预注册标签与质量控制：`locus`（model/policy、runtime、tool/environment、harness）→ `mechanism`（wrong tool、invalid argument、missed contradiction、stale plan、loop、premature termination 等），允许 unknown/ambiguous，并区分 first error、proximate cause、terminal symptom。只有通过 agreement、coverage 和 held-out增量预测 gate，才可报告 descriptive/predictive analysis；不得称为独立新 taxonomy 或 causal explanation。

## 12. P0-1 / P0-2 状态建议

- **P0-1 Research Contract Review：PARTIAL / R4 REVIEW COMPLETE（PROPOSED）**。R1 已完成文献/新颖性审查；R4 已完成可测量性、可证伪性、三个月资源可行性与公平性审查；最终是否接受、合并、拒绝仍由 R0 冻结。
- **P0-2 Evaluation Contract v0：DRAFT COMPLETE / PENDING R0 FREEZE**。本文件提供 task unit、strata、baseline、变量、metrics、repetition、controls、risks、falsification 与 cost envelope；在 R0 未确定 active RQs、MCID、等效性界限和最终预算前，不得作为正式实验授权。

# ROLE UPDATE

**ROLE-LOG-ID:** ROLE-20260921-R4-001  
**Role:** R4 — Benchmark & Experiment Scientist  
**Date:** 2026-09-21  
**Task:** M0 / P0-1 Research Contract measurability-validity review；P0-2 Evaluation Contract v0 草案  
**Context:** Phase 0 — Project Initialization；Milestone M0 — Research Charter Freeze；RQ-001–RQ-004 均为 CANDIDATE；当前无实验结果或正式 Finding；M0 前禁止代码、架构冻结和大规模 benchmark 生成。  
**What Was Done:** 逐一审查 RQ-001–RQ-004 的可测量性、可证伪性、三个月可行性、baseline、控制变量、primary/secondary metrics、重复与方差假设、confounds、leakage、ambiguity、validity risks 和 disposition；提出 task unit、difficulty strata、baseline matrix、公平性协议、否证条件与资源包络。  
**What Changed:** R4 建议 RQ-001 = NARROW；RQ-002 = MERGE → RQ-001 dynamic perturbation subproblem；RQ-003 = NARROW；RQ-004 = MERGE → RQ-001/RQ-003 analysis layer。新增的 Evaluation Contract v0 仍是 PROPOSED，不改变 shared memory 中候选状态，也不构成 R0 freeze。  
**Evidence:** `PROJECT_DOCS/GOVERNANCE/Project Instructions.md`（R4职责、R4实验协议、统计与 handoff）；`PROJECT_MEMORY/03_RESEARCH_QUESTIONS.md`（candidate definitions 与 ReAct implication）；`PROJECT_MEMORY/06_LITERATURE.md`；`PROJECT_DOCS/ROLE_DELIVERABLES/R1_M0_LITERATURE_NOVELTY_REVIEW.md`（R1 collision、ReAct、ADAPT、reflection 与 taxonomy validity evidence）。  
**Files Affected:** `PROJECT_DOCS/ROLE_DELIVERABLES/R4_M0_EVALUATION_CONTRACT_V0.md`（新增本草案）；未修改 R0/R6-owned project memory、RQ registry 或实验代码。  
**Research Questions Affected:** RQ-001 NARROW proposal；RQ-002 MERGE proposal；RQ-003 NARROW proposal；RQ-004 MERGE-as-analysis proposal；四者仍为 CANDIDATE，等待 R0 决议。  
**Architecture Impact:** NONE AUTHORIZED；仅提出实验所需的 trace、budget、verifier 和 strategy separation requirements；不冻结接口或实现。  
**Experiment Impact:** 允许在 R0 冻结后先做 protocol-only/verifier pilot，再决定 RQ-001 formal comparison；要求 ReAct 保留 observation-driven adaptation；要求控制 demos、tool access、model capability、calls/tokens/latency/cost、termination 与 failure denominator；禁止在 M0 前写 runner 或生成大 benchmark。  
**New Risks:** 若 R0 同时激活 RQ-001/002/003，三个月预算和重复数可能不足；dynamic replanning 与 retry/repair/普通 ReAct adaptation 仍可能不可分离；reflection 的 signal 可能携带 oracle；task dependency depth 可能与 horizon/tool coverage 共线；verifier、成本记录和 API 非确定性可能成为主要 validity bottleneck；RQ-004 标签 agreement 或 held-out 增量预测可能失败。  
**Recommended Next Step:** R0 审查本草案并记录最终 ACCEPT / MERGE / NARROW / REJECT 决议、Research Identity v1、active RQ set、MCID/等效性界限和三个月预算；随后 R6 归档本 ROLE UPDATE 并登记 P0-1/P0-2 状态。若 R0 接受 RQ-001，下一步应是 protocol-only pilot design review，而非实现 benchmark runner。  
**Need Handoff:** YES — To R0 for final Research Contract freeze and budget prioritization; To R6 for shared-memory registration/role log; conditional To R3/R2 only after R0 freeze and only for protocol/trace implementation planning; To R5 if failure label/recovery taxonomy review is activated.
