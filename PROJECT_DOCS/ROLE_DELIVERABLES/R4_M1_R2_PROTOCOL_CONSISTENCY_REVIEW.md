# R4 — R2 Requirements / Frozen Contract Consistency Review

**Date:** 2026-09-21  
**Status:** REVIEW COMPLETE / CLARIFICATIONS REQUIRED；不是 M1 PASS 或执行授权。  
**Authority:** `DEC-20260921-R0-M0-001`，及 R0 M0 PASS recheck。旧 R4 v0 草案、freeze-support memo 与之冲突时，以 R0 冻结决议为准。

## 1. 总体判断

R2 requirements 总体符合唯一 active core RQ-001、独立 verifier、全量 denominator、ReAct observation-driven adaptation、累计预算与 M1 measurement-validity 目标。未发现 R2 明文修改冻结数值或授权执行。

但目前只能判为 **方向一致、协议闭合不足**。下列要求遗漏与语义歧义可能改变 treatment、success 或资源统计，不能据此宣布 protocol validity PASS。M0 已 PASS，不因本次 M1 待决项而自动撤销。

核对来源：

- [R2 requirements](R2_M1_MINIMUM_REQUIREMENTS_REVIEW.md)，§1–10 与 ROLE UPDATE。
- [R0 final freeze](R0_M0_FINAL_FREEZE_DECISION_20260921.md)，§3–8。
- [R0 PASS recheck](R0_M0_PASS_RECHECK_20260921.md)，§4–6。
- [Decision record](../../PROJECT_MEMORY/05_DECISIONS.md)、[Project state](../../PROJECT_MEMORY/01_PROJECT_STATE.md)、[Experiment record](../../PROJECT_MEMORY/07_EXPERIMENTS.md)。

## 2. 冻结值对照：不得重开为 UNKNOWN

| 项目 | 冻结内容 | R2 一致性判断 |
|---|---|---|
| Primary outcome | independent-verifier episode end-state success；full enrolled-run denominator | §5 一致；终止与成功优先级仍未闭合，见 C2 |
| MCID | success 绝对差 **10 percentage points** | 未重述；不是改值，但须显式引用，且 M1 不检验效应 |
| Equivalence / NI | plan minus ReAct **[-5,+5] pp / -5 pp** | §5 将测试排除在 M1 之外正确；不显著不等于等效 |
| Practical benefit（未来） | ≥10 pp 且 episode cost 增幅≤20%；或 success 非劣且 cost per successful episode 降低≥20% | R2 有原始 telemetry，未定义汇总口径；不得在 M1 使用这些规则作收益 claim |
| Per-episode caps | **12 requests、24,000 input+output tokens、180 s、16 tool invocations、2 corrective/revision/reflection calls** | §7 只引用 frozen hard caps；须把这五项绑定到决议版本，不能由配置另定 |
| 并行 | **M1 禁止 parallel model/tool execution** | R2 将并行列为 out-of-scope，却未显式列为 REQUIRED 禁止；需补齐 |
| 总成本 | **M1 USD150；formal USD500 conditional；RQ-002/003 USD0** | §7 episode telemetry 一致，但缺 work-package ceiling、超支升级规则及 paid evaluation services/local compute 分类 |
| Fairness | 同 demonstrations、信息、model、tools、retry、termination、budget；paired assignments | §3/8 基本一致；demos 与相同 retry policy 应明确写入审计表 |
| RQ-004 | κ/α≥**0.60**、预指定盲法双标子集、coverage/unknown/held-out reporting | ROLE UPDATE 承认既有 gate；§9 仅要求未来可标注 trace，当前不执行分析，符合权限 |
| M1 | 只审查 measurement validity，无 effect/harm/equivalence/NI/generalization claims | §10 与 scope 一致；不能把纸面审查称为已验证运行闭环 |

## 3. 冲突风险与必须补齐的要求

以下是 **R4 interpretation / recommendation**；区分明确遗漏与尚待裁决的潜在冲突。

