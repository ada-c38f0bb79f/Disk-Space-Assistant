# Agent Runtime Research Project — Decision Record

| 字段 | 当前值 |
|---|---|
| Version | v1.1 |
| Updated | 2026-09-21 |
| Primary | 对应决策角色 |
| Owner of record | R6 |

## Decision Index

| Decision ID | Date | Authority | Decision | Status |
|---|---|---|---|---|
| `DEC-20260921-R0-M0-001` | 2026-09-21 | R0 | M0 Final Research Contract Freeze | **EFFECTIVE; M0 PASS** |

## DEC-20260921-R0-M0-001 — M0 Final Research Contract Freeze

**Source:** [`R0_M0_FINAL_FREEZE_DECISION_20260921.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R0_M0_FINAL_FREEZE_DECISION_20260921.md)  
**Milestone judgment in source:** M0 = **PARTIAL**；Research Contract 已冻结，R6 operational registration 当时未完成。  
**Registration state:** R6 已完成 14-file operational registration；R0 已完成 consistency recheck 并将 M0 评为 PASS。

### Frozen Research Identity v1

> 在固定模型、工具、任务信息、终止规则和总推理预算的条件下，研究 explicit ex-ante subgoal planning 相对于 ReAct 是否会随任务 dependency depth 改变工具任务的 end-state success，以及这种差异的资源代价。

### Frozen RQ Disposition

- **RQ-001:** ACTIVE CORE。
- **RQ-002:** GATED SUBPROBLEM under RQ-001；不是独立 active RQ。
- **RQ-003:** CONDITIONAL P1；M1 无预算分配。
- **RQ-004:** ANALYSIS LAYER；不是独立 RQ 或 novelty claim。
- **RQ-005 Memory:** NOT CREATED / DEFERRED。

### Frozen Thresholds

- **MCID:** end-state success rate 的绝对差异 10 percentage points。
- **Equivalence region:** explicit plan minus ReAct = `[-5, +5]` percentage points。
- **Non-inferiority margin:** `-5` percentage points。
- M1 不运行 effect test，不作 equivalence、non-inferiority、superiority 或 planning-benefit claim。
- 未来 practical-benefit claim 需要：至少 10-point MCID 且 episode cost 增幅不超过 20%；或 success 不低于 -5-point margin 且 cost per successful episode 至少降低 20%。

### Frozen Inference Budget v1 — Per Enrolled Episode

| Resource | Hard cap |
|---|---:|
| Total model requests | 12 |
| Combined model input + output tokens | 24,000 |
| Wall-clock time | 180 seconds |
| Tool invocations | 16 |
| Corrective/revision/reflection calls | 2 |
| Parallel model/tool execution | Disabled for M1 |

所有 planner、retry、repair、reflection、revision 与可观测 hidden subcall 都计入累计预算。达到任一上限即终止并保留在 denominator。ReAct 与 explicit planning 使用相同 hard caps；plan-generation call 计入同一 episode budget。

### Frozen Cost Budget v1

| Work package | Ceiling | Authorization |
|---|---:|---|
| M1 protocol/measurement-validity work | 暂定规划数字：USD 150 | 无实际成本测算或支出授权 |
| Formal RQ-001 first comparison | 暂定规划数字：USD 500 | 无实际成本测算；需另行确认与 execution authorization |
| RQ-002 / RQ-003 | USD 0 | Gated / conditional；未授权 |

必须记录 model version、input/output tokens、price snapshot、tool/API charges、queue latency、estimated cost 与 actual paid cost。失败批次不得记为零成本。

### Frozen Fairness Controls

1. 相同 model snapshot/endpoint version、sampling、max-output、seed/replay policy。
2. 相同 initial state、task input/information、demonstrations、tool registry/schema/permissions。
3. 只有 strategy-specific instruction 是预期 treatment difference；不得提供 future observations、hidden decomposition、gold failure labels 或 verifier internals。
4. 相同 termination、verifier、hard caps、observation/error format 与 retry policy。
5. 统计所有 model/tool calls、tokens、rejections、retry/repair/revision/reflection、latency 与 cost。
6. ReAct 保留正常 observation-driven adaptation，不得人为制造 straw-man。
7. Strategies 使用 paired tasks 与共享 task/seed assignments（适用时）。
8. 禁止 post-hoc test-task exclusion；infrastructure failures 保留 full-run accounting 并做分离 sensitivity report。
9. 记录或 hash config、prompt、model、task、schema、verifier 与 price versions。
10. M1 禁止 parallel execution。
11. Development selection 与未来 test evaluation 使用不同 frozen splits。
12. Missing telemetry 必须报告，并阻止对应 normalized claim；不得按零填补。

### Frozen M1 Single Objective

> 在冻结的 RQ-001 协议下，完成一个本地、可重放、自动 verifier 可审计的最小测量闭环，并证明 ReAct 与 explicit ex-ante planning 的 baseline 行为、trace、termination、budget accounting 和 success 判定在一个小型、分层的 task set 上没有已知 ambiguity、leakage 或策略不公平。

M1 只产出 measurement-validity evidence，不产出 planning effect、harm、equivalence、non-inferiority、generalization、architecture contribution 或 failure-taxonomy novelty claim。

### Authorization Boundary

本决议不授权：代码、benchmark/task generation、pilot execution、formal comparison 或 architecture freeze。任何 M1 执行仍需单独授权。

### M0 PASS Recheck

Source: [`R0_M0_PASS_RECHECK_20260921.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R0_M0_PASS_RECHECK_20260921.md)。R0 确认 R6 registration 未改变本决议，M0 = **PASS**。

