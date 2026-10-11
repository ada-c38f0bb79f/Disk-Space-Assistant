# Agent Runtime Research Project — Failure Database

| 字段 | 当前值 |
|---|---|
| Version | v0.1 |
| Updated | 2026-09-21 |
| Primary | R5 — Failure & Reliability Analyst |
| Owner of record | R6 |
| Registered failures | 0 |

## 1. Current Status

尚无运行、pilot 或实验，因此没有可登记的 agent/runtime/tool failure，也没有 failure finding。

## 2. Frozen Future Analysis Control — RQ-004 Layer

未来 RQ-001/RQ-003 trace analysis 最低要求：

- two-level labels：`locus` 与 `mechanism`；
- 分离 `first error`、`proximate cause`、`terminal symptom`；
- 分离 model/policy、runtime、tool/environment、harness/engineering loci；
- 保留 `unknown` 与 `ambiguous`；
- 在预注册 trace subset 上做 blinded double annotation；
- Cohen’s κ 或 Krippendorff’s α 至少为 **0.60** 才继续使用 taxonomy；
- 报告 coverage、unknown/ambiguous 比例、annotation changes 与 held-out performance；
- predictive association 不得表述为 causal explanation。

## 3. Future Failure ID Convention

使用 `FAIL-YYYYMMDD-NNN`，记录 Immediate Cause、Root Cause、Severity、Frequency、Detectability、Recoverability、Evidence、Affected EXP 与 proposed fix status。
