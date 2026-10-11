# R0 Feasibility Review — Agent Runtime 优化与重构总纲

**Role:** R0 — Project Director / Principal Investigator  
**Date:** 2026-09-21  
**Input:** `Agent_Runtime_R0_优化重构总纲.md`（外部参考材料，版本 1.0）  
**Review status:** R0 feasibility assessment; not an implementation authorization

## 1. Executive verdict

**结论：设计层面可行；整体方案当前不可直接执行；建议 `TEST FIRST`，不是整体 `PURSUE`。**

这份总纲的核心方向与项目主线相容，尤其是：

- 把 Runtime、Policy、Tool Pipeline、Environment、Evaluator 和 Trace 分离；
- 把成功率、成本、延迟、预算和 failure analysis 放在同一评价协议内；
- 强调 fair baseline、inference-budget control、独立 verifier 和可复现 trace；
- 把 rollback、reflection、retry、replan 分成不同 intervention。

但它目前同时包含：

1. 研究问题重写；
2. 全新 runtime 实现；
3. benchmark/evaluation framework；
4. rollback-capable environment；
5. dynamic robustness suite；
6. MCP/Paper2Agent provider ecosystem；
7. resource/concurrency profiling；
8. memory/reflection system。

把这些当成一个单一“重构”会超过当前项目的 Scope、M0 状态和 3 个月资源边界。当前仓库也没有可供重构的 runtime source、tests 或 dependency manifest；实际情况是 **文档初始化项目，而不是已有代码库的重构项目**。因此，附件应改名理解为：

> 候选 Runtime 研究架构与分阶段迁移提案。

## 2. Evidence boundary

### FACT

- 当前仓库可见内容主要是 Project Memory、Project Docs 和论文材料；没有 `src/`、测试套件、依赖锁定或实验结果可作为现状证据。
- 项目仍处于 Phase 0 / M0，M0 未通过前禁止 architecture freeze 和 implementation。
- R1 已完成 M0 literature/novelty review，并建议将原四个候选 RQ 收缩为两个核心 treatment families：explicit planning boundary 与 evidence-grounded correction policy；RQ-002 并入前者，RQ-004 降为分析层。
- R4 的 measurability/validity review 尚未登记；R0 尚未作最终 RQ freeze 决议。

### PROPOSAL / IDEA

附件中的接口、模块、failure taxonomy、指标、里程碑、MCP 集成和 rollback 流程均是设计建议，不是当前系统已有能力，也不是外部论文的复现规范。

### UNKNOWN

- 可用模型、调用方式、成本上限、目标交付期限；
- 将要采用的语言、依赖、任务集和本地可快照环境；
- 任何模块的运行性能、可复现性或实验收益。

## 3. Feasibility by dimension

| 维度 | 判断 | R0 结论 |
|---|---|---|
| 研究方向一致性 | 中高 | 核心思想服务当前 runtime-strategy 研究，但附件的五个 RQ 比 R1 收缩建议更宽 |
| 最小闭环工程可行性 | 高（M0 后） | RunState、budget、validator、executor、trace、verifier 可作为第一阶段最小闭环 |
| 3 个月完整落地 | 低 | 若同时做 rollback、动态环境、MCP、资源评测和 memory，极易失控 |
| 6 个月分阶段落地 | 中高 | 只有按优先级拆轨道，并允许 M4/M5 负结果或不做扩展 |
| 研究可测量性 | 中高 | 附件指标与控制意识较好，但仍需 R4 固定分母、预算、任务族和重复方案 |
| 新颖性 | 当前中低；收窄后中高 | 模块数量不是 novelty；可辩护差异应来自 boundary、budget curve、negative result 和机制分解 |
| 可复现性 | 中高 | trace、版本、seed、config、verifier 设计正确；但目前没有实际环境验证 |
| 用户学习价值 | 中高 | 结构利于教学；全量一次性实现会削弱用户理解与掌控 |

## 4. What should be accepted in principle

### A. Core runtime/evaluation spine — candidate M1 scope

以下部分最适合作为 M0 通过后的最小实现方向：

- `RunState / BudgetManager`：显式状态、累计预算、终止原因；
- `ToolRegistry / Validator`：稳定 ID、schema 校验、结构化拒绝；
- `Executor`：timeout、错误封装、调用审计；
- `TraceRecorder`：run/step/call 事件与版本信息；
- 独立 `Verifier` 与最小 `Evaluation Runner`；
- ReAct 与 explicit ex-ante planning 的可切换策略接口。

