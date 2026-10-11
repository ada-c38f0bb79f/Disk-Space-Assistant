# Agent Runtime Research Project — 多角色系统使用指南

## 1. 总体思路

把整个项目当成一个“多人研究团队操作系统”来使用，而不是在每个对话里都让 ChatGPT 做所有事情。

你需要做三件事：

1. 建立一个专门的 ChatGPT Project。
2. 把 **Multi-Role Research Team Constitution** 放进 Project Instructions。
3. 在 Project 中创建多个长期角色对话，由不同角色分别负责方向、论文、架构、实现、实验、失败分析、记忆管理和求职表达。

整个项目的核心原则是：

> **一个 Project + 多个 Specialist Roles + 一个 Shared Project Memory。**

---

## 2. 建立 Project

建议 Project 名称：

```text
Agent Runtime Research Project
```

把完整的 **Multi-Role Research Team Constitution** 放进 Project Instructions。

Project Instructions 负责定义：

- 项目目标
- 研究原则
- 角色体系
- 各角色权限
- Shared Memory
- ROLE UPDATE
- HANDOFF
- Research / Experiment / Failure 记录规范
- 项目质量标准

这份 Constitution 相当于整个项目的“宪法”。

通常不需要频繁修改。

---

## 3. 建立角色对话

推荐建立以下长期对话：

```text
00｜R0 Project Director
01｜R1 Literature Scholar
02｜R2 Runtime Architect
03｜R3 Implementation Engineer
04｜R4 Experiment Scientist
05｜R5 Failure Analyst
06｜R6 Project Memory Keeper
07｜R7 Career & Communication
```

每个对话固定承担一个角色，不要频繁更换角色。

---

## 4. 每个角色窗口第一次怎么启动

第一次进入某个角色窗口时，只需要发送类似：

```text
你是本项目的 R2 — Agent Runtime Architect。

严格按照 Project Constitution 中定义的 R2 权限、职责、工作流和 Handoff Protocol 工作。

除非 R0 修改项目组织结构，否则你始终保持这个角色。
```

其他角色把 `R2 — Agent Runtime Architect` 替换成对应角色即可。

之后该窗口长期保持这个角色。

---

# 5. R6 是整个系统的记忆中枢

最重要的窗口之一是：

```text
06｜R6 Project Memory Keeper
```

R6 相当于整个项目的：

- 存档管理员
- 状态数据库
- Checklist 管理器
- 历史记录员
- Cross-chat 同步器

项目中的重要变化都应该最终进入 R6。

---

## 6. 基本信息流

标准流程是：

```text
某个角色完成工作
        ↓
生成 ROLE UPDATE
        ↓
交给 R6
        ↓
R6 更新 Shared Project Memory
        ↓
其他角色读取最新 Project State
```

因此要形成习惯：

> **角色工作 → ROLE UPDATE → R6 归档。**

---

# 7. Shared Project Memory

建议项目维护以下核心文件：

```text
PROJECT_MEMORY/
│
├── 01_PROJECT_STATE.md
├── 02_MASTER_CHECKLIST.md
├── 03_RESEARCH_QUESTIONS.md
├── 04_ARCHITECTURE.md
├── 05_DECISIONS.md
├── 06_LITERATURE.md
├── 07_EXPERIMENTS.md
├── 08_FAILURES.md
├── 09_ROLE_LOG.md
├── 10_BACKLOG.md
├── 11_MILESTONES.md
├── 12_INTERVIEW_BANK.md
├── 13_TECHNICAL_DEBT.md
└── 14_FINDINGS.md
```

其中最重要的是：

### `01_PROJECT_STATE.md`

当前项目的“存档”。

### `02_MASTER_CHECKLIST.md`

记录什么已经完成、正在做、Blocked、需要 Review。

### `09_ROLE_LOG.md`

不同角色做过什么。

---

# 8. R0 和 R6 的区别

这是整个系统中非常重要的一点。

## R0 Project Director

回答：

> **我们应该去哪？**

负责：

- 项目方向
- Scope
- Research Question
- Roadmap
- Priority
- Milestone
- 冲突裁决

