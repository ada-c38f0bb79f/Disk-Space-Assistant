# Agent Runtime Research Project — Architecture Record

| 字段 | 当前值 |
|---|---|
| Version | v0.1 |
| Updated | 2026-09-21 |
| Primary | R2 — Agent Runtime Architect |
| Owner of record | R6 |
| Architecture status | **NOT FROZEN / MINIMUM LOOP PREPARATION ONLY** |

## 1. Current Boundary

M0 的最终 Research Contract 只冻结研究问题、测量阈值、预算、公平性控制与 M1 measurement-validity 目标。M0 PASS 后仅授权 R2 做 architecture-neutral requirements review；没有冻结系统架构，也没有授权实现。

R0 于 2026-09-21 进一步调整执行重点：完成最小协议后，优先准备一个最小 runnable loop；不再继续扩写完整 Runtime、MCP、rollback、memory 或 resource-scheduler 设计。Gate B 是否开始实现，需要 R0 单独授权。

## 2. Future M1 Input — Not a Decision

以下仅是 R0 feasibility review 中保留的候选最小 runtime spine，供 M0 PASS 后由 R2 设计：

- `RunState / BudgetManager`
- `ToolRegistry / Validator`
- `Executor`
- `TraceRecorder`
- 独立 `Verifier`
- 最小 `Evaluation Runner`
- 可切换的 ReAct 与 explicit ex-ante planning policy

候选测量闭环：

`task → policy → validation → executor → observation → verifier → trace`

该列表不是接口、模块边界、实现顺序或架构批准。

## 3. Explicitly Not Authorized

- 写代码或生成项目骨架；
- 冻结 interface、data model、dependency 或 framework；
- MCP / Paper2Agent provider ecosystem；
- rollback、dynamic environment、resource scheduler、concurrency optimization；
- Memory；
- 全量 benchmark framework。

## 4. M1 R2 Requirements Review Boundary

R2 当前只可定义：

- state requirements；
- trace requirements；
- verifier requirements；
- budget/cost accounting requirements；
- reproducibility and auditability requirements。

R2 不可实现、选框架、选依赖、冻结接口、生成任务或运行任何 agent。

## 5. Entry Conditions for R2

R2 只有在以下条件满足后才能开始 architecture requirements/design：

1. R0 已完成 M0 PASS recheck；
2. R0 已明确授权本次 bounded M1 requirements review；
3. R2 使用冻结的 RQ-001、budget v1、fairness controls 与 M1 objective 作为约束；
4. 任何设计选择不得被写成 research finding。

当前没有 ARCH-ID 或 architecture decision。

## 6. R2 M1 Review Record

R2 completed the requirements-only review and R4 found clarifications required. The only near-term architecture input is a minimal runnable loop; no interface, framework, dependency, data model, or architecture is approved. Gate B implementation requires separate R0 authorization.
