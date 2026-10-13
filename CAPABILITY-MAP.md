# dsh 能帮用户完成什么工作

**dsh 是让用户把任务交给 Agent、在工作区中持续执行并查看过程的工作台，也提供供其他产品调用的运行框架。** 它把对话、文件、工具、计划和子代理放进同一工作过程。对产品团队，值得研究的是这套“委派—监督—交付—续接”体验；目前还不能据此承诺企业多人服务的完整治理或生产可靠性。[官方产品说明][readme]、[安全声明][safety]

按当前资料，适合优先研究的场景是：围绕一组工作区文件开展分析或修改、把有多个步骤的任务交给助手并持续审阅、让现有应用调用 Agent 执行局部工作。这些是**产品适用性判断**，不是本项目完成过的任务案例。前提是有人明确工作范围、配置所需模型和外部资源，并检查结果；上传文件、调用工具或回复结束，都不能单独证明业务目标完成。

最影响选型的限制有四个：文件卡片不提供内置的访问者下载或不可变副本；任务恢复不能替外部动作消除重复和未知结果；长期记忆、组织权限与整项任务费用上限需要分别设计；官方仍声明开发者预览、未经安全审计。当前姿态为**借鉴、验证和观察**，暂无生产运行时采用结论。

下面沿着用户完成工作的顺序阅读。正文解释当前行为和使用边界；每节末的核验记录直接列出稳定能力 ID、证据、配置条件与下一步问题。

