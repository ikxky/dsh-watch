# 关键发现与机会

当前范围：v0.2.1-alpha.2／`d743267388641bc76f17c45ce8b4c231aed1d32c`，2026-10-12 登记并补充历史证据。以下是公开资料与静态源码分析，不是已复现漏洞清单。没有本项目运行测试。背景能力见 [OVERVIEW](OVERVIEW.md)，版本变化见 [release 分析](releases/v0.2.1-alpha.2.md)，纵向证据见 [EVOLUTION](EVOLUTION.md)。历史已修复事项不作为当前缺陷登记。

## F-01 · 默认 Session Log 外发需要独立治理

**P1 · 验证 · 已确认默认配置与实现；尚无运行证据。**

官方说明 `session-log-deepseek` 可在 DeepSeek 请求中增量附带规范会话日志。源码确认基础 bundle 默认挂载它，schema 的 `enabled` 默认为 true，按接受水位选取连续事件后缀。它与 OTel 的反馈触发上报是两个独立通道；关闭后再开启会继续补传未确认后缀，包括关闭期间记录的内容。插件包名称与版本还有独立的默认元数据字段。

**历史补充：**逐个核对已发布 tag 后确认，Session Log 在 v0.1.2-alpha.1 引入时默认关闭，至 v0.1.5-rc.2 仍为 false；v0.1.6-alpha.1 起改为 true。升级时依赖默认值的集成尤其需要复查，而非假定关闭状态自然延续。[相邻版本源码及分析](releases/v0.1.6-alpha.1.md)

