# Agent Runtime Research Project — Research Question Index

| 字段 | 当前值 |
|---|---|
| Version | v1.0 |
| Updated | 2026-09-21 |
| Primary roles | R0 + R1 + R4 |
| Owner of record | R6 |
| Governing decision | `DEC-20260921-R0-M0-001` |
| Active core RQ count | **1** |
| Gated subproblems | **1** |
| Conditional P1 RQs | **1** |
| Analysis layers | **1** |

> 本文件已按 R0 最终 Research Contract 决议更新。此前的 candidate/proposal wording 在与 `DEC-20260921-R0-M0-001` 冲突时失效。

## 1. Final Disposition Index

| ID | Name | Final status | Current authorization |
|---|---|---|---|
| RQ-001 | Planning Boundary | **ACTIVE CORE** | Research status active；implementation/pilot/formal experiment 均未授权 |
| RQ-002 | Dynamic Perturbation and Recovery | **GATED SUBPROBLEM under RQ-001** | 未达到 entry gate；USD 0；无实现/实验授权 |
| RQ-003 | Evidence-grounded Reflection | **CONDITIONAL P1** | M1 无预算；无实现/实验授权 |
| RQ-004 | Failure Analysis | **ANALYSIS LAYER** | 未来质量控制层；不是独立 RQ/novelty claim |
| RQ-005 | Memory | **NOT CREATED / DEFERRED** | 不在当前路线 |

## 2. RQ-001 — ACTIVE CORE

### Frozen Question

在 fully observed、stationary task conditions 下，固定 model snapshot、tool registry/schema、initial state、task information、termination/verifier 和总 inference budget，explicit ex-ante subgoal plan 相对于 ReAct 的 episode end-state success 是否随 dependency depth 改变，并产生什么 resource cost？

### Operational Treatment Boundary

- Explicit planning 必须在第一次 external action 前生成并记录 prospective plan。
- Plan 至少包含两个 future subgoals/action units，以及记录的 order 或 dependency。
- ReAct 保持 observation-driven `Thought → Action → Observation` loop；不得称为 no-planning/no-adaptation baseline。
- Ordinary next-action choice、post-hoc summary、retry、argument repair 与 unrecorded reasoning 不属于 explicit planning。
- 首轮 task factor 只使用 dependency depth；其他因素控制或延期。

### Primary Outcome

由 independent verifier 判定的 episode end-state success，使用 full enrolled-run denominator。Budget exhaustion、timeout、invalid action 与 agent failure 均为失败；infrastructure failures 单独标注但保留完整核算。

### Falsification Condition

若在冻结控制与足够重复下没有稳定的 treatment × dependency-depth interaction，或表面差异可由 unequal information、prompt、model、tool access、termination 或 inference budget 解释，则 working planning-boundary hypothesis 不获支持。

### Frozen Decision Thresholds

- MCID: 10 absolute percentage points。
- Equivalence region: `[-5, +5]` percentage points。
- Non-inferiority margin: `-5` percentage points。
- 详细 budget、cost 与 fairness controls 见 [05_DECISIONS.md](05_DECISIONS.md)。

### Claim Boundary

未来正式实验只可支持 task-family- and budget-bounded comparison、预注册 dependency-depth interaction/non-interaction 与 resource-normalized differences。不得泛化为“planning generally better”或新算法贡献。

## 3. RQ-002 — GATED SUBPROBLEM UNDER RQ-001

RQ-002 不是独立 active RQ。只有以下条件全部满足后才可进入：

1. RQ-001 ReAct/explicit-plan protocols 通过 paired-task、verifier、trace-completeness 与 budget audits。
2. 选择一种 typed、replayable perturbation family 与 independent ground truth；首个研究只用 explicit tool error 或 verifiable stale-plan event 之一。
3. 预先冻结 failure timing、observability、recoverability 与 recovery denominator。
4. Replanning 必须改变 recorded plan state 或 unexecuted subgoals；retry、argument repair、ordinary ReAct adaptation 不计为 replanning。
5. 保留 ReAct、static plan 与 retry/argument-repair controls，并使用相同 total budget。
6. Protocol-only check 证明 injection 不泄漏 gold perturbation signal，且 revision 可与 ordinary adaptation 区分。