1. [从哪里交代任务](#start)
2. [如何看进度、改主意和叫停](#control)
3. [哪些决定留给人](#approval)
4. [能使用哪些文件、系统和模型](#resources)
5. [如何收到成果并确认完成](#delivery)
6. [过几天回来，怎样接着做](#continuity)
7. [失败或中断后怎么办](#recovery)
8. [多个 Agent 如何合作](#collaboration)
9. [怎样扩展成自己的工作方式](#extensions)
10. [面向团队提供服务，还缺哪些环节](#operations)

本页对应 **v0.2.1-alpha.2**，固定提交 `d743267388641bc76f17c45ce8b4c231aed1d32c`；能力证据核查日期为 **2026-10-13**。本轮是阅读结构重写，没有新增运行验证。默认值均以新配置、无用户覆盖为条件。参考 [LLM 101 的 Agent 产品设计文章](https://llm101.ai/agent-product-101-product-design-checklist/) 从任务与使用体验提问，按 dsh 的既有证据重新组织；该文章不作为 dsh 规范，也不用于评分。

<a id="start"></a>

## 1. 从哪里交代任务

**我能直接把工作交给它，还是需要先开发一个入口？** 个人使用可从 Web 或 Desktop 工作区发起会话，写下任务并附上文件。比如，要求助手围绕已有材料整理分析，再在同一会话里追问。文件上传解决的是把材料送入工作区；某种文档能否读懂，仍取决于模型、读取工具和文件限制，不能把上传成功当作已理解内容。

现有业务产品也可以通过程序接口发起任务、订阅过程事件。这里需要产品方自己提供任务表单、状态显示和结果验收，不能直接照搬 Web 的交互与默认权限。程序收到返回值时，工作可能只结束了当前主会话的一段活动，完整完成条件见[成果交付](#delivery)。

如果希望从聊天软件收件，当前资料尚未确认官方 Slack、飞书等会话及附件入口。实验性 GitHub 事件入口可在配置规则后触发工作，但接到事件的回执不证明规则已执行，也不证明已存入可恢复的队列。将它用于业务自动处理前，要先确定谁负责重试、重复事件和丢失事件；本页不据此否定社区连接器的可能性。

### 核验记录：适用条件、固定来源与待确认问题

<a id="cap-in-01"></a>

**CAP-IN-01 · 从工作区会话输入任务与附件**

支持；已读源码；归属默认插件。条件为Web；文件上传插件与会话 UI。支持输入和文件保存，不证明模型能理解每一种上传格式。

依据：[Web 组合配置][web]、[使用指南][web-guide]。后续核验：各文件类型的读取工具和大小限制是否与界面提示一致？

<a id="cap-in-02"></a>

**CAP-IN-02 · 程序调用与事件订阅**

支持；已读源码；归属默认插件。条件为Headless／TypeScript、Python SDK；相应 profile。不同入口的交互、默认工具和权限不同；调用返回不自动表示业务成功。

依据：[SDK 契约][sdk]、[等待实现][sdk-wait]、[SDK Minimal 配置][sdk-minimal]。后续核验：逐项补齐 SDK、Headless 与 ACP 的交互及权限差异。

<a id="cap-in-03"></a>

**CAP-IN-03 · 官方 IM 会话与附件入口**

待确认；仅文档；归属外部平台／连接器（实现待确认）。条件为固定版本产品与插件资料检索范围。本轮未确认官方 Slack、飞书等运行入口；不据此断言不存在社区接入。

依据：[产品说明][readme]、[包目录][packages]。后续核验：是否有已发布、可验证的官方 IM 包及收件／附件契约？

<a id="cap-in-04"></a>

**CAP-IN-04 · 外部事件触发 Agent 工作**

部分；仅文档；归属官方可选。条件为实验 GitHub webhook／规则 runtime，显式配置。签名校验与202接纳不等于规则成功或持久队列落盘。

依据：[事件入口说明][webhook]。后续核验：入口、队列持久性、重试与业务幂等分别由谁负责？

<a id="control"></a>

## 2. 如何看进度、改主意和叫停

**交出去以后，我能知道它在做什么，并及时纠正吗？** dsh 提供计划、执行过程和用量记录。在需要先讨论方案的任务中，用户可通过 `/plan` 进入计划模式，审阅后再推进；执行过程中，也可以继续补充信息或发出取消。这样的体验适合需求逐步明确、需要边做边看的工作。

计划表达“准备怎么做”，执行记录说明“发生过什么”，两者需要一起看。计划模式主要通过给模型的指令约束行为，本身不锁住文件写入权限。界面上的等待、重试、压缩和后台状态也不能独立证明全部工作已结束；需要追查问题时，应回到持久会话事件及子任务记录。

取消是一项协作过程：主会话停止等待、工具释放资源和最后状态写入日志可能先后发生。对慢工具或外部系统操作，应先确认已经完成的动作，再决定下一步。本轮没有实测插话与取消的竞态，也没有由历史修复次数推算可靠性；需要进一步核验的是新消息、取消与子任务完成同时到达时，用户最终看到什么。

### 核验记录：适用条件、固定来源与待确认问题

<a id="cap-ctl-01"></a>

**CAP-CTL-01 · 计划展示与用户审阅**

支持；仅文档；归属默认插件。条件为Web Plan 组合；exit_plan_mode。计划约束主要在提示词；不是文件权限。tag 与 npm 的计划提示词差异见 PLUGINS。

依据：[计划模式说明][plan]。后续核验：对实际发行包，退出计划的确认与取消分支如何对应日志？

<a id="cap-ctl-02"></a>

**CAP-CTL-02 · 运行中插话、暂停与取消**

部分；已读源码；归属核心／默认插件。条件为Agent loop、inbox、Goal；后端支持协作取消。停止、资源回收、持久终态不同时发生；多个历史修复不能当作可靠性指标。

依据：[执行循环源码][loop-source]、[执行与恢复说明][loop]。后续核验：取消与新消息、慢工具、子任务完成同时发生时的优先级是什么？

<a id="cap-obs-01"></a>

**CAP-OBS-01 · 回看执行事件与用量**

支持；仅文档；归属核心／默认插件／官方可选。条件为Session、Trajectory、stats；深层诊断可选。持久事件与实时协调通知不同；日志不自动获得防篡改和组织审计权限。

依据：[事件与状态说明][lifecycle]、[用量统计说明][stats]。后续核验：用户视图、原始事件和成本统计是否能关联同一任务及子树？

<a id="approval"></a>

## 3. 哪些决定留给人

**助手准备越过工作范围时，谁来决定是否继续？** dsh 有工具权限请求、人工批准与文件访问策略。在有人使用的入口中，可以让用户审阅需要增加权限的动作；适合需要控制文件修改范围、遇到例外再决定的工作。实际是否出现审批，取决于入口和权限配置，不能只看某个按钮是否存在。

当前基础配置使用工作区写入加询问的组合，但精简程序入口默认采用更宽的文件权限。因此，“少一些工具”不代表“授权更少”。开始一类任务前，应明确允许读取和修改的范围、哪些动作必须人工确认，以及无人值守时如何处理等待批准；这些是接入产品需要给用户解释的规则。

现有沙箱主要约束工具进程的文件访问，能力随操作系统变化，没有完整网络或租户隔离保证。插件可以在宿主进程中执行，本地凭据的文件权限也不能向同一系统用户运行的工具隔离全部机密。企业平台仍需负责业务用户身份、凭据交付和审批留痕；当前证据不足以确认所有动作都能关联到实际批准者。实验性自动评审另见[插件选择](PLUGINS.md#review)，不能省略这些边界。

### 核验记录：适用条件、固定来源与待确认问题

<a id="cap-ctl-03"></a>

**CAP-CTL-03 · 工具权限请求与人工批准**

部分；已读源码；归属默认插件。条件为base 支持的权限预设；入口能呈现审批。默认配置因 profile 不同；审批并不覆盖宿主插件和所有外部副作用。

依据：[权限预设][permission]、[基础配置][base]、[SDK Minimal 配置][sdk-minimal]。后续核验：哪些调用跳过人工路径，哪些审批事件能关联实际批准者？

<a id="cap-sec-01"></a>

**CAP-SEC-01 · 约束工具进程的文件访问**

部分；仅文档；归属默认插件。条件为本地 sandbox 支持的 OS／backend；明确策略。存在 partial 等能力差异，无完整网络／租户隔离保证；未安全审计。

依据：[沙箱说明][sandbox]、[安全声明][safety]。后续核验：按目标 OS 核实读、写、网络与失败闭合的实际范围。

<a id="cap-sec-02"></a>

**CAP-SEC-02 · 隔离模型与工具可用的凭据**

部分；仅文档；归属默认插件／外部平台。条件为本地 credentials 与适配器凭据引用。本地文件权限不向同一 OS 用户的工具隔离机密；企业凭据代理需另定。

依据：[凭据说明][credentials]。后续核验：哪些凭据会进入子进程环境，哪些仅由 Host 逐请求读取？

<a id="resources"></a>

## 4. 能使用哪些文件、系统和模型

**我要它处理的资料和业务工具，怎样交到它手上？** 本地任务以会话的工作目录为起点，可以读取或改变当前目录。比如，先分析一个目录下的材料，再将后续工作移到另一个目录。切换会话目录不会改变已经启动的终端或进程所在位置，也不会自动扩大授权；长任务里应保留清楚的文件位置约定。

外部系统可通过 MCP 连接器提供工具和资源。它是把服务接入 Agent 的一种协议，需要配置具体服务器及其认证；连接能力随附，不代表已经接通企业资料库或业务系统。当前支持工具、资源和资源模板，不支持 MCP 的提示词模板。外部系统的可读范围、写入后果、断线恢复和凭据刷新仍需由相应服务与接入方确认。

模型方面，官方提供 DeepSeek 适配器，也能配置其他提供方和网关。用户选择的不只是模型名称：文件理解、工具调用、统计、取消等能力需要与具体端点匹配。当前 DeepSeek 入口采用 Messages 协议，旧协议配置已移除；其他模型的连接组件即使已经加载，也可能尚无可用路由。本轮未调用任何模型，不把目录中出现的名称当作完整兼容保证。

### 核验记录：适用条件、固定来源与待确认问题

<a id="cap-file-01"></a>

**CAP-FILE-01 · 读取和改变 Session 工作目录**

支持；已读源码；归属默认插件。条件为working_directory 工具及目录服务挂载。切换 Session 目录不改变已启动 Shell／进程的自身目录。

依据：[目录工具源码][cwd]。后续核验：目录迁移对相对路径、fork、恢复和已有终端分别如何生效？

<a id="cap-ext-03"></a>

**CAP-EXT-03 · 接入 MCP 工具与资源**

部分；仅文档；归属默认插件／第三方。条件为配置 MCP 服务器及认证；stdio／HTTP。支持工具、资源与资源模板；不支持 MCP prompt 模板。服务器行为、权限与可靠性不由协议自动保证。

依据：[外部工具连接说明][mcp]。后续核验：重连后目录变化、取消、分页失败与认证刷新如何影响运行任务？

<a id="cap-mod-01"></a>

**CAP-MOD-01 · 调用 DeepSeek Messages 路由**

支持；已读源码；归属默认插件。条件为官方适配器；适配的凭据与 Messages endpoint。已移除旧 protocol 配置；错误网关协议不能靠修改名称适配。

依据：[DeepSeek 适配器源码][llm]。后续核验：自定义 endpoint 对图片、扩展字段、缓存与取消的支持是否一致？

<a id="cap-mod-02"></a>

**CAP-MOD-02 · 配置其他模型提供方**

部分；仅文档；归属默认插件／第三方。条件为pi-ai 显式 provider 配置。挂载插件时可以没有路由；模型目录和 ID 随依赖变化，不保证每项能力兼容。

依据：[其他模型配置][pi-ai]。后续核验：以目标模型逐项确认工具、视觉、动态系统提示词及统计字段。

<a id="delivery"></a>

## 5. 如何收到成果并确认完成

**它说“做好了”，我能拿到什么，又凭什么验收？** 在常用 Web 模式中，助手可以把工作区文件声明为成果，显示为可预览的文件卡片。对本机使用者，这便于查看并在运行 dsh 的电脑上打开或定位文件；对远程访问者，“在运行端打开”和“下载到我这台电脑”是不同操作。

当前文件卡片没有内置的访问者下载入口，也不保存不可变副本。它引用当前源文件，之后修改、移动或删除该文件，会影响看到的成果。因此，用于报告交付或多人验收时，上层产品仍需要确定怎样交到收件人手中、验收哪个版本、保存多久。这里的“不支持”只针对当前官方卡片这两项窄能力，不是说 dsh 无法传输任何文件。

用户可通过 `/export` 导出会话日志 ZIP，保存工作记录，但其中不带上卡片所指源文件的内容。开发者也可通过经过鉴权和文件权限检查的接口读取文件；这提供了实现交付流程的基础，却不等于已经提供了下载按钮、授权分享或长期保留。上传附件、网络取文件、聊天软件收件同样需要分别判断。

完成回执也有层次：程序调用返回、主助手暂时空闲、受管理的子任务都结束、业务验收通过，分别回答不同问题。当前接口提供等待子任务树结束的机制，但“文件内容正确且被接受”仍由用户或接入产品判断。对于一份交付物，应先约定验收标准，再将任务记录、最终文件和确认动作关联起来；本轮未验证这条完整链路。

### 核验记录：适用条件、固定来源与待确认问题

<a id="cap-file-02"></a>

**CAP-FILE-02 · 声明文件并展示交付卡片**

支持；已有上游测试但未运行；归属默认插件。条件为Web standard／PTC／创造模式的 present。记录当前源文件路径；可以预览及通过 Host 打开／定位。文件后续修改会改变所见内容。

依据：[文件卡片说明][present]、[文件交付测试][present-test]。后续核验：远程浏览器、无桌面 Host、SSH 文件系统分别支持哪些打开动作？

<a id="cap-file-03"></a>

**CAP-FILE-03 · 从 present 卡片下载到访问者电脑**

不支持；已有上游测试但未运行；归属默认插件。条件为仅指当前官方 Web present 卡片内置入口。官方决策不保留 present 下载端点；测试断言没有浏览器下载。不是“dsh 无法传文件”。

依据：[文件交付设计决策][present-decision]、[文件交付测试][present-test]。后续核验：后续 release 是否新增明确的客户端交付入口与保留策略？

<a id="cap-file-04"></a>

**CAP-FILE-04 · 下载 Session 日志 ZIP**

支持；已有上游测试但未运行；归属默认插件。条件为Web /export／session.export。响应为 attachment ZIP；不包含 present 声明所指源文件的字节。

依据：[日志导出实现][zip]、[文件交付测试][present-test]。后续核验：后代会话选择、附件及敏感内容导出范围是否分别清楚？

<a id="cap-file-05"></a>

**CAP-FILE-05 · 通过鉴权 API 读取文件内容**

支持；已读源码；归属默认插件。条件为GET／HEAD /api/file，组合文件系统允许读取的绝对路径。受浏览器鉴权、文件权限和响应大小限制；没有下载按钮语义，不能据 MIME 限制推断授权。

依据：[文件读取实现][file-api]、[浏览器连接与鉴权][connection]。后续核验：具体 profile 的读取根目录与 maxImageBytes 默认及覆盖项是什么？

<a id="cap-file-06"></a>

**CAP-FILE-06 · 由 present 保存不可变交付文件副本**

不支持；已有上游测试但未运行；归属默认插件。条件为仅指 present 交付声明及其 Session 导出。声明不复制／保留源字节，修改、删除或移动源文件会影响后续访问。

依据：[文件交付设计决策][present-decision]、[文件交付测试][present-test]。后续核验：若产品要长期验收版本，需哪一层提供快照、保留和删除？

<a id="cap-run-04"></a>

**CAP-RUN-04 · 等待子树完成并形成业务回执**

部分；已读源码；归属核心／默认插件。条件为SDK session/wait；受管理后代。run 仍在根首次 idle 结束活动区间；wait 不替上层判定业务验收成功。

依据：[等待实现][sdk-wait]、[调用实现][sdk-run]。后续核验：业务任务 ID、多个 prompt 与最后回复的因果归属如何建立？

<a id="continuity"></a>

## 6. 过几天回来，怎样接着做

**长工作能持续推进吗，它还记得之前的决定吗？** dsh 保存会话，可压缩较长的对话，并通过长期目标功能在同一会话里继续下一轮工作。比如，把一项需要多轮检查的任务留在同一会话持续推进。重新打开或分叉会话后，自动续行不会自行重新启用，需要用户决定继续；轮数上限也不是金额或时间预算。

继续原会话、找回其他会话、形成长期知识，是三种不同需要。压缩会用额外模型调用生成摘要，不能保证所有细节无损，也无法缩小全部提示词或工具信息。可选的会话搜索让 Agent 检索当前工作区历史，需要先启用；它与用户在侧栏查找会话不是同一能力。外部记忆还需要另外配置，其身份、来源、冲突、保留和删除由提供方及接入产品处理。

Web 还有持久提醒，可用于在之后把事项投递回会话。这里的投递回执表示消息进入收件队列，不表示模型已经完成事项；故障恢复中还可能重复提醒。把提醒用于业务动作时，应先规定重复投递如何识别、是否需要再次人工确认。对“回来还能接着做”的承诺，本轮确认的是记录与续接机制，尚未确认跨模型压缩质量、历史检索范围和实际重启表现。

### 核验记录：适用条件、固定来源与待确认问题

<a id="cap-ctx-01"></a>

**CAP-CTX-01 · 压缩长对话上下文**

部分；仅文档；归属默认插件。条件为compaction 与可选工具结果 pruner；模型容量已知。摘要需要额外模型调用；不能缩减全部系统提示词、工具目录或不可分单元，也不保证语义无损。

依据：[压缩说明][compaction]。后续核验：不同模型预算和大工具结果的有效阈值、失败行为是什么？

<a id="cap-ctx-02"></a>

**CAP-CTX-02 · 让 Agent 搜索历史会话**

支持；仅文档；归属官方可选（随附关闭）。条件为启用 session-search bundle；当前工作区。增加全局工具，包括 minimal；与侧栏搜索、跨用户知识权限是不同问题。

依据：[会话搜索说明][session-search]。后续核验：工作区范围、隐藏／归档会话与索引生命周期如何约束？

<a id="cap-ctx-03"></a>

**CAP-CTX-03 · 外接长期记忆与管理其生命周期**

部分；仅文档；归属第三方／外部平台。条件为官方默认关闭的 MCP memory 示例。可连接外部系统；初始化、身份、保留、删除及迁移由提供方负责，没有通用知识治理保证。

依据：[外部记忆指南][memory]。后续核验：所选系统如何处理权限过滤、来源、冲突与删除后召回？

<a id="cap-run-01"></a>

**CAP-RUN-01 · 在同一会话自动推进长期目标**

支持；仅文档；归属默认插件。条件为Goal 已启用续行且 round 容量允许。恢复／fork 不自动重启续行；round 上限不是费用或时长预算。

依据：[长期目标说明][goal]。后续核验：暂停、blocker 与后续人工输入如何决定下一轮准入？

<a id="cap-run-02"></a>

**CAP-RUN-02 · 持久定时提醒与恢复投递**

部分；仅文档；归属默认插件。条件为Web schedule；标准／PTC／创造模式提供工具。投递回执确认 inbox，不确认模型执行；Session 与任务表是独立写入，故障后可能重复提醒。

依据：[提醒投递说明][schedule]、[Web 组合配置][web]。后续核验：重启、补发与重复投递是否需要上层业务幂等键？

<a id="recovery"></a>

## 7. 失败或中断后怎么办

**网络断了、工具卡住了，能安全地再试一次吗？** dsh 的恢复处理区分工具未启动与结果未知，这有助于继续对话时保留真实的不确定性。例如，一个动作已经发向外部系统、但没有拿到回执，此时不能因为重新打开会话就认定动作失败，也不能直接重复执行。

用户或接入产品需要先查看记录、核对外部状态，再决定重试、补偿还是人工处理。会话持久化不负责撤销外部事务，也不保证动作只发生一次。持久化失败、取消和运行异常应进入可见的异常处理路径；它们不应被包装成成功交付。

本项目读过上游文件交付和恢复测试，能确认相应断言存在；没有运行测试，也没有以它们推算真实成功率。当前尚不清楚具体部署下恢复要多久、哪些工具能自行对账、需要谁接手。选取真实业务场景验证这些问题之前，不能向用户承诺“一键恢复后一定安全完成”。

### 核验记录：适用条件、固定来源与待确认问题

<a id="cap-run-03"></a>

**CAP-RUN-03 · 恢复持久会话并识别未知副作用**

部分；已读源码；归属核心／默认插件。条件为JSONL Session 与工具恢复处理。区分未启动、结果未知；可继续对话不等于外部事务回滚或 exactly-once。

依据：[恢复修复源码][repair]、[执行与恢复说明][loop]。后续核验：对有副作用的具体工具，谁核对外部状态并决定重试？

<a id="cap-obs-02"></a>

**CAP-OBS-02 · 借助上游测试核对能力契约**

支持；已有上游测试但未运行；归属核心（上游测试资产）。条件为固定 tag 的测试策略与已阅读测试。确认测试和断言存在，未运行、未读取本轮 CI 结果；不代表生产任务成功率。

依据：[上游测试策略][testing]、[文件交付测试][present-test]、[恢复测试][resume-test]。后续核验：哪些现有无模型测试覆盖最高优先级问题，何时另行授权复验？

<a id="collaboration"></a>

## 8. 多个 Agent 如何合作

**能把复杂任务分给几个助手，再由一个人统一验收吗？** dsh 支持创建、分叉和继续子代理，可用来研究把一个大任务拆成相对独立的子工作。内置子代理与外部后端的能力不同，能否覆盖模型选择、工具范围、取消和持续状态，要按实际后端确认；统一入口不代表完全一致的行为。

可选的实验性 Team 提供任务板、依赖和成员消息。例如，可用任务分工组织并行研究，再由主助手汇总。但当前消息发送被接纳不等于工作已交付，成员退出、重复动作和冲突任务也仍需要明确处理责任。任务板本身不保证多个助手修改同一文件时没有冲突。

这里的“团队”主要指 Agent 之间的协作。多人用户共同拥有任务、按角色审批、交接责任的产品契约尚未确认，见[团队服务](#operations)。对业务产品，先约定谁拆任务、谁合并结果、谁最终验收，再决定是否引入多个 Agent；本轮没有运行并发协作或可靠消息验证。

### 核验记录：适用条件、固定来源与待确认问题

<a id="cap-col-01"></a>

**CAP-COL-01 · 创建、fork 与继续子代理**

支持；已读源码；归属默认插件／官方可选。条件为内置子代理；外部 provider 需安装配置。工具与后端能力不同；当前统一 activation 不等于跨后端同样支持所有覆盖项。

依据：[基础配置][base]、[子代理说明][subagent]。后续核验：逐后端核对模型、工具过滤、取消、持久状态与完成回执。

<a id="cap-col-02"></a>

**CAP-COL-02 · 团队任务板与成员消息**

部分；已读源码；归属官方可选（随附关闭）。条件为实验 Team bundle。任务 CAS、直接 inbox 和发送接纳不是可靠消息总线；旧重试／去重机制已移除。

依据：[协作实现][team-source]、[协作说明][team]。后续核验：成员退出、结果未知、冲突任务及重试的责任如何分配？

<a id="extensions"></a>

## 9. 怎样扩展成自己的工作方式

**同一套助手能按岗位或任务增加能力吗？** dsh 可以组合和启停插件，给工作台增加搜索、终端、协作或其他能力。用户应从缺少的工作能力出发选择扩展；具体入口、会话模式和插件配置共同决定最终可见的工具。有哪些可选能力、何时值得开启，见[插件指南](PLUGINS.md)。

扩展可能影响不止当前会话。某些全局工具启用后会出现在多个会话模式中，宿主插件也可能接触运行环境；因此需要说明影响范围、外部服务和额外费用。切换插件、重新加载代码和升级整个发行版本是不同变更，不能把界面上能开关视为兼容性与信任保证。

已有 Codex 或 Claude 工作规则时，可研究命令挂钩的复用，但要显式配置，且仅支持规定的子集。配置错误可能警告后继续，不宜直接承担“任何时候都必须拦住”的组织策略。当前还存在源码与发行包的计划提示词差异，说明核验扩展时需要落实到实际版本与发布内容；差异本身没有证明运行缺陷，详见[发行证据](PLUGINS.md#发行包核验与版本纪律)。

### 核验记录：适用条件、固定来源与待确认问题

<a id="cap-ext-01"></a>

**CAP-EXT-01 · 组合、启停与版本化插件能力**

支持；已读源码；归属核心／默认插件。条件为profile、bundle、preset 和插件管理器。Host 全局工具可跨 preset；HMR、包升级和实例生命周期不完全等价。发行包差异另见 PLUGINS。

依据：[入口组合配置][profile]、[Web 组合配置][web]、[插件管理说明][plugin-manager]。后续核验：给定 profile 的实际工具、权限、hooks 和依赖变更能否完整列出？

<a id="cap-ext-02"></a>

**CAP-EXT-02 · 复用外部 command hooks**

部分；仅文档；归属官方可选。条件为显式挂载 Codex／Claude hooks 并指定配置路径。仅支持文档规定的子集；配置失败可能警告后继续，不能当成默认强制策略。

依据：[Codex 命令挂钩说明][hooks]、[Claude 命令挂钩说明][claude-hooks]。后续核验：每个 hook 的失败策略、超时、日志和强制续行范围是什么？

<a id="operations"></a>

## 10. 面向团队提供服务，还缺哪些环节

**个人能用的工作台，怎样成为对业务负责的团队服务？** dsh 有本地 Web、Desktop 和程序入口，也支持配置远程访问。运行方需要设置访问入口和认证，负责证书及代理运维；有 HTTPS 或一个公开地址，并不等于已经完成组织用户登录、角色授权和会话隔离。

组织身份、租户权限、Agent 上线审批和下线流程，目前没有足够证据确认是本版本提供的完整产品能力。这些应由上层平台明确承担或进一步核实官方范围，不能把未覆盖企业功能直接视为 harness 缺陷。对多人使用，还要确定谁拥有任务和成果、谁能查看日志、谁承担出站数据与凭据管理责任。[数据通道与接入判断](OVERVIEW.md#decision)

运营也需要回答“花了多少钱、完成了多少、失败后怎样接手”。当前有执行和用量记录，但尚未确认统一的业务验收指标或整项任务货币上限。主助手、子任务、压缩、标题、重试和自动评审都可能形成费用；单次输出限制和任务轮数无法替代总预算。现阶段适合围绕明确任务研究和验证，不宜据这些基础机制承诺生产服务水平。

### 核验记录：适用条件、固定来源与待确认问题

<a id="cap-sec-03"></a>

**CAP-SEC-03 · 组织身份、角色与租户授权**

待确认；仅文档；归属外部平台（实现待确认）。条件为企业部署需求；不是默认单操作者入口的保证。匿名安装 ID、模型登录和浏览器 cookie 不等于组织 RBAC／SSO。

依据：[安装标识说明][identity]、[浏览器连接与鉴权][connection]、[产品说明][readme]。后续核验：是否有官方企业身份契约，或明确的上层身份接入点？

<a id="cap-dep-01"></a>

**CAP-DEP-01 · 本地运行与受控远程 Web 入口**

支持；仅文档；归属默认插件／外部平台。条件为Web／Desktop；指定监听、TLS／代理配置。公告 URL、Host 校验与身份认证各自独立；证书生命周期仍需外部运维。

依据：[远程部署指南][public-deploy]、[浏览器连接与鉴权][connection]。后续核验：在目标反向代理和多访问者条件下，哪个组件负责身份和会话隔离？

<a id="cap-dep-02"></a>

**CAP-DEP-02 · 企业 Agent 发布与治理生命周期**

待确认；仅文档；归属外部平台（实现待确认）。条件为组织内注册、评估、审批、部署与下线。本地插件管理不能直接证明已有企业平台治理；外置功能未覆盖不构成 harness 产品失败。

依据：[产品说明][readme]、[插件管理说明][plugin-manager]、[安全声明][safety]。后续核验：官方是否提供此类产品范围，还是应由接入平台负责？

<a id="cap-obs-03"></a>

**CAP-OBS-03 · 按业务任务统计验收与恢复质量**

待确认；仅文档；归属外部平台（实现待确认）。条件为企业任务完成／接受／恢复指标。现有 token 统计和产品交互埋点不足以确认业务验收指标已交付。

依据：[用量统计说明][stats]、[产品交互采集说明][telemetry]。后续核验：是否存在任务级结果定义、验收事件与失败样本的公开契约？

<a id="cap-obs-04"></a>

**CAP-OBS-04 · 统一限制整项任务费用**

待确认；仅文档；归属外部平台（实现待确认）。条件为包含主循环、子代理、摘要、评审与重试。未确认通用货币预算与耗尽终态；不能将输出上限或 Goal round 当成总预算。

依据：[长期目标说明][goal]、[压缩说明][compaction]、[用量统计说明][stats]。后续核验：预算所有者、实时归集、超额处理和取消已发请求怎样设计？

## 如何继续这份研究

下一批仍优先处理四个会影响使用承诺的问题：实际发行内容是否与源码一致；远程文件怎样交付与保留；完成、提醒和故障恢复怎样对接业务回执；不同入口的权限如何向用户解释。具体问题保留在各节记录中，本次重写没有改变支持状态。

核验记录的“支持”表示限定条件下有文档或实现依据；“部分”表示目标仅由部分机制覆盖；“不支持”只用于明确排除的窄能力；资料不足则“待确认”。源码与测试阅读均不是本项目实测。36项中，支持15项、部分14项、不支持2项、待确认5项；证据为仅文档19项、已读源码12项、已有上游测试但未运行5项、我们实测0项。这是核查范围，不是评分或完成比例。

稳定 ID 用于每周追踪，可跨章节移动，不能因改名或状态变化而删除。未来变更同时修订用户可见的行为说明与核验记录；历史版本结论见 [EVOLUTION](EVOLUTION.md)，插件来源和发行内容见 [PLUGINS](PLUGINS.md)。

[base]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/base/cordis.patch.yml
[claude-hooks]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/hooks-claude-code/README.zh.md
[compaction]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/compaction/compaction-basic/README.zh.md
[connection]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/client/connection/README.zh.md
[credentials]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/credentials/credentials-local/README.zh.md
[cwd]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/tool-working-directory/src/index.ts
[file-api]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/api/session-controller/src/media-references.ts
[goal]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/goal/goal-round-driver/README.zh.md
[hooks]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/hooks-codex/README.zh.md
[identity]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/identity/anonymous-user-id/README.zh.md
[lifecycle]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/agent-lifecycle.zh.md
[llm]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/llm/llm-deepseek/src/config.ts
[loop]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/README.zh.md
[loop-source]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/src/agent.ts
[mcp]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/mcp/mcp-client/README.zh.md
[memory]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/user/guide/mcp-memory.zh.md
[packages]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/README.md
[permission]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/interaction/permission-presets/README.zh.md
[pi-ai]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/llm/llm-pi-ai/README.zh.md
[plan]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/plan/plan-mode/README.zh.md
[plugin-manager]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/boot/plugin-manager/README.zh.md
[present]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/deliverables/tool-present/README.zh.md
[present-decision]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/feature/2026-09-08-present-workspace-source-files.zh.md
[present-test]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/apps/web/tests/present.e2e.ts
[profile]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/boot/app-boot/src/profile.ts
[public-deploy]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/user/guide/public-deployments.zh.md
[readme]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/README.zh.md
[repair]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/session/src/repair.ts
[resume-test]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/tests/resume.spec.ts
[safety]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/SAFETY.zh.md
[sandbox]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/sandbox/sandbox-local/README.zh.md
[schedule]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/schedule/schedule/README.zh.md
[sdk]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/sdk/client/README.zh.md
[sdk-minimal]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/sdk-minimal/cordis.patch.yml
[sdk-run]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/sdk/client/src/api.ts
[sdk-wait]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/sdk/server/src/server.ts
[session-search]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/session-search/README.zh.md
[stats]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/session-stats/README.zh.md
[subagent]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/subsystems/subagent.zh.md
[team]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/agent-team/README.zh.md
[team-source]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/agent-team/src/index.ts
[telemetry]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/client/product-analytics/README.zh.md
[testing]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/testing.zh.md
[web]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/web-app/cordis.patch.yml
[web-guide]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/user/guide/index.zh.md
[webhook]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/webhook-github/README.zh.md
[zip]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session-query/session-log-export/src/index.ts