**插件补查（2026-10-13）：**Desktop 另有默认启用的产品交互埋点，普通 Web 不装配；它与会话反馈的采集政策独立，关闭新采集不会清空已排队导出。官方规定的事件字段不含提示词、回复或凭据，不能将它笼统描述为会话全文上传。[分类与来源](PLUGINS.md#data-channels)

**影响推断：**“本地产品”或“关闭遥测”不足以描述实际数据出站范围；企业应逐条确认模型请求、Session Log、OTel、插件元数据及新增翻译服务。这里没有证据可判断服务端保留期、二次使用或删除效果，也没有把该行为认定为未披露漏洞。

**下一次值得改变结论的证据：**固定版本下关闭各通道后的网络记录，含普通请求、摘要、标题、恢复及重新开启；自定义 DeepSeek baseURL 的字段行为也要核验，不能仅凭“官方 API”文案假定更换地址会关闭扩展。通用平台可借鉴“按通道列出 payload、目的、开关、补传和保留策略”的数据清单。

来源：[说明](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/session-log-deepseek/README.zh.md)、[默认 schema 与 prepare](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/session-log-deepseek/src/index.ts#L38)、[基础挂载](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/bundle/base/cordis.patch.yml#L43)、[适配器接线](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/llm/llm-deepseek/src/host.ts)、[OTel](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/session/session-telemetry-otel/README.zh.md)、[插件清单](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/llm/plugin-package-inventory-deepseek/README.zh.md)。

## F-02 · 根代理 idle 与完整任务完成必须分开

**P1 · 借鉴／验证 · 已确认代码语义；不是新缺陷指控。**

本版统一子代理 activation，工具可先返回 child ID；SDK 新增 `session/wait`，等待根 Agent、受管理后代及后代触发的根摘要工作。源码中的 wait 循环会在等待后代后复核根状态与日志序列。另一方面，`HarnessSession.run()` 仍以根首次 idle 结束活动区间；返回的最后助手文本不保证只由该 prompt 因果产生。

**历史补充：**暂停、恢复和队列边界在 v0.1.3、v0.1.5、v0.2.1-alpha.1 均有不同修复；0.2 还强调未知工具副作用的恢复处理。这支持持续观察生命周期边界，不足以证明同一缺陷反复回归。[演进证据](EVOLUTION.md)、[0.2 分析](releases/v0.2.0-rc.2.md)

**影响推断：**把 run 返回直接映射成“整个业务任务完成”，可能漏掉后代活动或混淆结果归属。此处是接口选择和业务建模风险；本轮未复现提前完成错误。带外部副作用的系统还应保留“结果未知”，不能仅靠重发 prompt 恢复。

**下一步验证条件：**用可控的慢子任务检查接收、根 idle、子树完成及最终汇总的顺序；并覆盖取消、冷恢复、运行时退出和结果未知。仅在未来单独授权运行时进行。可立即借鉴的是区分活动状态、持久终态与业务成功的设计。

来源：[SDK 契约](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/sdk/client/README.zh.md)、[run 源码](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/sdk/client/src/api.ts#L187)、[wait 源码](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/sdk/server/src/server.ts#L214)、[嵌套任务完成修复 commit](https://github.com/deepseek-ai/deepseek-harness/commit/50da6f0b168d3bb1fe85ed3f8f20fd2a918a7d26)、[未知工具结果处理](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/README.zh.md)。

## F-03 · Team 简化了消息链路，也改变了交付承诺

**P1 · 观察／验证 · alpha.1→alpha.2 兼容性变化已由 diff 确认。**

本版移除 Team 独立 mailbox/outbox，改为直接调用目标 inbox／steer；发送成功只表示消息已接收，不表示模型已处理，也不额外等待同步持久化。原自动重试和显式重发去重不再提供；`maxPendingMessagesPerMember`、发送结果中的旧字段等需迁移。历史消息记录仍可读取，但不再按旧机制重新投递。

**影响推断：**依赖旧 outbox 达成业务保证的消费者需重新指定重试、幂等和交付回执的所有者。不能把 Team 的任务 CAS、持久 roster 和消息处理统称为 exactly-once 工作流。共享任务板的路径重叠提示也不是文件锁。

**观察触发条件：**后续正式交付契约、迁移说明、失败重试策略或跨进程协调变化。企业平台可借鉴 CAS 与发送者归属，但当前不采用 Team 作为可靠消息总线。

来源：[当前 Team 契约](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/agent-team/README.zh.md)、[sendAdmitted 源码](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/agent-team/src/index.ts#L224)、[直接投递 commit](https://github.com/deepseek-ai/deepseek-harness/commit/c772c85c173d6727504195f7a3d8546a23de259f)、[历史 mailbox 处理变更](https://github.com/deepseek-ai/deepseek-harness/commit/a5098110cff77f81a700cc65918dd405e073b939)。

## F-04 · 现有审批和文件沙箱不构成企业隔离

**P1 · 跳过当前生产采用；借鉴权限拆分 · 官方限制明确。**

官方安全文件明确未审计、非生产就绪。本地沙箱可能报告 partial；文件写入策略不能覆盖所有读取、网络、宿主插件或同用户凭据访问。计划模式是文本约束；实验性 Auto review 获准后以 Full access 执行，不覆盖所有 PTC 直接效果，也不保存完整评审输入与输出。Python PTC 本版接入 Session 文件策略是进步，但仍是实验组件，且没有随附 profile 默认启用。

**历史补充：**官方曾报告 v0.1.1-rc.1 修复 Linux bwrap 路径绕过、v0.1.7-alpha.1 修复 Windows 授权目录外删除；这些是历史修复记录，不是本项目复现或当前未修漏洞。v0.1.6 的 Python PTC 当时仍明确没有文件沙箱，说明执行后端的版本边界不可混用。[历史来源与限定](EVOLUTION.md)、[当时 PTC 契约](releases/v0.1.6-alpha.1.md)

**入口条件：**当前 `sdk-minimal` 不叠加 base，其文件策略默认 Full access；不能把 base 的 `workspace-write + ask` 推广到所有 SDK 入口。[固定配置与发行核验](PLUGINS.md#当前默认组成与重要例外)

**影响推断：**企业需要外部的执行环境隔离、凭据代理、网络策略和业务授权。模型评审适合辅助判断，不能单独替代确定性权限检查。这里记录的是产品自己声明的适用边界，没有证明可利用的绕过路径。

**改变结论所需证据：**具体目标平台的隔离测试、独立审计、明确的租户及身份契约、审计留存要求和失败闭合策略。本轮不开展此类测试。

来源：[SAFETY](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/SAFETY.zh.md)、[沙箱](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/sandbox/sandbox-local/README.zh.md)、[凭据限制](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/credentials/credentials-local/README.zh.md)、[Auto review](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/auto-review/README.zh.md)、[Python PTC](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/experimental/ptc-runtime-python/README.zh.md)。

## F-05 · 压缩、外部记忆和资源预算应分别设计

**P2 · 借鉴／验证 · 官方能力与限制已确认。**

压缩替换旧上下文而保留日志，摘要会消耗额外模型调用；不可分大工具结果、系统提示词和工具目录有独立上限。外部记忆是默认关闭的 MCP 示例，数据生命周期由其提供方负责。Goal round 上限不是 token、费用或时间上限，循环也没有内置通用轮次预算。

**机会推断：**企业知识系统可保留“可回放工作状态”与“带权限和出处的长期事实”两层；预算控制应覆盖主循环、摘要、子代理、重试及评审，不能只统计最终答案或根会话输出。

**下一步验证条件：**选择已固定模型和非敏感任务，测摘要前后事实保真、检索权限、删除后召回、子树费用归集以及预算耗尽终态。当前没有准确率、费用或性能优越性结论。

来源：[Compaction](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/compaction/compaction-basic/README.zh.md)、[Memory MCP](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/user/guide/mcp-memory.zh.md)、[Goal 限制](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/goal/goal-round-driver/README.zh.md)、[Agent loop 限制](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/packages/core/agent-loop/README.zh.md)。

## Upstream 跟踪状态

以上均有可回溯的官方源码／文档／commit 引用。目前没有登记可访问的 issue 或 PR 页面；官方仓库关闭 Issues，合并日志内的 PR 编号不能假定可通过官方仓库 URL 访问。后续仅在核实可访问及内容相关后增加 issue/PR 条目，不用编号凑成缺陷证据。没有向上游发送报告、评论或变更。

## F-06 · 固定主版本仍需核对插件发行内容

**P1 · 验证／观察 · 静态差异已确认；无运行故障结论。**

2026-10-13 的归档抽查发现，alpha.2 的 base 与三个 Web preset 的 Plan 提示词首句与 tag 不同；registry integrity 核验通过。早期样本内部依赖使用版本范围，近期样本为精确版本。另有 v0.1.3-alpha.1 的四个 npm 包样本当前不可得，原因未知。

**影响推断：**只固定 CLI 名称和版本不足以替代插件配置、依赖及发行物证据；不能把文字差异直接认定为权限漏洞，或把404认定为某种撤包原因。下一步先查发布构建来源、精确依赖与归档元数据，保持静态研究。[完整样本、源码、tarball 与 integrity](PLUGINS.md#发行包核验与版本纪律)、[能力跟踪 CAP-EXT-01](CAPABILITY-MAP.md#cap-ext-01)
