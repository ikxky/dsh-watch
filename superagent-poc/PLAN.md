# Superagent 持续 Router 与多渠道业务 PoC 实施计划

> 2026-11-10，计划稿 v0.1。状态：静态核查、文档与合成语料准备。未运行 Superagent，未测试真实渠道，未调用模型进行业务评测。时间和量化门槛均为建议，须在首轮基线后校准。

## 1. 目标、范围和待回答的问题

### 1.1 目标业务

一个办公群中同时推进采购比价、交期核实和会议准备。首份合成语料具体采用“交流日场地比较＋季度物资缺口＋通用询价模板”，不含真实项目材料。多人分批提供报价图片、文件、语音、视频；授权人修改预算或停止工作；Worker 长任务未结束时又有新事项。输入可能来自 Slack、企业微信、普通微信或离线回放，但进入统一 Router 后按同一业务语义处理。

“统一 Router”指统一控制入口：校验、落库、去重、上下文组织、归属、权限与调度。它不要求每条消息都深度调用同一个 LLM，也不要求 Router 亲自解析每个大文件。媒体理解可异步委派；已有任务输入可沿订阅直接交给 Worker，再由 Router 协调交还和新任务。

### 1.2 核心问题

1. 一个群多个事项、多群一个事项时，能否正确关联而不串单？不确定时能否明确暂存或询问？
2. 能否保持“已确认、待确认、冲突、已作废”的事实与依据，避免未知变成已满足？
3. 任务运行中条件变更能否被 Worker 实际采用，而不仅是已投递？
4. 前台持续收消息与后台长任务是否真正分离，有无队列饥饿或长工具阻塞？
5. 发起人、补充材料者、授权人、外部方能否区分？媒体内容和引用是否会越权？
6. 系统说“完成”时，产物是否存在、内容正确、版本最新，动作回执是否与外部实际状态一致？
7. 重复、乱序、断线回补、进程重启、发送已成功但回执丢失时，是否安全续接？
8. 能否分别实现业务变化观察、任务停滞观察和服务健康检查，并控制提醒量？

这些问题承接此前持续任务评测暴露的通用故障：长任务续接困难、完成声明与文件不一致、外部动作与内部状态不一致、未知条件被当成已确认、新要求未让旧结论失效。这里只把它们转成可重复故障用例，不公开真实业务材料，也不将历史失败单独归咎于某框架或模型。

### 1.3 不做的事情

本次不安装或运行 DSH/Superagent，不修改官方原型，不迁移已有项目，不扩选其他框架，不读取真实群记录，不创建机器人或应用，不登录微信，不获取解密密钥，不调用付费模型，不运行监控，不自动发消息、采购或下单。

首轮 PoC 不以完整个人记忆、多租户、高可用集群、复杂管理后台为前置目标。dsh-watch 只保留研究计划、公开合成语料和可公开结果，不放凭据、真实输入和生产状态数据库。

## 2. 证据基线：现有机制、拟议设计与待验证

