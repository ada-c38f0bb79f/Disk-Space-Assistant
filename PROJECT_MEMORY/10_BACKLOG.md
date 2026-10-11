# Agent Runtime Research Project — Backlog

| 字段 | 当前值 |
|---|---|
| Version | v0.1 |
| Updated | 2026-09-03 |
| Primary | R0 + R6 |
| Promotion authority | R0 |

> Backlog 保存“可能有价值、但当前不应做”的事项。进入此文件不等于承诺实施，也不代表它是 active RQ。

## 1. Backlog Index

| ID | Item | Current disposition | Earliest review | Why not now |
|---|---|---|---|---|
| BL-001 | Multi-agent coordination/communication failures | BACKLOG | M3 后或新 R0 review | 扩大 scope，干扰 single-agent causal study |
| BL-002 | Browser / GUI / computer-use environments | BACKLOG | M3 后 | 环境复杂度与不可控因素过高 |
| BL-003 | Long-term memory / memory consolidation | BACKLOG | M3 gate | 当前无 active memory RQ；需 evidence-triggered hypothesis |
| BL-004 | Learned planning/routing/reflection policies | BACKLOG | M3 后 | 涉及训练/策略学习，超出前三月核心范围 |
| BL-005 | Human-in-the-loop agents | BACKLOG | M3 后 | 引入人类变量，当前实验难以公平控制 |
| BL-006 | Security/adversarial tool-use beyond basic robustness | BACKLOG | M5 scope review | 当前只保留基础 robustness |
| BL-007 | Multimodal tasks | BACKLOG | M3 后 | 不服务当前文本/tool-use核心 RQs |
| BL-008 | RAG systems / knowledge graphs / general assistants | BACKLOG | 无计划 | 与 runtime strategy causal focus 不一致 |
| BL-009 | Reinforcement learning / model fine-tuning | BACKLOG | 无计划 | 超出 runtime-level intervention 范围 |
| BL-010 | Distributed execution / production orchestration | BACKLOG | Release 后另立项目 | 属于平台工程，不是当前研究对象 |
| BL-011 | General LangChain/LangGraph replacement | BACKLOG | 无计划 | 容易退化为 framework project |
| BL-012 | Many integrations/tools/polished product features | BACKLOG | M6 后 | 不产生当前 RQ 所需证据 |
| BL-013 | Broader model families and longer-horizon tasks | CONDITIONAL | M3 | 核心方法可信后用于 generalization |
| BL-014 | Second task family / external benchmark | CONDITIONAL | M3 | 核心 benchmark 与 protocol 先需稳定 |
| BL-015 | Potential preprint | CONDITIONAL | M3/M6 | 仅在结果支持 defensible claims 时 |

## 2. Memory-Specific Entry Rule

Memory 不是当前 RQ。只有以下条件全部满足，R0 才可考虑将 BL-003 转为 RQ-005：

- M3 已完成或至少有足够核心证据；
- 观察到 cross-episode 或 long-horizon failure；
- failure 无法被已有 state/trace/replanning 机制更简单地解释或修复；
- memory intervention 可与其他策略分离；
- 有 fair no-memory baseline；
- 不破坏 M4–M6 核心 schedule。

## 3. Promotion Protocol

任何 backlog item 升级前，R0 必须执行 Idea Evaluation：

1. **Problem:** 要解决的明确问题是什么？
2. **Why now:** 为什么现在必须做？
3. **RQ relation:** 服务哪个 active RQ？若无，是否值得正式创建新 RQ？
4. **Expected value:** 预期研究/工程/学习价值是什么？
5. **Cost:** 时间、模型调用、标注、实现与维护成本是什么？
6. **Risk:** 最大 validity/scope/reproducibility 风险是什么？
7. **Alternatives:** 是否有更小、更可控的验证方式？
8. **Fastest validation:** 最小证据测试是什么？

允许的结论：`PURSUE` / `TEST FIRST` / `BACKLOG` / `DROP`。

## 4. Automatic Backlog Rule

任何没有直接 active-RQ 映射的新 feature 自动进入 backlog，包括但不限于：

- 新 planner 类型；
- 新 memory store；
- 新 tool integration；
- 新 UI/demo；
- 新 framework migration；
- “因为热门”而提出的 agent capability。

## 5. Backlog Is Not Evidence

- Backlog 条目统一分类为 **IDEA** 或 **CONDITIONAL DECISION**。
- 不得将其写入 FINDINGS。
- 未经 R0 promotion decision，不得进入 MASTER_CHECKLIST 的当前 P0/P1。