当前只授权 Gate A protocol convergence；Gate B implementation、benchmark、pilot、formal comparison 与 architecture freeze 均未授权。

## Supplemental Evidence Note — R1-20260921-003

R1 后续提交的 [`R1_M0_ADDITIONAL_LITERATURE_UPDATE_20260921.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R1_M0_ADDITIONAL_LITERATURE_UPDATE_20260921.md) 补充了 ADaPT、Reflexion、Plan-and-Solve 与 ReAct 的 PAPER EVIDENCE、边界和 novelty warnings。

该材料：

- 支持但不改变 `DEC-20260921-R0-M0-001`；
- 不新增 RQ、Decision、Finding 或 claim；
- 不改变 RQ-001 ACTIVE CORE、RQ-002 GATED、RQ-003 CONDITIONAL P1、RQ-004 ANALYSIS LAYER；
- 不产生 implementation、pilot、benchmark 或 architecture authorization。

### Role Log ID Conflict

源文档声明 `ROLE-20260921-R0-003`，但该 ID 已用于 R0 feasibility review。R6 保留旧记录，并将本次 final freeze canonical 登记为 `ROLE-20260921-R0-004`；源 ID 作为冲突别名保留，不覆盖历史。

## M1 Requirements Review Status — No New Decision

R2's [`R2_M1_MINIMUM_REQUIREMENTS_REVIEW.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R2_M1_MINIMUM_REQUIREMENTS_REVIEW.md) and R4's [`R4_M1_R2_PROTOCOL_CONSISTENCY_REVIEW.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R4_M1_R2_PROTOCOL_CONSISTENCY_REVIEW.md) are archived as requirements/clarification records only. They do not alter `DEC-20260921-R0-M0-001` and do not authorize implementation, benchmark generation, pilot execution, formal comparison, or architecture freeze.

## R0 Execution Focus Adjustment — ROLE-20260921-R0-007

R0 changed near-term priority to: **Gate A minimum protocol → Gate B minimal runnable loop → Gate C measurement sanity → Gate D RQ-001 pilot decision**. The USD 150 / USD 500 figures are provisional planning numbers, not confirmed budgets, actual expenditure, or execution authorization. Gate B requires a separate R0 implementation decision.