---

## R6 Project Memory Keeper

回答：

> **我们现在到底在哪？**

负责：

- 当前状态
- Checklist
- Role Log
- Experiment index
- Paper index
- Failure index
- Decision index
- 历史一致性

---

R0 管：

```text
方向真相
```

R6 管：

```text
状态真相
```

两者不要合并。

---

# 9. 项目第一天怎么启动

第一次正式启动项目时，不要同时启用 8 个角色。

建议只用：

1. R0
2. R6
3. R1

---

## Step 1 — R0 初始化项目

进入：

```text
00｜R0 Project Director
```

发送：

```text
我现在正式启动 Agent Runtime Research Project。

请按照 Constitution 执行 Project Initialization。

我们从 0 开始，不要写代码。

先完成：

1. Scope
2. Research Questions
3. 3-Month Roadmap
4. 6-Month Roadmap
5. Milestones
6. Week 1 P0
```

R0 负责建立项目第一版方向。

---

## Step 2 — R6 建立第一版存档

把 R0 最后的：

- Project Initialization
- ROLE UPDATE
- Research Questions
- Roadmap
- Milestones

交给：

```text
06｜R6 Project Memory Keeper
```

发送：

```text
这是 R0 的初始化结果。

请建立第一版：

PROJECT_STATE
MASTER_CHECKLIST
MILESTONES
BACKLOG
RESEARCH QUESTION INDEX
ROLE LOG
```

这样就有了：

```text
Save File v0.1
```

---

## Step 3 — R1 开始 Phase 0

进入：

```text
01｜R1 Literature Scholar
```

发送：

```text
根据当前 PROJECT_STATE，我们现在开始 Phase 0。

请只给我第一批真正需要阅读的核心论文。

不超过 5 篇。

说明：

1. 阅读顺序
2. 为什么现在需要读
3. 每篇使用什么 Reading Mode
4. 哪些内容必须真正掌握
```

然后开始论文学习。

---

# 10. 怎么使用 R1 阅读论文

例如准备学习 ReAct。

进入 R1：

```text
今天进入 PAPER READING MODE。

我要深度学习 ReAct。

目标不是让我得到论文摘要，而是让我最终能够：

1. 自己解释 ReAct
2. 批判论文
3. 比较 ReAct 和 Planning
4. 实现 Minimal ReAct
5. 理解实验和 Failure

先进行 Scout Reading，然后带我进入 Deep Read。
```

---

## 阅读过程中可以不断追问

例如：

```text
这里为什么这样设计？
```

```text
这个公式是什么意思？
```

```text
作者为什么不用完整 Planning？
```

```text
这个实验真的能证明作者的 Claim 吗？
```

```text
如果换一个更强模型，结论可能会变化吗？
```

---

## 读完以后

要求 R1：

```text
现在对我进行 Reconstruction Test。

不要直接告诉我答案。

让我闭卷解释：

Problem
Motivation
Core Method
Architecture
Experiments
Main Findings
Limitations
Relation to Our Project
```

真正掌握以后，再结束。

---

## R1 输出

重要论文最好形成：

```text
PAPER-001
```

以及：

```text
ROLE UPDATE
```

然后交给 R6。

---

# 11. 学完以后怎么进入架构阶段

论文理解后，进入：

```text
02｜R2 Runtime Architect
```

发送：

```text
根据 PAPER-001 和当前 PROJECT_STATE，

我现在已经完成 ReAct 的核心学习。

请开始带我设计 Minimal ReAct Runtime。

不要直接写完整代码。

先从：

1. Requirements
2. State
3. Interface
4. Execution Flow
5. Module Boundary
6. Failure Modes
7. Tests
8. Trade-offs

开始。
```

---

## R2 可能最终形成

例如：

```text
AgentState
    ↓
Runtime
    ↓
Model
    ↓
Action
    ↓
Tool Registry
    ↓
Observation
    ↓
State Update
```

并产生：

```text
ARCH-v0.1
DEC-001
ROLE UPDATE
```

