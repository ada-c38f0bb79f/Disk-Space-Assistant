# Agent Runtime Research Project — Project Initialization

Status: **PROPOSED BY R0 — awaiting R1/R4 review and R6 registration**  
Authority: R0 Project Director / Principal Investigator  
Date: 2026-09-03  
Current phase: Phase 0 — Project Initialization  
Current milestone: M0 — Research Charter Freeze

---

## 1. Research Identity

This project studies **when and why runtime-level agent strategies improve or harm reliable tool-using task completion under controlled conditions**.

The primary object of study is not a framework or feature collection. It is the causal relationship among:

- runtime strategy (ReAct, planning, replanning, reflection, later memory);
- task/environment conditions (dependency depth, uncertainty, tool failure, environmental change, horizon);
- model capability;
- measurable outcomes (success, recovery, efficiency, and trace-level failure modes).

The first 3 months focus on a minimal, observable single-agent runtime and controlled comparisons. The 6-month path may extend to memory only after the core benchmark and causal evaluation methodology are credible.

### Working thesis

**HYPOTHESIS:** More agent machinery is not uniformly better. Planning, replanning, and reflection are expected to help only under identifiable task and failure conditions, and may reduce reliability or efficiency elsewhere.

This is a hypothesis, not a finding.

---

## 2. Scope

### IN SCOPE — first 3 months

1. A minimal single-agent runtime sufficient to compare strategies fairly.
2. Explicit agent state, action, observation, termination, error, and trace semantics.
3. Tool use from single-tool tasks through dependent multi-tool tasks.
4. ReAct as the primary simple-agent baseline.
5. Static planning and plan-and-execute.
6. Dynamic replanning under tool failure, stale plans, and environmental change.
7. No reflection, always-reflect, and selective/trace-grounded reflection comparisons.
8. Controlled benchmark tasks with explicit ground truth and difficulty strata.
9. Model × architecture comparisons that separate model capability from runtime effects.
10. Failure taxonomy, root-cause analysis, robustness tests, ablations, cost, latency, and reproducibility.
11. Open-source-quality documentation and a technical research report.

### CONDITIONAL IN SCOPE — months 4–6 only after M3

1. Memory as a controlled experimental variable, beginning with short/episodic runtime memory.
2. Broader model families and harder/longer-horizon tasks.
3. Generalization tests on a second task family or benchmark.
4. A potential preprint if results support defensible claims.

Entry requires evidence that the addition directly serves an active RQ and will not invalidate the core experimental schedule.

### OUT OF SCOPE for the current roadmap

1. Multi-agent systems.
2. Browser, GUI, computer-use, or multimodal agents.
3. RAG systems, knowledge graphs, and general-purpose knowledge assistants.
4. Reinforcement learning or model fine-tuning.
5. Distributed execution, production orchestration, and enterprise platform features.
6. A general replacement for LangChain, LangGraph, or other frameworks.
7. Building many integrations, tools, or polished product features.
8. Claiming novelty before literature and experimental review.

### BACKLOG

- Multi-agent coordination and communication failures.
- Browser/computer-use environments.
- Long-term memory and memory consolidation.
- Learned planning, routing, or reflection policies.
- Human-in-the-loop agents.
- Security and adversarial tool-use research beyond basic robustness.
- Multimodal tasks.

Backlog items require R0 Idea Evaluation before promotion.

---

## 3. Candidate Core Research Questions

The project starts with four candidate RQs. They become active only after R1 novelty review and R4 measurability review.

### RQ-001 — Planning value boundary

Under controlled model capability and tool access, **under which task conditions does explicit planning outperform a simple ReAct loop, and under which conditions does it hurt success or efficiency?**

- Primary independent variables: runtime strategy; task dependency depth; horizon; uncertainty.
- Primary outcomes: task success, partial success, steps, tool calls, tokens, latency, cost, failure distribution.
- Falsification condition for the working hypothesis: no stable interaction between planning and task conditions across adequate repetitions, or observed differences are explained by prompt/implementation inequity.

### RQ-002 — Dynamic replanning and recovery

When an initial plan becomes invalid because of tool failure, incomplete observations, or environmental change, **when does dynamic replanning improve recovery over static planning and ReAct, and what does it cost?**

- Primary independent variables: replanning availability/trigger; failure type; failure timing; recoverability.
- Primary outcomes: recovery rate, final success, repeated-error rate, excess steps, latency, tokens, cost.
- Falsification condition: replanning offers no robust recovery improvement over fair baselines, or gains disappear after controlling for additional inference budget.

### RQ-003 — Reflection policy

Can **selective, trace-grounded reflection** reduce repeated agent failures more effectively than no reflection or unconditional reflection without unacceptable cost or new failure modes?

- Primary independent variables: no reflection; always reflect; selective reflection trigger; evidence available to reflection.
- Primary outcomes: corrected-failure rate, repeated-mistake rate, false-intervention rate, success, steps, tokens, latency, cost.
- Falsification condition: selective reflection does not outperform one or both fair baselines, or its benefits do not exceed its added errors and budget.

### RQ-004 — Explanatory failure model

