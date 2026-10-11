# Agent Runtime Research

研究工具使用型 LLM Agent 中，**显式执行前规划（explicit ex-ante planning）相对于 ReAct，是否会随着任务依赖深度变化而影响成功率，以及这种差异带来多少资源成本**。

项目从文献、研究协议与可测量性审查开始，逐步建立最小运行闭环、独立验证器和可审计的执行记录。目标是在相同模型、工具、任务信息和总推理预算下进行公平比较。

> 当前公开版本为研究准备与协议文档。最新项目状态记录日期为 2026-09-21，首次公开整理日期为 2026-10-11。尚未交付本项目的 Runtime 实现、benchmark、pilot 或正式实验结果。

## 研究问题

核心问题 RQ-001（Planning Boundary）关注：在 fully observed、stationary 的工具任务中，显式子目标规划与 ReAct 的 end-state success 差异是否随 dependency depth 改变。

ReAct 包含 observation-driven adaptation 和隐式 online/local planning。任务成功由独立 end-state verifier 判定，模型自身的成功声明不能替代验证。

| 研究项 | 当前状态 |
|---|---|
| RQ-001：Planning Boundary | Active core |
| RQ-002：Dynamic Perturbation and Recovery | RQ-001 下的 gated subproblem |
| RQ-003：Evidence-grounded Reflection | Conditional P1 |
| RQ-004：Failure Analysis | Analysis layer |

详细定义、进入条件与 claims 边界见 [Research Question Index](PROJECT_MEMORY/03_RESEARCH_QUESTIONS.md)。

## 已完成内容与当前进度

- M0 Research Charter 已通过审查；研究身份、核心问题和公平性约束已登记。
- 已整理 ReAct、ADaPT、Reflexion 与 Plan-and-Solve 的文献证据与机制边界。
- 已完成最小协议 requirements review 与 evaluation consistency review；仍有语义问题待裁决。
- 已建立 14 份共享项目记忆文件，记录状态、决策、文献、实验、失败、里程碑与延期事项。

当前重点为 **M1 / Gate A：将最低要求收敛为一页可执行协议**。最新审查结论为 `CLARIFICATIONS REQUIRED`，还没有 protocol-validity PASS。

## 近期路线

| Gate | 目标 | 当前状态 |
|---|---|---|
| A | 最小协议：策略边界、verifier、trace、budget ledger、fairness checklist | In progress |
| B | 最小 runnable loop | 等待单独实现授权 |
| C | Measurement sanity：检查验证、计量与策略区分 | 后续阶段 |
| D | 决定是否启动 RQ-001 pilot | 后续决策 |

候选最小闭环为：

```text
task → policy → action → tool → observation → verifier → trace
```

当前没有冻结完整架构。Reflection、replanning、rollback、MCP/Paper2Agent、memory、多模型、多 benchmark 和资源调度暂缓。

## 测量原则

比较应固定 model snapshot、工具 schema/access、任务信息、初始状态、termination/verifier、采样设置与总推理预算。Planner、retry、repair 和 revision 均计入同一 episode 预算。

协议记录的单 episode 上限为：12 model requests、24,000 input/output tokens、180 seconds、16 tool invocations、2 corrective/revision/reflection calls；M1 禁止 parallel execution。所有 enrolled episodes 保留核算，timeout、budget exhaustion、invalid action 和 infrastructure failure 不能静默消失。

研究合同中的 MCID 为 10 percentage points，equivalence region 为 `[-5, +5]`，non-inferiority margin 为 `-5`。这些是协议阈值，尚无效应估计。USD 150 / 500 仅为暂定规划数字，未构成已确认预算或执行授权。完整约束见 [Decision Record](PROJECT_MEMORY/05_DECISIONS.md)。

## 仓库导航

```text
PROJECT_MEMORY/              # 当前状态、Checklist、RQ、决策与证据索引
PROJECT_DOCS/
  GOVERNANCE/                # 项目角色与治理规则
  INITIALIZATION/            # 初始化材料
  ROLE_DELIVERABLES/         # 文献、协议、可行性与一致性审查
  GUIDES/                    # 项目使用指南
README.md
```

建议从以下文档开始：

1. [Project State](PROJECT_MEMORY/01_PROJECT_STATE.md) — 当前阶段与下一步。
2. [Master Checklist](PROJECT_MEMORY/02_MASTER_CHECKLIST.md) — 任务和 gate 进度。
3. [Research Questions](PROJECT_MEMORY/03_RESEARCH_QUESTIONS.md) — 研究边界。
4. [Literature](PROJECT_MEMORY/06_LITERATURE.md) — 文献证据及阅读记录。
5. [R2 Minimum Requirements](PROJECT_DOCS/ROLE_DELIVERABLES/R2_M1_MINIMUM_REQUIREMENTS_REVIEW.md) 和 [R4 Consistency Review](PROJECT_DOCS/ROLE_DELIVERABLES/R4_M1_R2_PROTOCOL_CONSISTENCY_REVIEW.md) — 最小协议及未决问题。
6. [Milestones](PROJECT_MEMORY/11_MILESTONES.md) — 分阶段路线。

项目使用 R0–R7 角色职责划分组织研究与交付，通过 shared project memory、role update 和 handoff 同步状态。角色安排不代表已实现 multi-agent runtime。治理规则见 [Project Instructions](PROJECT_DOCS/GOVERNANCE/Project%20Instructions.md)。

## 获取与复现状态

```bash
git clone https://github.com/ada-c38f0bb79f/agent-runtime-research.git
cd agent-runtime-research
```

当前可以查看研究文档和审查记录。尚无安装命令、运行 demo、测试套件或可复现实验；相应入口将在实现与执行获得授权并实际完成后补充。实验与研究发现分别见 [Experiments](PROJECT_MEMORY/07_EXPERIMENTS.md) 和 [Findings](PROJECT_MEMORY/14_FINDINGS.md)。

## 文献与本地资料

相关论文来源记录于 [Literature](PROJECT_MEMORY/06_LITERATURE.md)。本地论文 PDF、第三方 `react-official/` checkout、虚拟环境、生成产物及缓存不包含在此公开仓库中。可从 [官方 ReAct 仓库](https://github.com/ysymyth/ReAct) 获取参考实现；使用第三方材料时遵循其各自许可。

## 当前限制

协议仍需澄清 revision/retry/repair、invalid-action success、budget/verifier/termination 优先级、计数单位、depth/horizon、indeterminate/infra adjudication 和成本汇总。历史文档保留当时的提案；发生冲突时，以最新 R0 决议与 canonical project memory 为依据。

本项目尚未形成 planning benefit/harm、equivalence、generalization 或 architecture contribution 的实证结论。

## 许可

本项目尚未指定开源许可证。仓库公开用于查看与讨论；第三方论文和源码的许可由原作者规定。