| ID / 定位 | 问题与影响 | 所需处置 |
|---|---|---|
| **C1 — R2 §1/4/7，treatment contamination（潜在冲突）** | 要求 plan updates/revisions 可记录是合理的；但没有明确 M1 是否允许实际 revision。冻结的“2 corrective/revision/reflection calls”是上限，不是激活 RQ-002/003 的许可。更新完成状态也不等于改变计划结构。 | R2 区分只更新 execution status 与修改未执行 subgoals/edges；R4 建议 M1 禁止主动 dynamic revision/reflection，出现则记录 deviation。R0 裁定具体允许行为及偏离处理；保留双方相同普通 retry/repair。 |
| **C2 — R2 §1/2/5，success/denominator（潜在冲突）** | §2 允许 invalid action 后继续；R0 原文说 invalid action remain failures，同时允许 retry/repair。未明确“一次 invalid attempt 后完成”是否仍是 episode failure。§1 的单一 terminal outcome 与 §5 独立 verifier 也缺少优先级：恰好触顶但 end state 正确如何归类？ | R0 明确 invalid attempt 与终止型 invalid-action failure 的区别；定义 hard-cap termination、verifier result、primary success 的优先级。触顶/超时失败这一冻结规则不得由 R2 放宽。每次 invalid attempt 必须保留，无论最终分类。 |
| **C3 — R2 §7，budget enforcement（遗漏）** | 有累计账本但未定义发起前余额检查、token 预留/实际值冲突、超限返回及 deadline 后结果。invalid validation 是否算 tool invocation、“2 calls”按请求还是纠错过程计数也未定。 | R2 提交非执行语义澄清；R0 决定影响 cap 含义的规则。必须保持硬上限不变，不允许完成后因已花费而忽略超限。晚到结果计费保留，不能覆盖已终止记录。 |
| **C4 — R2 §7/8，总成本及显式公平控制（遗漏）** | episode telemetry 不能保证 USD150 work-package ceiling；未明确评测服务费、local compute 分列、超预算回 R0、demos equality、M1 禁止并行。 | R2 直接补录冻结条款，无需新科学决议。task 数只有在已批准范围内才能调整；当前无 task 生成/执行授权。任何增额均须 R0。 |
| **C5 — R2 §5/6，ground truth 与 difficulty（歧义）** | “final observable/environment state”若被解释为只读 agent observation，会让 silent wrong-state 无法核验；“required action graph”若只是单一参考解，则可把合法替代路径误判。depth、horizon、difficulty 的 held-fixed/stratified/deferred 三选一过宽，事后 success difficulty 不能作为前置分层标签。 | verifier 可以读取隔离的 verifier-only environment ground truth，policy 不可读取。R2/R4 纸面澄清等价合法 end states、替代路径与 depth 定义；R0 裁定 horizon 控制/分层及 depth strata。首轮仅 depth 是计划操纵因素，不能用“deferred”掩盖混杂。 |
| **C6 — R2 §3/8，trace/replay（歧义）** | visible Thought 格式若给一方额外推理调用，会改变策略预算；同 seed 不保证模型逐字重放。 | 用最小可审计 policy event，不要求 hidden chain-of-thought；任何生成调用计账。区分环境/日志重放与模型重新采样，记录 provider 不可控性。不能声称 seed 提供不存在的确定性。 |
| **C7 — R2 §5/10，质量裁决（UNKNOWN）** | indeterminate verifier、missing evidence、infra failure 的 adjudication 及 protocol acceptance threshold 未定义。固定 trace 子集“before any run authorization”不能被解释为需要现在运行 agent 产生 traces。 | 当前只审纸面规则，未来运行审计另行授权。所有 enrolled episodes 均保留；不能 adjudication 后删不利样本。R0 指定质量门槛、裁决人和重审条件。 |

**Denominator 口径建议（待 R0 对 C2 裁定）：** N 为所有已 enrolled episodes；primary success rate = 满足冻结 verifier 与终止规则的成功数 / N。infrastructure-failed、indeterminate、missing-evidence episodes 分别计数且不静默移除；敏感性分析如排除 infra，必须另列分母。RQ-002 的 recoverable-only denominator 不得挪用于 RQ-001。

**成本汇总待澄清：** episode cost 应明确按全部 enrolled episodes 汇总；cost per successful episode 建议为同组全部 episode 成本 / 成功数，而非只取成功 runs 的均价。零成功时标记 undefined/infinite、报告实际总支出；不能填零。R0 需确认该口径及未来 20% 条件的统计判定规则，M1 不做该效应判断。

## 4. UNKNOWN 与决策归属

**必须由 R0 裁决，R4/R2 不能自行改变合同：**

1. C1：M1 允许的 status update、retry/repair 与 plan revision 边界；是否构成 protocol violation。
2. C2：invalid attempt 后恢复的 episode success 定义；终止原因与 verifier/预算触顶的优先级。
3. C3：hard-cap 边界操作、tool invocation 和 corrective call 的计数单位；provider/local token 差异的权威口径。
4. C5：depth strata、horizon 控制、替代合法路径的 ground-truth 规则；并行 prerequisite 图不等于授权并行执行。
5. C7：indeterminate/infra adjudication、primary 与 sensitivity 口径、protocol-validity acceptance 与裁决责任；不能以 R4 review complete 代替 M1 PASS。
6. 成本/成功汇总定义；任何预算、MCID、margin、RQ 状态改变及一切后续执行授权。冻结值不因 UNKNOWN 自动重开。

**R2/R4 可继续纸面澄清、无需当前冻结架构：** visible policy event 最小字段、tool error envelope、预算 ledger 的计量来源和 missing 标记、replay 能力声明、schema/version/redaction/retention 对审计的影响。若影响信息公平、完整计量或可验证性，必须回 R0。snapshot vs event-sourcing、存储介质、精确状态词汇不应当作科学阻断条件，更不能在本次选择实现。

