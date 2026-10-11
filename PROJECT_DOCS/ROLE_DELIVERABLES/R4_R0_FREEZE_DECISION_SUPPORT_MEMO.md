# R0 Freeze Decision Support Memo

**Role:** R4 — Benchmark & Experiment Scientist  
**Date:** 2026-09-21  
**Status:** R4 recommendation；不构成 R0 freeze、实现授权或 benchmark 生成授权。

## 结论先行

R4 建议 R0 在三个月核心路线中只冻结 **RQ-001（收窄版）**；RQ-003 保留为候选的条件性第二阶段，而不是与 RQ-001 同时承诺为同等核心主线。RQ-002 作为 RQ-001 的动态扰动子问题，只有在 RQ-001 的协议、verifier、预算记录和 baseline validity 通过后才进入。RQ-004 只能作为跨 RQ 的预注册 analysis layer。

## 1. R0 最终需要冻结哪些 active RQs？

**R4 recommendation**

- **Active core:** RQ-001 Narrowed — fully observed、stationary、固定 task family/model/tool access/prompt/termination/budget 下，explicit ex-ante subgoal plan 相对 ReAct 的 end-state success 是否随 dependency depth 改变，并报告 resource-normalized comparison。
- **Merged subproblem:** RQ-002 不单独 active；登记为 RQ-001 的 conditional dynamic perturbation/recovery subproblem。
- **Conditional candidate:** RQ-003 Narrowed — same-episode、trace-grounded、非 oracle selective reflection；是否进入三个月正式路线由预算与 RQ-001 validity gate 决定。
- **Analysis layer:** RQ-004 不作为 active novelty RQ；只作为 RQ-001/003 的预注册 failure labeling、quality control 和 held-out analysis。

**R0 decision still required**

R0 必须明确 active set、Research Identity v1、每个 ID 的 ACCEPT/MERGE/NARROW/REJECT、允许 claims，以及对应 Decision ID。R6 在 R0 决策前不得把上述 proposal 改写成 accepted/active。

## 2. RQ-001 与 RQ-003 是否同时进入核心三个月路线？

**R4 recommendation：先只保留 RQ-001 为核心。**

理由是 RQ-001 已能形成一个闭合、可验证的首轮因果比较；RQ-003 还额外需要 failure signal schema、trigger/diagnosis/correction 分离、false intervention 分母、budget-matched extra-attempt control 与 reflection-specific verifier。两者同时作为同等主线会降低重复数、增加预算混杂，并使 M1 baseline validity 难以判断。

RQ-003 可记录为 **conditional P1 / second-stage candidate**：只有 RQ-001 pilot 通过 protocol validity、成本在预算内、且 reflection signal 不含 oracle，R0 才可将其加入三个月后半程。若 R0 出于项目目标坚持同时激活，必须明确降低 task/model breadth，而不得降低重复数、失败样本保留或 inference-budget accounting。

## 3. RQ-002 最小进入条件

**R4 recommendation：作为 RQ-001 的 gated subproblem，不在 M0 独立进入。**

最低条件为全部满足：

1. RQ-001 的 ReAct 与 explicit-plan protocol 已通过 paired task、自动 verifier、trace completeness 和 budget audit。
2. 只选择一种 typed、可重放、外部 ground truth 明确的 perturbation family；首选显式 tool error 或可验证的 stale-plan 事件，不同时混合 silent failure 与环境变化。
3. 明确 failure timing、observability、recoverability 与 recovery denominator；不可恢复样本不计入 recovery 分母。
4. dynamic revision 必须改变显式 plan state/subgoals；只重试、修 argument 或基于 observation 选择下一步不算 replanning treatment。
5. 必须同时保留 ReAct、static plan、retry/argument-repair control，并将 revision calls/tokens/latency/cost 计入同一总预算。
6. protocol-only pilot 证明 failure injection 不额外泄漏“这是扰动”的 gold signal，且 revision 与普通 ReAct adaptation 可区分。

**R0 decision still required：** 是否在三个月内为该 gated subproblem 分配独立预算和 milestone；否则只登记为后续 P1。

## 4. RQ-004 analysis layer 最低质量门槛

**R4 recommendation**

RQ-004 只有同时满足以下条件，才允许报告 descriptive/predictive analysis：