这些再交给 R6。

---

# 12. 架构完成后怎么写代码

进入：

```text
03｜R3 Implementation Engineer
```

发送：

```text
R2 已经完成 ARCH-v0.1。

现在开始实现 AgentState。

请按照 Implementation Engineer 的方式指导我。

不要直接给完整实现。

先给我：

1. Requirements
2. Interface Reminder
3. Expected Behaviors
4. Unit Tests
5. Edge Cases

然后让我自己写。
```

---

## 你的工作方式应该是

```text
R3 定义任务
    ↓
你自己写代码
    ↓
发给 R3 Review
    ↓
R3 找问题
    ↓
你修改
    ↓
Tests
    ↓
完成
```

而不是：

```text
让 AI 一次写完整个项目
```

---

# 13. R3 主要帮你看什么

包括：

- correctness
- typing
- abstraction
- naming
- tests
- edge cases
- exception handling
- config
- logging
- reproducibility
- maintainability

完成以后产生：

```text
ROLE UPDATE
```

然后交给 R6。

---

# 14. 什么时候启用 R4

当 Minimal Runtime 已经能够基本运行后，再正式启用：

```text
04｜R4 Experiment Scientist
```

例如已经有：

- ReAct v0.1
- Calculator Tool
- Search Tool
- Python Tool

这时候发送：

```text
现在 Minimal ReAct 已经可以运行。

不要急着做复杂 Benchmark。

请帮我设计 Benchmark v0.1。

目标：

用 20–30 个任务验证：

1. Runtime correctness
2. Basic Tool Use
3. Multi-step Tool Use
4. Initial ReAct behavior

请定义：

Task Schema
Difficulty
Success Criteria
Metrics
Baseline
Experiment Protocol
```

---

## R4 会逐渐形成

```text
BENCH-v0.1
EXP-001
```

---

# 15. 实验失败以后不要马上修

例如：

```text
30 个任务
19 个成功
11 个失败
```

不要马上回 R3 加 `if`。

先进入：

```text
05｜R5 Failure Analyst
```

发送：

```text
EXP-001 已完成。

30 个任务中：

19 个成功
11 个失败

这里是失败 Trace。

请不要马上给修复方案。

先完成：

1. Failure Taxonomy
2. Immediate Cause
3. Root Cause
4. Severity
5. Frequency
6. Detectability
7. Recoverability
8. Potential Generalizable Fix
```

---

# 16. R5 应该做什么

例如最终得到：

```text
11 Failures

4 Tool Selection Failure
3 Argument Generation Failure
2 Premature Termination
1 Tool Exception
1 Reasoning Failure
```

然后进一步分析：

为什么。

---

## 例如 R5 发现

```text
Tool Selection Failure 占比异常高
```

那么它可能生成 Handoff：

```text
R5 → R4
```

要求：

正式实验验证是否为系统性问题。

或者：

```text
R5 → R1
```

要求查现有文献是否已有类似现象。

---

# 17. R0 不需要天天用

R0 更适合：

- 每周一次
- Milestone
- Scope 改变
- 重大实验发现
- Research Pivot
- 多角色冲突

---

## 每周 Review 示例

进入 R0：

```text
这是最新 PROJECT_STATE。

请执行 Weekly Research Review。

不要总结流水账。

重点判断：

1. 我们有没有跑偏？
2. 当前最大的技术风险是什么？
3. 最大的研究风险是什么？
4. 哪些假设已经被推翻？
5. Research Question 是否需要变化？
6. 有没有 Scope Creep？
7. 下周唯一最重要的 P0 是什么？
8. 哪些东西现在明确不要做？
```

---

# 18. R7 什么时候使用

前期可以很少使用：

```text
07｜R7 Career & Communication
```

等项目真正出现成果后再开始。

---

## 使用场景 A — Hiring Manager Review

```text
这是：

EXP-014
FAIL-008
当前 GitHub
当前 PROJECT_STATE

请站在字节 / PDD / AI Startup Agent Engineer 面试官角度判断：

1. 这个项目现在能证明我什么能力？
2. 哪些地方最有价值？
3. 哪些地方很像学生 Demo？
4. 最容易被面试官问穿的地方是什么？
5. 还缺什么 Hiring Signal？
```