当前 USD 0 allocation；无实现或实验授权。

## 4. RQ-003 — CONDITIONAL P1

### Frozen Candidate Wording

在 same-episode tool use 中，仅使用预先允许的 trace-observable signals、且不访问 gold outcome 或 failure labels 的 selective reflection，相对于 no-reflection、always-reflect 和 budget-matched extra-attempt control，是否能提高 end-to-end correction 并降低 repeated mistake？

### Entry Conditions

- RQ-001 measurement validity 已通过；
- M1/RQ-001 cost 保持在 frozen ceiling 内；
- reflection signal schema 无 oracle failure label 或 future observation；
- trigger、diagnosis、correction 分别可观察；
- false-intervention 与 missed-detection denominators 已冻结；
- same-episode reflection 与 cross-episode memory 分离。

M1 无 active budget allocation；无实现或实验授权。

## 5. RQ-004 — ANALYSIS LAYER

RQ-004 不是独立 novelty RQ，不得报告为新 failure taxonomy 或 causal explanation。

### Frozen Minimum Protocol

- two-level labels: `locus` and `mechanism`；
- 分离 `first error`、`proximate cause`、`terminal symptom`；
- 分离 model/policy、runtime、tool/environment、harness/engineering loci；
- 保留 `unknown` 与 `ambiguous`；
- 在预注册 trace subset 上做 blinded double annotation；
- 只有 Cohen’s κ 或 Krippendorff’s α ≥ **0.60** 才继续使用 taxonomy；
- 报告 coverage、unknown/ambiguous proportion、annotation changes 与 held-out performance；
- predictive result 只能称 association/prediction，不能称 causal explanation。

## 6. Dependency Model

1. RQ-001 是唯一 ACTIVE CORE。
2. RQ-002 依赖 RQ-001 measurement-protocol PASS 与独立 entry gate。
3. RQ-003 依赖 RQ-001 validity、预算余量与 non-oracle signal schema。
4. RQ-004 只服务 RQ-001 与未来可能进入的 RQ-003。
5. Memory 不属于当前 Research Contract。

## 7. Evidence and Decision Trail

- R1: [`R1_M0_LITERATURE_NOVELTY_REVIEW.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R1_M0_LITERATURE_NOVELTY_REVIEW.md)
- R4: [`R4_M0_EVALUATION_CONTRACT_V0.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R4_M0_EVALUATION_CONTRACT_V0.md)
- R4: [`R4_R0_FREEZE_DECISION_SUPPORT_MEMO.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R4_R0_FREEZE_DECISION_SUPPORT_MEMO.md)
- R0: [`R0_M0_FINAL_FREEZE_DECISION_20260921.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R0_M0_FINAL_FREEZE_DECISION_20260921.md)
- R1 supplemental: [`R1_M0_ADDITIONAL_LITERATURE_UPDATE_20260921.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R1_M0_ADDITIONAL_LITERATURE_UPDATE_20260921.md)
- Canonical decision record: [05_DECISIONS.md](05_DECISIONS.md)

## 8. Current Claims Policy

### Allowed

- RQ-001 已被 R0 冻结为 active core research question。
- RQ-002/003/004 的 gated/conditional/analysis status。
- Frozen protocol、budget、MCID 与 fairness controls 是 project decisions。

### Not Allowed

- Planning improves or harms success。
- ReAct is a no-planning/no-adaptation baseline。
- RQ-004 is a novel or causal taxonomy。
- 任何 effect、equivalence、non-inferiority、generalization 或 architecture-contribution claim。

当前无 EXPERIMENT RESULT 或 FINDING。
