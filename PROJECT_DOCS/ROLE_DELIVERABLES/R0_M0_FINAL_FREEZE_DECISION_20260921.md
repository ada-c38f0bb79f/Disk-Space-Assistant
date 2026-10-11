# R0 M0 Final Freeze Decision

**Role:** R0 — Project Director / Principal Investigator  
**Decision date:** 2026-09-21  
**Decision ID:** `DEC-20260921-R0-M0-001`  
**Milestone:** M0 — Research Charter Freeze  
**Decision status:** Final R0 research decision; M0 milestone status is **PARTIAL**

## 1. Decision in one page

| Item | R0 final decision |
|---|---|
| Active core RQ | Freeze only narrowed **RQ-001** |
| RQ-002 | Merge under RQ-001 as a **gated dynamic perturbation/recovery subproblem** |
| RQ-003 | Keep as **conditional P1**, not active core |
| RQ-004 | Downgrade to a preregistered **analysis layer**, not an independent RQ or novelty claim |
| M1 | One goal: validate measurement protocol for RQ-001; make no planning-effect claim |
| M0 result | **PARTIAL** — research contract frozen; R6 operational registration incomplete |
| Implementation status | Still blocked until R6 completes the operational gate and R0 authorizes M1 execution |

This decision supersedes the earlier candidate-RQ wording where it conflicts with this document. It does not authorize code, benchmark generation, pilot execution, or architecture freeze.

## 2. Frozen Research Identity v1

> 在固定模型、工具、任务信息、终止规则和总推理预算的条件下，研究 explicit ex-ante subgoal planning 相对于 ReAct 是否会随任务 dependency depth 改变工具任务的 end-state success，以及这种差异的资源代价。

The project studies a treatment boundary under controlled conditions. It does not claim that planning is generally beneficial.

## 3. RQ disposition

### RQ-001 — ACTIVE CORE

**Frozen question**

在 fully observed、stationary task conditions 下，固定 model snapshot、tool registry/schema、initial state、task information、termination/verifier 和总 inference budget，explicit ex-ante subgoal plan 相对于 ReAct 的 episode end-state success 是否随 dependency depth 改变，并产生什么 resource cost？

**Operational treatment boundary**

- Explicit planning must create a recorded prospective plan before the first external action.
- The plan must contain at least two future subgoals/action units and a recorded order or dependency.
- ReAct remains an observation-driven `Thought → Action → Observation` loop; it is not labeled as a no-planning or no-adaptation baseline.
- Ordinary next-action choice, post-hoc summary, retry, argument repair, and unrecorded reasoning are not explicit planning.
- The first RQ-001 comparison uses dependency depth as the planned task factor. Other factors remain controlled or deferred.

**Primary outcome**

Episode end-state success according to an independent verifier, using the full enrolled-run denominator. Budget exhaustion, timeout, invalid action, and agent failure remain failures. Infrastructure failures are separately labeled and retained in the full accounting.

**Falsification condition**

The working planning-boundary hypothesis is not supported if, under the frozen controls and adequate repetitions, there is no stable treatment × dependency-depth interaction, or if any apparent difference is explained by unequal information, prompt, model, tool access, termination, or inference budget.

**Allowed claims after formal experiments**

- A task-family- and budget-bounded success-rate comparison.
- An interaction or non-interaction with the preregistered dependency-depth factor.
- Resource-normalized differences in tokens, calls, latency, and cost.

**Disallowed claims without additional evidence**

- Planning is generally better.
- Results generalize to arbitrary agents, domains, models, or long-horizon environments.
- The result is a new planning algorithm merely because a runtime module exists.

### RQ-002 — GATED SUBPROBLEM OF RQ-001

RQ-002 is not an active independent RQ. It may enter only as a dynamic perturbation/recovery subproblem after the RQ-001 measurement protocol passes.

**Entry gate**

All of the following must be satisfied:

