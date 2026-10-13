# 插件能为用户增加哪些能力

**先确定工作缺少什么，再选择扩展。** 常用 Web 工作台本身已有文件与终端工具、计划、长目标、压缩、子代理、文件卡片和提醒；不需要把可选插件全部开启才形成可用的任务流程。可选能力更适合按需补齐：找回旧工作、保持终端任务、组织多个助手，或改善输入与阅读体验。[默认会话配置][standard]

下文说明用户能增加什么能力，以及开启后需要接受的条件。插件在[14维评测框架](CAPABILITY-MAP.md)中作为能力实现依据；逐项支持状态与待验证问题只在[文末能力证据索引](CAPABILITY-MAP.md#evidence-index)维护。默认配置、版本比较和发行包证据仍由本页承载，避免重复登记。本文沿用 **v0.2.1-alpha.2／d743267388641bc76f17c45ce8b4c231aed1d32c**，证据核查日期 **2026-10-13**；仅静态阅读，未启用插件、安装运行环境或调用模型。

## 想让助手找回之前做过的工作

**用户要继续一个旧问题时，助手能自己寻找上下文吗？** 可选会话搜索让 Agent 检索当前工作区的历史会话，适合查找早先讨论过的材料和决定。它需要先启用；用户在侧栏搜索会话与 Agent 获得检索工具是两种体验。

如果希望在多个任务中长期保存事实，还需要连接外部记忆服务。官方给出的记忆配置是默认关闭的示例，服务安装、身份、数据保留、冲突处理和删除由提供方及接入产品负责。搜索到历史记录不代表它已经形成可信、永久有效的业务知识，仍需查看出处和适用时间。

会话搜索启用后给多个会话模式增加全局只读工具，连精简模式也会变化；外部记忆则引入独立服务和数据生命周期。选型时应先回答“希望回忆哪些工作、谁可见、何时失效”，再决定是否需要两者。依据：[会话搜索][search]、[外部记忆指南][memory]；后续问题见[工作空间与历史材料](CAPABILITY-MAP.md#dimension-05)。

## 想保持一个终端任务，或让多个助手分工

**长时间运行的工具工作和并行分工，需要哪些额外能力？** 可选持久终端给 Agent 提供可持续使用的终端工具；它与 Web 里已有的用户终端入口需要分开看。启用后会向各会话模式提供全局工具，所以不能把变更理解为只影响当前一个任务。具体工作能否安全取消、恢复，仍要按工具和进程确认。[持久终端说明][terminal]

Team 可用于研究任务板、依赖和助手间消息，让一个主助手组织多个成员。它是默认关闭的实验能力；消息被接纳不代表任务完成，成员退出和冲突任务仍需要明确负责人。对业务使用，应该先确定拆分方式、合并者和验收者，再引入分工。[Team 说明][team]、[协作边界](CAPABILITY-MAP.md#dimension-12)

如果已有 Codex 或 Claude Code 使用环境，可研究把它们作为外部子代理。官方桥接包需要按需安装，相应外部运行时与认证不会因安装 dsh 自动具备。它们的模型覆盖、工具过滤和持续会话能力也不能按内置子代理一概承诺。[按需目录][on-demand]

## 想更方便地输入、阅读和整理会话

**扩展能减少哪些日常操作，又会新增什么代价？** 随附可选项中包括语音输入、思考内容翻译和全提示词标题。它们可供需要这些体验的使用者选择，均未被当前默认模板选中；本项目未运行语音输入，也未验证其识别效果或服务条件。[可选目录][profile]

翻译开启后，展开的思考内容可能发送给翻译服务。默认使用 Bing，也可选择 Google 或需显式配置的 DeepSeek；不能默认认为翻译发生在本机，或某服务不可用时一定自动回退。用户是否愿意把这些内容发到所选服务，应当是开启前可理解的选择。[翻译说明][translation]

默认标题依据首条提示词生成；可选的全提示词标题会替换它，改变标题生成所依据的内容。当前首提示词标题的输出上限已从64改为4096，但上限不等于每次实际用量，普通 SDK 程序入口也关闭了该标题插件。它提醒产品方把辅助体验的调用与主任务成本一起考虑。[标题替换][title]、[基础配置][base]、[普通 SDK 配置][sdk]

<a id="review"></a>

## 想减少人工审批，或沿用已有工作规则

**哪些重复判断可以辅助，哪些决定仍需要明确负责人？** 实验性 Auto review 会用当前模型审查工具权限请求，可能在评审后以更宽权限执行。它默认关闭、会增加模型调用，也可能误判；评审内容并非全部持久化，且不覆盖所有直接程序效果。适合研究审批体验，现有证据不足以让它承担企业强制策略和完整审计。[Auto review 说明][auto-review]

已有 Codex 或 Claude 命令规则时，可以显式配置命令挂钩桥接，在相应执行环节调用外部命令。但只支持已声明的子集，配置失败可能警告后继续。若业务规定某类动作必须被阻止，就要先确认失败时是否继续、谁能修改规则、如何留下批准记录。桥接能力存在，并不表示这些组织约束已交付。[Codex 规则桥接][hooks]、[Claude 规则桥接][claude-hooks]

## 想接入自己的业务工具和模型

**增加一个连接组件后，就能访问业务系统了吗？** dsh 随附外部工具与模型的接入能力，但仍需配置具体服务、凭据和端点。MCP 负责连接外部工具和资源；其他模型由相应适配器配置路由。两者都可能处于“组件已加载、目标服务尚未接通”的状态。[MCP 说明][mcp]、[其他模型配置][pi-ai]

这类扩展更接近一项集成工作。产品方需要说明用户能访问什么、哪些调用会修改外部数据、连接失败后如何恢复，以及选择模型后哪些功能仍可使用。本轮没有验证任何第三方服务可用性；详细边界见[资源使用](CAPABILITY-MAP.md#dimension-12)。

## 决定开启之前，先看影响范围

插件可以由设置中的插件管理器选择，但供给方式不同：有些随安装提供而默认关闭，有些需另行安装，有些还需外部服务和认证。一次配置变化也可能影响多个会话，而不只改变当前对话。具体开关、安装步骤和可用工具应以实际版本为准；本项目只核对了配置与发行内容。

除了是否多一个按钮，还应看三个实际变化：助手能接触哪些资源；是否增加外部服务或调用费用；是否改变人工确认与日志外发。文件成果的带走和保留方式也不能由“装有文件插件”推断，见[成果交付](CAPABILITY-MAP.md#dimension-05)。

<a id="data-channels"></a>

### 数据发送要按功能分别判断

当前会话日志、显式反馈、包清单及 Desktop 产品交互采集是不同通道。Desktop 默认装配产品交互采集，普通 Web 不装配；官方规定的交互事件字段不含提示词、回复或凭据，关闭新采集不会清空已排队导出。它不能与会话全文或反馈开关混称。依据：[交互采集][product-analytics]、[导出队列][product-exporter]；会话日志的独立默认行为见 [F-01](FINDINGS.md#f-01--默认-session-log-外发需要独立治理)。

## 配置与版本证据

以下供维护者复核，不是使用者需要逐项完成的安装清单。所有“默认”均指新配置且无用户覆盖；随包存在、被加载、已经接通服务是不同事实。

<a id="当前默认组成与重要例外"></a>

### 当前组成：入口差异、随附关闭清单与按需安装

**常用 Web。** standard 是默认会话模式，提供文件／Shell、Skills、计划、长期目标、压缩、子代理、工作流、文件卡片和提醒。程序化工具调用模式（PTC）改变工具呈现，并关闭该模式的 workflow；创造模式开放插件管理工具。minimal 主要提供持久 Shell，但宿主与全局扩展仍可增加工具。依据：[standard][standard]、[PTC][ptc]、[创造模式][creator]、[minimal][minimal]。

**程序入口。** Headless 和普通 SDK 基于基础组合再叠加自己的配置；普通 SDK 关闭标题模型和热重载。SDK Minimal 使用独立组合，默认文件策略为 `danger-full-access`，不能套用基础组合的 `workspace-write + ask`；同时挂载 Session Log、包清单扩展和目录工具。该精简入口的 tag 与抽查 npm 配置一致。依据：[入口组合][profile]、[普通 SDK][sdk]、[SDK Minimal][sdk-minimal]、[对应发行元数据](https://registry.npmjs.org/@deepseek-ai/dsh-sdk-minimal/0.2.1-alpha.2)。权限名称不代表隔离实测。

**11个随附关闭组合。** 当前清单为会话搜索、Ralph、持久终端、Badge Skill、全提示词标题、Team、语音输入、思考翻译、Auto review、Inspector、Worktree。源码将其列为随安装提供、未被默认模板选择、插件管理器中默认关闭；是否实验性另行判断。目录出现不等于本项目完整核验了每项用户体验。会话搜索提供5个全局只读工具，持久终端提供6个全局工具，启用后包括 minimal 在内的会话模式均会受到影响。依据：[随附列表][profile]、[CLI manifest][manifest]、[搜索][search]、[终端][terminal]。

**按需安装与第三方。** Codex、Claude Code 是官方按需子代理包，其 provider runtime 不随主分发安装；命令挂钩还需显式加载和配置路径。MCP memory 示例指向外部服务器，默认关闭，不能作为 dsh 默认长期记忆或官方背书。依据：[按需目录][on-demand]、[规则桥接][hooks]、[外部记忆][memory]。

**文件交付的独立边界。** 从首次公开文件卡片版本 v0.1.5-alpha.2 起，卡片引用源文件的语义就已存在。当前卡片支持预览及运行端打开／定位，无内置访问者下载入口，也不保留源文件副本；日志 ZIP 不携带卡片源文件字节。鉴权文件读取接口另有文件权限和响应大小约束。依据：[早期卡片说明][present-first]、[当前设计决策][present-decision]、[未运行的上游测试][present-test]、[日志导出][zip]、[文件读取][file-api]、[鉴权][connection]。产品判断见[05工作空间](CAPABILITY-MAP.md#dimension-05)，逐项状态只在[能力证据索引](CAPABILITY-MAP.md#evidence-index)维护。

**如何得出默认值。** 复核顺序为 profile → 有序 bundle → 配置补丁 → 会话 preset／条件／用户覆盖 → 插件 schema 与实现。Web 会先关闭部分基础工具，再按会话模式加载；补丁对目标行的 `config` 整体替换，不能假定深层合并。随包包括由生产依赖带来的组件，并非所有内容都位于 CLI 的归档中。依据：[profile][profile]、[基础配置][base]、[Web manifest][web-manifest]、[Web 配置][web]。

### 历史变化：六个版本怎样改变用户可见能力与集成条件

以下使用对应专题的上一已发布版本作为比较基准；最早的 rc.7 只建立当时基线。没有变化的插件名称也可能包含重要实现变更。

- **[v0.1.0-rc.7](releases/v0.1.0-rc.7.md)：** 已有基础与 Web 分层；基础层加载 Ralph，Web 再禁用；遥测组件虽然加载，模式默认关闭。仅数包或配置行无法判断最终能力。[基础配置][rc7-base]、[Web 配置][rc7-web]
- **[v0.1.3-alpha.1](releases/v0.1.3-alpha.1.md)：** 相对 v0.1.2-rc.1，基础插件行集合不变，Web 增加文件上传；会话句柄、异步创建和结算仍有破坏变更。该版抽样发行包不可取得，见下方证据。[Web 配置][a13-web]
- **[v0.1.6-alpha.1](releases/v0.1.6-alpha.1.md)：** 新增外部资源、图片卸载、Node 程序化工具与相应工作流，移除旧工作流 worker-thread；Ralph 默认关闭，Web 增终端入口。工具名称、异步初始化事件及 Session Log 默认值变化，会影响工作过程和数据外发；技术迁移为 PTC 重命名、`agent/session-start` → 异步 `agent/created`。[基础配置][a16-base]、[Web 配置][a16-web]
- **[v0.2.0-rc.2](releases/v0.2.0-rc.2.md)：** 相对 rc.1，基础和 Web 配置行无实质差异，但模型依赖 pi-ai 从 `^0.85.1` 到 `^0.87.1`，可能影响保存的模型选择；随附可选组合为 Team、语音、Auto review、Schedule 四项。[清单][rc20-profile]、[旧依赖][pi-before]、[新依赖][pi-after]
- **[v0.2.1-alpha.1](releases/v0.2.1-alpha.1.md)：** 提醒进入 Web 默认组合，旧可选 Schedule 自动清理，Inspector 进入可选清单；子路径元数据、活动／用量注册及 invariant 导出有破坏迁移。此版已按顺序加载独立会话配置，不能据此认定配置拆分始于本版。[Web 配置][a21-web]、[清单][a21-profile]
- **[v0.2.1-alpha.2](releases/v0.2.1-alpha.2.md)：** 随附关闭组合从4项增到11项，基础组合增加目录服务及工具、移走 Badge／Ralph 行；子代理移除 `backgroundMode` 配置。首提示词标题输出上限64 → 4096，主循环、工具呈现和 Team 也有实现变化。可选组合增多不能直接解释成默认权限扩大。[上版基础配置][a21-base]、[当前配置][base]、[普通 SDK][sdk]

更早的会话存储、协议与生命周期变化见 [EVOLUTION](EVOLUTION.md)。

## 发行包核验与版本纪律

当前有两处证据限制影响版本判断：alpha.2 的源码与 npm 发行包存在计划提示词文字差异；v0.1.3-alpha.1 的四个精确包样本不可取得。它们要求我们注明依据来自哪里，尚不能据此认定权限漏洞或撤包原因。

### 抽样范围、元数据、文字差异与校验摘要

对上述6个版本各查 `@deepseek-ai/dsh`、`dsh-base`、`dsh-web-app`、`dsh-app-boot`，另核当前 `dsh-sdk-minimal`。成功静态下载 **21个 tgz**，逐一匹配 registry 的 SHA-512 integrity；比对归档中 **52份 YAML**（含说明元数据），48份与对应 tag 字节一致，4份有下述提示词差异。没有安装依赖、执行生命周期脚本或验证整个依赖闭包、Desktop 二进制与 Python wheel。

- **v0.1.0-rc.7：** 四个主样本包结果：均可取；所查 YAML 一致；dsh 内部直接依赖写法：`^0.1.0-rc.7` 范围
- **v0.1.3-alpha.1：** 四个主样本包结果：四个精确版本端点均404；包总元数据的 versions 也无此项；dsh 内部直接依赖写法：仅保留 tag 源码结论，未完成发行包验证
- **v0.1.6-alpha.1：** 四个主样本包结果：均可取；所查 YAML 一致；dsh 内部直接依赖写法：`^0.1.6-alpha.1` 范围
- **v0.2.0-rc.2：** 四个主样本包结果：均可取；所查 YAML 一致；dsh 内部直接依赖写法：精确 `0.2.0-rc.2`
- **v0.2.1-alpha.1：** 四个主样本包结果：均可取；所查 YAML 一致；dsh 内部直接依赖写法：精确 `0.2.1-alpha.1`
- **v0.2.1-alpha.2：** 四个主样本包结果：均可取；base 一处、Web 三个 preset 同一文字差异；dsh 内部直接依赖写法：精确 `0.2.1-alpha.2`

可追溯入口如下，每格为本轮实际查询的精确版本元数据：

- **0.1.0-rc.7：** [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.1.0-rc.7)；[Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.1.0-rc.7)；[Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.1.0-rc.7)；[Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.1.0-rc.7)
- **0.1.3-alpha.1：** [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.1.3-alpha.1)；[Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.1.3-alpha.1)；[Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.1.3-alpha.1)；[Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.1.3-alpha.1)
- **0.1.6-alpha.1：** [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.1.6-alpha.1)；[Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.1.6-alpha.1)；[Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.1.6-alpha.1)；[Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.1.6-alpha.1)
- **0.2.0-rc.2：** [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.2.0-rc.2)；[Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.2.0-rc.2)；[Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.2.0-rc.2)；[Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.2.0-rc.2)
- **0.2.1-alpha.1：** [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.2.1-alpha.1)；[Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.2.1-alpha.1)；[Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.2.1-alpha.1)；[Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.2.1-alpha.1)
- **0.2.1-alpha.2：** [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.2.1-alpha.2)；[Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.2.1-alpha.2)；[Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.2.1-alpha.2)；[Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.2.1-alpha.2)

**源码与包的差异：**alpha.2 tag 的 Plan 首句要求用户通过 `exit_plan_mode` 批准或切换模式；npm 归档改为 `exit_plan_mode` 成功或用户切换模式。差异位于 base 的 Plan section，以及 Web standard／ptc／cordis 的同一 section，其他所查 YAML 一致。这是可复核的发行内容差异；没有运行证据证明权限绕过，也未确认构建来源或差异原因。对模型实际提示词的判断应同时注明来源。[tag base][base]、[tag standard][standard]

- **[dsh-base tgz](https://registry.npmjs.org/@deepseek-ai/dsh-base/-/dsh-base-0.2.1-alpha.2.tgz)：** 本轮验证通过的 integrity：`sha512-/sJRnKbpjKIzgxtU+qpl65njlTMp0Y8s62AhZQnQmXTJMRurcy1PUWNyB1lWHJqLhnQT9JO+xg/jF1C0E3ypiw==`
- **[dsh-web-app tgz](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/-/dsh-web-app-0.2.1-alpha.2.tgz)：** 本轮验证通过的 integrity：`sha512-KJFOxsb9eaNW2DNzLwLbUMKonAHUGVpQlLggr5nLNDeUo4TEjyBM+fzIu2qTw78QzpM+cYNAXyNPtYvqutt83w==`

**版本记录：**样本包的 package version 与主版本相同，不据此编造独立插件发版史；组件代码以主 tag／commit 固定，包版本只按实际 manifest 记录。早期依赖范围说明仅固定 CLI 版本不足以确定安装后的全部代码；本项目未运行解析，未断言实际安装会选哪个版本。404也不能证明历史上从未发布、被撤回或撤回原因。

本轮仍未确认缺失历史包的原因、当前文字差异的构建来源、全部平台发行物的一致性、实际加载结果及第三方服务可用性。后续优先补公开资料和静态证据；本次产品化改写不改变任何支持状态，也不新增运行结论。

[profile]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/boot/app-boot/src/profile.ts
[base]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/base/cordis.patch.yml
[web]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/web-app/cordis.patch.yml
[manifest]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/apps/cli/package.json
[web-manifest]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/web-app/package.json
[standard]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/web-app/presets/standard.patch.yml
[ptc]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/web-app/presets/ptc.patch.yml
[minimal]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/web-app/presets/minimal.patch.yml
[creator]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/web-app/presets/cordis.patch.yml
[sdk-minimal]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/sdk-minimal/cordis.patch.yml
[sdk]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/sdk-app/cordis.patch.yml
[on-demand]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/boot/app-boot/src/official-bundle-packages.ts
[pi-ai]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/llm/llm-pi-ai/README.zh.md
[hooks]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/hooks-codex/README.zh.md
[claude-hooks]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/hooks-claude-code/README.zh.md
[search]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/session-search/README.zh.md
[terminal]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/terminal-bundle/README.zh.md
[title]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/session-titles-bundle/cordis.patch.yml
[translation]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/cot-translation-bundle/README.zh.md
[product-analytics]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/client/product-analytics/README.zh.md
[product-exporter]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/host/product-telemetry-otel/README.zh.md
[present]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/deliverables/tool-present/README.zh.md
[present-decision]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/.agents/notes/implemented/feature/2026-09-08-present-workspace-source-files.zh.md
[present-test]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/apps/web/tests/present.e2e.ts
[zip]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session-query/session-log-export/src/index.ts
[file-api]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/api/session-controller/src/media-references.ts
[connection]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/client/connection/README.zh.md
[cwd]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/tool-working-directory/src/index.ts
[memory]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/user/guide/mcp-memory.zh.md
[mcp]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/mcp/mcp-client/README.zh.md
[rc7-base]: https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/packages/bundle/base/cordis.patch.yml
[rc7-web]: https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/packages/bundle/web-app/cordis.patch.yml
[rc7-profile]: https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/packages/boot/app-boot/src/profile.ts
[a13-base]: https://github.com/deepseek-ai/deepseek-harness/blob/d347e703908d0406b7a7ef80e3a0e594d86b2215/packages/bundle/base/cordis.patch.yml
[a13-web]: https://github.com/deepseek-ai/deepseek-harness/blob/d347e703908d0406b7a7ef80e3a0e594d86b2215/packages/bundle/web-app/cordis.patch.yml
[a13-profile]: https://github.com/deepseek-ai/deepseek-harness/blob/d347e703908d0406b7a7ef80e3a0e594d86b2215/packages/boot/app-boot/src/profile.ts
[a16-base]: https://github.com/deepseek-ai/deepseek-harness/blob/0a15e36e7f82b6ed45af6fa9759f29b40dcd965d/packages/bundle/base/cordis.patch.yml
[a16-web]: https://github.com/deepseek-ai/deepseek-harness/blob/0a15e36e7f82b6ed45af6fa9759f29b40dcd965d/packages/bundle/web-app/cordis.patch.yml
[a16-profile]: https://github.com/deepseek-ai/deepseek-harness/blob/0a15e36e7f82b6ed45af6fa9759f29b40dcd965d/packages/boot/app-boot/src/profile.ts
[rc20-base]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/bundle/base/cordis.patch.yml
[rc20-web]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/bundle/web-app/cordis.patch.yml
[rc20-profile]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/boot/app-boot/src/profile.ts
[a21-base]: https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/bundle/base/cordis.patch.yml
[a21-web]: https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/bundle/web-app/cordis.patch.yml
[a21-profile]: https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/boot/app-boot/src/profile.ts
[present-first]: https://github.com/deepseek-ai/deepseek-harness/blob/b2e3b2a0125854567a4a5fcba75782e42fe84901/packages/fs/tool-present/README.zh.md
[pi-before]: https://github.com/deepseek-ai/deepseek-harness/blob/4878cdabd87d4041bdaff61d04c966883b9fd07a/packages/llm/llm-pi-ai/package.json
[pi-after]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/llm/llm-pi-ai/package.json

[auto-review]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/auto-review/README.zh.md
[team]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/agent-team/README.zh.md
