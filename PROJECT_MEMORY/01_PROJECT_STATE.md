# Agent Runtime Research Project — Project State

| 字段 | 当前值 |
|---|---|
| Memory version | v1.3 |
| 记录日期 | 2026-09-21 |
| Owner of record | R6 — Project Memory & Operations Keeper |
| 权威输入 | [`00_PROJECT_INITIALIZATION.md`](../PROJECT_DOCS/INITIALIZATION/00_PROJECT_INITIALIZATION.md)；`DEC-20260921-R0-M0-001`；`ROLE-20260903-R1-001`；`ROLE-20260921-R0-004`；`ROLE-20260921-R4-001`；`ROLE-20260921-R4-002`；`ROLE-20260921-R1-003` |
| 当前阶段 | Phase 1 — Gate A Protocol Minimum |
| 当前里程碑 | M1 — Gate A: Minimum Protocol Convergence |
| 里程碑状态 | **M0 PASS** |
| 实施授权 | **Gate A protocol convergence only；Gate B implementation requires separate R0 authorization** |

> 本文件记录项目的“状态真相”。方向与优先级由 R0 决定；R6 只登记已被输入材料支持的事实、决定和未决项。

## 1. Director Status

- **Current Phase:** Phase 1 — Gate A Protocol Minimum
- **Current Milestone:** M1 — Gate A: Minimum Protocol Convergence
- **Active RQs:** RQ-001 为 ACTIVE CORE；RQ-002 为 GATED SUBPROBLEM；RQ-003 为 CONDITIONAL P1；RQ-004 为 ANALYSIS LAYER。
- **Most Important Finding:** 暂无研究发现。最新 R0 输入是已冻结的 Research Contract；它是 DECISION，不是实验 Finding。
- **Largest Risk:** 在 M0 前把候选架构误当成已批准实施计划，进而引入 scope、实现、环境与评测器混杂。
- **Current P0:** 完成 Gate A 最小协议收敛；随后由 R0 单独决定是否开放 Gate B 最小闭环实现授权。
- **R2 Status:** COMPLETE；R4 consistency review: CLARIFICATIONS REQUIRED。
- **Implementation-first rule:** minimum protocol freeze 后优先最小 runnable loop；不等于当前已获代码授权。
- **Things We Should NOT Do Now:** 写代码、冻结架构、选择框架/依赖、大规模生成 benchmark 任务，或加入 memory、multi-agent、RAG、browser/GUI、multimodal、RL 等工作流。

## 2. Research Identity

**FROZEN DECISION — Research Identity v1; M0 PASS**

本项目研究：**在固定模型、工具、任务信息、终止规则和总推理预算的条件下，研究 explicit ex-ante subgoal planning 相对于 ReAct 是否会随任务 dependency depth 改变工具任务的 end-state success，以及这种差异的资源代价。**

主要研究对象是以下因素间的因果关系：

- runtime strategy：ReAct、planning、replanning、reflection；memory 仅在 M3 后有条件考虑；
- task/environment conditions：依赖深度、不确定性、工具失败、环境变化、任务长度；
- model capability；
- outcomes：成功、恢复、效率、成本与 trace-level failure modes。

**HYPOTHESIS:** 更多 Agent 机制并不总是更好。Planning、replanning、reflection 可能只在可识别的任务/失败条件下有效，并可能在其他条件下降低可靠性或效率。

该陈述是待验证假设，不是实验结果或研究发现。

## 3. Scope Snapshot

### Immediate scope — Gate A/B/C/D

- RQ-001 的 ReAct / explicit ex-ante planning 边界；
- end-state verifier、最小 trace、budget ledger、fairness checklist；
- 最小 runnable loop、measurement sanity 与后续 pilot decision gate。

Reflection、replanning、rollback、MCP/Paper2Agent、memory、多模型、多 benchmark、资源调度暂入 backlog。

### Months 4–6 — CONDITIONAL

