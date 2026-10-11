# R2 M1 Minimum Requirements Review

**Role:** R2 — Architecture & Runtime Engineer  
**Date:** 2026-09-21  
**Scope:** RQ-001 Planning Boundary; M1 protocol-only design review  
**Status:** Requirements review only; no architecture, implementation, benchmark, pilot, or experiment authorization

## Review boundary

This document translates the frozen RQ-001 research contract into minimum, research-neutral protocol requirements. It does not approve an architecture, interface implementation, framework, dependency, benchmark, or performance claim. `REQUIRED` means necessary for M1 protocol validity; `RECOMMENDED` is useful but non-blocking; `UNKNOWN` is intentionally unresolved; `OUT OF SCOPE` is excluded from M1.

## 1. State contract

### REQUIRED

- Every enrolled episode has an explicit, serializable state record with: `episode_id`, protocol/config version, initial state reference, current task reference, plan state (including `absent`), execution status, termination state, error state, and budget snapshot.
- `initial_state` is immutable and sufficient to identify task input, permitted information, tool registry/schema/permissions, and seed/replay context.
- `current_task` identifies the active task and its observable task information; hidden verifier state is excluded from agent-visible state.
- `plan_state` distinguishes at least `absent`, `present`, `active`, `completed`, `superseded`, and `invalid`; it records whether a prospective plan was created before the first external action.
- `execution_status` distinguishes runnable, waiting-for-model, waiting-for-tool, observing, terminated, and infrastructure-failed states, or an equivalently auditable vocabulary.
- `termination_state` records exactly one terminal outcome: success, agent failure, timeout, budget exhaustion, invalid-action exhaustion/termination, or infrastructure failure (with infrastructure failures separately flagged).
- `error_state` is structured, typed, and append-only; it distinguishes tool/domain errors, validation errors, timeout, budget exhaustion, policy/agent failure, and infrastructure failures.
- State transitions are monotonic and timestamped; a terminal state cannot be overwritten. Any repair/revision must remain linked to the preceding state.

### RECOMMENDED

- Record state-transition sequence numbers and a deterministic state hash for replay/audit.
- Keep agent-visible state and verifier-only state in separate namespaces.

### UNKNOWN

- Exact state vocabulary and whether a particular implementation needs an explicit `waiting-for-model` state.
- Whether state snapshots or event-sourcing is the better serialization representation.

### OUT OF SCOPE

- Production scheduling, concurrency, rollback, persistence service, distributed recovery, and memory across episodes.

## 2. Action / Observation contract

### REQUIRED

- Every action record contains: `episode_id`, `step_id`, `action_id`, action type/tool name, validated arguments or a redacted canonical representation, source strategy, pre-action state reference, request timestamp, and validation result.
- Every observation record contains: `episode_id`, `step_id`, `observation_id`, source (`tool_result`, `tool_error`, `validator`, or environment), canonical payload/reference, visibility to the agent, timestamp, and the action it follows.
- Tool result and tool error are disjoint typed outcomes. A tool may return a domain-level failure as `tool_error`; transport, harness, or infrastructure faults are separately typed and must not be silently converted into ordinary observations.
- Invalid actions record the attempted action, validation rule/error, whether execution occurred, and resulting termination or continuation. Invalid actions count against the episode accounting where applicable and never disappear through repair.
- Timeouts record deadline type, elapsed time, pending operation, and terminal classification. Budget exhaustion records the exhausted resource and observed cumulative value. Both remain denominator failures.
- Observation ordering is explicit; an observation cannot be attributed to an action without a stable linkage.
- The contract is strategy-neutral: ReAct receives ordinary observations and may adapt; explicit planning receives the same task/tool/observation information subject only to the frozen treatment instruction.

### RECOMMENDED

- Canonicalize arguments and observations for hashing while retaining reviewable raw payloads subject to privacy policy.
- Record schema version and payload size for every action and observation.

### UNKNOWN

- Whether tool-domain errors should be exposed to the policy using one common envelope or typed variants; protocol must decide before execution.
- Exact redaction rules for sensitive payloads.

### OUT OF SCOPE

- Tool-provider ecosystem selection, API implementation, or production-grade schema evolution.

## 3. ReAct trace contract

### REQUIRED