1. RQ-001 ReAct and explicit-plan protocols pass paired-task, verifier, trace-completeness, and budget audits.
2. One typed, replayable perturbation family is selected with independent ground truth. The first gated study uses either explicit tool error or a verifiable stale-plan event; it does not mix silent failure and environmental change.
3. Failure timing, observability, recoverability, and the recovery denominator are fixed before execution. Irrecoverable cases are excluded from the recovery denominator but reported.
4. Replanning changes the recorded plan state or unexecuted subgoals. Retry, argument repair, and ordinary ReAct adaptation do not count as replanning.
5. ReAct, static plan, and retry/argument-repair controls are retained. Revision calls, tokens, latency, and cost use the same total budget.
6. A protocol-only check shows that the injection does not leak a gold “this is a perturbation” signal and that revision is distinguishable from ordinary next-action adaptation.

No RQ-002 implementation or experiment is authorized by this decision.

### RQ-003 — CONDITIONAL P1

RQ-003 remains a conditional second-stage candidate and is not part of the active core route.

**Frozen candidate wording**

在 same-episode tool use 中，仅使用预先允许的 trace-observable signals、且不访问 gold outcome 或 failure labels 的 selective reflection，相对于 no-reflection、always-reflect 和 budget-matched extra-attempt control，是否能提高 end-to-end correction 并降低 repeated mistake？

**Entry conditions**

- RQ-001 measurement validity has passed.
- The M1/RQ-001 cost envelope remains within the frozen ceiling.
- The reflection signal schema contains no oracle failure label or future observation.
- Trigger, diagnosis, and correction are separately observable.
- False-intervention and missed-detection denominators are fixed.
- Same-episode reflection is separated from cross-episode memory.

RQ-003 has no active budget allocation in M1.

### RQ-004 — ANALYSIS LAYER

RQ-004 is not an active novelty RQ and cannot be reported as a new failure taxonomy or causal explanation.

It is a preregistered analysis and quality-control layer for RQ-001 and any later RQ-003 study.

**Frozen minimum protocol**

- Two-level labels: `locus` and `mechanism`.
- Separate `first error`, `proximate cause`, and `terminal symptom`.
- Separate model/policy, runtime, tool/environment, and harness/engineering loci.
- Preserve `unknown` and `ambiguous`.
- Use blinded double annotation on a prespecified trace subset.
- Continue using the taxonomy only if Cohen’s κ or Krippendorff’s α is at least **0.60** on the prespecified subset.
- Report coverage, unknown/ambiguous proportion, annotation changes, and held-out performance.
- Any predictive result is reported as association/prediction. It is not a causal explanation.

## 4. Frozen measurement and decision thresholds

### MCID

The RQ-001 minimum clinically/research practically important difference is:

**MCID = 10 absolute percentage points in end-state success rate.**

This threshold is a decision threshold, not an expected result. It must be reported together with an absolute confidence interval, cost, tokens, calls, and latency. Statistical significance alone cannot replace the MCID.

### Equivalence and non-inferiority

For future formal RQ-001 interpretation:

- **Equivalence region:** `[-5, +5]` percentage points in success-rate difference (explicit plan minus ReAct).
- **Non-inferiority margin:** `-5` percentage points.
- A result outside the equivalence region is not evidence of equivalence.
- If the protocol does not implement a prespecified equivalence method or confidence-interval rule, the result must be reported as inconclusive rather than equivalent.
- M1 does not run an effect test and does not make equivalence, non-inferiority, superiority, or planning-benefit claims.

### Resource interpretation

Success remains the primary outcome. A future practical-benefit claim requires either:

- at least the 10-point MCID at no more than 20% higher total episode cost; or
- non-inferior success (not below the -5-point margin) together with at least 20% lower cost per successful episode.

Latency, token use, and call count remain secondary outcomes and must be reported even when success is unchanged.

## 5. Frozen inference budget v1

The budget applies per enrolled episode and includes every model call, planner call, repair call, reflection call, revision call, and hidden subcall that can be observed by the harness.

| Resource | Hard cap per episode |
|---|---:|
| Total model requests | 12 |
| Combined model input + output tokens | 24,000 |
| Wall-clock time | 180 seconds |
| Tool invocations | 16 |
| Corrective/revision/reflection calls | 2 |
| Parallel model/tool execution | Disabled for M1 |