- 预注册两层标签：`locus` 与 `mechanism`；区分 first error、proximate cause、terminal symptom，并保留 `unknown/ambiguous`。
- 工程/harness、runtime/policy、tool/environment、model failure 分层；标签者不能依赖隐藏 gold outcome。
- 至少一部分正式 traces 进行盲法双标注；agreement 指标（Cohen κ 或 Krippendorff α）达到 R0 预设最低门槛。R4 起始建议 κ/α ≥ 0.60 作为需继续使用的质量门槛，最终数值由 R0 冻结。
- 报告 coverage、unknown/ambiguous 比例和标签变更记录；不得结果后重写 taxonomy。
- 在 held-out runs 上，相对 task difficulty + model + aggregate progress 的 baseline，failure labels 对 failure/recovery 有预注册的增量预测价值。
- 结论降级为 association/prediction；不得写成 causal explanation 或“新 failure taxonomy”，除非另有 R0 批准的证据。

## 5. R0 必须明确的 MCID、等效性界限、预算和 inference-budget controls

**R0 decision still required；以下为 R4 起始建议。**

- **MCID：** RQ-001 success rate 的最小实际重要差异；RQ-002 recovery success 与 RQ-003 correction success 各自独立设定；不能用“统计显著”替代 MCID。应在 pilot 前固定为百分点或风险差，并说明 resource-adjusted interpretation。
- **等效性/非劣界限：** 对“无 interaction”“reflection 不优于 control”或 budget-matched null 结论，预设 success-rate margin；未通过等效性设计时只能说未观察到足够证据，不能说相同。
- **预算上限：** 每 episode 的 max model calls、total input/output tokens、wall-clock deadline、retry/revision/reflection calls、tool calls；超预算/超时的处理规则必须冻结。
- **成本记录：** model version、token price/version、input/output tokens、model/tool/queue latency、估计 cost；价格变化需版本化。
- **策略公平：** 相同 demos、prompt information、tool registry/schema、初始 state、observation、termination/verifier、model sampling 参数；planner/reflection/revision 的额外调用全部计入总预算。
- **统计承诺：** pilot 每 cell 至少 5 seeds 仅用于 verifier/variance/cost；正式主比较建议每 cell 至少 10 seeds、paired tasks、95% CI，并预注册 mixed-effects 或 paired bootstrap 分析。R0 必须决定正式 task 数与最低可接受 power/precision 目标。
- **主结局：** RQ-001 用 episode end-state success；resource-adjusted comparison 使用固定 hard cap 下 success 与 budget-response curve，不把 success、latency、cost 同时称 primary。

## 6. M1 单一目标

**R4 recommendation：**

> 在冻结的 RQ-001 协议下，完成一个本地、可重放、自动 verifier 可审计的最小测量闭环，并证明 ReAct 与 explicit ex-ante planning 的 baseline 行为、trace、termination、budget accounting 与 success 判定在一个小型、分层的 pilot task set 上没有已知 ambiguity、leakage 或策略不公平；M1 只产出 measurement-validity evidence，不产出 planning effect claim。

M1 不应同时承诺 RQ-002、RQ-003、MCP、rollback、memory 或大规模 benchmark 泛化。

## 7. 哪些条件会阻止 M0 通过？

以下任一项未解决，R4 建议保持 M0 **BLOCKED / NO-CODE**：

- active RQ 仍无法写成 measurable、falsifiable 的单一主比较；
- R0 未决定 RQ-001/RQ-003 的优先级与 RQ-002 的 gated status；
- ReAct 被错误写成无 planning，或 treatment 边界无法区分 observation adaptation、retry/repair 与 dynamic revision；
- 没有明确 end-state verifier、recovery/correction 分母或 ambiguity handling；
- MCID、等效性/非劣界限、正式预算和 max inference budget 未冻结；
- prompt demonstrations、tool access、model capability、tokens、latency、cost、termination 中任一关键公平控制缺失；
- 没有可执行 falsification condition；
- RQ-004 被要求作为独立 taxonomy/causal RQ，却没有 annotation reliability 和 held-out validation；
- R0 将 M1 表述为“实现 runtime”或“证明 planning 有效”，而不是 measurement-validity gate；
- 任何实现、架构冻结、大规模任务生成在 freeze 前提前启动。

## 8. RQ-001 接受后的最小 protocol-only / verifier pilot

**Proposed pilot design；尚未授权执行。**

