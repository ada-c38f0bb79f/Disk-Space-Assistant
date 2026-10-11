# Agent Runtime Research Project — Master Checklist

| 字段 | 当前值 |
|---|---|
| Version | v1.1 |
| Updated | 2026-09-21 |
| Owner | R6 |
| Current phase | Phase 1 — Gate A Protocol Minimum |
| Current gate | M0 — PASS; Gate A in progress |

## Status Legend

- `[x]` DONE — 有可定位证据。
- `[>]` IN PROGRESS — 已开始但未满足完成条件。
- `[ ]` PENDING — 尚未开始或没有证据。
- `[!]` BLOCKED — 明确依赖尚未满足。
- `[~]` CONDITIONAL / DEFERRED — 尚未获准进入当前路线。

## 1. Current P0 — Week 1

### P0-1 — Research Contract Review

- `[x]` R0 提交 Project Initialization v0.1。Evidence: [`00_PROJECT_INITIALIZATION.md`](../PROJECT_DOCS/INITIALIZATION/00_PROJECT_INITIALIZATION.md)
- `[x]` R1 完成 RQ-001–RQ-004 literature/novelty review。Evidence: `R1_M0_LITERATURE_NOVELTY_REVIEW.md`。
- `[x]` R0 完成 refactor feasibility review，并提出 `TEST FIRST`；该项不等于 architecture freeze。
- `[x]` R4 完成 measurability/validity review；交付 `R4_M0_EVALUATION_CONTRACT_V0.md`。
- `[x]` R4 完成 RQ-001–RQ-004 measurability/validity review；结果为 NARROW / MERGE proposals，尚待 R0 决议。
- `[x]` R4 完成 freeze-support memo；建议三个月只冻结 RQ-001，RQ-002 gated、RQ-003 conditional P1、RQ-004 analysis layer。
- `[x]` 冻结 `planning`、`replanning`、`reflection`、`recovery`、`task success` 与 `fair baseline` 操作定义。
- `[x]` 记录允许/不允许提出的初始 claims。
- `[x]` R0 决议 Research Identity v1 与 RQ dispositions；见 `DEC-20260921-R0-M0-001`。
- `[x]` R0 完成 M0 PASS recheck；确认 R6 registration 未改变 final decision。

**Done condition:** R1/R4/R0 Research Contract work 已完成，且 R0 完成 registration consistency recheck。

### P0-2 — Evaluation Contract v0

- `[x]` 确定 benchmark requirements 与 difficulty strata。
- `[x]` 建立 baseline matrix 与 control variables。
- `[x]` 定义 primary/secondary metrics、repetitions 与统计计划最小假设。
- `[x]` 定义 confounds、leakage、ambiguity 与 falsification checks。
- `[x]` 建立 rough cost envelope、MCID 与 equivalence/non-inferiority margins。
- `[x]` 为 RQ-001 建立正式 measurement-validity 形状与 falsification condition；RQ-002/003 仍受 gate/conditional 状态约束。

**Done condition:** R0 已冻结 active RQ、MCID/等效性界限、预算与 M1 objective；R6 已登记。

### P0-3 — Shared Project Memory Initialization

- `[x]` `01_PROJECT_STATE.md`
- `[x]` `02_MASTER_CHECKLIST.md`
- `[x]` `03_RESEARCH_QUESTIONS.md`
- `[x]` `04_ARCHITECTURE.md`
- `[x]` `05_DECISIONS.md`
- `[x]` `06_LITERATURE.md`
- `[x]` `07_EXPERIMENTS.md`
- `[x]` `08_FAILURES.md`
- `[x]` `09_ROLE_LOG.md`
- `[x]` `10_BACKLOG.md`
- `[x]` `11_MILESTONES.md`
- `[x]` `12_INTERVIEW_BANK.md`
- `[x]` `13_TECHNICAL_DEBT.md`
- `[x]` `14_FINDINGS.md`
- `[x]` 登记 Phase 0 与 M0。
- `[x]` 登记 candidate RQs、scope、roadmap、milestones 与 backlog。
- `[x]` 区分 FACT / DECISION / PROPOSED DECISION / HYPOTHESIS / UNKNOWN。
- `[x]` 登记 role activity；包含 R0 final decision、R4 reviews 与 R6 archival entries。

**Progress:** 14/14 shared-memory files created。P0-3 COMPLETE。

## 2. M0 — Research Charter Freeze

- `[x]` Research Identity v1 精确且可教学；已由 R0 冻结。
- `[x]` RQ dispositions 已由 R0 冻结：RQ-001 active；RQ-002 gated；RQ-003 conditional P1；RQ-004 analysis layer。
- `[x]` IN / CONDITIONAL / OUT / BACKLOG 边界已登记。
- `[x]` outcomes、controls、validity risks、MCID、budget、cost、fairness 与 M1 objective 已由 R0 冻结。
- `[x]` Shared-memory owners/status conventions 已建立；14/14 文件存在。
- `[x]` R0 已记录 M1 single objective。
- `[x]` No-code gate 已登记。

**Gate status:** PASS。Research Contract 与 operational registration 已完成；M1 仅允许 protocol-only requirements review。仍不得开始 implementation、benchmark generation、pilot 或 architecture freeze。

