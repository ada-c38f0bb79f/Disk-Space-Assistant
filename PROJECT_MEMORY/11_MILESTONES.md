# Agent Runtime Research Project — Milestones

| 字段 | 当前值 |
|---|---|
| Version | v1.1 |
| Updated | 2026-09-21 |
| Primary | R0 |
| Owner of record | R6 |
| Current milestone | M1 — GATE A: MINIMUM PROTOCOL CONVERGENCE (M0 PASS) |

> Milestone 只能由 R0 评为 PASS / PARTIAL / FAIL。代码存在不构成自动通过；每个 gate 需要与其阶段相称的理解、实现、测试、评估、文档和失败分析证据。

## 1. Milestone Index

| ID | Name | Target | Status | Gate purpose |
|---|---|---|---|---|
| M0 | Research Charter Freeze | Week 1 末 | **PASS** | 冻结研究合同与 no-code exit |
| M1 | Baseline and Measurement Validity | Week 4 末 | **GATE A — PROTOCOL MINIMUM** | 收敛最小协议并为后续 Gate B 提供输入 |
| M2 | Planning/Replanning Evidence | Week 8 末 | NOT STARTED | 形成规划/重规划的首轮可辩护证据 |
| M3 | Core Research Package | Week 12 末 | NOT STARTED | 综合 RQ-001–004 的核心研究包 |
| M4 | Memory Decision | Week 16 末 | CONDITIONAL | 基于证据测试/拒绝 memory extension |
| M5 | Generalization and Reliability | Week 20 末 | CONDITIONAL | 验证跨设置泛化与稳健性 |
| M6 | Research and Engineering Release | Week 24 末 | CONDITIONAL | 完成 clean reproduction 与公开交付 |

注：项目输入只定义了相对周次。除起始记录日期 2026-09-03 外，R0 尚未登记精确日历截止日。

## 2. M0 — Research Charter Freeze

**Current status:** IN PROGRESS  
**Exit authority:** R0  
**Required handoffs:** R1、R4、R6

- `[x]` **Understanding:** Research Identity v1 已由 R0 冻结。
- `[x]` **Research:** RQ-001 active core；RQ-002 gated；RQ-003 conditional P1；RQ-004 analysis layer，且各自有可测量/entry/quality boundary。
- `[x]` **Scope:** IN / CONDITIONAL / OUT / BACKLOG 已记录。
- `[x]` **Evaluation:** MCID、equivalence/non-inferiority、budget v1、cost v1、fairness controls 与 M1 objective 已冻结。
- `[x]` **Operations:** 14/14 shared-memory files 已存在；R6 registration complete。
- `[x]` **Decision:** R0 final decision 已登记；R0 PASS recheck 已完成。
- `[x]` **Guardrail:** No-code / no-architecture-freeze gate 已记录。

**PASS requires:** R1 novelty/literature review、R4 measurability/validity review、R6 完整登记、R0 final freeze decision 与 R0 registration PASS recheck。全部完成。

## 3. M1 — Baseline and Measurement Validity

**Target:** Week 4 末  
**Status:** GATE A IN PROGRESS

- `[x]` **Requirements:** R2 requirements-only review completed; R4 consistency review completed with clarifications required。
- `[>]` **Gate A:** 将关键语义 UNKNOWN 收敛为一页可执行协议；不得写代码。
- `[ ]` **Understanding:** 可解释 baseline behavior 与预期 failure modes。
- `[ ]` **Implementation:** minimum runtime 与 trace path 运行，且研究逻辑不被 framework 决定。
- `[ ]` **Tests:** state transitions、tools、termination、errors、trace serialization 有覆盖。
- `[ ]` **Evaluation:** Benchmark v0 与 baseline protocol 通过 ambiguity/leakage/fairness checks。
- `[ ]` **Documentation:** architecture、task schemas、configs、reproduction steps 当前且一致。
- `[ ]` **Failure analysis:** pilot failures 被分类；engineering bug 与 agent failure 分开。

## 4. M2 — Planning/Replanning Evidence

