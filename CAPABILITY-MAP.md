# dsh 产品评测：14维框架与能力证据

本页先定义 Agent 产品应当接受哪些评测，再逐维分析 dsh，最后保留36项能力的固定版本证据。**评测范围不以已有功能倒推；尚无明确实现或证据的要求仍保留为待评。** 本页用于判断产品适用范围和后续验证重点，不提供数字总分，也不把功能数量换算为成熟度。

维度名称及00–13顺序采用 [LLM 101《Agent 产品设计总表》](https://llm101.ai/agent-product-101-product-design-checklist/) 的框架。下列定义、基本要求、成熟表现和 dsh 分析为本项目原创阐释；不复制文章的完整检查题或评分法。框架用于提出问题，dsh 事实仅依据本项目已核对的官方资料、固定源码与发行物。

研究推进至 **v0.2.1-rc.2**，tag `dsh-v0.2.1-rc.2`，提交 `687f282e8625c6b8d11ff58211a90524be2e4317`；本周核查 **2026-10-19**。未受增量影响的记录继续使用 alpha.2／`d743267388641bc76f17c45ce8b4c231aed1d32c` 与2026-10-13证据，发生变化的条目单列新来源与日期，不把旧证据换链接冒充复查。没有安装运行 dsh、调用模型或端到端测试。默认值以新配置、无用户覆盖为条件；支持、证据与成熟度分开，未查明仍待评。[本周版本报告](releases/v0.2.1-rc.2.md)、[当前安全声明](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/SAFETY.zh.md)。

## 评测维度总览

本表同时是00–13章节目录。“基本要求”说明一类承诺至少需要什么依据；“成熟表现”是更完整的目标形态，**不是 dsh 已实现状态**。对 harness 自身与上层业务平台分别判断承担范围，不因某项应由外部产品提供就将 dsh 判为失败。

| 维度与章节 | 评什么 | 基本要求 | 成熟表现 |
|---|---|---|---|
| [00 产品承诺](#dimension-00) | 委派的工作与交付责任 | 约定工作范围、产出和验收者 | 能说明适用与退出条件，承诺有任务证据支撑 |
| [01 任务入口](#dimension-01) | 输入如何成为可追踪任务 | 保留目标、材料、发起者及接收状态 | 多入口保持身份、上下文与结果归属一致 |
| [02 控制层](#dimension-02) | 执行过程的干预手段 | 能审阅计划、修改要求并请求停止 | 干预有明确生效范围与回执，覆盖关键执行边界 |
| [03 人类节点](#dimension-03) | 参与角色、介入时机与责任 | 关键决定有人接收、判断并反馈 | 等待、交接与继续执行保留决定者和依据 |
| [04 权限模型](#dimension-04) | 允许主体对资源执行的动作 | 入口授权、工具边界与拒绝原因明确 | 最小授权、凭据及撤权在目标环境中有效 |
| [05 工作空间](#dimension-05) | 任务材料和成果的稳定承载 | 能找回任务、定位成果并知道其版本 | 可交接、验收、保留及删除，权限与来源可追溯 |
| [06 长任务](#dimension-06) | 跨时间与子任务的过程状态 | 区分等待、执行、阻塞和结束 | 状态、通知、预算与完成条件可跨续接保持一致 |
| [07 信任体验](#dimension-07) | 用户理解证据、风险与责任 | 能区分建议、已执行动作及未确认结果 | 关键判断可核对，数据使用与责任说明可理解 |
| [08 产品指标](#dimension-08) | 投入是否形成有效工作结果 | 为任务、验收和介入定义统计口径 | 指标关联目标场景、失败原因和单位结果成本 |
| [09 评估](#dimension-09) | 如何验证任务表现与变化 | 固定样本、环境、判据及证据来源 | 真实任务和故障样本可重复核验并支持版本比较 |
| [10 可观测性](#dimension-10) | 执行记录的关联与解释能力 | 能追到消息、工具、状态与错误 | 不同角色可沿同一任务追查原因且访问受控 |
| [11 可靠性](#dimension-11) | 故障后的安全处置与恢复 | 保留不确定结果，避免无依据重复动作 | 故障路径有可验证的恢复、对账和接手责任 |
| [12 平台能力](#dimension-12) | 共享执行与治理的复用范围 | 组件、版本、集成与承担方明确 | 跨任务复用且变更、隔离和生命周期可管理 |
| [13 自主等级](#dimension-13) | 任务可被托付到什么程度 | 范围、停止条件和人工介入有约束 | 随风险、可逆性、权限和恢复证据调整委派范围 |

相邻维度按评测对象区分：**控制层**检查可用的干预手段，**人类节点**检查谁在何时决定，**权限模型**检查动作是否被允许，**信任体验**检查用户是否理解证据与责任。**工作空间**承载任务材料和成果，**长任务**管理过程状态，**可靠性**处理故障与安全恢复。**产品指标**定义衡量结果的口径，**评估**规定验证方法，**可观测性**提供可追查的执行记录。平台能力和自主等级分别回答由谁提供共用能力、在何种边界内委派。

评测中分开表达三件事：

| 判断轴 | 本页用法 | 不能据此推导 |
|---|---|---|
| 能力支持状态 | 在索引中维持支持、部分、不支持、待确认；适用条件限定范围 | 支持不等于本项目运行成功；未找到证据不等于不支持 |
| 证据强度 | 记录官方文档、已读源码、已读但未运行的上游测试；实测需独立记录 | 源码或测试存在不证明部署表现、业务效果或安全性 |
| 维度成熟度 | 以初步、局部、较完整描述已获证据覆盖的环节；其余明确待评 | 不由支持项数量计算，不将待评写成零分，不给全局总等级 |

下文成熟度均为**静态研究判断**。“较完整”只可能用于明确限定的机制或资料覆盖；本轮不对实际运行成熟度作肯定结论。所有完整能力记录统一在[文末证据索引](#evidence-index)维护；每项只有一个主归属，其他章节按需交叉引用。00产品承诺与07信任体验综合引用现有记录，没有为凑齐维度新增或挪用能力 ID。

<a id="dimension-00"></a>

## 00 产品承诺

### 定义与边界

产品承诺评测“交给谁、做哪类工作、产出什么、由谁接受结果”。它确定任务范围与交付责任，不承担界面功能盘点，也不直接用调用成功判断履约。对一个执行框架，应先分清它提供执行基础还是同时负责业务成果；本维度因此综合引用入口、交付和完成记录，不新建重复能力项。

### 检查问题与判断依据

应检查目标用户是否能把预期成果、输入条件和验收方式说清，以及超出范围或结果不确定时由谁决定下一步。判断依据包括公开定位、实际产出形态、完成事件的契约和可复核的任务样本。只有功能列表时，可以确认能力构成；没有验收样本时，交付质量与效率价值仍待评。

### dsh 当前表现

dsh 提供围绕工作区的 Agent 工作台和可被其他产品调用的运行框架。Web 会话把输入、文件、工具、计划与子代理放在持续工作中；程序入口允许接入产品发起和跟踪任务。基于这些机制，可优先研究文件分析与修改、有人审阅的多步骤任务，以及已有产品中的局部执行工作。这些是适用性推断，并非已验证场景。

交付承诺仍要收窄到具体条件：文件卡片引用当前源文件，程序调用返回也可能早于全部后代活动结束。dsh 的执行与记录机制没有替业务产品规定“报告可接受”或“外部业务动作正确”的标准。将其描述为完整企业 Agent 平台，会掩盖尚待确认的组织授权、成果保留和费用责任。

### 版本与插件证据

定位依据为本版本[产品说明][readme]和[架构][architecture]；交付与完成分别交叉引用[文件卡片 CAP-FILE-02](#cap-file-02)、[不可变副本 CAP-FILE-06](#cap-file-06)及[任务等待 CAP-RUN-04](#cap-run-04)。插件条件按[默认组成](PLUGINS.md#当前默认组成与重要例外)确认，不能从某个 Web 模式推广到所有入口。

### 评测结论与待验证事项

**定位可初步判断，成果履约待评。** 当前资料足以支持“工作区执行工作台与可组合运行框架”的定位；生产任务成功率和可验收价值没有本项目实测。下一步需要为目标场景补齐输入、成果、验收者及失败退出条件，再判断是否超出 harness 的职责。现阶段借鉴交互与执行模式，不作生产运行时采用结论。

<a id="start"></a>
<a id="dimension-01"></a>

## 01 任务入口

### 定义与边界

任务入口评测输入如何成为持续可追踪的委派，包括任务目标、材料、发起来源与结果去向。它关注提交和接收时的上下文完整性；资源授权归04权限模型，后续运行状态归06长任务。聊天、程序调用与事件触发可以共存，但它们不天然共享相同的身份和完成语义。

### 检查问题与判断依据

应检查入口接收的是临时提问还是有结果目标的工作，附件能否被所选工具读取，以及提交回执指向哪项工作。还需确认重复提交、补充输入和外部事件能否归入正确任务。判断依据是入口配置、输入保存方式、事件验证与程序接口契约；按钮存在或上传成功不能证明上下文已被理解。

### dsh 当前表现

Web 支持从工作区会话输入任务和附件；它提供材料进入工作环境的路径，但不同格式的理解能力依赖读取工具和模型。Headless 及 TypeScript、Python SDK 提供程序入口和事件订阅，交互、工具及权限配置与 Web 不完全相同，接入产品需自己建立业务输入与任务记录的对应关系。

外部事件方面，实验性 GitHub webhook 需要显式配置规则；签名验证后的202回执只说明接纳和内存分发，不证明规则成功或持久队列已经保存。当前限定资料中未确认官方 Slack、飞书等会话与附件运行入口，不能据此否定社区接入，也不能对企业聊天收件作默认承诺。

**2026-10-19增量判断（alpha.3→rc.2）：**SDK 新增持久会话 resume，保留 ID、历史与目录且不发新输入；Minimal 增图片读取和压缩，但上传／工具可用仍不等于模型理解。当前入口范围扩大，跨入口身份与业务回执仍待评。[SDK 恢复契约](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sdk/client/README.zh.md)、[Minimal 配置](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/bundle/sdk-minimal/cordis.patch.yml)

### 版本与插件证据

主记录为[CAP-IN-01](#cap-in-01)至[CAP-IN-04](#cap-in-04)，依据[Web 组合][web]、[SDK 契约][sdk]及[事件入口][webhook]。上传插件及不同程序入口的历史与加载条件保留在[插件指南](PLUGINS.md)。本轮没有新的输入格式、聊天连接器或事件重试实测。

### 评测结论与待验证事项

**入口机制有局部支撑，跨入口的业务任务契约待评。** 已有资料可确认交互和程序入口；尚不能确认发起人、权限、附件和结果在多入口间完整一致。后续优先核对文件格式与大小提示、各入口权限差异，以及外部事件的持久性和重复处理责任。官方聊天入口维持待确认。

<a id="control"></a>
<a id="dimension-02"></a>

## 02 控制层

### 定义与边界

控制层评测用户或接入系统能够怎样改变正在执行的工作，例如审阅计划、补充要求、停止或调整后续活动。这里关注干预手段及其生效范围；谁有责任作决定归03人类节点，动作是否获得授权归04权限模型，失败后的恢复效果归11可靠性。

### 检查问题与判断依据

应检查计划能否在行动前被审阅，执行中的新要求何时生效，以及停止请求后哪些工作仍在运行。对外部规则，还应确认触发点、失败策略与超时行为。判断依据需要同时包含交互入口和运行时处理，不能把按钮的视觉状态或一条提示词视为强制停止和资源回收证据。

### dsh 当前表现

Web 可通过 `/plan` 进入计划模式，执行中可继续输入和请求取消；运行循环处理收件队列与协作取消。计划帮助用户讨论方法，但主要是提示词约束，不直接禁止文件写入。用户发出取消后，停止等待、工具清理和持久终态可能分阶段发生，当前没有本项目的竞态或响应时延验证。

对于已有 Codex 或 Claude 命令规则，可显式配置挂钩桥接，在支持的执行环节调用命令。它只覆盖文档规定的子集，配置失败可能警告后继续。因此，命令挂钩可以是干预实现的一部分，不能未经核验就被产品描述为任何情况下都有效的控制点；通用接管或回滚体验仍待评。

### 版本与插件证据

主记录为[计划 CAP-CTL-01](#cap-ctl-01)、[干预与取消 CAP-CTL-02](#cap-ctl-02)、[命令挂钩 CAP-EXT-02](#cap-ext-02)。[计划说明][plan]、[循环源码][loop-source]和[挂钩说明][hooks]界定各自范围。alpha.2 的 tag 与 npm 计划提示词有文字差异，详见[发行证据](PLUGINS.md#发行包核验与版本纪律)；该差异未被证明导致权限绕过。

### 评测结论与待验证事项

**干预机制具备局部成熟表现，控制闭环待评。** 计划与取消有明确入口和实现依据，但不能据此承诺所有动作可即时中止或撤销。后续需核对取消与新消息、慢工具、子任务结束同时发生时的最终状态，以及实际发行包中计划确认与取消如何进入记录。涉及审批角色和恢复责任时分别引用03与11，不重复登记能力状态。

<a id="approval"></a>
<a id="dimension-03"></a>

## 03 人类节点

### 定义与边界

人类节点评测谁在什么时刻介入、需要看到什么材料、决定后工作怎样继续。它覆盖澄清、审阅、批准与接手的角色和时机；干预按钮是否存在属于02控制层，批准能放开什么动作属于04权限模型。本维度不把“遇到问题再问人”视为已经形成完整的责任流程。

### 检查问题与判断依据

应检查发起者、内容审阅者和权限批准者是否为同一人，待人处理时工作如何等待，以及决定能否关联执行结果。如果无人响应、拒绝或需要换人接手，应能说明后续责任。判断依据是请求与响应记录、身份关联、继续执行条件和交接语义，而不只是一段请求批准的对话。

### dsh 当前表现

dsh 的工具权限请求可在支持交互的入口中呈现给操作者，计划和后续消息也为审阅与补充信息提供基础。它适合研究同一操作者持续参与的工作方式；不同程序入口的交互与权限默认值不同，不能默认拥有相同的人工节点。

当前资料不足以确认企业发起人、审阅人、批准人和管理员之间完整的职责分离，或每项批准都能关联实际业务用户。可选 Auto review 用模型辅助权限判断，仍会增加调用、可能误判且记录不完整；它没有代替人类或组织承担责任的产品契约。恢复长期目标需要重新决定续行，可作为显式介入的设计借鉴，但不等于组织审批流已经具备。

### 版本与插件证据

主记录为[人工批准 CAP-CTL-03](#cap-ctl-03)，依据[权限预设][permission]、[基础配置][base]及[精简程序入口][sdk-minimal]。交叉引用[续行 CAP-RUN-01](#cap-run-01)、[组织身份 CAP-SEC-03](#cap-sec-03)；自动评审的默认关闭和限制见[官方说明][auto-review]与[插件指南](PLUGINS.md#review)。

### 评测结论与待验证事项

**单操作者介入有局部支撑，多角色责任流程待评。** 不能把模型自动评审或一般浏览器认证等同于业务批准者身份。下一步需明确哪些请求需要人、由谁接收、拒绝或超时后怎样处理，以及决定和继续执行之间如何留痕。现有证据不足处保留待评，不新增强制审批制度或假定 dsh 已实现企业审批。

<a id="dimension-04"></a>

## 04 权限模型

### 定义与边界

权限模型评测主体在特定任务和环境中被允许读取、修改或调用什么资源，以及授权如何被约束和撤回。它评测实际动作边界；批准发生的时机归03人类节点，用户是否理解授权后果归07信任体验。工作目录、工具数量和界面模式都不能单独代表权限范围。

### 检查问题与判断依据

应检查入口默认授权、文件与外部工具边界、凭据可见范围，以及拒绝和不可用时是否清楚失败。对企业部署，还需核对业务身份与租户的传递和隔离。判断依据包括组合配置、实际执行后端、读取接口的鉴权与限制；操作系统差异和宿主插件必须计入，不能只审查某一层沙箱名称。

### dsh 当前表现

基础组合使用 `workspace-write + ask`，SDK Minimal 则使用独立组合，默认文件策略为 `danger-full-access`。因此，少工具的入口并不天然拥有更小授权范围。本地文件沙箱按操作系统和后端提供能力，存在部分支持情况；它不保证完整网络或多租户隔离。宿主插件和同一系统用户下的工具也可能接触资源，本地凭据文件权限不能被视为全面的秘密隔离。

鉴权文件接口可读取组合文件系统允许访问的绝对路径，受到浏览器认证、文件权限和响应大小限制；它不是任意文件访问许可。当前匿名安装标识、模型登录和浏览器 cookie 也不足以证明组织角色与租户授权已经交付，企业身份与凭据代理的承担方仍需明确。

**2026-10-19增量判断（alpha.3→rc.2）：**Web／Desktop 已保存凭据优先于启动环境和 `.env`；Headless 默认不读保存密钥，自定义 profile 需看叠加。新版 Search／Fetch 需主动选择，启用后搜索默认可能附带用户问题片段，URL 抓取交远端；不能把文件沙箱当成这条出站通道的完整治理。凭据隔离与目标服务策略仍待验证。[凭据优先级](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/credentials/credentials-local/README.zh.md)、[Headless 配置](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/bundle/headless/cordis.patch.yml)、[Search／Fetch 固定说明](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/web/web-deepseek-api/README.zh.md)

### 版本与插件证据

主记录为[CAP-SEC-01](#cap-sec-01)至[CAP-SEC-03](#cap-sec-03)及[文件读取 CAP-FILE-05](#cap-file-05)。依据[沙箱][sandbox]、[本地凭据][credentials]、[连接鉴权][connection]和[文件读取源码][file-api]；SDK Minimal 的 tag 与已抽查 npm 配置一致，见[入口配置证据](PLUGINS.md#当前默认组成与重要例外)。[安全声明][safety]仍明确未经审计。

### 评测结论与待验证事项

**文件策略存在局部实现，企业权限与隔离成熟度待评。** 静态配置可解释入口差异，但不能证明目标环境中所有动作都受控。后续应按实际操作系统核对读写、网络、失败处理和凭据传递范围，再确认业务身份接入。当前没有独立安全验证，不从公开公告为空推导安全，也不将官方边界写成已复现漏洞。

<a id="delivery"></a>
<a id="dimension-05"></a>

## 05 工作空间

### 定义与边界

工作空间评测任务材料、工作历史和成果是否有稳定的承载与定位方式，能否在后续交接和验收时找到正确内容。这里关注对象、来源、版本和保留；运行处于哪个阶段归06长任务，崩溃后能否安全重试归11可靠性。保存聊天记录或文件路径只是其中一部分。

### 检查问题与判断依据

应检查材料属于哪个任务、成果指向哪个版本、远程使用者如何取得文件，以及源文件变化后记录还能解释什么。跨会话知识还需核对来源、权限、更新与删除。判断依据包括目录服务、成果声明格式、文件读取与导出契约、历史检索范围；不能把预览、下载和保留副本合为一个能力勾选。

### dsh 当前表现

dsh 会话支持读取和切换工作目录，但不会改变已有终端进程的目录或扩大授权。常用 Web 模式中的文件卡片声明当前源文件，可预览并在运行 dsh 的主机打开或定位。当前卡片没有内置的访问者下载入口，也不保存不可变副本；修改、移动或删除源文件会影响后续所见。用于报告交付时，上层产品仍要明确验收版本和文件交付路径。

可选会话搜索可让 Agent 检索当前工作区历史，默认关闭；它和侧栏搜索并非同一能力。外接长期记忆需要独立服务，身份、来源冲突、保留和删除由提供方与接入产品负责。因此，工作记录、可再次使用的事实与正式交付物各有生命周期，不能由同一会话容器自动获得全部治理能力。

### 版本与插件证据

主记录为[目录 CAP-FILE-01](#cap-file-01)、[卡片 CAP-FILE-02](#cap-file-02)、[下载 CAP-FILE-03](#cap-file-03)、[副本 CAP-FILE-06](#cap-file-06)、[搜索 CAP-CTX-02](#cap-ctx-02)和[外部记忆 CAP-CTX-03](#cap-ctx-03)。依据[交付设计][present-decision]和[已读未运行的测试][present-test]；alpha.2 目录工具及插件加载证据见[本次版本分析](releases/v0.2.1-alpha.2.md)。日志 ZIP 属于记录导出，在10可观测性维护[CAP-FILE-04](#cap-file-04)。

### 评测结论与待验证事项

**本地材料与成果定位有局部支撑，稳定业务交付待评。** 卡片当前不提供下载和不可变副本，是明确的窄能力限制；它不代表所有文件传输都不可能。下一步需确认远程与无桌面环境的打开行为、可读文件范围、成果快照与保留承担方，以及检索和记忆的生命周期。未获证据前不承诺跨人交接后仍能验收同一版本。

<a id="continuity"></a>
<a id="dimension-06"></a>

## 06 长任务

### 定义与边界

长任务评测工作跨越多个执行轮次、子任务或时间间隔时，过程状态是否持续可管理。它关注等待、阻塞、继续、通知与完成的语义；材料保存归05工作空间，干预手段归02控制层，失败后恢复正确性归11可靠性。执行时间长并不自动意味着具有完整任务管理。

### 检查问题与判断依据

应检查用户或调用方能否区分消息已接收、模型处理、等待外部输入、子任务运行和最终结束，并确认状态如何对应下一责任人。通知要能说明需要决定还是已有结果，费用与时间边界也不能被轮数替代。判断依据是运行生命周期、等待接口、提醒持久化与续接规则，界面空闲不能单独作为业务成功依据。

### dsh 当前表现

长期目标可在同一会话继续下一轮，恢复或分叉后不自动重新启用续行。对话压缩支持更长的工作历史，但摘要增加模型调用且不保证无损，不能缩小所有提示词、工具目录或不可分的大内容。Web 的持久提醒可以把事项投递回会话；回执确认进入收件队列，不证明模型完成事项，任务表和会话的独立写入还可能带来重复提醒。

程序等待契约尤其影响集成：`run()` 在根会话首次空闲后返回，`session/wait` 会等待受管理后代及其引发的后续活动并复核状态。两者都不替业务产品判定成果合格，最后助手文本也不保证只对应当前输入。上层任务应明确接收、活动结束、后代结束与验收通过的对应关系。

**2026-10-19增量判断（alpha.3→rc.2）：**Minimal 增自动压缩，Web／Desktop 可手动 `/compact`；SDK resume 恢复持久会话而不恢复外部进程或自动发新任务。可选 PTC 内存模式尽力保留变量，重启／取消／超时会丢失，默认仍逐次进程。长任务状态、摘要保真与外部对账仍需上层验证。[Minimal 配置](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/bundle/sdk-minimal/cordis.patch.yml)、[SDK 恢复契约](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sdk/client/README.zh.md)、[PTC 内存模式契约](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/ptc-runtime/ptc-runtime-node/README.zh.md)

### 版本与插件证据

主记录为[压缩 CAP-CTX-01](#cap-ctx-01)、[提醒 CAP-RUN-02](#cap-run-02)、[任务等待 CAP-RUN-04](#cap-run-04)。依据[压缩说明][compaction]、[提醒契约][schedule]及[等待实现][sdk-wait]；alpha.1 提醒回到 Web 默认组合、alpha.2 等待语义的变化见[插件演进](PLUGINS.md)和[版本增量](releases/v0.2.1-alpha.2.md)。续行授权在13维护[CAP-RUN-01](#cap-run-01)，子代理能力在12维护[CAP-COL-01](#cap-col-01)。

### 评测结论与待验证事项

**持续执行和等待具有局部契约，业务状态管理待评。** 需要进一步确认阻塞原因、人工输入、子任务与通知能否关联同一业务任务，重启后的提醒是否需要业务去重，以及不同模型下压缩的有效范围。当前没有长任务成功率、时延或重启表现的运行证据，不把修复记录当作可靠性指标。

<a id="dimension-07"></a>

## 07 信任体验

### 定义与边界

信任体验评测用户能否根据产品呈现的证据，理解已发生的动作、仍不确定的结果、数据去向和责任承担。它评价信息是否足以支持判断，不以用户是否感到安心作为能力证明。工具能否停止归02、批准者是谁归03、授权是否有效归04；本维度综合引用这些事实，不另建同名支持记录。

### 检查问题与判断依据

应检查计划、执行结果和最终回复是否清楚区分，用户能否核对文件来源与状态，以及风险说明是否对应真实能力边界。还需检查产品如何解释人工决定、模型建议和系统执行之间的责任，以及数据发送和保留的范围。判断依据既要有可见记录，也要有用户能否正确理解这些记录的证据；后者不能由技术日志的存在代替。

### dsh 当前表现

计划、执行轨迹、文件预览和会话记录为用户核对过程提供了基础。但当前文件卡片反映的是可变源文件，根会话空闲也不等于业务验收；若上层产品将它们呈现为固定交付版本或任务成功，就会形成超出实际机制的期待。现有资料能帮助研究者识别这些差异，尚不能确认普通用户在界面中是否获得了充分说明。

数据方面，会话日志、显式反馈、包清单及 Desktop 交互采集各有开关和行为，不能统称为一个遥测选项。翻译扩展还可能向所选外部服务发送展开的内容。公开说明与可见设置是判断透明度的依据，但没有本项目用户理解测试，也没有实际网络记录，无法确认用户对数据去向和重新启用后的补传有何理解。

**2026-10-19增量判断（alpha.3→rc.2）：**已发送消息的凭据遮罩是显示层能力，不能承诺原始消息、日志或模型出站已脱敏。启用新搜索后的用户提示片段出站、Fetch 缺少目标状态与最终地址，应向使用者说明。信任体验有局部改善，内容治理与真实故障体验仍待评。[Web 遮罩配置](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/bundle/web-app/cordis.patch.yml)、[Search／Fetch 固定说明](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/web/web-deepseek-api/README.zh.md)

### 版本与插件证据

本维度交叉引用[计划 CAP-CTL-01](#cap-ctl-01)、[交付 CAP-FILE-02](#cap-file-02)、[批准 CAP-CTL-03](#cap-ctl-03)与[观察 CAP-OBS-01](#cap-obs-01)。默认外发的已核事实集中在[F-01](FINDINGS.md#f-01--默认-session-log-外发需要独立治理)，Desktop 与翻译的差异见[插件数据通道](PLUGINS.md#data-channels)；不以滚动文档替代本版本证据。

### 评测结论与待验证事项

**证据展示有局部基础，用户理解和责任表达待评。** 当前不能由计划、轨迹和安全说明的存在推导信任体验已经成熟。后续应以具体任务核对用户能否正确辨认文件版本、完成状态、批准后果和数据出站；界面是否提供了充分且及时的解释仍是开放问题。文档研究中的边界说明不等于这些说明已全部进入 dsh 产品界面。

<a id="dimension-08"></a>

## 08 产品指标

### 定义与边界

产品指标评测如何判断 Agent 为目标用户完成了有效工作，以及资源投入、人工参与和后续使用之间的关系。它定义业务结果的统计口径；09评估负责验证方法，10可观测性负责提供可追查记录。统计请求或 token 可以解释消耗，不能直接代表成果被接受。

### 检查问题与判断依据

应先确定一次业务委派的计数单位、接受成果的判据，以及取消、部分交付、重复尝试和人工完成如何计入结果。费用需要明确是否包括后代、压缩、标题和重试，避免同一任务被拆成多个看似成功的活动。判断依据是事件定义、统计口径及其与原始任务的关联，不是在本轮虚构指标数值。

### dsh 当前表现

dsh 提供会话用量统计和执行记录，Desktop 另有产品交互采集；这些可以为资源与使用分析提供原始信息。当前证据不足以确认其已经提供统一的业务任务验收、失败恢复质量和人工交接指标，也没有用户接受结果的公开契约可在本项目中复核。

程序返回、子任务结束和用户验收语义不同，意味着接入产品需要自行规定统计单位与结算时点。用量记录也不自动覆盖整项工作费用的预算控制；限制何时停止应在13自主等级判断。本轮既无真实业务样本，也无成本数据，因此不作效率提升、完成率或单位任务成本结论。

### 版本与插件证据

主记录为[业务指标 CAP-OBS-03](#cap-obs-03)，依据[用量统计说明][stats]与[产品交互采集说明][telemetry]。交叉引用[完成语义 CAP-RUN-04](#cap-run-04)和[预算边界 CAP-OBS-04](#cap-obs-04)；Desktop 采集与普通 Web 的差异见[插件指南](PLUGINS.md#data-channels)。

### 评测结论与待验证事项

**资源与交互信号已有依据，业务结果指标成熟度待评。** 后续需确认任务、尝试和成果是否可稳定关联，人工决定及恢复动作怎样纳入统计，以及费用归集能否覆盖整项工作。没有查明统一口径时保持待评，不将其写为不支持，也不把活跃度或调用量替代业务价值。

<a id="dimension-09"></a>

## 09 评估

### 定义与边界

评估维度检查用什么方法验证产品承诺、能力边界和版本变化，强调样本、环境、判据与结果的可复核性。它不等同于08中的运营指标，也不把代码测试数量当作任务质量。对本项目，还必须区分读到上游测试、观察到上游运行结果和亲自完成复验。

### 检查问题与判断依据

应检查验证对象是否覆盖任务输入、工具效果、人工决定和成果验收，并确认失败路径如何进入后续版本比较。每个样本需要说明预期结果、环境条件、判断者和允许的不确定性。文档与源码可以验证契约是否存在；实际完成质量、故障恢复和目标用户表现需要相应运行或使用证据。

### dsh 当前表现

本项目已阅读固定 tag 的测试策略，以及文件交付和恢复相关上游测试。它们为窄能力提供了具体断言，例如文件卡片不提供浏览器下载、导出不包含卡片源文件字节。这些断言帮助限定支持状态，但本轮没有运行，也未把当前上游持续集成结果作为已验证事实。

对业务任务的最终正确性、跨模型压缩质量、真实人工交接、长期任务成本和恢复表现，尚无本项目样本结果。已有版本研究可提出优先验证题目，但不能说明上游已完成同等覆盖的产品评估，更不能据测试文件存在宣称发布质量达到某一等级。

**2026-10-19增量判断（alpha.3→rc.2）：**本轮11个 rc.2 归档 integrity 及20份 YAML静态比较通过，仅提升发行配置的证据覆盖，不增加运行测试数或改变成熟度。[发行抽查范围](PLUGINS.md#发行包核验与版本纪律)

### 版本与插件证据

主记录为[测试资产 CAP-OBS-02](#cap-obs-02)，依据[测试策略][testing]、[文件交付测试][present-test]和[恢复测试][resume-test]。实际发行配置还应对照[插件归档核验](PLUGINS.md#发行包核验与版本纪律)，避免以 tag 上的测试对象直接代表不同发行内容。证据状态不因本次框架重写而升级。

### 评测结论与待验证事项

**契约核验有初步方法与样本，任务效果评估待评。** 后续可围绕完成语义、远程交付、权限入口差异、未知副作用和压缩保真建立验证样本；每项先说明判据与环境，不先填成功率。当前任务仍限静态研究，这些是待验证事项，不代表已经开展安装、测试或模型调用。

<a id="dimension-10"></a>

## 10 可观测性

### 定义与边界

可观测性评测能否从记录解释一次任务如何推进、为何失败，以及哪些动作和决定影响了结果。它负责事实链和诊断粒度；08定义结果如何衡量，09决定怎样验证，07关注用户能否理解。业务权限和日志访问控制则需与04明确连接，不能由有日志自动获得。

### 检查问题与判断依据

应检查会话消息、模型请求、工具调用、子任务、批准、文件与错误能否关联，历史记录与实时状态是否一致，以及不同使用者能够看到哪些内容。导出还需说明范围、敏感信息和源文件是否包含其中。判断依据是事件契约、持久化和导出格式、查询与界面投影；最终回复不是完整执行证据。

### dsh 当前表现

Session 事件、Trajectory 和用量统计提供执行回看基础，深层诊断能力可按组合加入。重建历史应使用持久事件，实时协调通知不能直接替代它们。当前版本对等待、压缩和后台状态显示已有修正，但这不足以证明界面在所有竞态下都准确，或能自动建立跨业务任务的完整关联。

用户可用 `/export` 导出会话日志 ZIP；导出不携带文件卡片所指源文件字节。记录留存与外发又是不同维度：默认会话日志、反馈、包清单和 Desktop 交互采集分别处理，事件可回放并不自动拥有防篡改、组织审计权限或保留期保证。排障视图、业务统计和企业审计需要各自明确范围。

**2026-10-19增量判断（alpha.3→rc.2）：**新 Search／Fetch API 不产生辅助请求事件，工具调用与结果仍进会话记录；只统计辅助模型请求会漏掉这类服务调用。意外退出后的“任务已停止”是官方报告的状态显示修复，未实测。完整审计关联仍待评。[Search／Fetch 固定说明](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/web/web-deepseek-api/README.zh.md)、[alpha.3 发布](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-alpha.3)

### 版本与插件证据

主记录为[执行观察 CAP-OBS-01](#cap-obs-01)和[日志导出 CAP-FILE-04](#cap-file-04)。依据[生命周期][lifecycle]、[统计][stats]、[导出实现][zip]与[交付测试][present-test]。当前状态显示变化见[版本分析](releases/v0.2.1-alpha.2.md)，外发通道条件保留在[F-01](FINDINGS.md#f-01--默认-session-log-外发需要独立治理)和[插件指南](PLUGINS.md#data-channels)。

### 评测结论与待验证事项

**执行记录与查询有局部成熟表现，跨角色业务追踪待评。** 后续应核对用户视图、原始事件、后代和成本是否对应同一任务，导出如何选择后代与附件，以及敏感记录的访问和保留责任。不能把记录完整性、审计合规和界面可理解性合并为一个“有 trace”的结论。

<a id="recovery"></a>
<a id="dimension-11"></a>

## 11 可靠性

### 定义与边界

可靠性评测故障发生后，系统能否保存已知事实、控制重复副作用，并让工作安全地继续或交由人处理。它关注失败路径与恢复正确性，区别于06的常态过程管理和05的材料承载。自动重试数量、会话可重开或历史修复次数都不能单独代表可靠性。

### 检查问题与判断依据

应检查请求未发出、动作已发生但回执丢失、存储未完成和运行进程退出时，系统如何判断结果。还需明确哪些动作可重做，哪些必须先查询外部状态，以及何时需要交接。判断依据是故障状态的表达、持久记录和具体工具契约；只有实际验证才能确认恢复时延和重复抑制效果。

### dsh 当前表现

dsh 的持久会话与修复处理区分未启动和结果未知，帮助续接时保留不确定性。会话恢复不负责撤销外部事务，也不保证外部动作只执行一次。对可能已经生效的操作，接入产品或操作者需要核对外部系统，再决定重试、补偿或人工处理。

取消采用协作机制，超时返回不等于底层资源完全释放；硬中断发生在结算前时，部分流记录可能尚未持久化。提醒的两处独立写入和 Team 消息接纳也有各自的重复与交付边界，不能统称为可靠工作流。本轮仅复用这些已确认契约，没有故障注入或重启试验。

**2026-10-19增量判断（alpha.3→rc.2）：**SDK resume 对缺失、不可读、不兼容、占用会话失败且不创建替代，不恢复 Shell／浏览器等外部进程。新网页 API 无自动重试或提供者回退，Fetch 的 HTTP 200 不能当作目标页面真实状态。恢复入口更明确，实际恢复成功率与业务重试安全性仍待验证。[SDK 恢复契约](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sdk/client/README.zh.md)、[Search／Fetch 固定说明](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/web/web-deepseek-api/README.zh.md)

### 版本与插件证据

主记录为[恢复 CAP-RUN-03](#cap-run-03)，依据[修复源码][repair]和[执行故障说明][loop]。交叉引用[取消 CAP-CTL-02](#cap-ctl-02)、[提醒 CAP-RUN-02](#cap-run-02)及[协作消息 CAP-COL-02](#cap-col-02)。alpha.2 的超时修复、Team 消息机制变化见[当前增量](releases/v0.2.1-alpha.2.md)与[F-03](FINDINGS.md#f-03--team-简化了消息链路也改变了交付承诺)。

### 评测结论与待验证事项

**恢复语义有局部设计，故障安全效果待评。** 保留“结果未知”是可以借鉴的机制，但真实任务是否能恢复、是否会重复外部动作、如何保留部分成果均需按工具验证。优先明确外部对账与重试责任，再评估目标环境下的取消、重启和持久化失败。没有统一回滚证据时，不承诺所有动作可撤销。

<a id="resources"></a>
<a id="collaboration"></a>
<a id="extensions"></a>
<a id="operations"></a>
<a id="dimension-12"></a>

## 12 平台能力

### 定义与边界

平台能力评测执行、连接、配置与治理能否被多个 Agent 和任务复用，并明确运行框架与上层平台的分工。它不以插件数量或 Agent 数量衡量成熟度。部署入口只是其中一部分；组织身份归04、结果衡量归08、可托付范围归13，相关实现可作为本维度的共用依赖。

### 检查问题与判断依据

应检查共用能力如何组合和版本化、跨任务变更会影响谁、外部系统需要哪些认证，以及发布和退出时由谁负责。共享接口还需说明后端能力差异和故障语义，避免表面统一。判断依据是入口组合、插件配置、模型和连接器契约、实际发行内容，以及明确的组织生命周期边界。

### dsh 当前表现

dsh 可通过插件组合执行循环、模型、工具、持久化和界面，提供多种交互及程序入口。外部工具连接与模型适配需要具体配置，组件加载不代表已有可用服务；MCP 支持工具与资源，但不支持提示词模板。DeepSeek 当前使用 Messages 协议，其他模型的能力需按端点确认。内置与外部子代理的覆盖项不同，实验 Team 也不能代替可靠消息系统。

入口组合影响实际授权和工具范围，部分全局工具可跨会话模式生效，宿主插件不受工作区文件沙箱约束。Web 支持本地及受控远程访问，但组织登录、租户隔离、Agent 发布审批和下线没有完整交付证据。当前共享运行机制较清楚，业务用户管理、验收、预算与企业运维仍需上层平台承担或继续核实。

| 能力责任 | 当前 dsh 依据 | 仍需明确的承担方 |
|---|---|---|
| 执行与扩展组合 | 插件、会话入口、模型及工具服务 | 具体业务配置与插件信任由接入方确定 |
| 多 Agent 协作 | 子代理接口、实验 Team 任务和消息 | 分工验收、消息重试和冲突处理需明确责任 |
| 远程服务入口 | 浏览器认证、监听与 TLS／代理配置 | 证书运维、组织身份和多用户隔离需单独提供 |
| 企业生命周期 | 未确认完整注册、评估、发布与下线契约 | 当前为上层平台需求，不能假定 harness 已交付 |

**2026-10-19增量判断（alpha.3→rc.2）：**alpha.4 起兼容声明优先 `engines.dsh`；自定义市场随包关闭，无官方索引，Creator 发现只读，安装权限独立。rc.2 新网页提供者需配置且依赖外部 API，默认仍旧搜索／HTTP；此处与模型路由分开评估。pi-ai manifest 为 `^1.1.0`，Azure 旧名称需迁移。扩展机制更丰富，索引信任、外部服务和组织治理仍待验证。[兼容判断源码](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/boot/app-boot/src/plugin-compatibility.ts)、[自定义市场](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/boot/plugin-market/README.zh.md)、[Search／Fetch 固定说明](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/web/web-deepseek-api/README.zh.md)、[pi-ai manifest](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/llm/llm-pi-ai/package.json)

### 版本与插件证据

主记录包括[扩展 CAP-EXT-01](#cap-ext-01)、[MCP CAP-EXT-03](#cap-ext-03)、[模型 CAP-MOD-01](#cap-mod-01)与[CAP-MOD-02](#cap-mod-02)、[部署 CAP-DEP-01](#cap-dep-01)与[治理 CAP-DEP-02](#cap-dep-02)、[子代理 CAP-COL-01](#cap-col-01)与[Team CAP-COL-02](#cap-col-02)。依据[插件管理][plugin-manager]、[入口配置][profile]及[远程部署指南][public-deploy]。随附关闭、按需安装、版本演进与归档差异统一在[PLUGINS](PLUGINS.md)维护，不在本页复制包清单。

### 评测结论与待验证事项

**共享运行机制有局部成熟表现，企业平台成熟度待评。** 当前适合借鉴可组合执行与能力服务，不将本地插件管理解释为完整组织治理。后续需核对目标入口的实际工具、权限和依赖，连接器故障与模型兼容，及配置升级对运行任务的影响。已发现的发行文字差异和历史包缺口保留为证据限制，不据此泛化为供应链故障。

<a id="dimension-13"></a>

## 13 自主等级

### 定义与边界

自主等级评测某类任务可以在多大范围内持续委派，以及何时必须缩小范围、停止或交由人决定。判断建立在任务风险、动作可逆性、实际权限和恢复证据之上，不按模型能力、运行轮数或是否全自动划等级。相同 Agent 在不同任务上可以具有不同委派边界。

### 检查问题与判断依据

应检查自动继续的授权从何而来、何时失效，资源耗尽和风险变化时如何停止，以及停止之后谁能理解并接手。更宽权限与更多执行轮数必须有相应证据支撑，不能反过来作为成熟度证明。判断依据组合02控制、03人类节点、04权限和11恢复的结果，而不是新增一套固定审批流程。

### dsh 当前表现

Goal 支持在同一会话持续推进，恢复或分叉后不会自动重新启用续行。这提供了显式恢复委派的机制，但轮数上限不等于金额或时间限制。主循环、子代理、压缩、标题、重试和自动评审都可能增加消耗；当前尚未确认统一的整项任务费用上限、预算耗尽状态和取消已发请求的费用处理。

计划、审批和权限预设可用于组合不同委派方式，但 Full access、自动评审或长期目标开启都不能单独证明某类任务适合更高自主。对于外部副作用不明、无法撤销或缺少验收条件的工作，当前静态资料不足以支撑扩大委派范围。以下只是评测时应补的证据，不是 dsh 已实现的等级体系或本项目的运行建议。

| 任务特征 | 判断委派边界需要补齐的证据 |
|---|---|
| 结果可重做、主要读取材料 | 数据授权、来源正确性、停止与结果核对方式 |
| 修改工作区且成果需验收 | 写入范围、变更前后内容、可保留版本与人工验收 |
| 改变外部状态或难以撤销 | 动作批准、结果对账、未知状态处理及责任人 |

**2026-10-19增量判断（alpha.3→rc.2）：**恢复持久会话和 PTC 跨调用内存不代表无人值守授权延续；新直接网页 API 虽无辅助模型 token，结果上下文和独立服务仍有成本。没有证据提高整项任务预算与自主成熟度。[SDK 恢复契约](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sdk/client/README.zh.md)、[PTC 内存模式契约](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/ptc-runtime/ptc-runtime-node/README.zh.md)、[Search／Fetch 固定说明](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/web/web-deepseek-api/README.zh.md)

### 版本与插件证据

主记录为[持续目标 CAP-RUN-01](#cap-run-01)和[任务预算 CAP-OBS-04](#cap-obs-04)，依据[Goal 契约][goal]、[压缩][compaction]与[统计][stats]。交叉引用[批准 CAP-CTL-03](#cap-ctl-03)和[恢复 CAP-RUN-03](#cap-run-03)；自动评审限制见[插件说明](PLUGINS.md#review)，不得从可选开关推导授权范围已经经过验证。

### 评测结论与待验证事项

**持续委派有局部机制，按任务风险分级的成熟度待评。** 当前不给 dsh 一个统一自主等级，也不把全自动设为目标。下一步需为明确任务约定权限、费用与停止条件，并取得相应恢复和验收证据；在此之前维持借鉴、验证、观察的研究姿态。业务预算所有者、超额处理及风险变化后的责任交接仍是待确认项。

<a id="evidence-index"></a>

## 现有36项能力ID证据索引

这里是逐项支持状态的唯一维护位置。每项标注一个主归属维度，章节间的交叉引用不形成第二份记录；主归属是研究分类，不代表实现只能影响该维度。无单列更新的条目沿用 alpha.2 与2026-10-13核查日期；仅受本周证据影响的条目增加2026-10-19记录。

36项的状态仍为支持15项、部分14项、不支持2项、待确认5项；证据仍为仅文档19项、已读源码12项、已有上游测试但未运行5项、我们实测0项。它们是覆盖范围，不是成熟度评分。“不支持”仅用于有明确否定依据的窄能力；对完整产品目标的证据不足仍写待评。维度结论在对应章节维护，不把能力状态提升为运行效果结论。

<a id="cap-in-01"></a>

### CAP-IN-01 · 从工作区会话输入任务与附件

主归属：[01 任务入口](#dimension-01)。支持状态：**支持**；证据：**已读源码**；实现归属：默认插件。

条件为Web；文件上传插件与会话 UI。支持输入和文件保存，不证明模型能理解每一种上传格式。

依据：[Web 组合配置][web]、[使用指南][web-guide]。后续核验：各文件类型的读取工具和大小限制是否与界面提示一致？
**更新：2026-10-19，rc.2／`687f282e8625c6b8d11ff58211a90524be2e4317`。** Web Minimal 新增图片读取／压缩条件，模型图片支持仍另核；[Web Minimal 配置](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/bundle/web-app/presets/minimal.patch.yml)。


<a id="cap-in-02"></a>

### CAP-IN-02 · 程序调用与事件订阅

主归属：[01 任务入口](#dimension-01)。支持状态：**支持**；证据：**已读源码**；实现归属：默认插件。

条件为Headless／TypeScript、Python SDK；相应 profile。不同入口的交互、默认工具和权限不同；调用返回不自动表示业务成功。

依据：[SDK 契约][sdk]、[等待实现][sdk-wait]、[SDK Minimal 配置][sdk-minimal]。后续核验：逐项补齐 SDK、Headless 与 ACP 的交互及权限差异。
**更新：2026-10-19，rc.2／`687f282e8625c6b8d11ff58211a90524be2e4317`。** TypeScript `resumeSession`／Python `resume_session` 恢复原持久会话，需沿用 home 和工作区；不发送新输入、不恢复外部进程。[SDK 恢复契约](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sdk/client/README.zh.md)、[Python 恢复入口](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/python/sdk/src/deepseek_harness/api.py)。


<a id="cap-in-03"></a>

### CAP-IN-03 · 官方 IM 会话与附件入口

主归属：[01 任务入口](#dimension-01)。支持状态：**待确认**；证据：**仅文档**；实现归属：外部平台／连接器（实现待确认）。

条件为固定版本产品与插件资料检索范围。本轮未确认官方 Slack、飞书等运行入口；不据此断言不存在社区接入。

依据：[产品说明][readme]、[包目录][packages]。后续核验：是否有已发布、可验证的官方 IM 包及收件／附件契约？

<a id="cap-in-04"></a>

### CAP-IN-04 · 外部事件触发 Agent 工作

主归属：[01 任务入口](#dimension-01)。支持状态：**部分**；证据：**仅文档**；实现归属：官方可选。

条件为实验 GitHub webhook／规则 runtime，显式配置。签名校验与202接纳不等于规则成功或持久队列落盘。

依据：[事件入口说明][webhook]。后续核验：入口、队列持久性、重试与业务幂等分别由谁负责？

<a id="cap-ctl-01"></a>

### CAP-CTL-01 · 计划展示与用户审阅

主归属：[02 控制层](#dimension-02)。支持状态：**支持**；证据：**仅文档**；实现归属：默认插件。

条件为Web Plan 组合；exit_plan_mode。计划约束主要在提示词；不是文件权限。tag 与 npm 的计划提示词差异见 PLUGINS。

依据：[计划模式说明][plan]。后续核验：对实际发行包，退出计划的确认与取消分支如何对应日志？

<a id="cap-ctl-02"></a>

### CAP-CTL-02 · 运行中插话、暂停与取消

主归属：[02 控制层](#dimension-02)。支持状态：**部分**；证据：**已读源码**；实现归属：核心／默认插件。

条件为Agent loop、inbox、Goal；后端支持协作取消。停止、资源回收、持久终态不同时发生；多个历史修复不能当作可靠性指标。

依据：[执行循环源码][loop-source]、[执行与恢复说明][loop]。后续核验：取消与新消息、慢工具、子任务完成同时发生时的优先级是什么？

<a id="cap-ctl-03"></a>

### CAP-CTL-03 · 工具权限请求与人工批准

主归属：[03 人类节点](#dimension-03)。支持状态：**部分**；证据：**已读源码**；实现归属：默认插件。

条件为base 支持的权限预设；入口能呈现审批。默认配置因 profile 不同；审批并不覆盖宿主插件和所有外部副作用。

依据：[权限预设][permission]、[基础配置][base]、[SDK Minimal 配置][sdk-minimal]。后续核验：哪些调用跳过人工路径，哪些审批事件能关联实际批准者？

<a id="cap-sec-01"></a>

### CAP-SEC-01 · 约束工具进程的文件访问

主归属：[04 权限模型](#dimension-04)。支持状态：**部分**；证据：**仅文档**；实现归属：默认插件。

条件为本地 sandbox 支持的 OS／backend；明确策略。存在 partial 等能力差异，无完整网络／租户隔离保证；未安全审计。

依据：[沙箱说明][sandbox]、[安全声明][safety]。后续核验：按目标 OS 核实读、写、网络与失败闭合的实际范围。

<a id="cap-sec-02"></a>

### CAP-SEC-02 · 隔离模型与工具可用的凭据

主归属：[04 权限模型](#dimension-04)。支持状态：**部分**；证据：**仅文档**；实现归属：默认插件／外部平台。

条件为本地 credentials 与适配器凭据引用。本地文件权限不向同一 OS 用户的工具隔离机密；企业凭据代理需另定。

依据：[凭据说明][credentials]。后续核验：哪些凭据会进入子进程环境，哪些仅由 Host 逐请求读取？
**更新：2026-10-19，rc.2／`687f282e8625c6b8d11ff58211a90524be2e4317`。** Web／Desktop 已保存凭据优先，Headless 默认禁用本地凭据；这改变来源选择，不改变同用户工具可读的隔离限制。[凭据优先级](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/credentials/credentials-local/README.zh.md)、[Headless 配置](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/bundle/headless/cordis.patch.yml)。显示遮罩不能替代出站治理，见[04权限模型](#dimension-04)。


<a id="cap-sec-03"></a>

### CAP-SEC-03 · 组织身份、角色与租户授权

主归属：[04 权限模型](#dimension-04)。支持状态：**待确认**；证据：**仅文档**；实现归属：外部平台（实现待确认）。

条件为企业部署需求；不是默认单操作者入口的保证。匿名安装 ID、模型登录和浏览器 cookie 不等于组织 RBAC／SSO。

依据：[安装标识说明][identity]、[浏览器连接与鉴权][connection]、[产品说明][readme]。后续核验：是否有官方企业身份契约，或明确的上层身份接入点？

<a id="cap-file-01"></a>

### CAP-FILE-01 · 读取和改变 Session 工作目录

主归属：[05 工作空间](#dimension-05)。支持状态：**支持**；证据：**已读源码**；实现归属：默认插件。

条件为working_directory 工具及目录服务挂载。切换 Session 目录不改变已启动 Shell／进程的自身目录。

依据：[目录工具源码][cwd]。后续核验：目录迁移对相对路径、fork、恢复和已有终端分别如何生效？

<a id="cap-file-02"></a>

### CAP-FILE-02 · 声明文件并展示交付卡片

主归属：[05 工作空间](#dimension-05)。支持状态：**支持**；证据：**已有上游测试但未运行**；实现归属：默认插件。

条件为Web standard／PTC／创造模式的 present。记录当前源文件路径；可以预览及通过 Host 打开／定位。文件后续修改会改变所见内容。

依据：[文件卡片说明][present]、[文件交付测试][present-test]。后续核验：远程浏览器、无桌面 Host、SSH 文件系统分别支持哪些打开动作？

<a id="cap-file-03"></a>

### CAP-FILE-03 · 从 present 卡片下载到访问者电脑

主归属：[05 工作空间](#dimension-05)。支持状态：**不支持**；证据：**已有上游测试但未运行**；实现归属：默认插件。

条件为仅指当前官方 Web present 卡片内置入口。官方决策不保留 present 下载端点；测试断言没有浏览器下载。不是“dsh 无法传文件”。

依据：[文件交付设计决策][present-decision]、[文件交付测试][present-test]。后续核验：后续 release 是否新增明确的客户端交付入口与保留策略？

<a id="cap-file-04"></a>

### CAP-FILE-04 · 下载 Session 日志 ZIP

主归属：[10 可观测性](#dimension-10)。支持状态：**支持**；证据：**已有上游测试但未运行**；实现归属：默认插件。

条件为Web /export／session.export。响应为 attachment ZIP；不包含 present 声明所指源文件的字节。

依据：[日志导出实现][zip]、[文件交付测试][present-test]。后续核验：后代会话选择、附件及敏感内容导出范围是否分别清楚？

<a id="cap-file-05"></a>

### CAP-FILE-05 · 通过鉴权 API 读取文件内容

主归属：[04 权限模型](#dimension-04)。支持状态：**支持**；证据：**已读源码**；实现归属：默认插件。

条件为GET／HEAD /api/file，组合文件系统允许读取的绝对路径。受浏览器鉴权、文件权限和响应大小限制；没有下载按钮语义，不能据 MIME 限制推断授权。

依据：[文件读取实现][file-api]、[浏览器连接与鉴权][connection]。后续核验：具体 profile 的读取根目录与 maxImageBytes 默认及覆盖项是什么？

<a id="cap-file-06"></a>

### CAP-FILE-06 · 由 present 保存不可变交付文件副本

主归属：[05 工作空间](#dimension-05)。支持状态：**不支持**；证据：**已有上游测试但未运行**；实现归属：默认插件。

条件为仅指 present 交付声明及其 Session 导出。声明不复制／保留源字节，修改、删除或移动源文件会影响后续访问。

依据：[文件交付设计决策][present-decision]、[文件交付测试][present-test]。后续核验：若产品要长期验收版本，需哪一层提供快照、保留和删除？

<a id="cap-ctx-01"></a>

### CAP-CTX-01 · 压缩长对话上下文

主归属：[06 长任务](#dimension-06)。支持状态：**部分**；证据：**仅文档**；实现归属：默认插件。

条件为compaction 与可选工具结果 pruner；模型容量已知。摘要需要额外模型调用；不能缩减全部系统提示词、工具目录或不可分单元，也不保证语义无损。

依据：[压缩说明][compaction]。后续核验：不同模型预算和大工具结果的有效阈值、失败行为是什么？
**更新：2026-10-19，rc.2／`687f282e8625c6b8d11ff58211a90524be2e4317`。** Minimal 增图片读取和自动压缩；Web／Desktop 提供 `/compact`。[Minimal 配置](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/bundle/sdk-minimal/cordis.patch.yml)。新增组合不证明摘要无损，维持部分支持；本记录的压缩算法证据仍为文档，配置补充不等于运行验证。


<a id="cap-ctx-02"></a>

### CAP-CTX-02 · 让 Agent 搜索历史会话

主归属：[05 工作空间](#dimension-05)。支持状态：**支持**；证据：**仅文档**；实现归属：官方可选（随附关闭）。

条件为启用 session-search bundle；当前工作区。增加全局工具，包括 minimal；与侧栏搜索、跨用户知识权限是不同问题。

依据：[会话搜索说明][session-search]。后续核验：工作区范围、隐藏／归档会话与索引生命周期如何约束？

<a id="cap-ctx-03"></a>

### CAP-CTX-03 · 外接长期记忆与管理其生命周期

主归属：[05 工作空间](#dimension-05)。支持状态：**部分**；证据：**仅文档**；实现归属：第三方／外部平台。

条件为官方默认关闭的 MCP memory 示例。可连接外部系统；初始化、身份、保留、删除及迁移由提供方负责，没有通用知识治理保证。

依据：[外部记忆指南][memory]。后续核验：所选系统如何处理权限过滤、来源、冲突与删除后召回？

<a id="cap-run-01"></a>

### CAP-RUN-01 · 在同一会话自动推进长期目标

主归属：[13 自主等级](#dimension-13)。支持状态：**支持**；证据：**仅文档**；实现归属：默认插件。

条件为Goal 已启用续行且 round 容量允许。恢复／fork 不自动重启续行；round 上限不是费用或时长预算。

依据：[长期目标说明][goal]。后续核验：暂停、blocker 与后续人工输入如何决定下一轮准入？

<a id="cap-run-02"></a>

### CAP-RUN-02 · 持久定时提醒与恢复投递

主归属：[06 长任务](#dimension-06)。支持状态：**部分**；证据：**仅文档**；实现归属：默认插件。

条件为Web schedule；标准／PTC／创造模式提供工具。投递回执确认 inbox，不确认模型执行；Session 与任务表是独立写入，故障后可能重复提醒。

依据：[提醒投递说明][schedule]、[Web 组合配置][web]。后续核验：重启、补发与重复投递是否需要上层业务幂等键？

<a id="cap-run-03"></a>

### CAP-RUN-03 · 恢复持久会话并识别未知副作用

主归属：[11 可靠性](#dimension-11)。支持状态：**部分**；证据：**已读源码**；实现归属：核心／默认插件。

条件为JSONL Session 与工具恢复处理。区分未启动、结果未知；可继续对话不等于外部事务回滚或 exactly-once。

依据：[恢复修复源码][repair]、[执行与恢复说明][loop]。后续核验：对有副作用的具体工具，谁核对外部状态并决定重试？
**更新：2026-10-19，rc.2／`687f282e8625c6b8d11ff58211a90524be2e4317`。** SDK resume 恢复持久历史与目录；占用／缺失／不兼容时失败且不创建替代。[SDK 恢复契约](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sdk/client/README.zh.md)、[resume 实现](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sdk/client/src/api.ts)。PTC 内存模式不是持久恢复：[PTC 内存模式契约](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/ptc-runtime/ptc-runtime-node/README.zh.md)。


<a id="cap-run-04"></a>

### CAP-RUN-04 · 等待子树完成并形成业务回执

主归属：[06 长任务](#dimension-06)。支持状态：**部分**；证据：**已读源码**；实现归属：核心／默认插件。

条件为SDK session/wait；受管理后代。run 仍在根首次 idle 结束活动区间；wait 不替上层判定业务验收成功。

依据：[等待实现][sdk-wait]、[调用实现][sdk-run]。后续核验：业务任务 ID、多个 prompt 与最后回复的因果归属如何建立？
**更新：2026-10-19，rc.2／`687f282e8625c6b8d11ff58211a90524be2e4317`。** resume 不发送新输入；`run()` 与子树 wait、业务验收仍分别判断，不因恢复 API 新增改变支持状态。[SDK 恢复契约](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sdk/client/README.zh.md)、[当前 run 实现](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sdk/client/src/api.ts)。


<a id="cap-col-01"></a>

### CAP-COL-01 · 创建、fork 与继续子代理

主归属：[12 平台能力](#dimension-12)。支持状态：**支持**；证据：**已读源码**；实现归属：默认插件／官方可选。

条件为内置子代理；外部 provider 需安装配置。工具与后端能力不同；当前统一 activation 不等于跨后端同样支持所有覆盖项。

依据：[基础配置][base]、[子代理说明][subagent]。后续核验：逐后端核对模型、工具过滤、取消、持久状态与完成回执。

<a id="cap-col-02"></a>

### CAP-COL-02 · 团队任务板与成员消息

主归属：[12 平台能力](#dimension-12)。支持状态：**部分**；证据：**已读源码**；实现归属：官方可选（随附关闭）。

条件为实验 Team bundle。任务 CAS、直接 inbox 和发送接纳不是可靠消息总线；旧重试／去重机制已移除。

依据：[协作实现][team-source]、[协作说明][team]。后续核验：成员退出、结果未知、冲突任务及重试的责任如何分配？

<a id="cap-ext-01"></a>

### CAP-EXT-01 · 组合、启停与版本化插件能力

主归属：[12 平台能力](#dimension-12)。支持状态：**支持**；证据：**已读源码**；实现归属：核心／默认插件。

条件为profile、bundle、preset 和插件管理器。Host 全局工具可跨 preset；HMR、包升级和实例生命周期不完全等价。发行包差异另见 PLUGINS。

依据：[入口组合配置][profile]、[Web 组合配置][web]、[插件管理说明][plugin-manager]。后续核验：给定 profile 的实际工具、权限、hooks 和依赖变更能否完整列出？
**更新：2026-10-19，rc.2／`687f282e8625c6b8d11ff58211a90524be2e4317`。** 兼容判断优先 `engines.dsh`，否则检查 dsh peer；自定义市场需启用并添加源，无官方索引，`plugin_market`只读发现与安装分开。[兼容判断源码](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/boot/app-boot/src/plugin-compatibility.ts)、[自定义市场](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/boot/plugin-market/README.zh.md)。发布样本与历史差异见[PLUGINS](PLUGINS.md#发行包核验与版本纪律)。


<a id="cap-ext-02"></a>

### CAP-EXT-02 · 复用外部 command hooks

主归属：[02 控制层](#dimension-02)。支持状态：**部分**；证据：**仅文档**；实现归属：官方可选。

条件为显式挂载 Codex／Claude hooks 并指定配置路径。仅支持文档规定的子集；配置失败可能警告后继续，不能当成默认强制策略。

依据：[Codex 命令挂钩说明][hooks]、[Claude 命令挂钩说明][claude-hooks]。后续核验：每个 hook 的失败策略、超时、日志和强制续行范围是什么？

<a id="cap-ext-03"></a>

### CAP-EXT-03 · 接入 MCP 工具与资源

主归属：[12 平台能力](#dimension-12)。支持状态：**部分**；证据：**仅文档**；实现归属：默认插件／第三方。

条件为配置 MCP 服务器及认证；stdio／HTTP。支持工具、资源与资源模板；不支持 MCP prompt 模板。服务器行为、权限与可靠性不由协议自动保证。

依据：[外部工具连接说明][mcp]。后续核验：重连后目录变化、取消、分页失败与认证刷新如何影响运行任务？

<a id="cap-mod-01"></a>

### CAP-MOD-01 · 调用 DeepSeek Messages 路由

主归属：[12 平台能力](#dimension-12)。支持状态：**支持**；证据：**已读源码**；实现归属：默认插件。

条件为官方适配器；适配的凭据与 Messages endpoint。已移除旧 protocol 配置；错误网关协议不能靠修改名称适配。

依据：[DeepSeek 适配器源码][llm]。后续核验：自定义 endpoint 对图片、扩展字段、缓存与取消的支持是否一致？
**更新：2026-10-19，rc.2／`687f282e8625c6b8d11ff58211a90524be2e4317`。** rc.2 release 声明适配 DeepSeek-V4.1-Flash-1017，模型可用性受账号与路由条件影响；不作模型效果结论。[rc.2 发布](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-rc.2)。网页 Search／Fetch 是独立外部服务，见[12平台能力](#dimension-12)。


<a id="cap-mod-02"></a>

### CAP-MOD-02 · 配置其他模型提供方

主归属：[12 平台能力](#dimension-12)。支持状态：**部分**；证据：**仅文档**；实现归属：默认插件／第三方。

条件为pi-ai 显式 provider 配置。挂载插件时可以没有路由；模型目录和 ID 随依赖变化，不保证每项能力兼容。

依据：[其他模型配置][pi-ai]。后续核验：以目标模型逐项确认工具、视觉、动态系统提示词及统计字段。
**更新：2026-10-19，rc.2／`687f282e8625c6b8d11ff58211a90524be2e4317`。** alpha.3 将 Azure 提供方名 `azure-openai-responses` 改为 `azure`；rc.2 pi-ai manifest 为 `^1.1.0`，不能将目录及版本声明等同兼容测试。[pi-ai manifest](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/llm/llm-pi-ai/package.json)、[alpha.3 发布](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-alpha.3)。


<a id="cap-obs-01"></a>

### CAP-OBS-01 · 回看执行事件与用量

主归属：[10 可观测性](#dimension-10)。支持状态：**支持**；证据：**仅文档**；实现归属：核心／默认插件／官方可选。

条件为Session、Trajectory、stats；深层诊断可选。持久事件与实时协调通知不同；日志不自动获得防篡改和组织审计权限。

依据：[事件与状态说明][lifecycle]、[用量统计说明][stats]。后续核验：用户视图、原始事件和成本统计是否能关联同一任务及子树？
**更新：2026-10-19，rc.2／`687f282e8625c6b8d11ff58211a90524be2e4317`。** Search／Fetch 的直接 API 请求没有辅助请求事件，常规工具调用／结果仍保留；审计覆盖需包含独立服务调用。[Search／Fetch 固定说明](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/web/web-deepseek-api/README.zh.md)。


<a id="cap-obs-02"></a>

### CAP-OBS-02 · 借助上游测试核对能力契约

主归属：[09 评估](#dimension-09)。支持状态：**支持**；证据：**已有上游测试但未运行**；实现归属：核心（上游测试资产）。

条件为固定 tag 的测试策略与已阅读测试。确认测试和断言存在，未运行、未读取本轮 CI 结果；不代表生产任务成功率。

依据：[上游测试策略][testing]、[文件交付测试][present-test]、[恢复测试][resume-test]。后续核验：哪些现有无模型测试覆盖最高优先级问题，何时另行授权复验？

<a id="cap-obs-03"></a>

### CAP-OBS-03 · 按业务任务统计验收与恢复质量

主归属：[08 产品指标](#dimension-08)。支持状态：**待确认**；证据：**仅文档**；实现归属：外部平台（实现待确认）。

条件为企业任务完成／接受／恢复指标。现有 token 统计和产品交互埋点不足以确认业务验收指标已交付。

依据：[用量统计说明][stats]、[产品交互采集说明][telemetry]。后续核验：是否存在任务级结果定义、验收事件与失败样本的公开契约？

<a id="cap-obs-04"></a>

### CAP-OBS-04 · 统一限制整项任务费用

主归属：[13 自主等级](#dimension-13)。支持状态：**待确认**；证据：**仅文档**；实现归属：外部平台（实现待确认）。

条件为包含主循环、子代理、摘要、评审与重试。未确认通用货币预算与耗尽终态；不能将输出上限或 Goal round 当成总预算。

依据：[长期目标说明][goal]、[压缩说明][compaction]、[用量统计说明][stats]。后续核验：预算所有者、实时归集、超额处理和取消已发请求怎样设计？
**更新：2026-10-19，rc.2／`687f282e8625c6b8d11ff58211a90524be2e4317`。** 新 API 没有辅助模型 token，不等于没有抓取服务或结果上下文成本，整项任务预算仍待确认。[Search／Fetch 固定说明](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/web/web-deepseek-api/README.zh.md)。


<a id="cap-dep-01"></a>

### CAP-DEP-01 · 本地运行与受控远程 Web 入口

主归属：[12 平台能力](#dimension-12)。支持状态：**支持**；证据：**仅文档**；实现归属：默认插件／外部平台。

条件为Web／Desktop；指定监听、TLS／代理配置。公告 URL、Host 校验与身份认证各自独立；证书生命周期仍需外部运维。

依据：[远程部署指南][public-deploy]、[浏览器连接与鉴权][connection]。后续核验：在目标反向代理和多访问者条件下，哪个组件负责身份和会话隔离？

<a id="cap-dep-02"></a>

### CAP-DEP-02 · 企业 Agent 发布与治理生命周期

主归属：[12 平台能力](#dimension-12)。支持状态：**待确认**；证据：**仅文档**；实现归属：外部平台（实现待确认）。

条件为组织内注册、评估、审批、部署与下线。本地插件管理不能直接证明已有企业平台治理；外置功能未覆盖不构成 harness 产品失败。

依据：[产品说明][readme]、[插件管理说明][plugin-manager]、[安全声明][safety]。后续核验：官方是否提供此类产品范围，还是应由接入平台负责？

[architecture]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/architecture.zh.md
[auto-review]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/auto-review/README.zh.md
[base]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/base/cordis.patch.yml
[claude-hooks]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/hooks-claude-code/README.zh.md
[compaction]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/compaction/compaction-basic/README.zh.md
[connection]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/client/connection/README.zh.md
[credentials]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/credentials/credentials-local/README.zh.md
[cwd]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/tool-working-directory/src/index.ts
[file-api]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/api/session-controller/src/media-references.ts
[format]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/session-format-status.zh.md
[goal]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/goal/goal-round-driver/README.zh.md
[hooks]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/hooks-codex/README.zh.md
[identity]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/identity/anonymous-user-id/README.zh.md
[lifecycle]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/agent-lifecycle.zh.md
[llm]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/llm/llm-deepseek/src/config.ts
[loop]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/README.zh.md
[loop-source]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/src/agent.ts
[mcp]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/mcp/mcp-client/README.zh.md
[memory]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/user/guide/mcp-memory.zh.md
[otel]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/session-telemetry-otel/README.zh.md
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
[session-log]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/session-log-deepseek/README.zh.md
[session-search]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/session-search/README.zh.md
[skills]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/skill/skill-filesystem/README.zh.md
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
