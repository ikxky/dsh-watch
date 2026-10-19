# dsh 适合承担什么工作

**dsh 是一个围绕工作区执行任务的 Agent 工作台，并提供可嵌入其他产品的运行框架。** 用户可以交代任务、提供文件、先审计划、观察工具执行，再检查助手交出的结果。它有价值的产品组合是把这些环节放在连续会话里，并允许按任务增加工具和子代理。[官方说明][readme]、[使用指南][guide]

当前更适合作为企业 Agent 平台和个人助理的研究对象。已有机制有助于设计委派、监督和续接体验，但组织身份、多人授权、结果验收与总费用控制仍需分别确认或由上层产品承担。官方将本版本列为开发者预览，声明未经安全审计；本项目目前没有生产运行时采用结论。[安全声明][safety]

本页保留产品定位与选型概览。系统评测从[14维总览](CAPABILITY-MAP.md#评测维度总览)开始，按00–13逐维阅读定义、判断依据、当前表现和待验证事项，再到[36项能力证据索引](CAPABILITY-MAP.md#evidence-index)核对支持状态；扩展条件与演进仍在[插件指南](PLUGINS.md)。框架要求、已有能力和运行成熟度分别判断，未查明处保持待评。

研究推进至 **v0.2.1-rc.2**／`687f282e8625c6b8d11ff58211a90524be2e4317`，最近核查 **2026-10-19**。未受本周增量影响的既有分析保留 alpha.2 固定证据，新增条件以本周报告和下文为准。结论来自官方文档、源码与发行包静态分析，没有安装或运行 dsh，也没有调用模型。下列场景是基于已有能力的适用性推断，不是成功案例。

本周的采用前检查新增三项：Web／Desktop 的已保存凭据优先，Headless 默认仅走环境／`.env`；第三方插件优先按 `engines.dsh` 判断兼容，自定义市场需启用并添加索引；新版 Search／Fetch 需主动选择，启用后搜索默认可附带截断的用户问题，抓取交由远端。SDK resume 和 Minimal 图片／压缩增加接入选择，但不证明外部进程恢复、可靠完成或生产安全。详见[本周相邻版本分析](releases/v0.2.1-rc.2.md)、[凭据优先级](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/credentials/credentials-local/README.zh.md)、[自定义市场](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/boot/plugin-market/README.zh.md)、[Search／Fetch 固定说明](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/web/web-deepseek-api/README.zh.md)。

## 哪些场景值得优先研究

**围绕一组文件完成有边界的工作。** 例如，请助手阅读工作区材料、形成分析或修改文件，并让用户检查过程与结果。前提是文件格式有对应读取能力、工作范围与权限明确。当前成果卡片指向工作区源文件；远程下载、冻结交付版本和长期保留不能默认承诺。[工作空间与成果交付](CAPABILITY-MAP.md#dimension-05)

**需要边做边讨论的多步骤任务。** 用户可以先讨论计划，执行中补充约束，必要时取消，并在之后回到会话。长期目标能继续推进，压缩能帮助对话延长，但摘要不保证无损，恢复也不会自动重新授权持续推进。适合研究人如何保持控制；还不能据此承诺无人值守长期工作的成功率。[进度与控制](CAPABILITY-MAP.md#dimension-02)、[工作续接](CAPABILITY-MAP.md#dimension-06)

**为已有产品增加局部执行能力。** 程序接口可以发起任务、订阅事件并等待受管理子任务。接入方仍需要提供业务入口、用户身份、结果验收和异常处理。当前未确认官方聊天软件收件入口，也不能把程序返回值直接展示为“业务已完成”。[任务入口](CAPABILITY-MAP.md#dimension-01)、[完成判断](CAPABILITY-MAP.md#dimension-06)

## 一项工作在这里怎样展开

**从交代需求到接受结果，用户需要参与哪些环节？** 一个可用的产品流程可沿以下顺序设计。它是对当前机制的归纳，不表示本项目已端到端验证。

1. **交代任务和工作范围。** 选择工作区，写清预期结果，附上所需材料。外部工具和模型需要预先配置；上传成功不等于内容已被理解。
2. **先看计划，再放行需要权限的动作。** 计划有助于讨论方法，权限审批决定特定动作能否继续。计划模式的提示词不能代替文件权限；入口不同，默认授权也可能不同。
3. **跟进执行并处理变化。** 用户查看过程、补充信息或取消；助手可使用工具和子代理。取消与资源释放可能先后发生，外部动作结果未知时需要核对后再决定重试。
4. **查看交付物并验收。** 检查实际文件和业务标准，区分主助手回复结束、子任务结束与验收通过。需要留下证据时，保存任务记录，并另行安排文件版本与保留。

流程中最值得借鉴的，是把计划、执行记录和人工介入放在同一个连续任务里。最需要验证的，是用户看到的状态能否准确对应真实结果，尤其是取消、子任务和外部系统操作。[逐项能力与证据](CAPABILITY-MAP.md#evidence-index)

## 原生提供什么，上层产品还要负责什么

**选择 dsh 作为执行基础后，哪些工作仍属于产品团队？** 原生机制主要围绕一次或一系列会话：交互入口、模型与工具执行、会话记录、计划、部分审批、子代理、续接和插件组合。具体能否使用，还要看入口、会话模式、操作系统及配置；原生可组合不代表全部默认开启。[插件选择与条件](PLUGINS.md)

上层平台需要明确业务责任：谁发起并拥有任务，哪些资料可读、哪些动作可做，什么叫成功，失败由谁接手，成果保存哪个版本，以及整项工作允许花多少钱。当前资料不足以确认 dsh 已提供完整的组织登录、角色与租户授权、Agent 上下线流程或业务验收指标。将这些能力放在外部是可行的产品分工判断，不是已验证的集成方案，也不应据此判定 harness 本身失败。[团队服务边界](CAPABILITY-MAP.md#dimension-12)

多 Agent 的 Team 也要与多人业务协作区分。它提供实验性的任务板和成员消息，并不自动赋予多人共享、审批和交接的组织契约。外部记忆与业务连接器同理：它们增加访问能力，数据权限、来源、保留和删除仍需要明确的责任方。[协作](CAPABILITY-MAP.md#dimension-12)、[外部能力](PLUGINS.md)

<a id="decision"></a>

## 当前如何做采用判断

**现在可以借鉴什么，哪些承诺需要先拿到证据？** 本轮判断如下；没有实测支撑的部分保留为验证目标。

- **采用：** 暂无生产运行时采用项。尚未完成目标业务、权限或可靠性验证。
- **借鉴：** 计划与审阅、执行过程回看、显式恢复长期目标、区分主任务与子任务状态，以及按任务组合能力。
- **验证：** 完成与验收如何关联，取消和未知副作用怎样处理，远程文件如何交付，各入口权限是否符合用户预期，以及模型兼容和数据外发控制。
- **观察：** 实验性 Team、自动评审、工作树及兼容桥接能否形成稳定的任务体验，发行内容与历史迁移是否可预测。
- **跳过：** 本轮不投入字体、语音识别效果等与核心接入判断关联较低的细节，也不开展部署或模型试用。

接入前尤其需要看清三件事。第一，文件沙箱和工具审批没有构成完整的组织隔离；精简程序入口甚至与基础入口使用不同权限默认值。第二，默认会话日志、显式反馈、包清单与 Desktop 产品交互采集是不同的数据通道，不能用一个遥测开关推断全部关闭。第三，用量记录、轮数和单次输出限制，不等于覆盖主任务、子代理、压缩、重试等费用的总预算。证据及后续问题见[关键发现](FINDINGS.md)、[插件数据通道](PLUGINS.md#data-channels)。

尚未知的是实际任务成功率、取消和崩溃恢复表现、吞吐时延、目标模型兼容程度，以及按业务任务归集的真实费用。2026-10-19 的专项检查未见已发布安全公告，这也不能抵消未经安全审计的声明；检查范围见[跟踪记录](TRACKING.md)。

## 技术审阅依据

以下保留影响产品承诺的实现依据；当前条目状态仍以[能力证据索引](CAPABILITY-MAP.md#evidence-index)为准。

### 执行、持久化、集成、权限和数据通道的关键依据

**执行与完成。** 一次模型请求及其工具执行构成 step，若干 step 构成 turn；输入经持久 inbox 准入。源码对可并行工具使用有界池，默认上限10，独占工具形成屏障；不能据此假定任意写操作互不冲突。SDK `session/wait` 复核根与受管理后代的空闲状态，`HarnessSession.run()` 仍在根首次 idle 后返回；最后助手文本未必只因果归属于本次 prompt。取消是协作式，超时返回不保证资源完全释放，根上下文关闭时最终 `turn/end` 可能未持久化。[架构][architecture]、[工具调度][tool-calls]、[循环契约][loop]、[wait 实现][wait]、[run 实现][run]、[超时修复](https://github.com/deepseek-ai/deepseek-harness/commit/dbb150ff0e589ec5b34a261c201a853affe71a29)

**会话与恢复。** 追加事件日志是持久事实，模型上下文由其派生；逻辑格式当前为 v4。写入旧格式时生成新代际并保留旧代际，不代表通用降级；硬中断前的流片段也可能尚未结算持久化。恢复区分未启动与结果未知，不能代替外部事务对账。[格式状态][format]、[循环与故障][loop]

**长工作与资源。** Goal 恢复或分叉后不自动续行，轮数不等于金额或时长预算。压缩可先修剪超大工具结果，再额外调用模型摘要；无法缩小所有系统提示词、工具目录或不可分单元，也不保证语义无损。[长期目标][goal]、[压缩][compaction]、[重试][retry]

**扩展与入口。** Cordis 插件组合可替换执行循环、模型、工具、持久化和界面；Host 插件在宿主进程中执行。Web、Headless、SDK、SDK Minimal 和 ACP 的工具与交互不同，Desktop 携带匹配运行时。Skills 扫描项目、自定义和用户目录，摘要与正文按需加载；指令不是权限凭证。TypeScript 与 Python SDK 驱动独立运行时，协议、包与运行时版本需要一起核验。[架构][architecture]、[插件管理][plugin-manager]、[Skills][skills]、[Python SDK][python-sdk]

**远程与隔离。** Web 默认监听回环地址，可配置 IPv4／IPv6、原生 TLS 和代理外部地址。启动 token 与签名 cookie 承担浏览器认证；公告地址、Host 接纳与身份认证各自独立。证书启动时读取，签发续期由运行方负责。文件沙箱按平台采用 bwrap／Landlock、Seatbelt 或 Windows ACL runner，不可用时失败，也有 partial 能力差异；它与 Python 文件策略均不应被解释为完整网络或多租户隔离。同一系统用户运行的工具仍可能接触本地凭据。[远程指南][public-deploy]、[连接鉴权][connection]、[沙箱][sandbox]、[Python 文件策略][python-policy]、[本地凭据][credentials]

**审批与观测。** Auto review 默认关闭，可额外调用模型后以 Full access 执行；可能误判，不覆盖程序化工具全部直接 Node 效果，也不持久化全部审查细节。日志重建应使用持久 `session/event`，`agent/*` 主要用于实时协调；事件可回放不自动具有防篡改、组织审计权限或保留策略。[自动评审][auto-review]、[生命周期][lifecycle]、[统计][stats]

**出站与升级。** 基础组合中的 Session Log 默认启用，请求字段可增量携带完整规范事件；反馈 OTel 默认在显式反馈后释放日志前缀，另有包清单与 Desktop 交互采集。其目标、保留与自定义端点行为仍需分别验证。alpha.2 的 pi-ai 依赖从0.87.1到1.0.2；本周 rc.2 manifest 已为 `^1.1.0`，Azure 名称迁移见[本周报告](releases/v0.2.1-rc.2.md)；预稳定接口、会话格式与插件发行内容要分别跟踪。抽查归档不能替代完整供应链或漏洞审计，本项目未扫描 CVE。[会话日志][session-log]、[默认配置源码][log-source]、[反馈遥测][otel]、[包清单][inventory]、[依赖锁定][lock]、[发行内容](PLUGINS.md#发行包核验与版本纪律)

下一步阅读：[14维评测总览与分析](CAPABILITY-MAP.md) → [36项能力证据索引](CAPABILITY-MAP.md#evidence-index) → [插件实现与版本依据](PLUGINS.md) → [关键发现](FINDINGS.md)。历史变化见 [EVOLUTION](EVOLUTION.md)，当前版本的具体增量见 [v0.2.1-rc.2](releases/v0.2.1-rc.2.md)。

[readme]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/README.zh.md
[guide]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/user/guide/index.zh.md
[safety]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/SAFETY.zh.md
[architecture]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/architecture.zh.md
[tool-calls]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/src/tool-calls.ts
[loop]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/README.zh.md
[wait]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/sdk/server/src/server.ts
[run]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/sdk/client/src/api.ts
[format]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/session-format-status.zh.md
[goal]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/goal/goal-round-driver/README.zh.md
[compaction]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/compaction/compaction-basic/README.zh.md
[retry]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/llm/llm-retry/README.zh.md
[plugin-manager]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/boot/plugin-manager/README.zh.md
[skills]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/skill/skill-filesystem/README.zh.md
[python-sdk]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/python/sdk/README.zh.md
[public-deploy]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/user/guide/public-deployments.zh.md
[connection]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/client/connection/README.zh.md
[sandbox]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/sandbox/sandbox-local/README.zh.md
[python-policy]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/ptc-runtime-python/README.zh.md
[credentials]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/credentials/credentials-local/README.zh.md
[auto-review]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/auto-review/README.zh.md
[lifecycle]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/agent-lifecycle.zh.md
[stats]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/session-stats/README.zh.md
[session-log]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/session-log-deepseek/README.zh.md
[log-source]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/session-log-deepseek/src/index.ts
[otel]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/session-telemetry-otel/README.zh.md
[inventory]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/llm/plugin-package-inventory-deepseek/README.zh.md
[lock]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/pnpm-lock.yaml