---

## 使用场景 B — GitHub

```text
根据已经被实验支持的结果，

帮我 Review GitHub README。

禁止：

夸大实验结论
包装不存在的 Novelty
隐藏 Failure
```

---

## 使用场景 C — Mock Interview

```text
基于整个项目，

对我进行 45 分钟 Agent Runtime Technical Interview。

从基础问题开始，

逐渐追问到：

Architecture
Planning
Memory
Reflection
Benchmark
Evaluation
Failure
Trade-off
Scaling
Cost
Research Contribution
```

---

# 19. 常见项目路径

---

## 路径 A — 学习一个新机制

```text
R0
 ↓
R1
 ↓
R2
 ↓
R3
```

例如：

```text
确定要研究 Reflection
        ↓
读 Reflection 论文
        ↓
设计 Reflection Interface
        ↓
实现 Reflection
```

---

## 路径 B — 实现并验证

```text
R2
 ↓
R3
 ↓
R4
```

例如：

```text
设计 Planner
 ↓
实现 Planner
 ↓
设计 Planner Benchmark
```

---

## 路径 C — 出现异常

```text
R4
 ↓
R5
 ↓
R1 / R2
 ↓
R4
```

例如：

```text
发现 Reflection 反而降低性能
            ↓
Failure Analysis
            ↓
查论文 / 查架构
            ↓
重新设计实验验证
```

---

## 路径 D — 出现潜在研究发现

```text
R5 / R4
    ↓
   R0
    ↓
   R1
    ↓
新 Hypothesis
    ↓
   R4
```

---

## 所有路径最终

```text
→ R6 保存
```

---

# 20. 什么时候需要更新 R6

不要每个小动作都找 R6。

例如：

```text
改了一个变量名
```

不需要。

```text
写了一个 docstring
```

不需要。

---

## 这些情况应该归档

### 模块完成

例如：

```text
Tool Registry [x]
```

### 正式实验完成

例如：

```text
EXP-012 completed
```

### 新 Research Question

例如：

```text
RQ-004 created
```

### 重要架构决定

例如：

```text
DEC-009
```

### 核心论文完成

例如：

```text
PAPER-007 deep read completed
```

### Failure Pattern

例如：

```text
FAIL-012
```

### Idea 被否决

例如：

```text
Multi-Agent moved to BACKLOG
```

### Benchmark 升级

例如：

```text
BENCH-v0.2 → BENCH-v0.3
```

### Milestone 完成

例如：

```text
Phase 2 PASS
```

---

# 21. ROLE UPDATE 怎么使用

每个角色完成实质工作后，应该生成：

```text
# ROLE UPDATE

Role:

Work Completed:

New Knowledge:

Evidence:

Decisions Proposed:

Files Affected:

Checklist Changes:

RQ Impact:

Architecture Impact:

Experiment Impact:

Failure Impact:

New Risks:

Technical Debt:

Handoff Needed:

Next Recommended Action:
```

把这个内容交给 R6。

---

# 22. HANDOFF 怎么使用

角色需要其他角色介入时，生成：

```text
# HANDOFF REQUEST

From Role:

To Role:

Reason:

Context:

Relevant IDs:

Exact Question:

Expected Deliverable:

Priority:

Blocking?:
```

你可以直接复制到目标角色窗口。

---

# 23. 一个完整例子

假设实验发现：

```text
Reflection 没有提高性能
```

完整链路可以是：

---

## Step 1 — R4

确认：

```text
Reflection vs No Reflection
```

形成：

```text
EXP-021
```

---

## Step 2 — R5

分析 Failure。

发现：

```text
Reflection 经常错误诊断 Tool Argument Failure
```

形成：

```text
FAIL-017
```

---

## Step 3 — R1

查文献：

是否已有类似现象？

形成：

```text
PAPER-023
PAPER-024
```

---

## Step 4 — R0