- 窄范围 episodic/runtime memory；
- 更多模型与更长任务；
- 第二任务族/benchmark 泛化；
- 证据充分时才考虑 preprint。

进入条件：新增内容必须直接服务 active RQ，且不破坏核心实验进度。

### OUT OF SCOPE

- Multi-agent；browser/GUI/computer-use；multimodal；
- RAG、knowledge graph、通用知识助手；
- RL 或 fine-tuning；
- 分布式/生产编排与企业平台能力；
- 通用框架替代品、大量集成或产品功能；
- 文献与实验审查前的 novelty claim。

完整延期事项见 [10_BACKLOG.md](10_BACKLOG.md)。

## 4. Research Question State

| ID | 简称 | 当前状态 | 激活条件 |
|---|---|---|---|
| RQ-001 | Planning Boundary | **ACTIVE CORE** | M1 measurement-validity gate |
| RQ-002 | Dynamic Perturbation and Recovery | **GATED SUBPROBLEM** | RQ-001 protocol PASS + entry gate |
| RQ-003 | Evidence-grounded Reflection | **CONDITIONAL P1** | RQ-001 validity + budget gate |
| RQ-004 | Failure Analysis | **ANALYSIS LAYER** | κ/α ≥ 0.60 and quality controls |
| RQ-005 | Memory | NOT CREATED | M3 后出现可分离的 memory failure hypothesis，且经 R0 批准 |

详细索引见 [03_RESEARCH_QUESTIONS.md](03_RESEARCH_QUESTIONS.md)。

## 5. Current Work State

| 顺序 | Work item | Owner | 状态 | 当前缺口 |
|---|---|---|---|---|
| P0-1 | Research Contract Review | R0；review: R1/R4 | **COMPLETE / M0 PASS** | R0 已完成 registration consistency recheck；`DEC-20260921-R0-M0-001` 未改变 |
| P0-2 | Evaluation Contract v0 | R4 | **FROZEN BY R0** | MCID、等效性/非劣界限、budget v1、cost v1、fairness controls 与 M1 objective 已登记 |
| P0-3 | Shared Project Memory Initialization | R6 | **COMPLETE (14/14 files)** | Constitution-defined shared-memory skeleton 已全部初始化并交叉链接 |

### Single Most Valuable Next Step

把 M1 protocol-only requirements 压缩成一页可执行协议：verifier、最小 trace、budget ledger、fairness checklist；之后才讨论 Gate B 最小闭环实现授权。

## 6A. Execution Focus Adjustment

R0 已于 2026-09-21 将项目重心调整为 **implementation-first after minimum protocol freeze**。当前目标是尽快形成一个本地、确定性、可验证的最小 tool-use 闭环，而不是继续扩写完整 Runtime 蓝图。

- Gate A：最小协议收敛；
- Gate B：最小 runnable loop（需单独实现授权）；
- Gate C：measurement sanity；
- Gate D：再决定是否授权 RQ-001 protocol pilot。

本调整不改变 RQ-001 active core，也不授权代码、benchmark、pilot、模型/API 调用或架构冻结。

## 6. Roadmap Snapshot

- **Immediate:** Gate A minimum protocol → Gate B minimal runnable loop → Gate C measurement sanity → Gate D pilot decision。
- **Month 2:** ReAct vs static planning、failure/stale-plan 场景、dynamic replanning、replication 与 ablation。Gate: M2。
- **Month 3:** reflection policies、model × architecture、robustness、replication、report v1。Gate: M3。
- **Month 4:** 只有在证据支持时研究 memory。Gate: M4。
- **Month 5:** 第二任务族/benchmark 泛化与 reliability audit。Gate: M5。
- **Month 6:** clean reproduction、release、report、preprint decision、interview narrative。Gate: M6。

完整 gate 条件见 [11_MILESTONES.md](11_MILESTONES.md)。

## 7. Initial Risk Register