**正式试验前才需另行完成（不要求 M1 现在跑统计）：** 预注册 sample size/precision、task-cluster 与重复 seed 的相关性、interaction estimand、equivalence/NI CI 判定、多重比较与成本不确定性。10 pp MCID 是成功率差的实用阈值，不能直接当作 depth interaction 的阈值；CI 包含零不等于无效应或等效。

## 5. 文档一致性附记与建议下一步

`01_PROJECT_STATE.md` §8/9 仍残留“baseline/control 尚未建立”“PASS recheck 尚未记录”“requirements review 结果 UNKNOWN”，与该文件顶部及 `05_DECISIONS.md` 冲突；三个月 Scope/Roadmap 也保留广泛 reflection/replanning 描述。应由 R6 依既有决议清理，不能据旧段落恢复授权。旧 R4 文档中的 tentative thresholds、pilot seeds/规模、USD 粗估也不能覆盖冻结上限。

建议：R0 先裁决上述语义问题 → R2 仅修订 requirements/交叉引用 → R4 做局部一致性复核 → R6 归档。此顺序不是代码、benchmark、pilot、formal experiment 或 architecture freeze 的许可。

# HANDOFF REQUEST

**From Role:** R4  
**To Role:** R0  
**Reason:** requirements 存在可能改变 treatment、success、budget 的未闭合语义。  
**Context:** M0 PASS；M1 仅 protocol-only review 获授权。  
**Relevant IDs:** DEC-20260921-R0-M0-001；RQ-001；C1–C7；ROLE-20260921-R2-001。  
**Exact Question:** 请裁定 §4 的六组事项，尤其 revision 权限、invalid-action success、触顶优先级、计数单位、depth/horizon、verifier adjudication 与成本汇总；冻结数值保持不变，除非另发决议。  
**Expected Deliverable:** 可登记的 protocol clarification / decision；明确保留无执行授权。  
**Priority:** P0。  
**Blocking?:** 阻止本 requirements 获得无保留 protocol-consistency PASS；不影响已完成的 M0 PASS。

# HANDOFF REQUEST

**From Role:** R4  
**To Role:** R6  
**Reason:** 归档 review 与清理过期状态段落。  
**Context:** 不改 R0 决议、不标 M1 PASS。  
**Relevant IDs:** ROLE-20260921-R4-003；DEC-20260921-R0-M0-001。  
**Exact Question:** 请登记 R4 review COMPLETE / CLARIFICATIONS REQUIRED，并按已冻结决议修正 Project State §8/9 的旧措辞；保留所有执行禁令。  
**Expected Deliverable:** Project Delta、role log 与交叉引用更新。  
**Priority:** P0。  
**Blocking?:** 不阻止 R0 阅读裁决；必须避免后续角色误读状态。

# ROLE UPDATE

**ROLE-LOG-ID:** ROLE-20260921-R4-003  
**Role:** R4 — Benchmark & Experiment Scientist  
**Date:** 2026-09-21  
**Task:** R2 M1 requirements 与冻结 Evaluation Contract 的 bounded consistency review。  
**Context:** M0 PASS；RQ-001 唯一 ACTIVE CORE；仅 protocol-only review 获授权。  
**What Was Done:** 核对 thresholds、inference/cost caps、公平性、denominator、verifier、treatment boundary 与 M1 objective；区分遗漏、潜在冲突、UNKNOWN、R0 决策和后续正式统计事项。  
**What Changed:** 新增 R4 review，结论为方向一致但 CLARIFICATIONS REQUIRED；未改变冻结合同或 RQ 状态。  
**Evidence:** R2_M1_MINIMUM_REQUIREMENTS_REVIEW §1–10；R0_M0_FINAL_FREEZE_DECISION §3–8；R0_M0_PASS_RECHECK §4–6；PROJECT_MEMORY/01、04、05、07、09。均为文档/决议证据，无实验结果。  
**Files Affected:** 仅新增 PROJECT_DOCS/ROLE_DELIVERABLES/R4_M1_R2_PROTOCOL_CONSISTENCY_REVIEW.md；未修改 requirements、冻结决议、shared memory 或代码。  
**Research Questions Affected:** RQ-001 的测量语义；RQ-002/003 不因 cap 字段获得激活；RQ-004 保持 analysis layer 与 κ/α≥0.60 gate。  
**Architecture Impact:** NONE；没有选择或冻结接口、框架、存储、架构。  
**Experiment Impact:** 识别 protocol 闭合缺口；没有生成 benchmark、运行 pilot/formal experiment 或发出执行授权。  
**New Risks:** 预算上限被误读为机制许可；invalid-action 恢复与 success 冲突；触顶后 verifier 覆盖终止；成本只统计成功样本；depth 图偏向参考路径；历史状态段落造成授权漂移。  
**Recommended Next Step:** R0 裁决关键语义，R2 仅修订要求，R4 局部复核，R6 归档；继续保持 no-execution。  
**Need Handoff:** YES — R0（协议裁决）、R6（归档/状态一致性）；R2 修订依据为 R0 后续裁决与本 review，不是实现授权。