## 3. M1 — Baseline and Measurement Validity

- `[>]` **Current P0:** Gate A — 将 R4/R2 requirements 压缩为最小可执行协议，服务后续最小闭环。
- `[x]` R2 completed the requirements-only review covering state, action/observation, ReAct trace, explicit plan, verifier, depth, budget/cost, fairness/reproducibility, telemetry, and validity checks。
- `[!]` R4 re-review is required before any later execution authorization。
- `[!]` **Authorization boundary:** 当前只允许最小协议收敛；Gate B 之前代码、benchmark、pilot、正式 comparison 与 architecture freeze 均禁止。
- `[ ]` 可解释 baseline behavior 与预期 failure modes。
- `[ ]` 最小 runtime 与 trace path 可运行。
- `[ ]` 覆盖 state transition、tools、termination、errors、trace serialization 测试。
- `[ ]` Benchmark v0 与 baseline protocol 通过 ambiguity/leakage/fairness checks。
- `[ ]` Architecture、task schema、config 与 reproduction 文档完成。
- `[ ]` Pilot failures 已分类，engineering bug 与 agent failure 已分离。

### Execution focus adjustment

- `[x]` R0 已决定把近期重点从扩写设计文档转为最小可运行闭环准备。
- `[>]` Gate A：最小协议、verifier、trace、budget ledger、fairness checklist。
- `[!]` Gate B：最小 runnable loop；等待 R0 单独实现授权。
- `[~]` Gate C：measurement sanity；Gate B 后再进入。
- `[~]` Gate D：RQ-001 protocol pilot decision；Gate C 后再进入。

### Gate A / B / C / D

- `[>]` **Gate A — Minimum protocol convergence:** one-page executable protocol covering treatment boundary, verifier, minimal trace, budget ledger, fairness checklist, and R4/R0 semantic decisions。
- `[!]` **Gate B — Minimal runnable loop:** requires separate R0 implementation authorization; no code is currently authorized。
- `[~]` **Gate C — Measurement sanity:** only after Gate B authorization and completion。
- `[~]` **Gate D — RQ-001 pilot decision:** only after Gate C review; not pilot authorization。

## 4. M2 — Planning/Replanning Evidence

- `[ ]` 明确 observed boundary、mechanism 与 alternative explanations。
- `[ ]` Planning/replanning 是隔离、可配置的 intervention。
- `[ ]` Planner/executor boundary 与 recovery path 有测试。
- `[ ]` 比较协议包含 repetitions、variance、cost、ablation。
- `[ ]` Experiment 与 decision records 完整。
- `[ ]` Planning-specific failures 与 recovery failures 可 trace-link。

## 5. M3 — Core Research Package

- `[ ]` RQ-001–RQ-004 有 evidence-calibrated provisional answers。
- `[ ]` ReAct/planning/replanning/reflection variants 可复现。
- `[ ]` Critical paths 与 known regressions 有测试。
- `[ ]` Core experiments 已复现并控制 model/inference-budget confounds。
- `[ ]` Report v1、findings、limitations、negative results 可审查。
- `[ ]` Aggregate metrics 配有 root-cause distributions 与 trace examples。

## 6. Conditional Months 4–6

### M4 — Memory Decision

- `[~]` 由 M3 证据触发 narrow memory hypothesis，或明确决定不加入 memory。
- `[~]` 建立 fair no-memory baseline 与 retrieval-quality analysis。
- `[~]` 登记 memory failures 与 added cost。

### M5 — Generalization and Reliability

- `[~]` 在第二任务族/benchmark 测试核心效应。
- `[~]` 复现 robustness 与 model × architecture 结果。
- `[~]` Claims 通过 validity/failure audit。

### M6 — Research and Engineering Release

- `[~]` Clean environment 重现 headline results。
- `[~]` 每个 claim 可链接 experiment，每个 limitation 显式记录。
- `[~]` Repository/report/benchmark/metadata/failure records 一致。
- `[~]` 完成 evidence-based preprint decision。
- `[~]` 项目可在专家面试中解释和辩护。

## 7. Near-term P1 / P2

### P1 — M0 之后

- `[x]` R1 prioritized literature map 与不超过 5 篇的 must-read sequence 已登记；后续阅读仍不构成实现授权。
- `[!]` R2 minimum architecture requirements。Blocked until M0 PASS。
- `[ ]` 完整 risk register。
- `[ ]` Terminology glossary。

### P2

- `[ ]` Repository/public narrative planning。
- `[ ]` Interview-bank seed questions。
- `[ ]` Preprint venue exploration。

## 8. Stop Conditions

以下任一条件成立时，保持 no-code：

- `[x]` 已有 measurable primary RQ：RQ-001。
- `[x]` 已有 fair baseline definition。
- `[x]` 已有 falsification condition。
- `[x]` Shared source of truth 已完整初始化。
- `[x]` 未支持的 feature additions 均不得进入 scope。
- `[x]` R0 final decision 与 R4 Evaluation Contract v0 已登记；二者仍不构成 M1 execution authorization。

## 9. Next Checklist Update Trigger

以下任一事件发生即更新：R1/R4 review 返回；R0 freeze 决议；其余 shared-memory 文件建立；M0 review；优先级或 scope 变化；R0 feasibility review 被接受、修改或否决。