| Risk | 状态 | 当前控制 |
|---|---|---|
| Scope dilution | OPEN / HIGH | M0 no-code gate；新能力必须映射 active RQ |
| Architecture–model confounding | OPEN | 预先设计 model × architecture controls |
| Unequal inference budget | OPEN | R4 明确 calls/tokens/latency/cost 控制 |
| Benchmark bias | OPEN | benchmark ambiguity/leakage/fairness review |
| Framework leakage | OPEN | M0 前不选框架；研究语义独立于框架 |
| Trace insufficiency | OPEN | M1 前定义可用于 failure analysis 的 trace contract |
| Premature novelty | OPEN | R1 review 前禁止 novelty claim |
| Learning displacement | OPEN | 关键概念需用户可解释、可重建、可辩护 |
| Architecture overreach before M0 | OPEN / HIGH | R0 已明确 `TEST FIRST`；M0 前不冻结完整架构、不写代码 |

## 8. Known Unknowns / Unresolved Items

- `planning`、`replanning`、`reflection`、`recovery`、`task success`、`fair baseline` 的操作定义尚未冻结。
- R1 supplemental literature update 已归档并支持既有 final disposition；formal experiment evidence 仍不存在。
- baseline matrix、control variables、统计/重复假设与 rough cost envelope 尚未建立。
- M0 的精确日历截止日期未由 R0 记录；当前仅有“Week 1 末”。
- 14 份 Constitution-defined shared-memory 文件已建立；R0 PASS recheck 已记录。

## 9. Evidence Classification

- **FACT:** R0 final decision、R1 novelty review、R4 Evaluation Contract 与 freeze-support memo 均已登记。
- **DECISION:** RQ-001 ACTIVE CORE；RQ-002 GATED；RQ-003 CONDITIONAL P1；RQ-004 ANALYSIS LAYER；M0 PASS；当前聚焦 Gate A。
- **PROPOSED DECISION:** Gate A 一页协议中的语义裁决仍待 R0；Gate B 实现授权仍未给出。
- **HYPOTHESIS:** 更多 runtime machinery 并非普遍更好。
- **PAPER EVIDENCE:** PAPER-001 — ReAct；与 RQ-001/RQ-002 相关，详细见 [06_LITERATURE.md](06_LITERATURE.md)。
- **ROLE REVIEW:** R0 feasibility review 建议 `TEST FIRST`；R4 已建议三个月只冻结 RQ-001、M1 只证明 measurement validity；二者都不是架构冻结、实施授权、实验结果或 Finding。
- **UNKNOWN:** Gate A 中 revision/retry/repair、invalid-action success、cap/verifier/termination precedence、计数单位、depth/horizon、indeterminate/infra adjudication 与成本汇总；后续 execution authorization、formal experiment results 与 findings。
- **EXPERIMENT RESULT / FINDING:** 无。

## 10. Frozen Operational Summary

- **MCID:** 10 absolute percentage points。
- **Equivalence region:** `[-5, +5]` percentage points。
- **Non-inferiority margin:** `-5` percentage points。
- **Per-episode hard caps:** 12 model requests；24,000 combined tokens；180 seconds；16 tool invocations；2 corrective/revision/reflection calls；M1 禁止 parallel execution。
- **Cost planning:** USD 150/500 仅为早期暂定规划数字；没有实际成本测算、用户预算确认或支出授权。RQ-002/RQ-003 当前不分配预算。
- **M1 objective:** 只验证 RQ-001 measurement protocol，不产出 planning effect claim。
- **Authorization:** Gate A protocol convergence only；Gate B implementation、benchmark generation、pilot、formal comparison 与 architecture freeze 均未授权。

## 11. Update Rule

只有出现 R0 决议、角色交付、正式实验、架构决定、failure 记录或 milestone review 时才更新本文件。未被来源支持的内容必须保持 UNKNOWN，不得推测补齐。
