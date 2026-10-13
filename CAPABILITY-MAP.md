# Agent 能力清单地图

这是 dsh-watch 唯一的逐项能力状态表，用来持续回答“在什么版本和条件下，dsh 能做什么、证据到哪里、还需确认什么”。插件供给与加载清单放在 [PLUGINS](PLUGINS.md)，完整解释放在 [OVERVIEW](OVERVIEW.md)、[FINDINGS](FINDINGS.md) 和 [版本分析](EVOLUTION.md)，这里通过链接复用，不复制全部结论。

参考 [LLM 101 的 Agent 产品设计检查文章](https://llm101.ai/agent-product-101-product-design-checklist/) 的产品核验视角，条目按本项目的 dsh 证据原创组织。文章不是 dsh 产品规范；不采用成熟度总分，也不把开源 harness 与企业平台混为同一交付范围。外部平台承担的能力仍可记录，但资料缺口不直接判为产品失败。

本版所有条目适用 **v0.2.1-alpha.2／d743267388641bc76f17c45ce8b4c231aed1d32c**，核查日期均为 **2026-10-13**；各条另列入口、配置与范围。默认含义以新配置、无用户覆盖为前提。历史版本只从链接中的独立分析读取，不能把本表状态倒推到旧版。

## 状态与证据怎么读

- **支持**：在条目限定条件下有明确契约或实现证据；不等于我们运行成功。
- **部分**：目标只被部分机制覆盖，或存在影响该目标的明确限制。
- **不支持**：仅用于官方明确排除或实现／测试明确否定的窄能力；不是检索无结果。
- **待确认**：证据不足；保留一个可继续核验的问题。**不适用**只在确认超出所选任务范围时使用，首版未使用。
- 验证程度依次区分 **仅文档、已读源码、已有上游测试但未运行、我们实测**；前3类都不是本项目运行验证，源码与测试存在也不能证明部署效果。

实现归属可同时包含核心、默认插件、官方可选、第三方或外部平台；“官方可选”中的随附与按需安装再到 PLUGINS 区分。稳定 ID 不随名称或状态变化；删除／替代能力保留 ID 和解释，不靠删行抹去历史。

首版 **36项**：支持15项、部分14项、不支持2项、待确认5项。证据分布：仅文档19项、已读源码12项、已有上游测试但未运行5项，**我们实测0项**。这是覆盖盘点，不是评分或能力占比。

| 核查领域 | 条目 | 当前阅读重点 |
|---|---|---|
| [任务入口](#任务入口) | CAP-IN-01～CAP-IN-04（4项） | 从工作区会话输入任务与附件等 |
| [执行控制与人类介入](#执行控制与人类介入) | CAP-CTL-01～CAP-CTL-03（3项） | 计划展示与用户审阅等 |
| [权限与隔离](#权限与隔离) | CAP-SEC-01～CAP-SEC-03（3项） | 约束工具进程的文件访问等 |
| [工作区与文件交付](#工作区与文件交付) | CAP-FILE-01～CAP-FILE-06（6项） | 读取和改变 Session 工作目录等 |
| [上下文与记忆](#上下文与记忆) | CAP-CTX-01～CAP-CTX-03（3项） | 压缩长对话上下文等 |
| [长任务、调度与恢复](#长任务调度与恢复) | CAP-RUN-01～CAP-RUN-04（4项） | 在同一会话自动推进长期目标等 |
| [子代理协作](#子代理协作) | CAP-COL-01～CAP-COL-02（2项） | 创建、fork 与继续子代理等 |
| [工具、插件与连接器](#工具插件与连接器) | CAP-EXT-01～CAP-EXT-03（3项） | 组合、启停与版本化插件能力等 |
| [模型兼容](#模型兼容) | CAP-MOD-01～CAP-MOD-02（2项） | 调用 DeepSeek Messages 路由等 |
| [观察、评测与费用](#观察评测与费用) | CAP-OBS-01～CAP-OBS-04（4项） | 回看执行事件与用量等 |
| [部署与企业治理](#部署与企业治理) | CAP-DEP-01～CAP-DEP-02（2项） | 本地运行与受控远程 Web 入口等 |

## 任务入口

### CAP-IN-01 · 从工作区会话输入任务与附件

**支持｜已读源码｜默认插件**

适用：v0.2.1-alpha.2；Web；文件上传插件与会话 UI。核查：2026-10-13。

支持输入和文件保存，不证明模型能理解每一种上传格式。依据：[web][web]、[web-guide][web-guide]。**下一步：**各文件类型的读取工具和大小限制是否与界面提示一致？

### CAP-IN-02 · 程序调用与事件订阅

**支持｜已读源码｜默认插件**

适用：v0.2.1-alpha.2；Headless／TypeScript、Python SDK；相应 profile。核查：2026-10-13。

不同入口的交互、默认工具和权限不同；调用返回不自动表示业务成功。依据：[sdk][sdk]、[sdk-wait][sdk-wait]、[sdk-minimal][sdk-minimal]。**下一步：**逐项补齐 SDK、Headless 与 ACP 的交互及权限差异。

### CAP-IN-03 · 官方 IM 会话与附件入口

**待确认｜仅文档｜外部平台／连接器（实现待确认）**

适用：v0.2.1-alpha.2；固定版本产品与插件资料检索范围。核查：2026-10-13。

本轮未确认官方 Slack、飞书等运行入口；不据此断言不存在社区接入。依据：[readme][readme]、[packages][packages]。**下一步：**是否有已发布、可验证的官方 IM 包及收件／附件契约？

### CAP-IN-04 · 外部事件触发 Agent 工作

**部分｜仅文档｜官方可选**

适用：v0.2.1-alpha.2；实验 GitHub webhook／规则 runtime，显式配置。核查：2026-10-13。

签名校验与202接纳不等于规则成功或持久队列落盘。依据：[webhook][webhook]。**下一步：**入口、队列持久性、重试与业务幂等分别由谁负责？

## 执行控制与人类介入

### CAP-CTL-01 · 计划展示与用户审阅

**支持｜仅文档｜默认插件**

适用：v0.2.1-alpha.2；Web Plan 组合；exit_plan_mode。核查：2026-10-13。

计划约束主要在提示词；不是文件权限。tag 与 npm 的计划提示词差异见 PLUGINS。依据：[plan][plan]。**下一步：**对实际发行包，退出计划的确认与取消分支如何对应日志？

### CAP-CTL-02 · 运行中插话、暂停与取消

**部分｜已读源码｜核心／默认插件**

适用：v0.2.1-alpha.2；Agent loop、inbox、Goal；后端支持协作取消。核查：2026-10-13。

停止、资源回收、持久终态不同时发生；多个历史修复不能当作可靠性指标。依据：[loop-source][loop-source]、[loop][loop]。**下一步：**取消与新消息、慢工具、子任务完成同时发生时的优先级是什么？

### CAP-CTL-03 · 工具权限请求与人工批准

**部分｜已读源码｜默认插件**

适用：v0.2.1-alpha.2；base 支持的权限预设；入口能呈现审批。核查：2026-10-13。

默认配置因 profile 不同；审批并不覆盖宿主插件和所有外部副作用。依据：[permission][permission]、[base][base]、[sdk-minimal][sdk-minimal]。**下一步：**哪些调用跳过人工路径，哪些审批事件能关联实际批准者？

## 权限与隔离

### CAP-SEC-01 · 约束工具进程的文件访问

**部分｜仅文档｜默认插件**

适用：v0.2.1-alpha.2；本地 sandbox 支持的 OS／backend；明确策略。核查：2026-10-13。

存在 partial 等能力差异，无完整网络／租户隔离保证；未安全审计。依据：[sandbox][sandbox]、[safety][safety]。**下一步：**按目标 OS 核实读、写、网络与失败闭合的实际范围。

### CAP-SEC-02 · 隔离模型与工具可用的凭据

**部分｜仅文档｜默认插件／外部平台**

适用：v0.2.1-alpha.2；本地 credentials 与适配器凭据引用。核查：2026-10-13。

本地文件权限不向同一 OS 用户的工具隔离机密；企业凭据代理需另定。依据：[credentials][credentials]。**下一步：**哪些凭据会进入子进程环境，哪些仅由 Host 逐请求读取？

### CAP-SEC-03 · 组织身份、角色与租户授权

**待确认｜仅文档｜外部平台（实现待确认）**

适用：v0.2.1-alpha.2；企业部署需求；不是默认单操作者入口的保证。核查：2026-10-13。

匿名安装 ID、模型登录和浏览器 cookie 不等于组织 RBAC／SSO。依据：[identity][identity]、[connection][connection]、[readme][readme]。**下一步：**是否有官方企业身份契约，或明确的上层身份接入点？

## 工作区与文件交付

### CAP-FILE-01 · 读取和改变 Session 工作目录

**支持｜已读源码｜默认插件**

适用：v0.2.1-alpha.2；working_directory 工具及目录服务挂载。核查：2026-10-13。

切换 Session 目录不改变已启动 Shell／进程的自身目录。依据：[cwd][cwd]。**下一步：**目录迁移对相对路径、fork、恢复和已有终端分别如何生效？

### CAP-FILE-02 · 声明文件并展示交付卡片

**支持｜已有上游测试但未运行｜默认插件**

适用：v0.2.1-alpha.2；Web standard／PTC／创造模式的 present。核查：2026-10-13。

记录当前源文件路径；可以预览及通过 Host 打开／定位。文件后续修改会改变所见内容。依据：[present][present]、[present-test][present-test]。**下一步：**远程浏览器、无桌面 Host、SSH 文件系统分别支持哪些打开动作？

### CAP-FILE-03 · 从 present 卡片下载到访问者电脑

**不支持｜已有上游测试但未运行｜默认插件**

适用：v0.2.1-alpha.2；仅指当前官方 Web present 卡片内置入口。核查：2026-10-13。

官方决策不保留 present 下载端点；测试断言没有浏览器下载。不是“dsh 无法传文件”。依据：[present-decision][present-decision]、[present-test][present-test]。**下一步：**后续 release 是否新增明确的客户端交付入口与保留策略？

### CAP-FILE-04 · 下载 Session 日志 ZIP

**支持｜已有上游测试但未运行｜默认插件**

适用：v0.2.1-alpha.2；Web /export／session.export。核查：2026-10-13。

响应为 attachment ZIP；不包含 present 声明所指源文件的字节。依据：[zip][zip]、[present-test][present-test]。**下一步：**后代会话选择、附件及敏感内容导出范围是否分别清楚？

### CAP-FILE-05 · 通过鉴权 API 读取文件内容

**支持｜已读源码｜默认插件**

适用：v0.2.1-alpha.2；GET／HEAD /api/file，组合文件系统允许读取的绝对路径。核查：2026-10-13。

受浏览器鉴权、文件权限和响应大小限制；没有下载按钮语义，不能据 MIME 限制推断授权。依据：[file-api][file-api]、[connection][connection]。**下一步：**具体 profile 的读取根目录与 maxImageBytes 默认及覆盖项是什么？

### CAP-FILE-06 · 由 present 保存不可变交付文件副本

**不支持｜已有上游测试但未运行｜默认插件**

适用：v0.2.1-alpha.2；仅指 present 交付声明及其 Session 导出。核查：2026-10-13。

声明不复制／保留源字节，修改、删除或移动源文件会影响后续访问。依据：[present-decision][present-decision]、[present-test][present-test]。**下一步：**若产品要长期验收版本，需哪一层提供快照、保留和删除？

## 上下文与记忆

### CAP-CTX-01 · 压缩长对话上下文

**部分｜仅文档｜默认插件**

适用：v0.2.1-alpha.2；compaction 与可选工具结果 pruner；模型容量已知。核查：2026-10-13。

摘要需要额外模型调用；不能缩减全部系统提示词、工具目录或不可分单元，也不保证语义无损。依据：[compaction][compaction]。**下一步：**不同模型预算和大工具结果的有效阈值、失败行为是什么？

### CAP-CTX-02 · 让 Agent 搜索历史会话

**支持｜仅文档｜官方可选（随附关闭）**

适用：v0.2.1-alpha.2；启用 session-search bundle；当前工作区。核查：2026-10-13。

增加全局工具，包括 minimal；与侧栏搜索、跨用户知识权限是不同问题。依据：[session-search][session-search]。**下一步：**工作区范围、隐藏／归档会话与索引生命周期如何约束？

### CAP-CTX-03 · 外接长期记忆与管理其生命周期

**部分｜仅文档｜第三方／外部平台**

适用：v0.2.1-alpha.2；官方默认关闭的 MCP memory 示例。核查：2026-10-13。

可连接外部系统；初始化、身份、保留、删除及迁移由提供方负责，没有通用知识治理保证。依据：[memory][memory]。**下一步：**所选系统如何处理权限过滤、来源、冲突与删除后召回？

## 长任务、调度与恢复

### CAP-RUN-01 · 在同一会话自动推进长期目标

**支持｜仅文档｜默认插件**

适用：v0.2.1-alpha.2；Goal 已启用续行且 round 容量允许。核查：2026-10-13。

恢复／fork 不自动重启续行；round 上限不是费用或时长预算。依据：[goal][goal]。**下一步：**暂停、blocker 与后续人工输入如何决定下一轮准入？

### CAP-RUN-02 · 持久定时提醒与恢复投递

**部分｜仅文档｜默认插件**

适用：v0.2.1-alpha.2；Web schedule；标准／PTC／创造模式提供工具。核查：2026-10-13。

投递回执确认 inbox，不确认模型执行；Session 与任务表是独立写入，故障后可能重复提醒。依据：[schedule][schedule]、[web][web]。**下一步：**重启、补发与重复投递是否需要上层业务幂等键？

### CAP-RUN-03 · 恢复持久会话并识别未知副作用

**部分｜已读源码｜核心／默认插件**

适用：v0.2.1-alpha.2；JSONL Session 与工具恢复处理。核查：2026-10-13。

区分未启动、结果未知；可继续对话不等于外部事务回滚或 exactly-once。依据：[repair][repair]、[loop][loop]。**下一步：**对有副作用的具体工具，谁核对外部状态并决定重试？

### CAP-RUN-04 · 等待子树完成并形成业务回执

**部分｜已读源码｜核心／默认插件**

适用：v0.2.1-alpha.2；SDK session/wait；受管理后代。核查：2026-10-13。

run 仍在根首次 idle 结束活动区间；wait 不替上层判定业务验收成功。依据：[sdk-wait][sdk-wait]、[sdk-run][sdk-run]。**下一步：**业务任务 ID、多个 prompt 与最后回复的因果归属如何建立？

## 子代理协作

### CAP-COL-01 · 创建、fork 与继续子代理

**支持｜已读源码｜默认插件／官方可选**

适用：v0.2.1-alpha.2；内置子代理；外部 provider 需安装配置。核查：2026-10-13。

工具与后端能力不同；当前统一 activation 不等于跨后端同样支持所有覆盖项。依据：[base][base]、[subagent][subagent]。**下一步：**逐后端核对模型、工具过滤、取消、持久状态与完成回执。

### CAP-COL-02 · 团队任务板与成员消息

**部分｜已读源码｜官方可选（随附关闭）**

适用：v0.2.1-alpha.2；实验 Team bundle。核查：2026-10-13。

任务 CAS、直接 inbox 和发送接纳不是可靠消息总线；旧重试／去重机制已移除。依据：[team-source][team-source]、[team][team]。**下一步：**成员退出、结果未知、冲突任务及重试的责任如何分配？

## 工具、插件与连接器

### CAP-EXT-01 · 组合、启停与版本化插件能力

**支持｜已读源码｜核心／默认插件**

适用：v0.2.1-alpha.2；profile、bundle、preset 和插件管理器。核查：2026-10-13。

Host 全局工具可跨 preset；HMR、包升级和实例生命周期不完全等价。发行包差异另见 PLUGINS。依据：[profile][profile]、[web][web]、[plugin-manager][plugin-manager]。**下一步：**给定 profile 的实际工具、权限、hooks 和依赖变更能否完整列出？

### CAP-EXT-02 · 复用外部 command hooks

**部分｜仅文档｜官方可选**

适用：v0.2.1-alpha.2；显式挂载 Codex／Claude hooks 并指定配置路径。核查：2026-10-13。

仅支持文档规定的子集；配置失败可能警告后继续，不能当成默认强制策略。依据：[hooks][hooks]、[claude-hooks][claude-hooks]。**下一步：**每个 hook 的失败策略、超时、日志和强制续行范围是什么？

### CAP-EXT-03 · 接入 MCP 工具与资源

**部分｜仅文档｜默认插件／第三方**

适用：v0.2.1-alpha.2；配置 MCP 服务器及认证；stdio／HTTP。核查：2026-10-13。

支持工具、资源与资源模板；不支持 MCP prompt 模板。服务器行为、权限与可靠性不由协议自动保证。依据：[mcp][mcp]。**下一步：**重连后目录变化、取消、分页失败与认证刷新如何影响运行任务？

## 模型兼容

### CAP-MOD-01 · 调用 DeepSeek Messages 路由

**支持｜已读源码｜默认插件**

适用：v0.2.1-alpha.2；官方适配器；适配的凭据与 Messages endpoint。核查：2026-10-13。

已移除旧 protocol 配置；错误网关协议不能靠修改名称适配。依据：[llm][llm]。**下一步：**自定义 endpoint 对图片、扩展字段、缓存与取消的支持是否一致？

### CAP-MOD-02 · 配置其他模型提供方

**部分｜仅文档｜默认插件／第三方**

适用：v0.2.1-alpha.2；pi-ai 显式 provider 配置。核查：2026-10-13。

挂载插件时可以没有路由；模型目录和 ID 随依赖变化，不保证每项能力兼容。依据：[pi-ai][pi-ai]。**下一步：**以目标模型逐项确认工具、视觉、动态系统提示词及统计字段。

## 观察、评测与费用

### CAP-OBS-01 · 回看执行事件与用量

**支持｜仅文档｜核心／默认插件／官方可选**

适用：v0.2.1-alpha.2；Session、Trajectory、stats；深层诊断可选。核查：2026-10-13。

持久事件与实时协调通知不同；日志不自动获得防篡改和组织审计权限。依据：[lifecycle][lifecycle]、[stats][stats]。**下一步：**用户视图、原始事件和成本统计是否能关联同一任务及子树？

### CAP-OBS-02 · 借助上游测试核对能力契约

**支持｜已有上游测试但未运行｜核心（上游测试资产）**

适用：v0.2.1-alpha.2；固定 tag 的测试策略与已阅读测试。核查：2026-10-13。

确认测试和断言存在，未运行、未读取本轮 CI 结果；不代表生产任务成功率。依据：[testing][testing]、[present-test][present-test]、[resume-test][resume-test]。**下一步：**哪些现有无模型测试覆盖最高优先级问题，何时另行授权复验？

### CAP-OBS-03 · 按业务任务统计验收与恢复质量

**待确认｜仅文档｜外部平台（实现待确认）**

适用：v0.2.1-alpha.2；企业任务完成／接受／恢复指标。核查：2026-10-13。

现有 token 统计和产品交互埋点不足以确认业务验收指标已交付。依据：[stats][stats]、[telemetry][telemetry]。**下一步：**是否存在任务级结果定义、验收事件与失败样本的公开契约？

### CAP-OBS-04 · 统一限制整项任务费用

**待确认｜仅文档｜外部平台（实现待确认）**

适用：v0.2.1-alpha.2；包含主循环、子代理、摘要、评审与重试。核查：2026-10-13。

未确认通用货币预算与耗尽终态；不能将输出上限或 Goal round 当成总预算。依据：[goal][goal]、[compaction][compaction]、[stats][stats]。**下一步：**预算所有者、实时归集、超额处理和取消已发请求怎样设计？

## 部署与企业治理

### CAP-DEP-01 · 本地运行与受控远程 Web 入口

**支持｜仅文档｜默认插件／外部平台**

适用：v0.2.1-alpha.2；Web／Desktop；指定监听、TLS／代理配置。核查：2026-10-13。

公告 URL、Host 校验与身份认证各自独立；证书生命周期仍需外部运维。依据：[public-deploy][public-deploy]、[connection][connection]。**下一步：**在目标反向代理和多访问者条件下，哪个组件负责身份和会话隔离？

### CAP-DEP-02 · 企业 Agent 发布与治理生命周期

**待确认｜仅文档｜外部平台（实现待确认）**

适用：v0.2.1-alpha.2；组织内注册、评估、审批、部署与下线。核查：2026-10-13。

本地插件管理不能直接证明已有企业平台治理；外置功能未覆盖不构成 harness 产品失败。依据：[readme][readme]、[plugin-manager][plugin-manager]、[safety][safety]。**下一步：**官方是否提供此类产品范围，还是应由接入平台负责？

## 下一批优先核验

1. **插件与发行物的一致性**：沿 CAP-EXT-01／CAP-CTL-01 核查 npm Plan 提示词差异、历史包缺口及实际依赖版本范围，先补静态来源。
2. **远程文件交付**：分别检查 CAP-FILE-02～06 的打开位置、文件读取策略、ZIP 内容和长期保留；不把它们合并成一个“下载”勾选项。
3. **任务完成与恢复**：沿 CAP-RUN-02～04、CAP-COL-02 核查提醒重复、结果未知、子树等待与消息接纳，明确业务回执的上层责任。
4. **入口的权限差异**：沿 CAP-CTL-03、CAP-SEC-01～03 比较 SDK Minimal、普通 SDK 和 Web；再判断企业身份与凭据代理需要哪些外部能力。

每周仅更新受实质变更影响的条目、证据日期和下一步问题；新出现且可独立核验的能力才新增 ID。上游文档、源码、测试三类证据分别记录。只有另行实施并记录环境、版本、输入和结果的测试才可标“我们实测”；本轮不执行测试或模型调用。

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
