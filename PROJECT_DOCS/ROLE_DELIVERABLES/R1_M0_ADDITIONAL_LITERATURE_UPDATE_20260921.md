# R1 Literature Learning Update — ReAct, ADaPT, Reflexion, Plan-and-Solve

**Role:** R1 — Literature & Theory Scholar  
**Date:** 2026-09-21  
**Purpose:** Supplementary learning update for R6 archive; consolidates the four papers discussed after the original M0/P0-1 review.  
**Status:** ROLE UPDATE — literature evidence and interpretation only; no architecture or implementation authorization.

## 1. PAPER EVIDENCE

### PAPER-001 — ReAct

- [Yao et al., ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- ReAct interleaves Thought, Action, and Observation.
- Observations can update subsequent decisions, so ReAct already contains implicit online/local planning and adaptation.
- ReAct must not be represented as a “no-planning” or “no-recovery” straw baseline.

### PAPER-002 — ADaPT

- [Prasad et al., ADaPT: As-Needed Decomposition and Planning with Language Models](https://aclanthology.org/2024.findings-naacl.264/)
- ADaPT uses an executor first and calls a planner only when the executor cannot complete the current task/subtask.
- The planner recursively decomposes the failed subtask; successful subtasks allow execution to resume at the parent task.
- The paper defines planning colloquially as designing a list of subtasks, not as classical AI planning.
- ADaPT is best characterized as failure-triggered recursive decomposition, not full global replanning.
- It compares against ReAct, plan-and-execute, retry-style methods, and Reflexion on ALFWorld, WebShop, and TextCraft.

### PAPER-003 — Reflexion

- [Shinn et al., Reflexion: Language Agents with Verbal Reinforcement Learning](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
- Reflexion converts evaluator/environment feedback into verbal feedback and stores it as context for later trials without updating model parameters.
- The mechanism couples Actor, Evaluator, Self-Reflection, and memory.
- Its main setting is cross-trial improvement; it is not equivalent to same-episode, trace-grounded reflection.
- Reflection quality depends on evaluator quality, feedback observability, memory use, and additional trials.

### PAPER-004 — Plan-and-Solve Prompting

- [Wang et al., Plan-and-Solve Prompting](https://aclanthology.org/2023.acl-long.147/)
- Plan-and-Solve first devises a textual reasoning plan and then carries out the subtasks.
- PS targets missing-step errors; PS+ adds variable extraction and intermediate calculation instructions.
- Results are on static reasoning datasets, not tool-interacting environments.
- This is evidence for static explicit reasoning plans, not direct evidence that runtime action planning improves tool-task completion.

## 2. INTERPRETATION

The four papers distinguish four mechanisms:

| Mechanism | Primary intervention |
|---|---|
| Plan-and-Solve | static, ex-ante textual reasoning plan |
| ReAct | implicit online Thought–Action–Observation loop |
| ADaPT | failure-triggered local recursive task decomposition |
| Reflexion | verbal feedback and memory across later trials |

The main conceptual boundary is not “planning versus no planning.” ReAct already performs implicit planning. The defensible comparison is explicit ex-ante planning or decomposition versus ReAct’s implicit online planning, under controlled information and inference budget.

ADaPT, retry, repair, replanning, and reflection must remain distinct:

- Retry repeats the same task at the same granularity.
- ADaPT changes task granularity by decomposing the failed subtask.
- Replanning modifies the unexecuted plan after new evidence invalidates its assumptions.
- Reflection is a separate meta-level inference over trace/feedback that produces corrective guidance.

## 3. RQ DISPOSITION AND NOVELTY WARNING

### RQ-001 — Planning value boundary

**Disposition:** NARROW.

Existing papers establish several planning variants, but no paper here establishes a general boundary across dependency depth, model capability, uncertainty, and budget. The original question is too broad and risks conflating prompt-level reasoning plans with runtime action plans.

**Recommended wording:** Compare explicit ex-ante subgoal planning against ReAct implicit online planning on a controlled task family, with dependency depth as the first primary task factor.

**Novelty warning:** “Planning helps complex tasks” is not novel; ADaPT is a direct collision. Potential contribution must come from controlled interaction boundaries, negative effects, resource-normalized comparisons, or reproducible heterogeneity.

### RQ-002 — Dynamic replanning and recovery

**Disposition:** MERGE into RQ-001 as a dynamic perturbation/recovery subproblem.

ReAct already adapts to observations, and ADaPT already handles executor-level failure via recursive decomposition. Tool failure, stale plans, incomplete observations, and environmental change should not be collapsed into one treatment.

**Novelty warning:** Calling retry, parameter repair, or ordinary next-action selection “replanning” would create nominal rather than substantive novelty.

### RQ-003 — Reflection policy

**Disposition:** NARROW.

Reflexion establishes a strong precedent for verbal feedback, but it binds reflection to evaluator feedback, additional trials, and episodic memory. A more distinct question is same-episode, trace-grounded, non-oracle selective reflection versus no reflection, always reflection, and budget-matched extra attempts.

**Novelty warning:** “Selective” and “trace-grounded” alone do not establish novelty. Trigger, diagnosis, correction, oracle access, and added compute must be separated.

### RQ-004 — Explanatory failure model

**Disposition:** MERGE as an analysis layer, not an independent core treatment.

The four papers already expose missing-step, calculation, semantic, executor-complexity, repeated-strategy, and misdiagnosis failures. A new taxonomy alone is unlikely to be novel. The useful contribution is a pre-registered trace analysis that distinguishes model/policy, runtime, tool/environment, and harness failures and tests reviewer reliability and predictive value.

**Novelty warning:** Trace association is not causal explanation. A post-hoc taxonomy must not be presented as a causal mechanism without intervention or a clearly limited descriptive claim.

## 4. TERM CLARIFICATIONS FOR R6 ARCHIVE

These are project proposals, not claims of a universal academic definition.

- **Planning:** Before the first covered external action, generate a recordable prospective artifact containing at least two future subgoals/action units with order or dependency, and make that artifact available to execution.
- **Replanning:** After an external action/observation, explicitly modify, replace, or reorder the unexecuted plan because new evidence invalidates an assumption or expected progress. Require an auditable `old plan → trigger evidence → new plan` record.
- **Reflection:** A separate meta-level inference that reads specified trace evidence/feedback and emits diagnosis or corrective guidance that is used by a subsequent action or attempt.
- **Recovery:** Success after a declared recoverable perturbation, reported both end-to-end over all injected recoverable cases and conditionally over detected cases.
- **ReAct baseline:** Same model/tool/task information and controls, using an interleaved Thought–Action–Observation loop but no independent ex-ante plan artifact, planner call, explicit replan event, reflection pass, or cross-episode reflective memory.

## 5. HYPOTHESIS AND IDEA BOUNDARY

**HYPOTHESIS:** Explicit planning may help when dependency depth exceeds the executor’s reliable local composition ability, but may hurt when assumptions become stale or when its extra inference budget is not justified.

**HYPOTHESIS:** Selective reflection may have positive net value only when failure detection and diagnosis are sufficiently reliable; otherwise reflection can add false interventions or reinforce an incorrect explanation.

**IDEA:** Different failure loci may require different interventions: task-complexity failures may benefit from decomposition, strategy-repetition failures from reflection, and environment/tool-state failures from explicit replanning. This is not an approved architecture or experiment.

## 6. R6 HANDOFF

**ROLE-LOG-ID:** ROLE-20260921-R1-003  
**Role:** R1 — Literature & Theory Scholar  
**Task:** Supplementary literature learning update after ReAct, ADaPT, Reflexion, and Plan-and-Solve reading.  
**What Was Done:** Consolidated PAPER EVIDENCE, interpretations, terminology boundaries, RQ dispositions, and novelty warnings.  
**What Changed:** No canonical project state changed. This update reinforces the existing M0 recommendation: RQ-001 NARROW; RQ-002 MERGE; RQ-003 NARROW; RQ-004 analysis layer.  
**Architecture Impact:** NONE.  
**Experiment Impact:** None authorized; only fairness and trace requirements were clarified.  
**Recommended Next Step:** R6 archive this update and link it from the literature/role records; R0 may use it as supplementary evidence for the already recorded M0 freeze.  
**Need Handoff:** YES — R6 for archive; NO new implementation or experiment authority.