- **任务：** 约 12–24 个小型、可重放任务；覆盖 L1 sanity、L2 sequential、L3 dependency、L4 planning，每层少量实例；不生成大规模 benchmark。
- **策略：** ReAct 与 explicit ex-ante plan 两个 protocol variants；同一 model、tool registry、prompt information、termination 和 hard budget。ReAct 保留 observation-driven adaptation。
- **重复：** 每个策略/任务运行 3–5 seeds，仅用于协议验证、verifier 一致性、trace 完整性、成本/延迟方差估计；不作正式效果结论。
- **验证：** 独立 verifier 判定 end state；人工抽查每层若干 traces；检查 invalid action、timeout、budget exhaustion、tool error、termination reason 是否可审计。
- **公平性 audit：** 对每个 episode 核对 demos、tool access、model config、calls、tokens、latency、cost；确认 plan generation 计入总预算，且没有 future observation/gold decomposition 泄漏。
- **预期输出：** protocol pass/fail、verifier agreement、missing-trace rate、ambiguous-task list、预算分布、初步 variance estimate、是否具备正式 RQ-001 试验条件。
- **禁止输出：** planning superiority claim、正式 Finding、generalization claim 或 architecture freeze。

## 9. 当前权限状态

**Not yet authorized work：** 在 R0 完成 Research Contract freeze 之前，不启动 pilot、不写实现、不生成任务集、不冻结架构。当前只允许 R0 审阅本 memo，并由 R6 登记最终决议。

# ROLE UPDATE

**ROLE-LOG-ID:** ROLE-20260921-R4-002  
**Role:** R4 — Benchmark & Experiment Scientist  
**Date:** 2026-09-21  
**Task:** R0 Freeze Support Mode；将 R4 Evaluation Contract v0 转换为冻结决策支持 memo  
**Context:** Phase 0 — Project Initialization；M0 — Research Charter Freeze；P0-1/P0-2 review 已完成；RQ-001–RQ-004 仍为候选，R0 尚未完成 Research Contract freeze。  
**What Was Done:** 基于 Project State、Master Checklist、Research Question Index、R0 feasibility review 与 R4 Evaluation Contract v0，给出 active RQ 建议、RQ-001/RQ-003 路线优先级、RQ-002 最小进入条件、RQ-004 analysis-layer quality gate、MCID/等效性/预算控制清单、M1 单一目标、M0 阻断条件与 RQ-001 protocol-only/verifier pilot 草案。  
**What Changed:** R4 明确建议三个月核心路线先只冻结 RQ-001；RQ-003 降为 conditional P1；RQ-002 仅作为 gated subproblem；RQ-004 仅作为质量受控的 analysis layer。未改变 shared memory 中 RQ 状态，未产生实现授权。  
**Evidence:** `PROJECT_MEMORY/01_PROJECT_STATE.md`；`PROJECT_MEMORY/02_MASTER_CHECKLIST.md`；`PROJECT_MEMORY/03_RESEARCH_QUESTIONS.md`；`PROJECT_DOCS/ROLE_DELIVERABLES/R0_20260921_REFACTOR_FEASIBILITY_REVIEW.md`；`PROJECT_DOCS/ROLE_DELIVERABLES/R4_M0_EVALUATION_CONTRACT_V0.md`。  
**Files Affected:** `PROJECT_DOCS/ROLE_DELIVERABLES/R4_R0_FREEZE_DECISION_SUPPORT_MEMO.md`（新增）；未修改 shared project memory、RQ registry、architecture files 或实验代码。  
**Research Questions Affected:** RQ-001 active-core recommendation；RQ-002 merged/gated-subproblem recommendation；RQ-003 conditional recommendation；RQ-004 analysis-layer recommendation；最终状态仍待 R0 决定。  
**Architecture Impact:** NONE AUTHORIZED；仅定义 M1 measurement-validity target 与未来 pilot 的协议要求。  
**Experiment Impact:** 若 R0 接受 RQ-001，未来可进入最小 protocol-only/verifier pilot design review；当前未授权执行 pilot 或任何实现。  
**New Risks:** 只激活 RQ-001 可能延后 reflection evidence；若 R0 同时激活 RQ-003，三个月预算、重复数和 treatment separation 可能不足；MCID/等效性界限不恰当会导致 null/negative interpretation 错误；pilot 任务过小可能漏掉策略性 ambiguity。  
**Recommended Next Step:** R0 冻结 active RQ、Research Identity、MCID、等效性/非劣界限、预算、inference-budget controls 与 M1 单一目标；R6 登记决议后，再进行 protocol-only pilot design review。  
**Need Handoff:** YES — To R0 for final Research Contract freeze; To R6 for registration after R0 decision. No handoff to R2/R3 for implementation before freeze.