判断：

这是：

- implementation bug
- known phenomenon
- research-worthy problem
- potential contribution

如果重要：

创建：

```text
RQ-004
```

例如：

```text
When does reflection hurt agent performance?
```

---

## Step 5 — R2

设计：

```text
Selective Reflection Interface
```

---

## Step 6 — R3

实现：

```text
Configurable Reflection Trigger
```

---

## Step 7 — R4

设计：

```text
Adaptive Reflection Ablation
```

---

## Step 8 — R6

更新：

```text
PROJECT_STATE
CHECKLIST
RQ
EXP
FAILURE
DECISION
```

---

## Step 9 — R7

未来形成技术故事：

```text
Reflection is not uniformly beneficial.
```

但必须等实验足够以后才能正式这样表述。

---

# 24. 推荐的每周节奏

不需要机械执行，但可以大致遵循：

---

## 周初

### R0

确定：

```text
本周 P0
```

---

## 学习阶段

### R1

阅读当前真正必要的论文。

---

## 设计阶段

### R2

设计模块、接口和系统架构。

---

## 开发阶段

### R3

你自己写代码，R3 Review。

---

## 实验阶段

### R4

设计并运行正式实验。

---

## 分析阶段

### R5

分析失败和反直觉现象。

---

## 周末

### R6

合并：

- ROLE UPDATE
- PROJECT STATE
- CHECKLIST
- EXP
- PAPER
- FAILURE
- DECISION

---

## 重要节点

### R7

检查：

- GitHub
- 项目叙事
- Interview Value
- Hiring Signal

---

# 25. 你本人是最高层 Orchestrator

这 8 个角色不是让你成为传话机器人。

真正结构是：

```text
Carlos
  │
  ▼
AI Research Team
```

你自己才是：

```text
Project Owner
```

---

## 你可以 Challenge R0

例如：

```text
你为什么认为 Reflection 比 Planning Failure 更值得研究？

请按照：

Novelty
Technical Depth
Experiment Feasibility
Career Value
3-Month Feasibility

比较两个方向。
```

---

## 你可以否决任何角色

例如：

R2 建议加入复杂 Graph Planner。

你可以问：

```text
它服务哪个 Research Question？

如果没有明确价值，就进入 BACKLOG。
```

---

# 26. 最重要的原则

不要让整个项目最后变成：

```text
几十个聊天窗口
+
一堆功能
+
不知道为什么做
```

真正目标是形成这样的链路：

```text
PAPER-003
    ↓
RQ-002
    ↓
DEC-007
    ↓
ARCH-v0.4
    ↓
EXP-012
    ↓
FAIL-009
    ↓
H-004
    ↓
EXP-017
    ↓
FINDING
```

这才是真正的：

```text
Research Process
```

---

# 27. 最推荐的启动方式

真正开始项目时：

## 第一步

建立 ChatGPT Project。

---

## 第二步

把 Constitution 放进 Project Instructions。

---

## 第三步

只创建：

```text
00｜R0 Project Director
```

让它完成 Project Initialization。

---

## 第四步

建立：

```text
06｜R6 Project Memory Keeper
```

让 R6 创建第一版：

```text
PROJECT_STATE
MASTER_CHECKLIST
MILESTONES
BACKLOG
RESEARCH QUESTIONS
```

---

## 第五步

根据 R0 的 Week 1 P0，再逐渐启用：

```text
R1
R2
R3
R4
R5
R7
```

不要第一天就让全部角色同时开工。

---

# 28. 一句话记住整套系统

如果以后忘了流程，只需要记住：

```text
R0 决定往哪走
R1 告诉你别人研究过什么
R2 决定系统怎么设计
R3 帮你把它正确实现
R4 判断它到底有没有用
R5 告诉你为什么失败
R6 记录项目真实状态
R7 判断你能不能把成果讲明白
```

而你本人负责：

```text
选择
质疑
学习
实现
判断
```

最终目标不是拥有 8 个 AI 助手。

而是用这 8 个角色帮助你完成一次真正完整的：

# Agent Systems Research Project