这些组件直接服务 RQ-A（planning boundary）和 RQ-B（evidence-grounded correction），也能支撑 R4 的公平比较。

### B. Reliability controls — candidate M2/M3 scope

可在最小闭环稳定后加入：

- 有界 retry、replan、reflection 的独立开关；
- typed tool failure 与 controlled failure injection；
- budget-matched extra-attempt control；
- first error / proximate cause / terminal symptom 的 trace 记录；
- 只在本地、可快照沙箱中做 checkpoint/restore 的小规模验证。

### C. Optional extensions — conditional M4/M5 scope

- 固定 seed 的 dynamic environment wrapper；
- 一个经过人工审查的 MCP provider；
- direct-vs-MCP adapter overhead 对照；
- 第二任务族或外部 benchmark 泛化。

这些不是当前 M0/M1 的必要条件。

## 5. What is not feasible as one current workstream

### 5.1 把附件五个 RQ 原样加入项目

附件将 planning、reflection、tool validation、扰动泛化、资源延迟同时作为研究问题。当前 R1 已指出：

- planning 与 dynamic replanning 应先收窄并合并；
- reflection 需要区分 detection、diagnosis、correction 与额外 test-time compute；
- failure taxonomy 更适合作为跨 RQ 的分析层；
- tool validation 和资源延迟应作为实验基础设施/诊断变量，而不是自动成为新的核心 RQ。

因此不得把附件 Section 1 的 5 个问题直接登记为 active RQs。

### 5.2 在 M0 未通过前实现 P0 模块

附件的 `RunState`、`ToolRegistry`、`Executor`、`TraceRecorder` 和 `Evaluation Runner` 都属于实现工作。当前 Constitution 与 Shared Memory 明确要求：

- R4 review 尚未完成；
- R0 尚未 freeze Research Identity 与 accepted RQs；
- M0 前禁止 architecture freeze 和 implementation。

所以这些模块可以进入 **候选 M1 design input**，不能在当前阶段开始写代码。

### 5.3 同时实现 rollback、MCP、dynamic environment 和资源调度

这些方向的依赖链不同：

- rollback 依赖可快照环境、在途调用协调、幂等/补偿语义；
- dynamic environment 依赖稳定 verifier、可解性检查和变体版本化；
- MCP 依赖协议版本、provider 依赖、命名空间和资源安全边界；
- resource scheduling 依赖先测出真实瓶颈，并且不能改变主实验的成功率口径。

将它们并列放入第一轮会产生大量交互效应，无法判断失败来自研究策略还是基础设施。

### 5.4 将 Memory 作为当前主线

当前 Project Memory 明确：Memory 不是 M0–M3 的 active RQ；只有在核心实验显示 cross-episode 或 long-horizon failure 且现有 state/trace/replanning 无法解释时，才创建 RQ-005。附件中的 Memory/Reflection 设计可保留为条件性材料，不能现在升格。

## 6. Compatibility with current project direction

### Compatible

- “相同模型、任务和资源预算下比较策略”与当前 fair-baseline 原则一致。
- 独立 verifier、全量 run 统计、失败不静默丢失，与当前 Evaluation Contract 目标一致。
- ReAct 不被错误地当成“无 planning”；附件允许把 ReAct 与 explicit ex-ante planning 分开定义，这与 R1 evidence 一致。
- reflection、retry、replan、rollback 分离，符合当前避免 treatment contamination 的要求。
- `Trace / Metrics` 横切运行时而不依附单一策略，适合 RQ-004 的分析层降级方案。

### Needs modification

- “Tool-Using Agent Runtime + Evaluation Framework”要保持主次关系：Evaluation Framework 是研究基础设施，不应与 Runtime 并列成第二个产品目标。
- 研究问题必须采用 R1 收窄建议，至少等 R4 review 后才能决定最终措辞。
- Failure taxonomy 要预注册最小标签，保留 unknown/ambiguous，避免看完结果后发明类别。
- “反思收益来自总结、重试还是状态恢复”需要拆成可独立开关和预算匹配实验，不应作为一句混合问题。
- `MCP Provider` 和 `Paper2Agent` 只能是 optional provider case study，不得成为核心 runtime 研究的必要依赖。
- 资源/并发评测先作为 observability，只有测出瓶颈后才进入优化工作流。