- A ReAct episode records ordered units of `Thought -> Action -> Observation` for each external-action cycle; no action may be attributed to an unlinked observation.
- Thought is a trace category for the policy decision context, not a claim that hidden chain-of-thought must be exposed. A concise decision rationale or policy-event record is sufficient if the protocol specifies what is observable and comparable.
- Observation-driven adaptation is allowed after every observation, including successful results and typed tool errors. The next thought/action may revise the immediate course without being labeled replanning.
- ReAct is not a straw-man: it receives the same initial task information, tool registry/schema/access, termination rules, hard caps, and observation/error format as explicit planning; it retains ordinary adaptation and retry/argument repair under the same budget.
- The trace distinguishes ordinary next-action adaptation, retry, argument repair, and any later explicit plan artifact. A post-hoc summary is never relabeled as prospective planning.

### RECOMMENDED

- Record policy-event boundaries even when no external action is taken, so budget and termination reasoning are auditable.
- Use blinded protocol review to check that ReAct is not artificially prevented from reacting to observations.

### UNKNOWN

- The minimum visible Thought representation that preserves auditability without requiring unrestricted hidden reasoning capture.
- Whether a policy can emit multiple internal decision events between observations under the frozen model API.

### OUT OF SCOPE

- Comparing chain-of-thought quality, interpretability, or a new reasoning format.

## 4. Explicit planning artifact contract

### REQUIRED

- A prospective plan is generated before the first external action and is recorded as a distinct artifact with creation time, plan version, authoring strategy, and link to the pre-action state.
- The artifact contains at least two future subgoals/action units and an explicit order or dependency relation. Each unit has a stable identifier and status (`unstarted`, `active`, `done`, `blocked`, `superseded`, or equivalent).
- Order/dependency edges are explicit and auditable; absence of an edge must not be inferred as an ordering guarantee.
- Plan updates create a new version linked to the prior version and record the trigger observation/event, changed units/edges, and whether the update is a genuine revised plan or ordinary next-action choice.
- Plan artifact is distinct from ordinary Thought, action arguments, retry/repair, and post-hoc summary. A plan created after the first external action does not satisfy the RQ-001 explicit ex-ante treatment; it may be recorded as a protocol violation or separate event.
- Planner calls, plan tokens, and plan revisions use the same episode budget and telemetry rules as all other model activity.

### RECOMMENDED

- Store a normalized plan graph plus the human-readable artifact used for audit.
- Require a plan checksum and parent-plan checksum for every revision.

### UNKNOWN

- Whether subgoals must be semantically typed beyond stable identifiers and verifiable completion predicates.
- The permitted granularity of plan text versus structured units.

### OUT OF SCOPE

- Choosing a planner algorithm, framework, planning language, or production plan persistence system.

## 5. Verifier requirements

### REQUIRED

- Episode success is determined by an independent, deterministic verifier over the final observable/environment state and frozen task specification, not by the agent's self-report.
- The verifier emits a typed result with `success`, failure reason/category, verifier version/hash, and evidence references sufficient for audit.
- The full enrolled-run denominator includes success, agent failure, invalid action, timeout, budget exhaustion, and infrastructure-failure episodes. Infrastructure failures are separately reported and sensitivity-analyzable; they are never silently dropped or counted as success.
- Verifier disagreement, indeterminate outcomes, or missing required evidence are explicit non-success/quality statuses pending adjudication; the protocol must predefine the rule before execution.
- Termination and verifier decisions are recorded independently so a terminal success cannot be inferred solely from reaching a stop condition.

### RECOMMENDED

- Use a second read-only verifier audit on a fixed trace subset before any run authorization.
- Store verifier inputs and deterministic evidence hashes.

### UNKNOWN

- The exact adjudication rule for verifier-indeterminate cases and whether an independent human audit is required.
- Whether infrastructure failures should be excluded from a secondary sensitivity denominator; primary accounting must retain them.

### OUT OF SCOPE

- Statistical effect testing, equivalence/non-inferiority testing, or claims about planning performance.

## 6. Dependency-depth task requirements

### REQUIRED

- Dependency depth is defined prospectively as the length of the longest prerequisite chain of required action units in a task's ground-truth dependency graph; the graph and depth label are frozen before execution.
- Depth must be separable from horizon (total action count), difficulty (success probability or effort), and uncertainty (unobserved/variable information). Each is either held fixed within a depth comparison, independently stratified and reported, or explicitly deferred.
- The first protocol factor is dependency depth only. Tool identity, task family, observation format, failure injection, environment change, and uncertainty are fixed or deferred unless required to define the depth manipulation.
- Task validity checks must detect accidental depth changes caused by optional actions, retries, invalid actions, or tool errors; those events are outcomes/telemetry, not redefinitions of ground-truth depth.

### RECOMMENDED

- Report both graph depth and total required action count for every task specification.
- Use paired tasks with shared seeds/assignments where applicable.

### UNKNOWN

- The minimum number of depth strata and acceptable within-stratum variation.
- Whether parallel prerequisites are allowed in the task formalism; M1 should defer this unless explicitly frozen.