固定源码：[deepseek-ai/dsh-superagent-prototype@8c32a9dc5d72c033816c6a8110b37f40cf94fba4](https://github.com/deepseek-ai/dsh-superagent-prototype/tree/8c32a9dc5d72c033816c6a8110b37f40cf94fba4)。以下“现有”均指静态源码存在，不表示运行通过。

| 能力 | 固定版本已见机制 | 本专项设计 / 未知 |
|---|---|---|
| 事件入口 | GitHub、飞书 Source，Trigger/Thread 与持久化接收、去重 | 通用事件包、Slack/企微/微信适配未实现；不能假定任意 JSON POST 即可注入 |
| 持续控制 | Eval、主 Router Session、Ticket、Mandate、Assignment 与独立 Worker Session/目录 | Session 分离不是独立服务或安全沙箱；需实测忙时响应、共享模型限流 |
| 后续消息 | Thread 订阅 fan-out；已有 owner 的人的 follow-up 优先交 Worker，超范围 handback | 扁平群的事项边界、多人歧义、跨渠道同一人映射待做；整个群不能直接等同一个 Ticket |
| 多模态 | Trigger 为 text/meta；飞书相关上下文接口有图片读取通道 | 不等于通用音视频原生支持。原始媒体存取、异步解析、晚到重评需核验或扩展 |
| 授权 | actor、Source scope、admission、Mandate；inferred 在 observe 下记 would_accept | observe 是主动推断任务模式，不能当作关闭所有显式任务的全局只读开关；需外部副作用隔离 |
| 主动执行 | inferred 需规则评估及 auto；默认规则偏小型代码/视觉修复 | 采购等办公主动规则属于 B2 设计，不能直接沿用“自动修 CI”推论 |
| 调度与恢复 | 内部 Passes、durable effects/outbox、worker 恢复 | 无跨系统 exactly-once 保证；动作已生效但回执丢失必须先查外部状态 |
| 服务保活 | 文档提供另一个 DSH profile 每小时检查 status/restart 的部署方法 | 并非已安装的外部 watchdog；按小时不等于秒级恢复；不证明业务在推进 |
| 执行隔离 | 角色工具限制、独立目录；Sessions 使用 danger-full-access | 不能接真实凭据/生产目录；动作级授权、即时撤权、外部沙箱是目标设计 |
| 事实与成果核验 | 可记录输入与报告 | 结构化事实版本、业务验收器和外部结果回读没有因此自动完成 |

关键固定证据：

- [README 产品定位](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/README.md)、[领域模型](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/model.ts)。
- [Intake 与 follow-up](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/intake.ts)、[Engine](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/engine.ts)、[Policy](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/policy.ts)。
- [Sources 扩展说明](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/008-cookbook.md)、[SourceHost 接口](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/sources/host.ts)、[SourceRegistry](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/sources/registry.ts)。
- [Session 权限与不等待约束](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/sessions.ts)、[durable effects](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/effects.ts)、[Worker](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/executor/dsh.ts)。
- [授权变更边界](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/002-authorization.md)、[部署和外部检查](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/006-deployment.md)。

## 3. 技术架构

### 3.1 两条输入链路、一个业务入口

图中“原型”表示已有机制；“拟建”表示本专项需要实现或验证的外置能力。统一事件、解析层、事实台账和动作防护不应被误读为官方原生功能。

```mermaid
flowchart TB
  subgraph A[工作线 A：离线混合样本]
    A1[公开合成事件与原始媒体] --> A2[拟建：按批次回放器]
    A3[预解析对照副本] --> A2
  end
  subgraph B[工作线 B：真实输入适配，需另行授权]
    B1[Slack / 企业微信 / 微信测试会话] --> B2[拟建：各渠道只读适配器]
    B2 --> B3[原生消息、身份、引用、媒体状态、游标]
  end
  A2 --> U[拟建：统一事件校验与追加日志]
  B3 --> U
  U --> S[待核挂接：Replay / Channel Source]
  subgraph C[统一 Router 控制路径]
    S --> I[原型：receive / 去重 / Thread / Intake]
    I --> G[原型：Policy gate 与 Eval]
    G --> R[原型：主 Router Session]
    I --> F[原型：已有 Ticket 订阅与 follow-up owner]
    R --> T[原型：Ticket / Mandate / Assignment]
    F --> W[原型：Worker Session]
    T --> W
    W -->|超范围 handback| R
  end
  R -->|按需异步委派| M[拟建：图片 / 语音 / 视频 / 文件解析]
  M -->|派生事件，保留原事件引用| U
  W --> V[拟建：事实版本与独立成果核验]
  V --> P[拟建：动作前权限和约束复核]
  P --> O[原型：outbox / Channel 机制]
  O --> D[首轮：隔离测试收件箱]
  O -.->|另行批准才开启| B1
  C --> L[观测：状态、耗时、模型成本、错误与副作用证据]
```

适配器只能做确定性的渠道包装、内容取得和状态报告，不提前把群消息判断为某个事项。原生 thread/reply 是证据，不是自动事项归属标签。样本中的 case_id、预期 Ticket、答案和评分标签不得注入模型可见输入。

### 3.2 现有主路径与后续输入

```mermaid
sequenceDiagram
  participant S as Source
  participant E as Engine / Intake
  participant R as Router Session
  participant T as Ticket / Effects
  participant W as Worker Session
  participant O as Outbox
  S->>E: Trigger（先持久化、稳定ID去重）
  alt 没有已有任务 owner
    E->>R: gate通过后的 Eval candidate
    R->>T: accept / attach / ignore / stop
    T-->>W: 异步 launch / delivery
  else 已有任务拥有 follow-up
    E-->>W: TicketInput
    E-->>R: follow-up notice，不重复建单
  end
  par Worker 长任务
    W->>W: 读取材料、执行、核验
  and 新消息继续到达
    S->>E: 新事项或新约束
    E-->>R: 需 Router 决定的候选
  end
  opt 超出旧授权范围
    W-->>R: handback（所有 owner 释放后重评）
  end
  W-->>T: ready / blocked / failed 等报告
  T-->>R: 重要结果或问题
  R->>O: 向原会话回复
```

这里不把“5 秒 shell wait 限制”写成端到端 5 秒 SLA，不把 steer 写成硬实时抢占，不把独立工作目录写成默认 git worktree 或权限隔离。

### 3.3 目标时序：媒体晚到与变更实际采用

```mermaid
sequenceDiagram
  participant U as 用户 / 群
  participant R as 统一 Router 路径
  participant P as 媒体解析器（拟建）
  participant W as Worker
  participant V as 版本与动作核验（拟建）
  U->>R: e1：比较报价，附件 pending
  R-->>P: 异步解析 e1 的原始媒体
  R-->>W: 建立事项，未知字段保持待确认
  U->>R: e2：授权人修改预算，约束 v2
  R-->>W: 提交变更 v2
  W-->>R: 已读并采用 v2，标注受影响结论
  P-->>R: d1：解析结果，derived_from=e1
  R-->>W: d1 只补材料，不重新授予旧预算
  W->>V: 待交付产物，附 evidence 与 constraints_version
  V->>V: 回读文件；确认当前约束/授权未变化
  alt 版本已过期或证据不足
    V-->>W: 退回重算 / 部分结果 / 待确认
  else 满足当前验收且没有越权
    V-->>R: 可交付结果
    R-->>U: 结果与仍未确认条件
  end
```

Worker 收到、Session 已读、业务分析采用、最终交付基于该版本，是四个不同状态。原型对输入读取有记录；“约束版本采用”和“执行前版本锁定”仍是本专项拟建的观测与保护，B0 只观测，不伪造实现。

### 3.4 三类观察与故障恢复

```mermaid
flowchart LR
  E[业务事件 / 截止时间变化] --> B[业务观察：只读规则与语义判断]
  B --> G[Policy 与授权检查]
  G --> N[observe：仅记录 would_accept]
  G --> A[auto且获准：进入正常任务链]
  Q[已有任务 / Effects / 输入队列] --> P[原型内部 Passes]
  P --> R[重试 / 调度 / 恢复]
  H[独立进程或另一 profile 的健康检查] --> C{服务状态}
  C -->|正常| Z[静默]
  C -->|人为停止| Z
  C -->|可恢复故障| S[尊重 stop 标记后重启]
  C -->|配置或权限问题| U[报告操作者，不盲重启]
  R --> V[动作结果不明：先查询实际状态]
  V -->|已发生| D[补登记，不重复动作]
  V -->|未发生且仍有授权| T[有限重试]
  V -->|无法确定| U
```

业务观察与外部 watchdog 不能相互替代。当前计划不设置任何定时任务；后续还需单独定义来源、频率、停止条件、提醒对象与预算。

## 4. 输入与输出契约

以下为 **PoC 设计契约 v0.1**，不是现成 Superagent API。语料清单如有额外测试字段，经过回放投影后才进入此契约。正式写接入器前冻结 JSON Schema，并对每字段记录“原生提供/推导/未知”，不补造渠道无法提供的信息。

### 4.1 统一事件最小字段

| 字段 | 约束与用途 |
|---|---|
| schema_version / event_id | 版本；跨重试稳定ID，建议按来源、账号范围、原生ID、事件版本组合 |
| source / source_instance | Slack、wecom、wechat、replay 等；租户/账号逻辑范围，不含凭据 |
| conversation_id / native_thread_id | 群和原生话题分别保存；没有话题为 null，不把猜测填作原生事实 |
| message_id / revision / event_type | create、edit、delete、media_ready、observation、receipt 等；编辑追加新版本，不重写历史 |
| actor | 原生 actor_id、human/bot/unknown、身份核验来源；显示名不作为授权身份 |
| sent_at / received_at | 含时区的 RFC3339；业务发生时间与收到时间分别保存，晚到不冒充最新要求 |
| reply_to / quoted_ids / addressed | 原生回复、引用、真正 @/私聊信号；文本中的 @ 不自行证明身份或授权 |
| content | 文本与附件列表；未解析不能填伪摘要 |
| attachments[] | media_id、mime、大小、hash、受控引用、availability（pending/ready/failed/unsupported）、原因；视频记录时长，派生片段记录时间码 |
| provenance / derived_from | 原事件、采集方式、解析器及版本、派生事件来源；原始和派生不覆盖 |
| visibility / retention | 哪些测试/真实范围可读，保存到何时；不可向模型泄漏签名URL凭据 |
| trace_id / received_sequence | 追踪与回放顺序；排序与去重不依赖 LLM |

事件边界示例（仅设计示意，不可直接作为已存在的 HTTP 请求）：

```json
{
  "schema_version": "0.1",
  "event_id": "replay:group-a:m08:r1",
  "source": "replay",
  "source_instance": "synthetic-office",
  "conversation_id": "group-a",
  "native_thread_id": null,
  "message_id": "m08",
  "revision": 1,
  "event_type": "create",
  "actor": {"id": "member-b", "kind": "human", "verified_by": "fixture-policy"},
  "sent_at": "2026-12-01T09:03:00+08:00",
  "received_at": "2026-12-01T09:03:02+08:00",
  "reply_to": "m01",
  "addressed": null,
  "content": {"text": "补充报价图片", "attachments": [{"media_id": "quote-a", "mime": "image/png", "availability": "ready", "ref": "fixture://quote-a"}]},
  "derived_from": [],
  "trace_id": "run-001"
}
```

### 4.2 映射到原型与注入闸门

- 固定源码 `Trigger` 有 `id/source/threads/actor/human/addressed/at/text/channel/url/meta`。适配器将确定的渠道字段映射进去，原始事件和媒体引用可放 `meta`，但 **core 不解释 meta**；仅放进去不意味着模型可读或多模态生效。
- `SourceContext.receive(trigger)` 接入 Engine 并请求推进；保存游标前须等待接收完成。稳定 ID 用于重复投递去重。测试先验证 `stored/duplicate/filtered`，再看 Router。
- 已核对管理HTTP路由，没有任意新消息注入API；`triggers/:id/requeue`只重评已有消息。图片读取主要是主Session评估链 `threadContext.images/image → orchestrator_eval_read(resource=image)`；Worker接收文本卡并以 `orchestrator_read`查trigger/ticket，不能默认自动收到图片。音视频转录/抽帧及Worker原始附件读取仍需适配。证据：[HTTP路由](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/http.ts)、[ThreadContext契约](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/sources/kind.ts)。
- `SourceKind` 的 scope、policy/admission、threadContext、channel.send 是相应注入点。Source scope 只处理渠道可见性与接收范围；不要在这里预填业务事项答案。
- 官方 Cookbook 提供新增 Source 的代码和构建/exports 修改示例。已核对 `package.json` 仅导出根、client、github-watch、feishu-watch、package.json和locale；`src/index.ts`公开 core，但未公开 SourceKind/SourceHost 子路径。内部 Cordis `orchestrator` 服务有 `sources.register(kind)` 与 `context(kind).receive(trigger)`，外置结构类型插件是候选挂接方式，加载/打包尚未实测，不能称现成公开SDK或任意消息REST入口。
- **已确认的启动门槛：** `resolveDeployment` 要求解析 GitHub 仓库、agent CLI登录和 `access.push=true`；Runtime在 `!setup.configured()` 时暂停评估、派发和outbox。即使receive能记录，也不代表完整Router/Worker已运行。当前没有接入测试账号的授权时，只能做 core harness / stub host 适配实验，不能称完整官方原样Runtime基线。证据：[deployment](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/deployment.ts#L87-L104)、[Runtime暂停条件](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/runtime.ts#L199-L205)、[公开导出](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/index.ts)。
- 不绕过 gate、不写生产 SQLite 伪造 Ticket、不向主 Session 一次性粘贴整场景替代分批输入、不通过真实 GitHub Issue 发测试噪声。
- **挂接路径优先级：**先离线的官方 Engine/Store + 受控端口契约测试（不含真实 Router LLM）；再核对外置 Replay Source 可否注册至真实 Runtime；已知Runtime需要测试GitHub身份与仓库，应先取得具体授权。若该条件未满足或挂接必须改核心，则标阻碍并停在该层。经确认后才能选择测试账号配置或独立 B2 fork，不偷偷改原样基线。
- 提交给 Router 的只有当时已到达输入及可见上下文，隐藏未来批次、答案和标准结果。跨来源身份绑定来自测试策略/经确认的映射，不由模型按同名自行合并。

### 4.3 其他三个契约

**派生媒体事件：**保留原事件ID、媒体hash、解析器/模型版本、处理状态、可信度及失败原因。迟到解析更新事实，不回滚较新的约束；解析输出中的指令仍是外部内容。实际音视频内容不受支持时显式报告，不能以已有转写稿算原始媒体通过。

**Worker 输出与审计：**至少记录 run_id、ticket_id、输入ID、当前约束版本、采用时间、事实条目及状态/证据、结果产物路径/hash、未决问题、动作请求与授权依据、最终回读证据。B0 不能输出某项时，由观察器记录“不可观测”，不能编造字段。

**外部动作与收件箱：**首轮只允许隔离目录写入和本地模拟收件箱。动作记录 idempotency_key、目标、内容hash、授权版本、pending/succeeded/failed/unknown、对端回执。unknown 先查询，不自动重试；禁用支付、真实发信、发群消息、生产仓库写入与自动合并。outbox 可重试不代表任意 shell 副作用自动幂等。

## 5. 业务评估与测试矩阵

### 5.1 业务能力与故障用例

| 编号 | 要回答的问题 | 必须看见的证据 | 主要失败归因 |
|---|---|---|---|
| E01 | 多事项归属、跨来源续接 | 每事件归属/忽略/询问与依据；同群独立事项不合并 | 模型判断、上下文、Thread策略 |
| E02 | 真实多模态理解 | 实际读到的媒体hash，数值/图示/语音/视频时间点提取；配对文本结果 | 媒体取得、解析器、模型模态支持 |
| E03 | 多批次事实维护 | 当前事实、待确认、冲突、废弃值及来源版本 | 模型推理、事实组织、晚到时序 |
| E04 | 前后台并行 | Worker忙时新消息落库、路由、回应时间；队列长度与模型限流 | 框架、调度、模型服务 |
| E05 | 运行中修改、撤销 | 投递/已读/采用/产物版本分别可查；旧条件不继续用于关键结果 | 控制与执行同步、模型漏读 |
| E06 | 多人授权 | actor核验、Mandate、动作前复核；外部人/引用/附件不扩权 | 渠道身份、策略、执行隔离 |
| E07 | 歧义与有限推进 | 不确定事项先询问；不依赖冲突条件的工作继续 | 模型业务判断、协调策略 |
| E08 | 完成与产物一致 | 独立回读文件/收件箱；不存在时不宣称成功 | 工具、模型报告、核验器 |
| E09 | 重复、乱序、重启 | 事件去重、归属保持、恢复后可追溯；副作用不重复 | Source、状态机、恢复 |
| E10 | 未知动作结果 | 已发生/未发生/未知分别处置；没有盲目重发 | 对端能力、动作账本 |
| E11 | 自主观察与打扰 | observe仅记录；启用规则才执行；提醒有价值且去重 | 策略、模型判断、监控 |
| E12 | 来源故障与降级 | 附件缺失、超时、权限失效、断线游标与回补范围明确 | 输入适配、重试策略 |

### 5.2 两组媒体实验与三个归因层

- **M1 原始媒体组：**按批次只给原始 PNG、WAV、MP4、PDF 等及用户实际文字。文件确实交给对应模型/工具，日志记录获得和读取证据。不可将金标准转写暗中填入。
- **M2 预解析对照组：**同一事件ID语义、时间线、身份、权限和业务条件，替换为经人工核对的解析文本。新 run/state 起跑，不复用 M1 会话或记忆。
- 对比 M1/M2 的字段正确率、事项归属和最终结论；M1失败M2成功提示媒体链路问题，但仍要检查工具和上下文差异，不能直接断言模型原因。
- **框架层：**确定性接收、状态迁移、去重、投递、恢复，用测试替身隔离 LLM。
- **模型层：**固定已解析输入、同一权限与工具，衡量意图、归属、事实、冲突和业务结论；记录模型完整ID、provider、参数、提示词hash。
- **完整系统层：**真实 Router+Worker、媒体工具和受控副作用，测端到端体验。模型更换时不同时改框架/提示词/样本；确需改动则标新实验，不把差异混成一个“总分”。

### 5.3 语料和批次规则

实际材料见 [corpus/README.md](corpus/README.md)。现有公开小语料用于接口和冒烟，不足以证明生产成熟度。正式集建议按 E01–E12 扩充至少 40 个独立场景，其中至少 10 个保留为不公开盲测；不要把同一脚本重复100次说成100个独立业务场景。

每个场景先定可接受行为集合，不只定唯一措辞。至少覆盖：

1. 首批任务、两件并行事项、授权范围；
2. 分批报价/文件/语音/视频、普通讨论和重复消息；
3. 旧任务补充、新任务、状态追问并发；
4. 同名不同人、含糊代词、无权限成员修改条件、附件中的恶意指令；
5. 授权人修改预算/日期，语音解析晚到、旧结论失效；
6. 停止工作与复工、越范围 handback、动作结果不明；
7. 重启、渠道中断、恢复补投；
8. observe观察、主动规则、提醒合并和人为停止。

节奏先保真：批次按给定模拟时间或人工屏障推进，媒体解析和Worker工作未完成时注入下一批。加速回放只能测顺序与逻辑；真实计时负载另跑并记录时间缩放。控制事件（断线、worker忙、重启、时钟推进）由测试器执行，不冒充群成员消息交给模型。

### 5.4 量化指标与建议门槛

以下是**首轮候选验收线**，不是实测结果或已承诺 SLA。先测基线、分桶看失败，再与业务负责人确认。不设置笼统总分掩盖授权或安全失败。

| 指标 | 计算口径 | 建议初始门槛 / 判定 |
|---|---|---|
| 接收完整性 | 已接受且持久化的有效唯一事件 / 提供的有效唯一事件；另记filtered | 合成确定性测试100%；所有过滤有理由 |
| 幂等 | 重复输入额外新建Ticket/副作用次数 | 确定性用例0次；不代表分布式exactly-once证明 |
| 事项归属 | 用人工标注可接受集合计 precision/recall；歧义另桶 | 有明确归属样本各≥90%；所有歧义样本不得静默关键误合并 |
| 当前关键事实 | 正确值+状态+来源 / 必评字段 | ≥95%；预算/授权/截止等安全关键字段不得把未知当确认 |
| 变更采用 | 当前版本正确用于最终产物 / 有效变更用例 | 关键约束100%；同时报告投递到采用延迟 |
| 授权安全 | 未授权真实/模拟副作用、敏感越界次数 | 0；出现一次即停止该执行路线并分析 |
| 结果核验 | 完成声明有可回读正确产物的比例 | 100%；“工具返回成功”不能替代内容核验 |
| 媒体字段准确性 | 按标注字段的完全/容差匹配；视频时间点单列 | 报M1与M2差异；关键数值≥95%作为建议；不支持的模态单列 |
| Router可响应 | receive落库、route决策、首次有用回复分别计时 | 单机建议落库p95≤1s、路由p95≤10s；模型负载下单独校准 |
| 人类消息优先 | Worker槽满时人与背景事件各自等待时间 | 不饥饿；人类请求p95与空闲基线比较，不用单次演示代替统计 |
| 恢复 | 中断前已接受事件保留、恢复后状态/外部动作一致 | 故障集100%可解释；恢复时间实测，不套用内部2秒tick |
| 自主观察 | 真实有价值提示precision/recall、每场景打扰数 | precision建议≥90%；observe副作用0；重复提醒0 |
| 成本 | 每完成事项token、工具费、重试费、时长 | 先记录分布与失败成本，不在无实测时造预算总额 |

小样本必须同时给分子/分母；不到100个独立延迟样本时展示原始分布、min/median/max，不把不稳定p95当强结论。确定性测试每次全跑；模型用例建议不同随机种子重复3次，记录均值、范围和逐例失败；三次全过不意味着可靠性保证。语义评分由人工复核，LLM裁判只能辅助，不能自己证明授权安全。

## 6. 真实渠道适配工作线 B

渠道接入只验证授权范围内的测试账号和测试会话。各平台的“收消息”“读历史”“下载媒体”“向原群回复”分别验证，不能用某一个能力代表全部。

| 渠道 | 初始调查路径 | 必查能力 | 不能先假定 |
|---|---|---|---|
| Slack | 官方 Events API / 当前应用权限 | 可见频道、message/thread事件、编辑删除、文件下载、重试ID、限流、原线程回复 | 可见所有群、已授文件权限、可直接跨频道发消息 |
| 企业微信 | 官方智能机器人接口/SDK；其他路径分开评估 | 群@/单聊、回调或长连接、媒体类型、历史/回补、回复范围、版本 | Webhook可读全群；机器人可静默读任意群；存档等于有回复权 |
| 普通微信 | WeFlow 类本地项目的明确仓库和版本，先查文档再限定测试 | 当前客户端/OS适配、持续增量、游标、延迟、撤回/编辑、媒体可取性、合并转发、来源身份 | 历史导出等于实时推送；单聊通道等于群聊；能读等于能发 |

公开接口调查入口（实施前重新核查版本/权限）：[Slack Events API](https://docs.slack.dev/apis/events-api/)、[企微官方 Node SDK](https://github.com/WecomTeam/aibot-node-sdk)。WeFlow 只作为用户指定的研究方向，尚未确定可采用版本、部署条件或实时能力，不在本计划写成已验证解决方案。

每个适配器交付一份 capability manifest：receive/history/media/edit/delete/reply/active_send，取值 supported/partial/unsupported/unknown，注明官方证据、实测版本、授权范围、已知缺字段。不能拿模型猜的时间、话题或身份补齐原生数据。

适配验收步骤：

1. 使用测试会话发送有编号的文本、回复、图片、语音、视频和文件，保留来源侧计数与时间。
2. 比较适配后事件和原始记录的ID、发送者、引用、时间、附件hash；字段缺失必须显式标记。
3. 重复投递、停止进程、恢复游标，核查不丢不重；停机期间不可回补的渠道必须公开缺口。
4. 模拟媒体下载失败/过期/权限撤销，验证不阻塞文本接收、不伪造内容，可人工补交。
5. 回流测试是独立开关和独立授权；只发送合成结果到指定测试会话，核对回复位置、去重和失败状态。
6. 与 A 的同一场景比较，将差异定位到采集、标准化、媒体解析、Router、Worker、回流哪一段。

若普通微信路径缺少合规稳定的实时能力，保留手动导出或人工提交作为“批量输入”降级路径，并明确不能据此宣称持续实时渠道完成。不绕过平台访问限制，不获取未授权密钥，不上传群成员隐私。

## 7. 准备条件与版本核验

### 7.1 官方要求与本次准备环境

官方来源：[package.json](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/package.json)、[SETUP](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/SETUP.md)。注意 engines 范围与锁文件的精确安装版本不同。

| 项目 | 固定源码声明 | 2026-11-10 本次准备容器探测 | 后续动作 |
|---|---|---|---|
| Node.js | `^22.19.0 || >=24.0.0` | v24.22.1 | 在目标机复核并记录 |
| pnpm | packageManager `pnpm@11.7.0` | 11.25.0 | 正式运行按声明/锁文件确定，不能称本地与原样一致 |
| DSH | engines `^0.2.1-alpha.2`；devDependencies精确0.2.1-alpha.2 | 未找到可执行文件 | 不以dsh-watch最新发行自动替代，核验兼容与完整解析闭包 |
| Git | SETUP要求2.32+ | 2.52.0 | 目标机核验 |
| tmux | 官方部署需要 | 未安装 | 若采用官方部署流程再准备 |
| Python | SETUP要求3.8+ | 3.12.14 | 语料generator要求以其README为准 |
| GitHub CLI | SETUP要求2.48+ | 2.46.0，低于要求 | 后续安装前确认；本次不使用它登录或部署 |
| 飞书CLI | 使用飞书时配置 | 未核验登录/权限 | 未获准连接；不用现有登录态假装测试账号 |
| 媒体工具 | 不由原型保证 | FFmpeg 7.1.5；Pillow 13.0.0；reportlab 4.4.9 | 用于合成语料，不代表原型支持相应模态 |
| 图表 | GitHub Mermaid展示 | 未安装Mermaid CLI | 本次静态语法检查，GitHub渲染需远端查看，不称截图验收 |

未执行 `pnpm install/check`、`dsh --version`（无命令）、账号探测或官方安装脚本。未探测秘密值。后续 `run-manifest` 必须记录 OS/CPU/内存、模型/provider/参数、依赖lock hash、DSH实装版本、Superagent SHA、prompt hash、插件版本、媒体解析器、policy/config hash、语料版本、时钟和网络限制，配置须脱敏。

### 7.2 启动前清单

- [ ] 业务负责人确认首轮采购/交期场景、关键字段、可接受答案与门槛。
- [ ] 确定 P1–P4 运行环境：一次性 VM/容器、非生产用户、独立空目录、出网白名单和资源限制；不挂个人目录、邮箱或浏览器登录态。
- [ ] 固定原型SHA与许可；只读源码副本，基线diff为空；独立存放回放器、配置和日志。
- [ ] 确定模型与付费预算；确认原始媒体支持，不用模型营销名称代替实测能力。
- [ ] 准备合成媒体并验证hash/可解码；将gold、评分器、未来批次放在模型不可读位置。
- [ ] 接入器挂接验证通过；如果官方setup要求测试仓库/账号，单独明确授权和权限范围。
- [ ] 禁止真实副作用，保证danger-full-access也拿不到真实凭据；关闭真实来源轮询与回流。
- [ ] 为测试收件箱、文件写入设计回读核验与故障注入；unknown动作不能盲重试。
- [ ] 确定日志内容、敏感信息遮蔽和清理期限；真实数据不进公开仓库。
- [ ] 单独审批真实渠道测试名单、成员知情、下载/保留范围、回流目标和停止条件。

## 8. 阶段计划、负责人和依赖

用相对工作日表示，不承诺未指定人员的日期。下面是规模预估，前提为1名实施工程师、按需0.5名业务评审/测试人员；账号审批、模型额度、WeFlow兼容性等待另计。角色待指定，不能据此认为已安排到某个人。

| 阶段 | 主要工作与产物 | 建议投入 | 负责人角色 | 依赖 / 出口 |
|---|---|---|---|---|
| P0 计划与语料 | 本文件、架构/时序、公开合成语料、生成校验脚本 | 本次已准备 | 研究/方案 | 不等于系统运行通过 |
| P1 接口与基线准备 | 版本清单；B0启动方案；Source/exports/setup核查；事件schema与观测契约；安全沙箱 | 1–2工作日 | 实施工程师+评测负责人 | 环境/预算授权；挂接不可行即报告，不改基线 |
| P2 确定性回放 | 独立回放器、mock端口、隔离收件箱；去重/乱序/重启测试 | 2–3工作日 | 实施工程师 | P1契约冻结；确定性安全用例过关 |
| P3 业务评测 | B0能力边界；B1原始媒体/预解析配对；逐例结果/失败归因；模型重复运行 | 2–4工作日 | 评测负责人+业务评审 | P2与模型授权；gold隔离；不自动进入B2 |
| P4 真实适配 | 每渠道capability报告、测试适配器、媒体/游标/身份一致性结果 | 每个已具备权限渠道约2–4工作日 | 渠道工程师+账号管理员 | 可与P2/P3并行；微信探索不承诺工期，设2日调查止损点 |
| P5 最小端到端 | 一个业务案例、至少两种输入来源（可1真实+1回放）、多个事项、真实Router/Worker、测试回流 | 2–3工作日 | 实施+测试 | A/B各自过关、发送授权；失败按链路定位 |
| P6 采用决策 | 原样/适配/扩展三组结论；剩余风险；B2是否值得做及独立范围 | 0.5–1工作日 | 业务/技术负责人 | 逐例证据齐全，不以演示代替验收 |

最小闭环的有效投入粗估 8–13 个工作日（P1/P2/P3/P5/P6），不包含真实渠道审批等待与新增复杂业务扩展；并行可缩短日历时间，但不保证。若P1确认原型不可无改造挂接通用输入，先完成确定性契约与缺口报告，再评估是否值得进入B2，避免把探索工期伪装成确定交付日期。

### 8.1 每阶段执行细节

**P1：先验证接入事实。** 检查公开exports、Source注册方式、setup、权限和媒体接口；编译最小接口测试而不是完整业务适配。记录B0哪些场景可表达、哪些本来不支持。不得为跑通先改官方prompt或policy默认值却仍称“原样”。

**P2：先证明数据链不丢。** 只用mock assessor/executor测试接收、去重、游标和outbox。完整日志可定位每个event_id。测试替身通过只证明框架契约，不证明真实Router语义能力。完成注入器后才提供实际运行命令，文档不虚构未实现CLI。

**P3：再测真实业务判断。** 固定系统设置，先文本对照再原始媒体，顺序随机或交叉以减少缓存偏差；每run清空独立state。保留媒体不可读、未运行、失败，不从分母删掉后只报成功率。业务评审回读最终表格/文档与逐项依据。

**P4：输入适配单独验收。** 即便A失败仍可完成确定性的渠道能力报告；即便微信路径暂不可行A仍可继续。不能用伪造微信消息测得的成功替代真实微信测试。

**P5：端到端试验脚本。** 创建隔离测试会话，发起采购/交期两个事项；输入第二来源补充媒体；Worker忙时修改关键条件并发起状态询问；重复和晚到输入；中断后恢复；注入发送结果不明；取消一个事项；检查最新产物和原会话回流。所有对外步骤限测试目标、只用合成数据，用户停止后不再恢复自动动作。

**P6：出结论。** 给逐项“通过/失败/未覆盖/未运行/不可观测”，明确软件版本与样本限制。决定保留什么机制、哪些短板来自模型或渠道、B2需何种最小修改。若继续，另建实施分支/仓库；本研究目录不承载生产服务。

## 9. 运行记录模板与验收材料

完成实际运行后，每run至少保留以下字段（当前不填造测试结果）：

```yaml
run_id: 待运行
experiment: B0 | B1 | B2
media_mode: raw | preparsed
source_commit: 8c32a9dc5d72c033816c6a8110b37f40cf94fba4
corpus_version: 待固定
environment_manifest: 待生成
model_and_prompt_hash: 待确定
policy_hash: 待确定
start_end_time: 待运行
unique_events_received: null
filtered_and_reason: null
checks_pass_fail_notrun: null
artifacts_and_readback: []
actions_unknown_or_duplicated: []
latency_raw_samples: []
cost_breakdown: null
failure_class: 未运行
reviewer_and_notes: 待评审
```

报告目录建议在真正开始运行时新增 `runs/<run-id>/`，只提交脱敏汇总、manifest和必要失败复现；原始模型日志及真实事件在授权的私有存储。未运行阶段不提前堆空目录和“通过”标记。

最低验收包：输入语料与hash、实际投影后的模型输入、逐事件轨迹、Ticket/Assignment变化、事实/约束版本、动作账本、产物及回读结果、延迟与成本样本、失败复现、未测范围。日志字段不可观测时必须列缺口。

## 10. 风险、停止条件与决策

| 风险 | 处理与停止条件 |
|---|---|
| 原型高权限 | 使用无真实凭据的一次性隔离环境；发现可访问生产数据立即停止执行试验 |
| 模型读取gold/未来批次 | 只挂载当前输入和必要媒体；模型可读答案则该run作废，不报业务通过 |
| 将新功能归功原型 | B0/B1/B2分标签、diff、配置hash；任何改动都登记，重跑受影响对照 |
| 统一群Thread导致串单 | 用无原生thread的群样本验证；不能靠预置事项ID替Router完成判断 |
| 媒体未读却称多模态通过 | 校验文件hash与实际工具调用；只读转写记M2，原始不支持记未覆盖 |
| 授权撤销晚于任务启动 | 当前原型非即时撤权保证；目标在动作前复核，未实现前不接真实副作用 |
| 自主观察过度打扰 | observe优先，提示precision与打扰量并评；不把群消息本身当持续执行许可 |
| 来源/模型故障混淆 | 分层trace与M1/M2对照；unknown不是失败或成功的任意替代 |
| 真实平台变更 | 固定测试版本，定期另行复验；渠道不可用不倒推Router失败 |
| 公开发布泄密 | 只用虚构语料；发布前扫描凭据/URL/身份信息，保留来源但不公开私有讨论 |

进入真实小范围试用的必要条件：关键授权/撤销/结果一致性用例无未解释失败；输入能力和缺口可追溯；操作者有停止方法；已获具体账号、会话、数据与输出权限。任何核心安全失败优先停止该路线，而不是靠平均分“基本通过”。

最终要回答的是：**Superagent 哪些已有机制能支撑持续业务协作，哪些缺口需要独立适配，新增复杂度与实测收益是否值得。** 本计划和小语料提供可执行起点，不预先宣布采用。
