# DeepSeek Harness 发布演进

截至 **2026-10-26**，官方 Releases 集合 API 第1页返回32条、第2页为空；32条均为 `draft=false`、`prerelease=true`。因此本文使用“官方已发布版本”，不把 RC 或 0.2 当作稳定版。当前可见最早发布为 **v0.1.0-rc.7（2026-08-17 UTC）**，最新为 **v0.2.1-rc.3（2026-10-23 UTC）**。没有从 git tag 名称或 release compare 的起点推断更早公开发行。[完整 API](https://api.github.com/repos/deepseek-ai/deepseek-harness/releases?per_page=100&page=1)、[下一页](https://api.github.com/repos/deepseek-ai/deepseek-harness/releases?per_page=100&page=2)

研究为官方 release、历史 tag 对应源码及文档的静态分析，没有安装、运行、模型调用或安全实测。**官方说明**不等于复现，**源码核实**只确认实现与配置，企业影响均为**推断**；缺少证据的能力保留为**未知**。当前使用姿态仍以借鉴、验证、观察为主。[当前基线](OVERVIEW.md)、[关键发现](FINDINGS.md)、[检查规则](TRACKING.md)

## 核心判断

演进主线是把已成形的插件化 Agent 内核逐步做成更完整的本地产品，并持续重整持久化、执行和扩展边界。早期就有事件日志、工具并行、压缩、规划与子代理，不宜描述成“后来才从聊天升级为 Agent”。与此同时，默认出站行为、持久格式和插件 API 在 alpha／RC 中频繁变化；功能扩展速度不能替代稳定性、安全性或企业治理的证据。[早期基线](releases/v0.1.0-rc.7.md)、[执行边界节点](releases/v0.1.6-alpha.1.md)、[最近节点](releases/v0.2.1-alpha.1.md)

五个历史专题选取最早可见基线、持久化重构、执行环境扩张、0.2 版本分界和最新版本的直接前身。未单列的 v0.1.2／v0.1.5／v0.1.7 仍在下文覆盖关键变化；这不是逐版本完整源码审计。

2026-10-13 增补：[PLUGINS](PLUGINS.md) 按相同六个专题版本补查 manifest、默认加载配置和 npm 归档。插件演进同时记录供给方式、默认启用、工具／命令／hooks、实现与依赖变化；[CAPABILITY-MAP](CAPABILITY-MAP.md) 保存当前逐项状态，避免另建历史评分表。

## 完整发布索引

日期为 UTC。“专题”有独立文档；“定向”补充核实关键历史源码或比较范围；“索引”读发布说明并核 tag／commit，不声称完整六维评估。所有 tag 均已剥离 annotated tag 后核到 commit，表中仅显示其前12位便于阅读。每一行的发布版本链接指向官方 release；重点一栏是研究归纳。

| 发布版本 | 日期 | Commit 前缀 | 覆盖 | 重点 |
|---|---|---|---|---|
| [v0.1.0-rc.7][v0.1.0-rc.7] | 2026-08-17 | `99f6f02fecdb` | [专题](releases/v0.1.0-rc.7.md) | 当前可见最早发布；插件内核、日志、压缩、外部子代理已存在 |
| [v0.1.0-rc.8][v0.1.0-rc.8] | 2026-08-19 | `141eb6fef834` | 索引 | 图片输入、外部子代理组合；SQLite 格式不兼容变化 |
| [v0.1.1-rc.1][v0.1.1-rc.1] | 2026-08-21 | `528c682e0616` | 定向 | 官方报告修复 Linux bwrap 的 /proc 路径绕过 |
| [v0.1.1-rc.2][v0.1.1-rc.2] | 2026-08-21 | `b150a551b8d4` | 索引 | DeepSeek 图片上传复用相关改进 |
| [v0.1.2-alpha.1][v0.1.2-alpha.1] | 2026-08-27 | `cd5ef8148158` | 索引 | 入口统一到 profiles；网络 Web 启动认证、默认 WebFetch；Session Log 可选 |
| [v0.1.2-alpha.2][v0.1.2-alpha.2] | 2026-08-30 | `0a53fb55bea1` | 索引 | 恢复 SessionEvent.ignorable API |
| [v0.1.2-alpha.3][v0.1.2-alpha.3] | 2026-08-31 | `dd6322d604e0` | 索引 | 移除 SQLite 持久化后端，历史数据需旧版导出 |
| [v0.1.2-alpha.4][v0.1.2-alpha.4] | 2026-09-01 | `4e84901e6471` | 索引 | send_message 双向通信；Session 事件读取 API 变更 |
| [v0.1.2-alpha.5][v0.1.2-alpha.5] | 2026-09-02 | `db6bdc3576c2` | 索引 | 启动、历史标题等修复 |
| [v0.1.2-rc.1][v0.1.2-rc.1] | 2026-09-03 | `a66e47020478` | 定向 | 阶段汇总；正文覆盖前述 alpha，不能当成全为 rc.1 首创 |
| [v0.1.3-alpha.1][v0.1.3-alpha.1] | 2026-09-04 | `d347e703908d` | [专题](releases/v0.1.3-alpha.1.md) | Session v2、handle、单写锁、异步创建；已知历史加载回退 |
| [v0.1.3-alpha.2][v0.1.3-alpha.2] | 2026-09-07 | `82a5fd61a7cf` | 索引 | 长历史性能／进程清理改进；反馈触发 OTel 会话上报 |
| [v0.1.5-alpha.1][v0.1.5-alpha.1] | 2026-09-08 | `5dda764ed3aa` | 定向 | Session v3；系统提示词进入历史；Agent 与 Inbox API 变化 |
| [v0.1.5-alpha.2][v0.1.5-alpha.2] | 2026-09-09 | `b2e3b2a01258` | 索引 | 交互、安装与平台兼容改进 |
| [v0.1.5-rc.1][v0.1.5-rc.1] | 2026-09-10 | `183f08e9c6dd` | 索引 | 阶段候选版汇总 |
| [v0.1.5-rc.2][v0.1.5-rc.2] | 2026-09-10 | `fb2c4b9e698e` | 定向 | 反馈确认、文件展示等修复 |
| [v0.1.6-alpha.1][v0.1.6-alpha.1] | 2026-09-15 | `0a15e36e7f82` | [专题](releases/v0.1.6-alpha.1.md) | Node PTC 进程与文件策略、SSH、MCP resources；Session Log 默认开启 |
| [v0.1.6-alpha.2][v0.1.6-alpha.2] | 2026-09-17 | `ddefc45fbc7f` | 索引 | 插件运行时管理、Inbox 恢复与可继续子代理改进 |
| [v0.1.7-alpha.1][v0.1.7-alpha.1] | 2026-09-22 | `c36a83ff6bb9` | 定向 | Session v4、Messages-only、预设／配置迁移；Windows 删除越界修复 |
| [v0.1.7-alpha.2][v0.1.7-alpha.2] | 2026-09-22 | `00102833dfae` | 索引 | 后台任务连续唤醒修复；工具截断改 token 预算、部分自动依赖更新限补丁版 |
| [v0.1.7-rc.1][v0.1.7-rc.1] | 2026-09-23 | `46a7f68b0922` | 索引 | 阶段汇总；插件安装／启动的版本兼容检查 |
| [v0.1.7-rc.2][v0.1.7-rc.2] | 2026-09-24 | `477b4f420553` | 索引 | 持久定时提醒可选；动态工具缓存声明；账号／API Key 路由分开 |
| [v0.2.0-rc.1][v0.2.0-rc.1] | 2026-09-28 | `4878cdabd87d` | 定向 | 工具结果未知恢复、桌面交付；自动化改为可选 bundle |
| [v0.2.0-rc.2][v0.2.0-rc.2] | 2026-09-29 | `639ed0153972` | [专题](releases/v0.2.0-rc.2.md) | 桌面 CLI 管理、shell 环境、模型目录和审批诊断修复 |
| [v0.2.1-alpha.1][v0.2.1-alpha.1] | 2026-10-03 | `5badb15009ae` | [专题](releases/v0.2.1-alpha.1.md) | 实验 Mods、开发者工具；自动化回归 Web；删除 invariant 导出 |
| [v0.2.1-alpha.2][v0.2.1-alpha.2] | 2026-10-09 | `d74326738864` | [专题](releases/v0.2.1-alpha.2.md) | 子代理 activation、SDK wait、Team 直接投递、Python 文件策略与外部部署 |
| [v0.2.1-alpha.3](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-alpha.3) | 2026-10-14 | `2fbf4359b82f` | [本周报告](releases/v0.2.1-rc.2.md) | 相对 alpha.2：凭据优先级、SDK resume、Minimal 图片与压缩；热替换、恢复和显示修复 |
| [v0.2.1-alpha.4](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-alpha.4) | 2026-10-15 | `86a402200d95` | [本周报告](releases/v0.2.1-rc.2.md) | 相对 alpha.3：自定义插件索引、engines.dsh 优先规则、模型推理等级 UI |
| [v0.2.1-alpha.5](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-alpha.5) | 2026-10-16 | `1517a4dbca0a` | [本周报告](releases/v0.2.1-rc.2.md) | 相对 alpha.4：技能菜单刷新、终端重试、PTC 指引与模型名称 Slot；以官方修复说明记录 |
| [v0.2.1-rc.1](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-rc.1) | 2026-10-17 | `1600d8a1e140` | [本周报告](releases/v0.2.1-rc.2.md) | 相对 alpha.5：355个 package.json 版本字段更新；没有其他文件差异，正文为阶段汇总 |
| [v0.2.1-rc.2](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-rc.2) | 2026-10-17 | `687f282e8625` | [本周报告](releases/v0.2.1-rc.2.md) | 相对 rc.1：DeepSeek-V4.1-Flash-1017 适配及 Search／Fetch API；定向检查配置、实现和归档 |
| [v0.2.1-rc.3](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-rc.3) | 2026-10-23 | `1f81c047fc48` | [本周报告](releases/v0.2.1-rc.3.md) | API Key动态目录、更多菜单草稿、空白会话复用与Desktop交互事件 |


候选版正文可能汇总多个 alpha 的变化。例如 v0.1.2-rc.1 和 v0.1.7-rc.1 含阶段汇总，不能据正文位置把已经存在的能力记为该 RC 首次引入。表中未见 v0.1.4，也不据此虚构缺失版本或解释未公开的发布决策。

## 六维演进与企业含义

### 1. 产品定位、交互与部署

rc.7 的可组合内核已有 Web、Headless 和 SDK 入口；v0.1.2 阶段统一 profile 与网络 Web 认证，v0.1.6 增强 Headless、终端和 SSH 工作区，v0.2.0 收尾桌面 CLI 分发与启动环境，v0.2.1 增强代理入口并在 alpha.2 加入原生 TLS 等部署选项。[早期专题](releases/v0.1.0-rc.7.md)、[v0.1.2-alpha.1][v0.1.2-alpha.1]、[v0.1.6 专题](releases/v0.1.6-alpha.1.md)、[0.2 专题](releases/v0.2.0-rc.2.md)、[当前增量](releases/v0.2.1-alpha.2.md)

**推断／观察：**产品交付面持续拓展，但 profile、客户端与模式的能力不同；本次来源不足以确立企业多租户、SSO 或组织 RBAC 已交付。URL、token 认证、SSH 与 TLS 各解决局部问题，不能合并称作企业平台。

### 2. 执行循环、规划、工具、子代理、长任务与恢复

早期已经区分 turn／step、并行工具和独占屏障。后续更明显的主线是“谁拥有执行与完成”：v0.1.3 的异步创建及持有者，v0.1.5 的显式 Agent 和 Inbox API，v0.1.6 的初始化等待、可取消准备，0.2 的未知工具结果处理，再到 alpha.2 的子代理 activation 与 SDK 子树等待。[持久化专题](releases/v0.1.3-alpha.1.md)、[v0.1.5-alpha.1][v0.1.5-alpha.1]、[执行专题](releases/v0.1.6-alpha.1.md)、[0.2 专题](releases/v0.2.0-rc.2.md)、[F-02](FINDINGS.md#f-02--根代理-idle-与完整任务完成必须分开)

Goal 的暂停、恢复、停止、队列和父子任务归属在多个发布中有修复记录。Team 也不是不变协议：v0.1.3 调整 steer 归属，alpha.1 仍有 mailbox，alpha.2 改为直接 inbox，并取消旧重试／去重承诺。[v0.1.3-alpha.1][v0.1.3-alpha.1]、[v0.1.5-alpha.1][v0.1.5-alpha.1]、[v0.2.1-alpha.1][v0.2.1-alpha.1]、[F-03](FINDINGS.md#f-03--team-简化了消息链路也改变了交付承诺)

**推断／借鉴：**最值得采纳的设计思想是区分接收、开始、局部 idle、子树结束、业务成功及结果未知。反复出现相关修复说明该区域持续变化，不证明同一个缺陷反复回归，也不能据此计算失败率。

### 3. Context、压缩与 memory

自动摘要、工具结果修剪和默认关闭的第三方 memory 示例在 rc.7 已存在。v0.1.7-alpha.1 调整主动压缩的输出预算与余量，目标是减少长输出后才压缩的情况；alpha.2 又把工具内联截断从字节配置改为估算 token 预算。这些仍是会话上下文管理，没有证据证明由此获得有权限、出处、删除与冲突治理的长期知识库。[早期压缩][early-compaction]、[早期 memory][early-memory]、[v0.1.7-alpha.1][v0.1.7-alpha.1]、[v0.1.7-alpha.2][v0.1.7-alpha.2]

持久化的分界更清楚。截至2026-10-12逐个读取26个 tag 的 `SESSION_FORMAT_VERSION` 后得到：

| 产品发布区间 | 写入格式 | 关键变化 |
|---|---|---|
| rc.7 至 v0.1.2-rc.1 | 0 | 持久 assistant chunk；早期 SQLite 后端随后删除 |
| v0.1.3-alpha.1 至 alpha.2 | 2 | SessionHandle、单写锁、attempt settlement；旧代际保留并相邻迁移 |
| v0.1.5-alpha.1 至 v0.1.6-alpha.2 | 3 | 系统提示词纳入历史，旧 PTC／预设引用迁移，官方明确不支持升级后降级读取 |
| v0.1.7-alpha.1 至 alpha.2（rc.2复核仍为4） | 4 | 迁移工具和历史 V3 兼容处理；0.2 未再次改变常量 |

源码边界：[格式0][fmt0]、[格式2][fmt2]、[格式3][fmt3]、[格式4][fmt4]；迁移行为依据 [v0.1.3 专题](releases/v0.1.3-alpha.1.md)、[v0.1.5-alpha.1][v0.1.5-alpha.1]、[v0.1.7-alpha.1][v0.1.7-alpha.1]。迁移链有格式1的定义，但本次列表没有发现写格式1的已发布版本。v0.1.7-alpha.1 内的格式状态文档仍以较旧发布为证据，故“是否已发布”采用该 release 的事实加实际源码常量核定，不机械照搬文档登记。[当时格式状态页][format-status]

**推断／验证：**日志格式是单独的兼容接口。数据导出、统计、审计和自定义读取器都受影响；旧文件保留不意味着通用回滚可行。压缩摘要还需另行评估保真与调用费用。

### 4. 插件、Skills、MCP、模型、IM 与 SDK

插件一直是主结构；变化在分发和契约。v0.1.2 统一入口／远程服务机制，v0.1.6 移除内置 E2B、统一 PTC 名称并升级 MCP，v0.1.7 把预设和设置转为插件组合与 profile 配置，0.2.1 增加 Mods 演示并移除旧诊断导出。[v0.1.2-alpha.1][v0.1.2-alpha.1]、[v0.1.6 专题](releases/v0.1.6-alpha.1.md)、[v0.1.7-alpha.1][v0.1.7-alpha.1]、[插件专题](releases/v0.2.1-alpha.1.md)

模型协议有两个不同边界：v0.1.6-alpha.1 **默认** Messages，旧选项仍在；v0.1.7-alpha.1 **只接受** Messages，配置中残留 `protocol` 会抛错。pi-ai 的模型目录也随版本更新，目录中的 ID 不能视为长期稳定契约。[旧协议配置][protocol-old]、[新协议配置][protocol-new]、[v0.2.0-rc.2][v0.2.0-rc.2]

自动化的产品位置并非单向增加：v0.1.7-rc.2 默认关闭，0.2.0 改可选 bundle，0.2.1-alpha.1 回归 Web 内置并按模式开放工具。[v0.1.7-rc.2][v0.1.7-rc.2]、[可选组合][schedule-old]、[Web 组合][schedule-new] **推断：**企业配置清单要同时记录包、profile、默认值和工具暴露，不能只维护功能勾选表。Skills／MCP／SDK 的存在也不足以证明任一企业 IM 已有官方运行接入；本轮没有逐版完整 IM 插件考古，保持未知。

### 5. 身份、权限、审批、沙箱与审计

历史 release 包含明确安全相关修复：v0.1.1-rc.1 的 Linux bwrap `/proc` 路径问题，v0.1.7-alpha.1 的 Windows 授权目录外删除问题。前者额外核了修复后 PID namespace 参数；后者目前依据官方 release，未重现实验，也未把它写成当前漏洞。[v0.1.1-rc.1][v0.1.1-rc.1]、[修复后参数][bwrap-fixed]、[v0.1.7-alpha.1][v0.1.7-alpha.1]

v0.1.6 的 Node PTC 接入文件策略和进程限制，而同版实验 Python PTC 明确没有文件沙箱；Python 接入文件策略是 alpha.2 的后续变化。Auto review 与权限修复技能扩展的是局部审批体验，不能推出宿主插件、网络、同用户凭据和不同租户已隔离。[执行专题](releases/v0.1.6-alpha.1.md)、[当前安全边界](FINDINGS.md#f-04--现有审批和文件沙箱不构成企业隔离)

**推断／跳过当前生产采用：**安全能力必须按后端、OS、精确版本和实际执行方式验证；过去修复过某个平台问题既不能证明现在仍有该漏洞，也不能替代当前安全审计。当前 SAFETY 仍声明尚未审计、非生产就绪。[当前 SAFETY][safety]

### 6. 日志、Trace、异常、升级、依赖与成本

诊断逐步从事件／Trajectory 扩展到原始日志和开发者组合，但 invariant 运行时导出在 alpha.1 被移除。不要把“更多可视化”与“保留所有旧诊断 API”混为一谈。[插件专题](releases/v0.2.1-alpha.1.md)

数据出站有一条明确历史：Session Log 在 v0.1.2-alpha.1 出现，直到 v0.1.5-rc.2 的 schema 默认 false；v0.1.6-alpha.1 起默认 true，当前仍如此。OTel 的反馈触发上报是另一条通道。该结论核了各已发布 tag 的 schema，而不是依据当前说明回推。[引入时配置][upload-first]、[翻转前][upload-before]、[翻转后][upload-after]、[F-01](FINDINGS.md#f-01--默认-session-log-外发需要独立治理)

**推断／验证：**升级检查应覆盖默认出站、事件 payload、补传行为、模型目录和依赖组合；审计日志、产品诊断、反馈上报必须分开。没有运行数据可支持“新版本更便宜／更快／更可靠”的总体结论，摘要、子代理、评审与重试仍需统一费用归集。

## 2026-10-19：凭据来源、插件契约与外部服务

alpha.3 将已保存凭据置于环境之前，同时让 Headless 默认退出本地凭据存储；SDK 的显式 resume 补齐持久会话接入，但不恢复外部进程。alpha.4 增加 `engines.dsh` 优先兼容判断和默认关闭的自定义索引市场，随附关闭组合增至12项；发现、安装与运行分别有条件。rc.1 只是相邻版本字段更新，其跨版本摘要不重复计作新增。[凭据优先级](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/credentials/credentials-local/README.zh.md)、[SDK 恢复契约](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/sdk/client/README.zh.md)、[兼容判断源码](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/boot/app-boot/src/plugin-compatibility.ts)、[rc.2 入口与可选清单](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/boot/app-boot/src/profile.ts)

rc.2 的新网页 API 将搜索与抓取扩展为可选的直接远端服务。默认提供者没有改变；启用后的用户问题片段、URL出站、目标状态不可见和无自动回退，则增加了数据治理与失败处理责任。这个变化不能被“无辅助模型token”概括为无成本，也不能被界面遮罩概括为脱敏出站。[Search／Fetch 固定说明](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/web/web-deepseek-api/README.zh.md)、[本周报告](releases/v0.2.1-rc.2.md)

**迁移判断：**优先检查凭据来源、插件版本声明／索引可信度、网页提供者选择及失败语义；只有使用相应入口与配置的集成受影响。仍无足够证据提升生产采用或实际可靠性等级。

## 2026-10-26：目录与会话装配不再只看版本号

rc.3 的官方 API Key 模型发现按条件跟随远端目录，并执行最低客户端版本门槛；自定义目录停止跟随。新会话复用找回未发送草稿，同时失去“每次新建即按当前定义装配”的旧假设。两者都要求接入方记录运行时的目录／会话条件，而不是只固定安装版本。[API Key 动态目录](https://github.com/deepseek-ai/deepseek-harness/blob/1f81c047fc48fa190a683e469daa699857e9afe8/packages/llm/llm-deepseek-api-key/README.md)、[空白会话迁移指南](https://github.com/deepseek-ai/deepseek-harness/blob/1f81c047fc48fa190a683e469daa699857e9afe8/docs/upgrade-guide/v0.2.1-rc.2/new-session-blank-reuse/guide.zh.md)

Web 默认新增入口插件，但执行仍停在待用户发送的草稿；12项可选关闭组合与preset文件未变。Desktop扩展产品事件，不是普通Web默认采集或业务验收指标。以上保持“借鉴／验证／观察”，不提升自主或生产成熟度。[本周报告](releases/v0.2.1-rc.3.md)

## 迁移成本与持续观察

插件核查补充了两个独立变化轴：早期抽样 npm 内部依赖使用版本范围，近期改为精确版本；alpha.2 随附关闭组合从上一版4项增至11项，但并非默认启用11项新能力。也有“加载行没变、实现有变”的情况，如 v0.1.3 的 Session API、v0.2.0-rc.2 的 pi-ai 依赖。历史 alpha.2 发行归档与 tag 的 Plan 文本差异、v0.1.3-alpha.1 包抽样不可得的限制，统一登记在 [插件发行证据](PLUGINS.md#发行包核验与版本纪律)，不倒推成架构重写或运行缺陷。

以下成本等级是研究推断，取决于是否依赖相应接口，不是已测工时。

| 变化 | 性质 | 最受影响对象 | 成本判断与检查对象 |
|---|---|---|---|
| SQLite 删除、格式0→2→3→4 | 移除后端／变更格式 | 历史会话、自定义日志读取器 | 高：导出、代际、读取器及不可降级边界 |
| SessionHandle、异步创建、Agent／Inbox API | 引入持有契约／变更 API | 同进程插件、宿主编排 | 中至高：生命周期、锁释放、调用等待及归属 |
| PTC／E2B、初始化钩子、远程路径 | 变更执行边界／移除内置后端 | 自定义执行后端 | 高：配置、环境、取消、策略与资源限制 |
| Messages 默认再到唯一协议、模型 ID 变化 | 变更默认／移除旧协议和 ID | 私有模型网关、保存的模型配置 | 中至高：协议地址、旧字段、模型能力和回退 |
| 预设／设置／子路径元数据／invariant 变化 | 变更配置／移除导出 | 插件作者和运维配置 | 中：注册入口、组合、HMR 与重启要求 |
| Session Log 默认翻转 | 引入通道后变更默认 | 使用默认配置的所有相关集成 | 治理优先级高：实际 payload、目的地、开关和补传 |
| SDK wait、Team mailbox→直接 inbox | 引入等待 API／移除旧交付机制 | 异步业务任务和多代理协作 | 高：完成回执、重试、幂等、历史消息恢复 |

这些检查的版本证据分别在上文六维与对应 release 文档，不把未受影响的部署也认定为高成本。

持续出现的主题是：长历史与上下文压力、停止／恢复／队列边界、跨平台进程与沙箱、插件生命周期与配置迁移。它们有跨版本修复证据，宜保留为每周定向阅读入口；目前不足以断言同一 bug 回归、系统性不安全或质量持续恶化。最值得改变采用判断的证据是明确兼容承诺、长期任务完成与恢复契约、可验证的出站控制，以及目标平台的独立安全验证。[早期修复][v0.1.0-rc.7]、[持久化回退][v0.1.3-alpha.1]、[后续修复][v0.1.3-alpha.2]、[当前版本][v0.2.1-alpha.2]

本轮**采用**项为空；**借鉴**日志投影、执行归属与结果未知的设计；**验证**迁移、出站和完成语义；**观察**Team、插件兼容及安全成熟度；**跳过**在证据不足时将其作为生产或多租户运行时。后续只在实质变化时更新演进结论，不随每个 UI 修复复制整份历史。

[v0.1.0-rc.7]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.0-rc.7
[v0.1.0-rc.8]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.0-rc.8
[v0.1.1-rc.1]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.1-rc.1
[v0.1.1-rc.2]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.1-rc.2
[v0.1.2-alpha.1]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.2-alpha.1
[v0.1.2-alpha.2]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.2-alpha.2
[v0.1.2-alpha.3]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.2-alpha.3
[v0.1.2-alpha.4]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.2-alpha.4
[v0.1.2-alpha.5]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.2-alpha.5
[v0.1.2-rc.1]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.2-rc.1
[v0.1.3-alpha.1]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.3-alpha.1
[v0.1.3-alpha.2]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.3-alpha.2
[v0.1.5-alpha.1]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.5-alpha.1
[v0.1.5-alpha.2]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.5-alpha.2
[v0.1.5-rc.1]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.5-rc.1
[v0.1.5-rc.2]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.5-rc.2
[v0.1.6-alpha.1]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.6-alpha.1
[v0.1.6-alpha.2]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.6-alpha.2
[v0.1.7-alpha.1]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.7-alpha.1
[v0.1.7-alpha.2]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.7-alpha.2
[v0.1.7-rc.1]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.7-rc.1
[v0.1.7-rc.2]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.1.7-rc.2
[v0.2.0-rc.1]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.0-rc.1
[v0.2.0-rc.2]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.0-rc.2
[v0.2.1-alpha.1]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-alpha.1
[v0.2.1-alpha.2]: https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-alpha.2
[early-compaction]: https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/packages/compaction/compaction-basic/README.zh.md
[early-memory]: https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/examples/mcp-memory/README.zh.md
[fmt0]: https://github.com/deepseek-ai/deepseek-harness/blob/99f6f02fecdb7dff40c3fbc9470f5907c29f74ca/packages/core/session/src/types.ts
[fmt2]: https://github.com/deepseek-ai/deepseek-harness/blob/d347e703908d0406b7a7ef80e3a0e594d86b2215/packages/core/session/src/types.ts
[fmt3]: https://github.com/deepseek-ai/deepseek-harness/blob/5dda764ed3aa172535a7967b06ff95d9cbfe536a/packages/core/session/src/types.ts
[fmt4]: https://github.com/deepseek-ai/deepseek-harness/blob/c36a83ff6bb95e3f82cf79f9be7c724270a8aa61/packages/core/session/src/types.ts
[format-status]: https://github.com/deepseek-ai/deepseek-harness/blob/c36a83ff6bb95e3f82cf79f9be7c724270a8aa61/docs/session-format-status.zh.md
[protocol-old]: https://github.com/deepseek-ai/deepseek-harness/blob/0a15e36e7f82b6ed45af6fa9759f29b40dcd965d/packages/llm/llm-deepseek/src/config.ts
[protocol-new]: https://github.com/deepseek-ai/deepseek-harness/blob/c36a83ff6bb95e3f82cf79f9be7c724270a8aa61/packages/llm/llm-deepseek/src/config.ts
[schedule-old]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/experimental/schedule-bundle/cordis.patch.yml
[schedule-new]: https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/bundle/web-app/cordis.patch.yml
[bwrap-fixed]: https://github.com/deepseek-ai/deepseek-harness/blob/528c682e061696f5a160f363f236ecbf53cbd006/packages/sandbox/sandbox-local/src/profiles.ts
[safety]: https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/SAFETY.zh.md
[upload-first]: https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/session/session-log-deepseek/src/index.ts
[upload-before]: https://github.com/deepseek-ai/deepseek-harness/blob/fb2c4b9e698e30edb738bca4cf0618587db7d203/packages/session/session-log-deepseek/src/index.ts
[upload-after]: https://github.com/deepseek-ai/deepseek-harness/blob/0a15e36e7f82b6ed45af6fa9759f29b40dcd965d/packages/session/session-log-deepseek/src/index.ts