Which trace-observable failure modes explain performance differences across **runtime strategy × model capability × task difficulty**, and which failures are detectable and recoverable at runtime?

- Primary variables: failure category, severity, detectability, recoverability, runtime strategy, model, task stratum.
- Primary outcomes: failure frequency and transition patterns; contribution to task failure; detection precision/recall where labels permit.
- Falsification condition: the proposed taxonomy has poor inter-reviewer consistency, low trace coverage, or little explanatory/predictive value beyond aggregate success rate.

### RQ dependency

RQ-001 establishes the planning boundary. RQ-002 studies recovery when plans or execution fail. RQ-003 tests a targeted correction mechanism. RQ-004 provides the explanatory layer used across all three.

### Not yet an active RQ

Memory is deliberately excluded from the initial core RQs. It may become RQ-005 after M3 only if observed cross-episode or long-horizon failures show that memory is necessary and experimentally separable.

---

## 4. Minimum 3-Month Roadmap

### Month 1 — Foundations and valid baseline

Goal: freeze the research contract and establish a minimal, fair, reproducible baseline study.

- Week 1: Project Initialization and M0 charter freeze.
- Week 2: theory/literature map, operational definitions, benchmark requirements, and architecture requirements; still no implementation until reviews pass.
- Week 3: minimal runtime and trace design, benchmark v0 task specification, experiment protocol.
- Week 4: baseline implementation/validation and pilot runs for ReAct and controlled non-agent/tool-use references where appropriate.

Gate: M1 — Baseline and Measurement Validity.

### Month 2 — Planning and replanning

Goal: answer the first defensible part of RQ-001 and establish RQ-002 experiments.

- Weeks 5–6: static planning vs ReAct on stratified tasks.
- Week 7: tool failure and stale-plan scenarios; dynamic replanning pilot.
- Week 8: replicated comparison, ablation, failure analysis, and interim interpretation.

Gate: M2 — Planning/Replanning Evidence.

### Month 3 — Reflection and synthesis

Goal: evaluate reflection policies and form the first integrated research conclusions.

- Weeks 9–10: no/always/selective reflection experiments.
- Week 11: model × architecture checks, robustness tests, trace-level root-cause analysis.
- Week 12: replication, claim audit, technical report v1, and 3-month milestone review.

Gate: M3 — Core Research Package.

---

## 5. Full 6-Month Roadmap

The first 12 weeks remain identical to the minimum path.

### Month 4 — Evidence-driven memory extension

Proceed only if M3 evidence supports a memory-related failure hypothesis.

- Define a narrow memory RQ and fair no-memory baseline.
- Compare memory under relevant long-horizon or repeated-task conditions.
- Measure retrieval relevance, staleness, pollution, over-reliance, success, and cost.

Gate: M4 — Memory Decision. Outcome may be a validated negative result or a decision not to add memory.

### Month 5 — Generalization and reliability

- Test the strongest and weakest observed effects on a second task family or benchmark.
- Expand model × architecture comparisons.
- Conduct adversarial tool, observation, timeout, and environmental-change tests.
- Re-run critical experiments and audit statistical reliability.

Gate: M5 — Generalization and Reliability.

### Month 6 — Consolidation and communication

- Freeze benchmark, runtime, experiment records, findings, and limitations.
- Reproduce headline results from a clean environment.
- Complete failure database and negative-result record.
- Publish an open-source-quality repository and technical report.
- Decide whether evidence warrants a preprint.
- Produce project narrative, interview bank, and mock-interview review.

Gate: M6 — Research and Engineering Release.

---

## 6. Milestones and Exit Criteria

No milestone passes because code exists. Each gate requires evidence across understanding, implementation, tests, evaluation, documentation, and failure analysis where applicable.

### M0 — Research Charter Freeze (target: end of Week 1)

- Understanding: one-sentence research identity is precise and teachable.
- Research: 2–5 RQs are literature-aware, measurable, and falsifiable.
- Scope: IN/OUT/BACKLOG boundaries are recorded.
- Evaluation: primary outcomes, controls, and major validity risks are defined.
- Operations: all shared-memory files exist with owners/status conventions.
- Decision: R0 records accepted RQs and the single Month 1 objective.

PASS requires R1, R4, and R6 handoff deliverables. No code is required or permitted for M0.

### M1 — Baseline and Measurement Validity (target: end of Week 4)

- Understanding: baseline behavior and expected failure modes can be explained.
- Implementation: minimum runtime and trace path operate without framework-dictated research logic.
- Tests: state transitions, tools, termination, errors, and trace serialization are covered.
- Evaluation: benchmark v0 and baseline protocol pass ambiguity/leakage/fairness checks.
- Documentation: architecture, task schemas, configs, and reproduction steps are current.
- Failure analysis: pilot failures are classified and engineering bugs separated from agent failures.

### M2 — Planning/Replanning Evidence (target: end of Week 8)