Rules:

- Budget is cumulative. Retry, repair, reflection, replanning, and restore-related model calls do not reset it.
- A run that reaches any hard cap terminates with the corresponding reason and remains in the denominator.
- A strategy cannot receive extra calls because its internal policy happens to need them.
- The same cap applies to ReAct and explicit planning; the plan-generation call consumes the same episode budget.
- Any unobservable provider-side subcall is recorded as unavailable and prevents a clean resource-normalized claim for that run.

## 6. Frozen cost budget v1

Accounting currency is USD-equivalent at the recorded price snapshot. Model/API/tool charges and paid evaluation services count toward the ceiling; local development compute is recorded separately.

| Work package | Ceiling | Status |
|---|---:|---|
| M1 protocol/measurement-validity work | **暂定规划数字：USD 150** | No actual cost measurement, user budget confirmation, or spending authorization |
| Formal RQ-001 first comparison | **暂定规划数字：USD 500** | No actual cost measurement; requires later confirmation and separate execution authorization |
| RQ-002 and RQ-003 | **USD 0 allocated** | Gated / conditional P1; no work authorized |

Cost rules:

- If the expected unit cost would exceed the ceiling, reduce the prespecified M1 task count within the approved design range or return to R0; do not silently increase the ceiling.
- Record model version, input/output tokens, price snapshot, tool/API charges, queue latency, and estimated cost per run.
- Separate estimated cost from actual paid cost.
- No failed or zero-success batch is assigned zero cost.

## 7. Frozen fairness controls

The following controls are mandatory for RQ-001 and M1 measurement validation:

1. Same model snapshot or endpoint version, sampling parameters, maximum output settings, and seed/replay policy.
2. Same initial state, task input, task information, demonstrations, tool registry, schema, permissions, and available tool set.
3. Strategy-specific instructions are the only intended treatment difference; no strategy receives future observations, hidden decomposition, gold failure labels, or verifier internals.
4. Same termination rules, verifier, hard caps, observation format, error format, and retry policy.
5. Every model call, token, tool call, rejection, retry, repair, revision, reflection, latency, and cost is counted.
6. ReAct is evaluated as observation-driven adaptation; it is not denied normal observation updates to manufacture a contrast.
7. Tasks are paired across strategies, with shared task/seed assignments where seeds are meaningful.
8. No post-hoc test-task exclusion. Prespecified infrastructure-failure handling retains full-run accounting and reports separated sensitivity analysis.
9. Config, prompt, model, task, schema, verifier, and price versions are hashed or otherwise recorded.
10. M1 uses no parallel execution, so latency and queue behavior do not become an uncontrolled treatment difference.
11. Development selection and any later test evaluation use distinct frozen task-family splits; no tuning on the final comparison set.
12. Any missing telemetry is reported as missing and blocks the corresponding normalized claim; it is not silently imputed as zero.

## 8. M1 single objective

> 在冻结的 RQ-001 协议下，完成一个本地、可重放、自动 verifier 可审计的最小测量闭环，并证明 ReAct 与 explicit ex-ante planning 的 baseline 行为、trace、termination、budget accounting 和 success 判定在一个小型、分层的 task set 上没有已知 ambiguity、leakage 或策略不公平。

M1 produces measurement-validity evidence only. It does not claim:

- that planning improves success;
- that planning harms success;
- equivalence or non-inferiority;
- generalization;
- a new architecture contribution;
- a new failure taxonomy.

M1 design remains subject to a provisional planning figure only; no cost ceiling is treated as confirmed until actual model/tool prices and expected run counts are measured. The previously proposed 12–24 small-task protocol is a design envelope, not an authorization to generate benchmark tasks in this decision.

## 9. M0 final judgment

### Decision: **PARTIAL**

The research contract itself is frozen because:

- R1 has completed the literature and novelty disposition;
- R4 has completed measurability/validity review and freeze support;
- R0 has made the active/gated/conditional/analysis-layer decisions;
- MCID, equivalence/non-inferiority margins, inference budget, cost budget, fairness controls, and the M1 single objective are now explicit.