### OUT OF SCOPE

- Generating the benchmark/task corpus, tuning difficulty, or evaluating generalization across task families.

## 7. Budget accounting requirements

### REQUIRED

- Per enrolled episode, account for model requests, combined input+output tokens, tool invocations, wall-clock time, corrective/revision/reflection calls, and estimated/actual cost under the frozen hard caps.
- Planner calls count in the same episode budget. ReAct, planning, retries, repairs, revisions, and observable hidden subcalls are cumulative, not separate allowances.
- Every budget event has start/end timestamps (where applicable), resource type, increment, cumulative total, cap, and source call identifier. Reaching any cap terminates the episode and records the exhausted resource.
- Missing telemetry is explicit (`missing`, reason, scope, and affected episodes). It is never filled with zero; the corresponding normalized claim is blocked until resolved or qualified.
- Failed calls and infrastructure failures retain measured/estimated resource usage; failed batches are not zero-cost.
- Cost telemetry includes model version, input/output token counts, price snapshot, tool/API charges, queue latency, estimated cost, and actual paid cost where available.

### RECOMMENDED

- Maintain a single append-only budget ledger and derive summaries from it.
- Record clock source and monotonic elapsed time separately from wall-clock timestamps.

### UNKNOWN

- Exact treatment of provider-reported versus locally estimated token counts when they disagree.
- Currency conversion and rounding policy for cost summaries.

### OUT OF SCOPE

- Optimizing resource scheduling, parallel execution, procurement, or production billing integration.

## 8. Fairness and reproducibility requirements

### REQUIRED

- Freeze and record model snapshot/endpoint version, prompts and task information, tool registry/schema/permissions, initial state, termination/verifier versions, decoding/sampling settings, max output, seed/replay policy, and all hard caps.
- The only intended treatment difference is the strategy-specific instruction and required explicit plan artifact. No future observations, hidden decomposition, gold failure labels, verifier internals, or unequal tool access may be supplied.
- Use paired task assignment and shared task/seed assignments where applicable; do not exclude test tasks post hoc.
- Hash/version the complete configuration, prompts, model, task specification, schemas, verifier, price snapshot, and environment/reproduction metadata.
- Record development-selection versus frozen evaluation split. Any deviation is a protocol event requiring review.
- Replays must preserve initial state, task information, tool responses or deterministic seeds, decoding settings, and termination/verifier versions sufficiently to reconstruct the trace.

### RECOMMENDED

- Provide a machine-readable manifest plus a human-readable protocol record.
- Run a pre-execution equality audit across strategies.

### UNKNOWN

- Whether the provider can guarantee deterministic replay at the selected endpoint; if not, acceptable stochastic replay policy must be frozen before execution.
- Exact environment fingerprint fields needed for complete replay.

### OUT OF SCOPE

- Framework selection, dependency pinning as an implementation decision, deployment topology, or production reproducibility engineering.

## 9. Trace and telemetry requirements

### REQUIRED

- Retain identifiers and timestamps linking episode, state transitions, plan versions, thoughts/policy events, actions, observations, errors, budget events, verifier result, termination, and infrastructure status.
- Retain the initial task/config manifest, strategy label, model/prompt/tool/verifier/config hashes, seed/replay metadata, and complete terminal accounting.
- Preserve enough trace to audit whether planning was ex ante, whether ReAct adapted to observations, whether an action was invalid/retried/repaired, and why/when termination occurred.
- Mark fields needed for future RQ-004 analysis: first error, proximate cause, terminal symptom, locus, mechanism, unknown/ambiguous status, and annotation provenance. These labels may be absent during M1 execution but the trace must support later blinded annotation.
- Trace serialization must be versioned; dropped, redacted, truncated, or unavailable fields are recorded with reason and scope.

### RECOMMENDED

- Use immutable event identifiers and content hashes for each trace segment.
- Preserve a minimal review subset and a full audit trace with controlled access.

### UNKNOWN

- Retention duration, privacy constraints, and whether raw model outputs can be retained under provider terms.
- Exact schema format and storage medium.

### OUT OF SCOPE

- Production observability dashboards, long-term data lake design, and automated causal diagnosis.

## 10. M1 protocol validity checks

### REQUIRED

Before any execution authorization, the protocol review must test on paper that:

- **Ambiguity:** state, action, observation, plan, termination, error, depth, and success terms have one operational interpretation; unresolved terms remain flagged.
- **Leakage:** strategy prompts, plan requirements, task descriptions, tool schemas, observations, and verifier interfaces do not reveal future observations, gold decomposition, failure labels, or treatment-specific extra information.
- **Unequal information:** both strategies receive the same initial and ongoing observable information and tool access.
- **Unequal inference budget:** all model requests, tokens, tool calls, latency, corrective/revision/reflection calls, and planner calls are counted under identical caps.
- **Verifier disagreement:** success and indeterminate cases have deterministic predeclared handling, with versioned verifier evidence.
- **Missing telemetry:** missing fields are detected, reported, and prevent affected normalized claims; no zero imputation.
- **Framework-induced behavior:** the protocol remains expressible without committing to a framework, and framework defaults cannot silently add planning, memory, retries, parallelism, or hidden calls.
- **ReAct baseline validity:** ReAct remains observation-driven and adaptive, while explicit ex-ante planning is the only intended planning treatment difference.
- **Denominator integrity:** all enrolled episodes remain accounted for, including timeout, invalid action, budget exhaustion, and infrastructure failure.

### RECOMMENDED

- Use a signed checklist with independent R4 review before M1 execution authorization.
- Maintain a decision log for every ambiguity resolved after this review.

### UNKNOWN

- The exact acceptance threshold for a protocol-validity gate and who adjudicates residual disagreements.
- Whether a dry-run of serialization without model/tool execution is required; this may be authorized only if R0 explicitly permits it.

### OUT OF SCOPE

- Running a pilot, model/tool call, benchmark generation, formal comparison, or interpreting planning effects.

## Consolidated blockers and risks

The principal M1 blockers are unresolved operational definitions for the visible Thought record, verifier-indeterminate handling, replay guarantees, dependency-depth strata/parallelism, telemetry disagreement, and trace retention/privacy. These are protocol UNKNOWNs, not architecture decisions. Risks include hidden framework behavior, unequal inference budgets, denominator loss, plan leakage, and inability to distinguish ordinary adaptation from prospective planning or later revision.

## ROLE UPDATE

- **ROLE-LOG-ID:** `ROLE-20260921-R2-001`
- **Role:** R2 — Architecture & Runtime Engineer
- **Date:** 2026-09-21
- **Read canonical inputs:** `PROJECT_MEMORY/01_PROJECT_STATE.md`; `PROJECT_MEMORY/03_RESEARCH_QUESTIONS.md`; `PROJECT_MEMORY/04_ARCHITECTURE.md`; `PROJECT_MEMORY/05_DECISIONS.md`; `PROJECT_MEMORY/07_EXPERIMENTS.md`; `PROJECT_MEMORY/11_MILESTONES.md`; `PROJECT_DOCS/ROLE_DELIVERABLES/R0_M0_PASS_RECHECK_20260921.md`.
- **Completed requirements review:** RQ-001 state, action/observation, ReAct trace, explicit planning artifact, verifier, dependency-depth, budget, fairness/reproducibility, trace/telemetry, and M1 validity requirements, classified as REQUIRED / RECOMMENDED / UNKNOWN / OUT OF SCOPE.
- **New UNKNOWNs and risks:** visible Thought minimum; verifier-indeterminate adjudication; replay determinism/provider guarantees; depth strata and parallel prerequisites; provider/local telemetry disagreement; cost rounding/currency; trace retention/privacy; protocol-validity acceptance threshold; risk of framework-induced hidden behavior and denominator/plan-leakage failures.
- **Impact on RQ-001:** Provides minimum measurement-validity requirements and preserves the frozen claim boundary; no effect or performance claim is made.
- **Impact on RQ-002:** No activation or design authorization; requires RQ-001 protocol PASS plus separate perturbation/recovery gate.
- **Impact on RQ-003:** No activation or budget allocation; reflection remains conditional and must use the same telemetry/budget controls if later authorized.
- **Impact on RQ-004:** Trace fields support future blinded failure analysis; no taxonomy is executed or claimed, and existing κ/α quality gate remains applicable.
- **Architecture Impact:** No architecture, interface, framework, dependency, production runtime, or data model is frozen or approved. This is a research-neutral requirements record only.
- **Experiment Impact:** No benchmark/task generation, pilot, model/tool run, formal comparison, or result is authorized; M1 remains protocol-only measurement-validity work.
- **Need R4 re-review:** **YES.** R4 should review the requirements for consistency with the frozen evaluation contract, denominator, fairness, and M1 validity gate before any later execution authorization.
- **Recommended next step:** R6 archive this role update; R4 perform a bounded protocol-consistency review; R0 decide whether and when to authorize any subsequent non-executing protocol clarification or execution stage.
- **Explicit declaration:** No code, no benchmark generation, no pilot, and no formal experiment were produced or run.