- Understanding: observed boundaries and mechanisms have explicit alternative explanations.
- Implementation: planning and replanning are isolated, configurable interventions.
- Tests: planner/executor boundaries and recovery paths are covered.
- Evaluation: pre-registered comparisons include repetitions, variance, cost, and ablations.
- Documentation: experiment records and decisions are complete.
- Failure analysis: planning-specific failure modes and recovery failures are trace-linked.

### M3 — Core Research Package (target: end of Week 12)

- Understanding: provisional answers to RQ-001–RQ-004 are evidence-calibrated.
- Implementation: ReAct/planning/replanning/reflection variants are reproducible.
- Tests: critical paths and known regressions are covered.
- Evaluation: core experiments are replicated; model and inference-budget confounds are assessed.
- Documentation: report v1, findings, limitations, and negative results are reviewable.
- Failure analysis: aggregate scores are accompanied by root-cause distributions and examples.

### M4 — Memory Decision (target: end of Week 16)

- A narrow memory hypothesis is tested or rejected as unnecessary.
- Any memory claim has a fair no-memory baseline and retrieval-quality analysis.
- Memory failures and added costs are documented.

### M5 — Generalization and Reliability (target: end of Week 20)

- Core effects are tested beyond the development setting.
- Robustness and model × architecture results are replicated.
- Remaining claims survive a validity and failure-analysis audit.

### M6 — Research and Engineering Release (target: end of Week 24)

- A clean reproduction of headline results succeeds.
- Every claim links to an experiment; every limitation is explicit.
- Repository, report, benchmark, experiment metadata, and failure records are coherent.
- Preprint decision is evidence-based; presentation does not overclaim.
- Project can be explained and defended in an expert interview.

Milestones are graded PASS / PARTIAL / FAIL by R0.

---

## 7. Week 1 P0

Week 1 has three ordered P0 deliverables and a strict no-code gate.

### P0-1 — Research Contract Review

Owner: R0  
Required reviewers: R1 and R4

Deliverable:

- review the four candidate RQs;
- narrow, merge, or reject them if needed;
- define key terms: planning, replanning, reflection, recovery, task success, fair baseline;
- state initial claims we are allowed and not allowed to make;
- freeze Research Identity v1 and active RQs.

Done when: R1 novelty/literature review and R4 measurability/validity review are resolved by R0 in a recorded decision.

### P0-2 — Evaluation Contract v0

Owner: R4  
Inputs: accepted RQs and R1 evidence map

Deliverable:

- benchmark requirements and difficulty strata, not benchmark implementation;
- baseline matrix and control variables;
- primary/secondary metrics;
- minimum repetition/statistical plan assumptions;
- confounds, leakage, ambiguity, and falsification checks;
- rough cost envelope.

Done when: each active RQ has a feasible experiment shape and explicit falsification condition.

### P0-3 — Shared Project Memory Initialization

Owner: R6  
Input: this initialization and all review outputs

Deliverable:

- create and initialize the 14 Constitution-defined shared-memory files;
- register Phase 0, M0, candidate/accepted RQs, scope, roadmap, milestones, backlog, decisions, and role activity;
- distinguish VERIFIED, UNKNOWN, HYPOTHESIS, IDEA, and DECISION;
- mark unresolved reviewer items rather than guessing.

Done when: a new role can read shared memory and accurately state the phase, milestone, active RQs, P0, risks, and next action.

### Week 1 stop conditions

Do not start architecture or implementation if any of the following remains unresolved:

- no measurable primary RQ;
- no fair baseline definition;
- no falsification condition;
- no shared source of truth;
- scope includes unsupported feature additions.

---

## 8. Initial Priority Register

### P0

1. Research Contract Review.
2. Evaluation Contract v0.
3. Shared Project Memory Initialization.

### P1

- R1 prioritized literature map and must-read sequence.
- R2 minimum architecture requirements, only after M0 PASS.
- Initial risk register and terminology glossary.

### P2

- Repository/public narrative planning.
- Interview-bank seed questions.
- Preprint venue exploration.

### BACKLOG

All items listed in the Scope backlog, plus any new feature without a direct active-RQ link.

---

## 9. Initial Risks

1. **Scope dilution:** too many agent capabilities obscure causal claims.
2. **Architecture–model confounding:** stronger models may be mistaken for better runtime design.
3. **Unequal inference budget:** advanced strategies may win only by using more calls/tokens.
4. **Benchmark bias:** tasks may implicitly favor the designed architecture.
5. **Framework leakage:** framework behavior may determine results instead of our research design.
6. **Trace insufficiency:** aggregate success without usable traces prevents causal failure analysis.
7. **Premature novelty:** candidate ideas may already be known or not substantively different.
8. **Learning displacement:** AI may produce artifacts the user cannot explain or defend.

---

## 10. R0 Decision Gate

Current decision: **Proceed with Phase 0 only.**

Authorization granted:

- literature/theory review;
- experiment and benchmark design on paper;
- project memory initialization;
- terminology and decision clarification.

Not yet authorized:

- implementation;
- architecture freeze;
- dependency/framework selection;
- benchmark task generation at scale;
- adding memory, multi-agent, RAG, browser, GUI, multimodal, or RL workstreams.

The next R0 decision occurs after R1, R4, and R6 handoffs are returned.