**Target:** Week 8 末  
**Status:** NOT STARTED

- `[ ]` **Understanding:** observed boundaries/mechanisms 有明确 alternative explanations。
- `[ ]` **Implementation:** planning 与 replanning 是隔离、可配置 intervention。
- `[ ]` **Tests:** planner/executor boundaries 与 recovery paths 有覆盖。
- `[ ]` **Evaluation:** preregistered comparisons 包含 repetitions、variance、cost、ablations。
- `[ ]` **Documentation:** experiment records 与 decisions 完整。
- `[ ]` **Failure analysis:** planning-specific 与 recovery failures 可链接 traces。

## 5. M3 — Core Research Package

**Target:** Week 12 末  
**Status:** NOT STARTED

- `[ ]` **Understanding:** RQ-001–RQ-004 有 evidence-calibrated provisional answers。
- `[ ]` **Implementation:** ReAct/planning/replanning/reflection variants 可复现。
- `[ ]` **Tests:** critical paths 与 known regressions 有覆盖。
- `[ ]` **Evaluation:** core experiments 已复现，model 与 inference-budget confounds 已评估。
- `[ ]` **Documentation:** report v1、findings、limitations、negative results 可 review。
- `[ ]` **Failure analysis:** aggregate scores 配有 root-cause distributions 与例子。

## 6. M4 — Memory Decision

**Target:** Week 16 末  
**Status:** CONDITIONAL — M3 evidence required

- `[~]` Narrow memory hypothesis 被测试，或 memory 被证据性地判定为不必要。
- `[~]` 任一 memory claim 有 fair no-memory baseline 与 retrieval-quality analysis。
- `[~]` Memory failures 与 added costs 已记录。

有效结果可以是负结果或“不加入 memory”的决定。

## 7. M5 — Generalization and Reliability

**Target:** Week 20 末  
**Status:** CONDITIONAL

- `[~]` Core effects 在 development setting 之外被测试。
- `[~]` Robustness 与 model × architecture 结果被复现。
- `[~]` Remaining claims 通过 validity 与 failure-analysis audit。

## 8. M6 — Research and Engineering Release

**Target:** Week 24 末  
**Status:** CONDITIONAL

- `[~]` Clean reproduction of headline results 成功。
- `[~]` 每个 claim 链接 experiment；每个 limitation 显式记录。
- `[~]` Repository、report、benchmark、metadata、failure records 一致。
- `[~]` Preprint decision 基于证据且 presentation 不 overclaim。
- `[~]` 项目可在 expert interview 中解释与辩护。

## 9. Roadmap-to-Gate Mapping

| Period | Main work | Exit gate |
|---|---|---|
| Week 1 | Charter、R1/R4 reviews、memory initialization | M0 |
| Immediate | 最小协议 → 最小 runnable loop → measurement sanity → pilot decision | Gate A/B/C/D |
| Weeks 5–8 | Static planning、failure/stale plans、dynamic replanning、replication/ablation | M2 |
| Weeks 9–12 | Reflection、model × architecture、robustness、replication、report v1 | M3 |
| Weeks 13–16 | Evidence-driven memory extension or explicit rejection | M4 |
| Weeks 17–20 | Second setting、adversarial tests、statistical reliability | M5 |
| Weeks 21–24 | Freeze、clean reproduction、release、report/preprint decision | M6 |

## 10. Milestone Review Record

R0 final decision 初始将 M0 标为 PARTIAL；R6 完成 14/14 registration 后，R0 已验证注册未改变 `DEC-20260921-R0-M0-001`，并将 M0 评为 PASS。

当前阶段：Gate A 最小协议收敛；不得实现或执行任务。Gate B 最小 runnable loop 需要新的 R0 实现授权。

## 11. Execution Focus Adjustment

R0 已决定暂停继续扩写完整 Runtime 蓝图，把近期路线改为：

`最小协议 → 最小 runnable loop → measurement sanity → RQ-001 pilot decision`

M1 不再追求一次性定义所有未来模块。任何不直接阻止最小闭环运行或验证 RQ-001 的设计内容，先进入 backlog。