M0 cannot be marked PASS yet because the Constitution’s operations gate remains incomplete:

- only 7 of the 14 shared-memory files are currently initialized;
- the final decision has not yet been registered by R6 in the Project State, RQ index, checklist, decisions record, and milestone record;
- the repository still lacks the required operational skeleton for the remaining owner-of-record files.

M0 becomes eligible for PASS only after R6 completes the archival and consistency update, and after R0 verifies that no decision was changed during registration. Until then, no implementation, benchmark generation, pilot, or architecture freeze is authorized.

## 10. R0 ROLE UPDATE for R6

**ROLE-LOG-ID:** `ROLE-20260921-R0-003`  
**Role:** R0 — Project Director / Principal Investigator  
**Date:** 2026-09-21  
**Task:** M0 final Research Contract freeze decision  
**Context:** R1 literature/novelty review, R4 freeze-support memo, R0 feasibility review, and current Project Memory were reviewed. The project remained under the no-code gate.  
**What Was Done:** Finalized Research Identity v1; froze RQ-001 as the only active core RQ; made RQ-002 a gated subproblem; retained RQ-003 as conditional P1; reduced RQ-004 to an analysis layer; froze MCID, equivalence/non-inferiority margins, inference budget, cost ceilings, fairness controls, and M1’s single measurement-validity objective.  
**What Changed:** Candidate RQ state is now a final R0 decision proposal for registration. The active core is one RQ. No implementation or experiment authorization was issued.  
**Evidence:** `PROJECT_DOCS/ROLE_DELIVERABLES/R1_M0_LITERATURE_NOVELTY_REVIEW.md`; `PROJECT_DOCS/ROLE_DELIVERABLES/R4_R0_FREEZE_DECISION_SUPPORT_MEMO.md`; `PROJECT_DOCS/ROLE_DELIVERABLES/R0_20260921_REFACTOR_FEASIBILITY_REVIEW.md`; current `PROJECT_MEMORY/01_PROJECT_STATE.md`, `02_MASTER_CHECKLIST.md`, and `03_RESEARCH_QUESTIONS.md`.  
**Files Affected:** `PROJECT_DOCS/ROLE_DELIVERABLES/R0_M0_FINAL_FREEZE_DECISION_20260921.md`; R6 must update the shared-memory records of record.  
**Research Questions Affected:** RQ-001 → ACTIVE CORE; RQ-002 → GATED SUBPROBLEM under RQ-001; RQ-003 → CONDITIONAL P1; RQ-004 → ANALYSIS LAYER; RQ-005 Memory remains NOT CREATED / DEFERRED.  
**Architecture Impact:** No architecture freeze. The feasibility review’s staged runtime spine remains a future M1 input only.  
**Experiment Impact:** M1 is limited to measurement validity for RQ-001; no planning-effect claim, pilot, benchmark generation, or formal comparison is authorized by this decision.  
**Failure Impact:** RQ-004 labels and reliability threshold are frozen as future analysis controls; no failure finding exists.  
**New Risks:** The frozen 10-point MCID and 5-point equivalence/non-inferiority margins may be too coarse or too strict for a later task family; budget caps may limit longer tasks; RQ-003 may be deferred indefinitely if RQ-001 costs exceed the ceiling. These are explicit review conditions, not reasons to alter M0 silently.  
**Checklist Changes Requested:** Mark R1/R4/R0 decision work complete; mark accepted RQ dispositions and M1 objective as awaiting R6 registration; keep implementation, benchmark generation, pilot, and architecture freeze blocked until M0 operational PASS.  
**Recommended Next Step:** R6 creates/updates the 14 shared-memory records, registers `DEC-20260921-R0-M0-001` and `ROLE-20260921-R0-003`, and returns a Project Delta. R0 then performs the M0 PASS recheck.  
**Need Handoff:** YES — R6 for archival and consistency registration; R4/R1 only if R6 detects a conflict with their submitted evidence.
