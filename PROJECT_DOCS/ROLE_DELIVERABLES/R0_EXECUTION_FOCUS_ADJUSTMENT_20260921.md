# R0 Execution Focus Adjustment

**Date:** 2026-09-21  
**Role:** R0 — Project Director  
**Decision ID:** `DEC-20260921-R0-FOCUS-001`  
**Purpose:** 把项目从“继续扩充设计文档”调整为“尽快形成最小可运行闭环”。

## Decision

项目从现在起采用 **implementation-first after minimum protocol freeze** 的推进方式：

1. 保留 RQ-001、ReAct vs explicit ex-ante planning 的核心研究方向。
2. 只保留足以避免明显不公平和测量歧义的协议要求。
3. 暂停继续扩展架构蓝图、MCP、Rollback、Memory、Dynamic Environment、Reflection 细节。
4. 在 M1 protocol consistency review 完成后，进入一个单独的最小实现授权节点。
5. 最小实现只服务一个本地、确定性、可验证的 tool-use 闭环，不追求通用 Runtime。

## What changes in emphasis

之前的重心：

`研究问题 → 大量协议 → 完整架构设想 → 未来多阶段路线`

调整后的重心：

`最小协议 → 最小闭环 → 可运行 trace → verifier → 一个可复现例子 → 再决定是否扩展`

## What remains required before code

只保留四项短期纸面工作：

- RQ-001 的 ReAct 与 explicit plan 边界；
- end-state verifier 的成功/失败口径；
- 最小 trace 和 budget accounting；
- 一个可执行的 fairness checklist。

以下内容全部延后到有运行结果之后：

- 完整 failure taxonomy；
- Reflection 设计；
- Replanning / rollback；
- MCP / Paper2Agent；
- 多模型、多 benchmark、资源调度；
- 复杂架构抽象。

## New execution sequence

### Gate A — Protocol minimum

目标：解决会导致实验明显失真的少量 UNKNOWN。  
输出：一页协议、最小状态/事件清单、verifier 口径、预算记录口径。  
禁止：扩写完整架构、生成大任务集、运行模型。

### Gate B — Minimal runnable loop

目标：让一个本地确定性任务完整走通：

`task → policy → action → tool → observation → verifier → trace`

只要求一个 happy path、一个 invalid action、一个 budget/termination case。  
这一步需要 R0 单独的实现授权。

### Gate C — Measurement sanity

目标：用极少量手工准备的任务检查 trace、verifier、budget 和两种策略是否真的可区分。  
这仍然不是正式实验，也不能产生 planning effect claim。

### Gate D — RQ-001 pilot decision

只有 Gate C 通过，才决定是否授权小规模 protocol pilot；再之后才考虑正式比较。

## Scope reduction

以下文件今后只在发生决策或证据变化时更新，不再持续扩写：

- 04_ARCHITECTURE.md
- 10_BACKLOG.md
- 11_MILESTONES.md
- 12_INTERVIEW_BANK.md
- 13_TECHNICAL_DEBT.md

新的设计内容必须回答一个问题：**它是否阻止最小闭环运行或验证 RQ-001？** 如果不是，先放入 backlog。

## Current authorization

本次只调整项目优先级和文档策略：

- 已授权：压缩协议、整理最小实现输入、准备 Gate B 的实现任务说明；
- 尚未授权：写代码、生成 benchmark、启动 pilot、冻结架构、调用模型/API。

## R0 ROLE UPDATE

**ROLE-LOG-ID:** `ROLE-20260921-R0-007`  
**Role:** R0 — Project Director  
**Date:** 2026-09-21  
**Task:** Rebalance project emphasis toward implementation  
**What Was Done:** 根据 whole-project reality audit，确认文档设计已明显领先于代码和实验，重新安排项目优先级。  
**Decision:** 采用 implementation-first after minimum protocol freeze；先形成最小可运行闭环，再扩展研究机制。  
**What Changed:** 暂停扩写复杂架构和后续能力；将近期工作收敛到最小协议、最小闭环、trace、verifier 和 measurement sanity。  
**Research Impact:** RQ-001 不变；RQ-002/003/004 继续 gated/conditional/analysis-layer 状态。  
**Architecture Impact:** 不冻结架构；只准备最小闭环的实现输入。  
**Experiment Impact:** 仍无 pilot 或正式实验授权。  
**New Risk:** 过度压缩协议可能遗漏公平性约束，因此 Gate A 必须保留最小 fairness checklist。  
**Recommended Next Step:** 完成 Gate A 的一页协议收敛，之后由 R0 决定是否开放 Gate B 实现授权。  
**Need Handoff:** R6 归档本决定；R2 将需求审查压缩为 Gate B 输入。