## 7. Recommended migration order after M0

### Stage 0 — No-code decision gate

完成 R4 review；R0 决定采用两个核心 RQ 或其他明确收窄版本；R6 登记 decision、scope 和 P0/P1。

### Stage 1 — Minimum measurable loop

只实现一个本地、确定性、无副作用任务闭环：

`task → policy → validated action → executor → observation → verifier → trace`

加入 hard budget、termination reason、invalid-call rejection 和全量 run record。

### Stage 2 — Strategy comparison

只比较：

- ReAct；
- explicit ex-ante plan-and-execute；
- 一个 budget-matched control。

先完成 M1 baseline validity，再决定是否加入 replanning/reflection。

### Stage 3 — Controlled recovery

在同一确定性沙箱中逐个加入：retry、replan、reflection、restore；共享故障前缀和总预算，保留失败分支。

### Stage 4 — Optional robustness/provider extension

根据 M3 结果选择一个扩展：dynamic wrapper **或** 一个 MCP provider；不同时启动两个生态方向。

### Stage 5 — Generalization and release

只把已产生可解释结果的 intervention 扩展到第二任务族、外部 benchmark 或资源评测。

## 8. R0 decision proposal

**DECISION PROPOSAL: `TEST FIRST`**

附件整体不进入当前 P0，也不批准全盘重构。批准将其作为：

> M0 通过后的候选架构与研究扩展输入，按 Stage 1 → Stage 2 → Stage 3 逐步验证。

### Immediate next step

当前唯一最有价值的下一步仍是：

**完成 R4 measurability/validity review，并让 R0 冻结两个核心 RQ 和 M1 的单一目标。**

### Not authorized

- 代码实现；
- 全量架构文件冻结；
- MCP/Paper2Agent 接入；
- Memory 主线；
- rollback/dynamic environment/resource scheduler 并行开发；
- 将附件中的设计建议写成 FACT 或 FINDING。

## 9. ROLE UPDATE

**ROLE-LOG-ID:** ROLE-20260921-R0-002  
**Role:** R0 — Project Director / Principal Investigator  
**Date:** 2026-09-21  
**Task:** Feasibility review of `Agent_Runtime_R0_优化重构总纲.md`  
**Context:** 外部材料提出统一 runtime、可插拔策略、tool reliability、evaluation、rollback、dynamic environment、MCP provider 和 resource profiling 的组合方案；当前项目仍在 M0。  
**What Was Done:** 对照仓库实际内容、Project Memory、R1 literature review 和 Constitution 约束，评估研究一致性、实现可行性、时间范围、风险与迁移顺序。  
**What Changed:** 将附件从“可直接执行的重构总纲”降级为“候选架构与分阶段迁移提案”；提出 `TEST FIRST`，保留 core runtime/evaluation spine，延后 rollback、MCP、dynamic environment、resource scheduling 与 memory。  
**Evidence:** 当前仓库无 runtime source/tests/dependency manifest；`PROJECT_MEMORY/01_PROJECT_STATE.md`、`02_MASTER_CHECKLIST.md`、`03_RESEARCH_QUESTIONS.md`、`11_MILESTONES.md`；`R1_M0_LITERATURE_NOVELTY_REVIEW.md`；附件本身。  
**Files Affected:** `PROJECT_DOCS/ROLE_DELIVERABLES/R0_20260921_REFACTOR_FEASIBILITY_REVIEW.md`。  
**Research Questions Affected:** 不创建新 RQ；支持 R1 的收窄方向，反对将附件五个问题直接激活。  
**Architecture Impact:** 提出 Stage 1–5 候选迁移顺序；当前无架构冻结或实现授权。  
**Experiment Impact:** 要求先完成 R4 Evaluation Contract；以最小确定性任务验证闭环，再扩展 recovery/provider/robustness。  
**Failure Impact:** 支持 typed failure、trace-level first/proximate/terminal cause；拒绝在未验证前把 taxonomy 写成 finding。  
**New Risks:** 总纲可能导致 framework/evaluation scope split、rollback/MCP/dynamic environment 依赖爆炸、研究与工程贡献混淆。  
**Recommended Next Step:** 完成 R4 review；随后 R0 记录 M0 freeze decision，并由 R6 归档本评审。  
**Need Handoff:** YES — R4（评估总纲的可测量性审查）、R6（归档 R0 feasibility review）。

