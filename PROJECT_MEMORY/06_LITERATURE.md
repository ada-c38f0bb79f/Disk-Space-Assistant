# Agent Runtime Research Project — Literature Database

| 字段 | 当前值 |
|---|---|
| Version | v1.1 |
| Updated | 2026-09-21 |
| Primary | R1 — Literature & Theory Scholar |
| Owner of record | R6 |
| Registered papers | 4 evidence entries + R1 M0 evidence map |

> 本文件区分论文直接支持的内容、R1 的解释以及项目假设。登记论文不等于完成 novelty review，也不构成实验结果或项目 Finding。

## 1. Literature Index

| PAPER-ID | Title | Year/Venue | Priority | Reading status | Related RQs |
|---|---|---|---|---|---|
| PAPER-001 | ReAct: Synergizing Reasoning and Acting in Language Models | 2023 / ICLR | MUST READ | STANDARD READ COMPLETE；核心章节已重建；FULL DEEP READ PENDING | RQ-001、RQ-002 |

## 2. PAPER-001 — ReAct

**Title:** ReAct: Synergizing Reasoning and Acting in Language Models  
**Authors:** Yao et al.  
**Year:** 2023  
**Venue:** ICLR 2023  
**Link:** [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)  
**Topic:** Reasoning–acting interaction；tool/environment feedback；agent baseline  
**Reading Priority:** MUST READ  
**Reading Status:** STANDARD READ COMPLETE；CORE-SECTIONS RECONSTRUCTED；FULL DEEP READ NOT YET COMPLETE  

### PAPER EVIDENCE recorded from R1

- ReAct 以交错的 Thought / Action / Observation 形成在线闭环。
- 论文覆盖 knowledge-intensive reasoning 与 decision-making domains。
- 核心比较与分析涉及 Standard prompting、CoT、CoT-SC、Act-only、ReAct，以及 component/behavior ablations。
- ReAct 行为包括 observation-driven adaptation，并体现隐式 online/local planning。
- 论文讨论 dense/sparse Thought、hybrid routing、failure cases 与 prompt sensitivity。

### R1 Interpretation

- ReAct 不能作为“无 planning”baseline；它已有隐式、局部、在线的 planning/adaptation。
- RQ-001 更准确的对比应是 **explicit ex-ante planning vs ReAct**。
- RQ-002 必须区分普通 observation-driven adaptation、retry/repair 与显式 dynamic replanning。
- ReAct vs Act-style component ablation 对理解 reasoning component 的作用有价值。

### Project Relevance

**Which RQ:** RQ-001、RQ-002  
**Which Module:** 暂不映射架构模块；M0 no-architecture gate 仍有效。  
**Implementation Worthwhile?:** NOT YET DECIDED。ReAct 是候选 baseline，但实现需等 M0 PASS 与架构要求。  
**Novelty Impact:** PARTIAL / UNKNOWN。该阅读修正了 baseline 定义，但尚未完成 RQ-level novelty judgement。  

### Experiment Implications — not yet approved

- 控制 prompt demonstrations、tool access、inference budget 与 prompt sensitivity。
- 不将 best-of-N prompt 结果当作稳定单次性能。
- 不将小规模人工 failure sample 中的 0% 外推为总体零发生率。
- 保留能区分 ReAct 与 Act-only 的 component comparison。

### Remaining Work

- 完成 full deep read 所需的剩余细节与完整 paper note fields。
- 将 ReAct 放入 RQ-001/RQ-002 的 broader literature comparison。
- 不基于单篇论文给出 ACCEPT / REJECT novelty verdict。

## 3. Reading Queue

| Order | Paper/topic | Mode | Purpose | Status |
|---|---|---|---|---|
| 1 | ReAct | STANDARD READ → later DEEP READ | 建立可公平比较的 adaptive reasoning/acting baseline | STANDARD COMPLETE |
| 2 | ADAPT | SCOUT READ | 理解 failure-triggered recursive decomposition、`d_max`、ReAct/static-plan/retry baselines 与 inference-budget fairness | NEXT |

ADAPT 的完整 bibliographic metadata 与 PAPER-ID 等待 SCOUT READ 输入后登记，当前不猜测补齐。

## 4. Literature Review Status

- **RQ-001:** R1 disposition NARROW；最终由 R0 冻结为 ACTIVE CORE。
- **RQ-002:** R1 disposition MERGE → RQ-001；最终由 R0 冻结为 GATED SUBPROBLEM。
- **RQ-003:** R1 disposition NARROW；最终由 R0 冻结为 CONDITIONAL P1。
- **RQ-004:** R1 disposition MERGE → analysis layer；最终由 R0 冻结为 ANALYSIS LAYER。
- **M0 R1 handoff:** COMPLETE — [`R1_M0_LITERATURE_NOVELTY_REVIEW.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R1_M0_LITERATURE_NOVELTY_REVIEW.md)。

## 5. Evidence Boundary

- **PAPER EVIDENCE:** 仅限论文所报告的方法、设置、结果与分析。
- **INTERPRETATION:** R1 对 baseline 定义和项目含义的判断。
- **EXPERIMENT RESULT:** NONE。
- **PROJECT FINDING:** NONE。

## 6. R1 Supplemental Literature Update — 2026-09-21

Source: [`R1_M0_ADDITIONAL_LITERATURE_UPDATE_20260921.md`](../PROJECT_DOCS/ROLE_DELIVERABLES/R1_M0_ADDITIONAL_LITERATURE_UPDATE_20260921.md)  
Status: **SUPPLEMENTARY PAPER EVIDENCE; does not alter DEC-20260921-R0-M0-001**

### PAPER-002 — ADaPT

- [Prasad et al., ADaPT: As-Needed Decomposition and Planning with Language Models](https://aclanthology.org/2024.findings-naacl.264/)
- Executor-first；仅在 executor 无法完成当前 task/subtask 时调用 planner。
- 更准确地描述为 failure-triggered recursive decomposition，而非 full global replanning。
- 与 RQ-001/RQ-002 的 collision warning：必须控制 task complexity、failure trigger 与 inference budget。

### PAPER-003 — Reflexion

- [Shinn et al., Reflexion: Language Agents with Verbal Reinforcement Learning](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
- 将 evaluator/environment feedback 转为 verbal feedback，并保存为 later trials 的 context，不更新 model parameters。
- 与 RQ-003 的 boundary：Reflexion 涉及 evaluator feedback、additional trials 与 episodic memory；当前 RQ-003 仍限制为 same-episode、trace-grounded、non-oracle selective reflection。

### PAPER-004 — Plan-and-Solve Prompting

- [Wang et al., Plan-and-Solve Prompting](https://aclanthology.org/2023.acl-long.147/)
- 先形成 textual reasoning plan，再执行 subtasks。
- 可作为 explicit/static ex-ante plan 的 literature reference，但不自动等同于本项目 runtime treatment。

### Consolidated Boundary

当前 defensible comparison 不是 planning vs no planning，而是：

> explicit ex-ante planning/decomposition vs ReAct implicit online planning，在 controlled information、tool access 与 inference budget 下的边界。

该补充材料强化 RQ-001 ACTIVE CORE、RQ-002 GATED、RQ-003 CONDITIONAL P1、RQ-004 ANALYSIS LAYER 的既有决议；没有新增 RQ、Finding、实现授权或实验授权。
