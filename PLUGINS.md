# 插件组成与演进

基线 **v0.2.1-alpha.2**／`d743267388641bc76f17c45ce8b4c231aed1d32c`，核查 **2026-10-13**。本页维护插件的供给方式、加载条件和变化证据；能力支持状态统一放在 [CAPABILITY-MAP](CAPABILITY-MAP.md)，产品全景见 [OVERVIEW](OVERVIEW.md)。本轮仅静态读取源码和 npm 发行归档，不安装、执行插件或调用模型。

## “随包”与“默认”分开记录

供给来源与启用状态是两个维度。这里“随包提供”包含 dsh 的生产依赖带来的包，不表示全部代码位于 CLI 自己的 tgz 内；“默认挂载”指新 profile、没有用户补丁／环境覆盖时的配置，不是本项目观察到它成功运行。

| 分类 | 如何确认 | 当前例子 |
|---|---|---|
| 内置随包提供 | npm 生产依赖、发行归档及 bundle manifest | base、web-app，以及下列11个随附可选组合；依赖存在不证明启用 |
| 默认启用／挂载 | profile 的 bundle 顺序、patch、preset、OS 条件，再看插件自身 schema | Web 的 Session、文件工具、Plan、压缩、子代理；Bash／PowerShell 按 OS 选择 |
| 需配置才产生能力 | 插件可能已挂载，但 provider、凭据、路径或端点为空 | pi-ai 路由、MCP 服务器；不能把空的桥接服务当作已接通外部系统 |
| 官方可选 | 官方目录或随附清单，默认 profile 未选择 | 随附关闭的 Team／Auto review；另有按需安装的 Codex／Claude Code 子代理 |
| 第三方 | 外部作者／运行时与独立配置、数据生命周期 | MCP memory 示例的外部服务器；并非 dsh 默认长期记忆 |

源码链条为 **profile → 有序 bundle → bundle 的 patch 文件 → preset／条件／用户覆盖 → 插件 schema 与实现**。Web 会关掉部分 base 工具，再按会话 preset 挂载；patch 对目标行的 `config` 是整体替换，不能假定深层合并。只检查 `dependencies` 或 base 一层会误判默认能力。[profile][profile]、[base][base]、[Web manifest][web-manifest]、[Web patch][web]

## 当前默认组成与重要例外

| 作用域 | 已核实的组成／条件 | 场景影响 |
|---|---|---|
| Web standard | 默认 preset；文件／Shell、Skills、`/plan`、`/goal`、`/compact`、子代理、工作流、`present`、提醒工具 | 面向日常任务；持久服务与每个 Agent 的工具分开挂载 |
| Web PTC／创造模式 | PTC 改工具呈现，并关闭该 preset 的 workflow；创造模式开放插件管理工具；其余能力并非与 standard 完全等同 | 不能把某模式的工具目录推广到全部会话 |
| Web minimal | preset 主要提供持久 Shell；Host 层及全局可选工具仍可能补充能力 | “minimal”不是隔离或永久工具白名单 |
| Headless／SDK | 基于 base 再叠加自身 bundle；普通 SDK 关闭标题模型和 HMR | UI、标题调用和交互可用性取决于入口 |
| SDK Minimal | 独立 bundle，不继承 base；默认 `danger-full-access`；同时挂载 Session Log、包清单扩展及当前目录工具 | 不能沿用 base 的 `workspace-write + ask` 权限判断；此配置也已在 npm 包中确认 |

来源：[默认 profile][profile]、[standard][standard]、[PTC][ptc]、[创造模式][creator]、[minimal][minimal]、[SDK][sdk]、[SDK Minimal][sdk-minimal]、[其发布元数据](https://registry.npmjs.org/@deepseek-ai/dsh-sdk-minimal/0.2.1-alpha.2)。这里只核配置及实现，不把权限名称当作实际隔离测试。

当前 `OPTIONAL_BUNDLES` 有 **11项**：会话搜索、Ralph、持久终端、Badge Skill、全提示词标题、Team、语音输入、思考翻译、Auto review、Inspector、Worktree。源码明确它们随安装提供、未被默认模板选择、在插件管理器中默认关闭；它们的“实验性”身份与是否随附也是独立维度。[随附列表][profile]、[CLI manifest][manifest]

其中，会话搜索提供5个全局只读工具，持久终端提供6个全局工具；启用后包括 minimal 在内的各 preset 会看到目录变化。全提示词标题会关闭原首提示词标题插件；翻译默认使用 Bing，可选其他服务，展开内容可能出站。这些都是能力、作用域或费用路径变化，不能只记录“新增一个插件”。[搜索][search]、[终端][terminal]、[标题替换][title]、[翻译][translation]

按需官方目录当前列出 Codex、Claude Code 两个子代理包，其 provider runtime 不随 dsh 主分发安装。安装这类官方桥接仍需满足相应运行时和认证条件。[目录声明][on-demand] 另有 Codex／Claude command hooks 桥接，需显式挂载并指定配置文件；能阻止工具或续行不等于默认启用，更不等于企业策略引擎。[Codex hooks][hooks]、[Claude hooks][claude-hooks] pi-ai 的额外路由及 MCP 服务器也需具体配置。[pi-ai][pi-ai]、[MCP][mcp]

## 六个已选版本的插件变化

各行沿用对应 release 文档的相邻已发布比较基准；rc.7 只建立当时基线。下列不是所有包的机械增删列表，而是会改变能力、默认值或集成判断的条目。

| 版本 | 插件与默认变化 | 接口／迁移及场景含义 |
|---|---|---|
| [v0.1.0-rc.7](releases/v0.1.0-rc.7.md) | 已有 base→Web 分层；base 的 Ralph 行挂载，但 Web 再禁用它；OTel 插件挂载但 mode 默认 DISABLED | 已能看到“包存在／行挂载／功能开启”的区别；不可用一层计数代表全部 profile。[base][rc7-base]、[Web][rc7-web] |
| [v0.1.3-alpha.1](releases/v0.1.3-alpha.1.md) | 相对 v0.1.2-rc.1，base 行集合不变，Web 新增 file-upload | SessionHandle、异步 create 和 settlement 是已加载插件内部的破坏变化；插件名称不变也必须分析。该版 npm 抽样缺口见下文。[Web][a13-web] |
| [v0.1.6-alpha.1](releases/v0.1.6-alpha.1.md) | base 新增 MCP resources、image-offload、Node PTC／workflow-ptc，移除 workflow-worker-thread；Ralph 默认关闭。Web 增终端入口 | PTC 重命名、`agent/session-start`→异步 `agent/created`、Session Log 默认翻转；执行、hook 初始化和数据出站都需迁移。[base][a16-base]、[Web][a16-web] |
| [v0.2.0-rc.2](releases/v0.2.0-rc.2.md) | 与 rc.1 的 base／Web 插件行及配置无实质差异；随附可选清单为 Team、语音、Auto review、Schedule 四项 | 仍有内部依赖变化：pi-ai 范围从 `^0.85.1` 到 `^0.87.1`；已保存模型选择可能受影响。不能把“无新插件”写成“无插件变化”。[清单][rc20-profile]、[旧 manifest][pi-before]、[新 manifest][pi-after] |
| [v0.2.1-alpha.1](releases/v0.2.1-alpha.1.md) | Web 默认挂载 schedule／ui-schedule，可选 Schedule 退出清单，Inspector 进入；Web manifest 按顺序加载独立 preset patch | 旧 Schedule 选择自动清理；子路径元数据、activity／usage 注册项和 invariant 导出有破坏迁移。preset 拆分在此版已存在，不声称由此版首创。[Web][a21-web]、[清单][a21-profile] |
| [v0.2.1-alpha.2](releases/v0.2.1-alpha.2.md) | 随附关闭组合4→11；base 增当前目录服务／工具，移走 Badge／Ralph 行；子代理配置移除 backgroundMode | 主循环、工具呈现、Team 等实现变化仍需跟踪。首提示词标题的输出上限64→4096；普通 SDK 禁用该插件，此上限也不是每次实际用量。[旧 base][a21-base]、[当前 base][base]、[SDK][sdk] |

可选组合增多不等于默认授权扩大；反之，包列表不变也可能改变权限、模型提示词、schema、hooks 或默认出站。更早的存储、协议及生命周期变化见 [EVOLUTION](EVOLUTION.md)，各 release 文档保存具体迁移语义。

## 发行包核验与版本纪律

对上述6个版本各查 `@deepseek-ai/dsh`、`dsh-base`、`dsh-web-app`、`dsh-app-boot`，另核当前 `dsh-sdk-minimal`。成功静态下载 **21个 tgz**，逐一匹配 registry 的 SHA-512 integrity；比对归档中 **52份 YAML**（含说明元数据），48份与对应 tag 字节一致，4份有下述提示词差异。没有安装依赖、执行生命周期脚本或验证整个依赖闭包、Desktop 二进制与 Python wheel。

| 抽查版本 | 四个主样本包结果 | dsh 内部直接依赖写法 |
|---|---|---|
| v0.1.0-rc.7 | 均可取；所查 YAML 一致 | `^0.1.0-rc.7` 范围 |
| v0.1.3-alpha.1 | 四个精确版本端点均404；包总元数据的 versions 也无此项 | 仅保留 tag 源码结论，未完成发行包验证 |
| v0.1.6-alpha.1 | 均可取；所查 YAML 一致 | `^0.1.6-alpha.1` 范围 |
| v0.2.0-rc.2 | 均可取；所查 YAML 一致 | 精确 `0.2.0-rc.2` |
| v0.2.1-alpha.1 | 均可取；所查 YAML 一致 | 精确 `0.2.1-alpha.1` |
| v0.2.1-alpha.2 | 均可取；base 一处、Web 三个 preset 同一文字差异 | 精确 `0.2.1-alpha.2` |

可追溯入口如下，每格为本轮实际查询的精确版本元数据：

| 版本 | CLI | Base | Web | App Boot |
|---|---|---|---|---|
| 0.1.0-rc.7 | [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.1.0-rc.7) | [Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.1.0-rc.7) | [Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.1.0-rc.7) | [Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.1.0-rc.7) |
| 0.1.3-alpha.1 | [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.1.3-alpha.1) | [Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.1.3-alpha.1) | [Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.1.3-alpha.1) | [Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.1.3-alpha.1) |
| 0.1.6-alpha.1 | [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.1.6-alpha.1) | [Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.1.6-alpha.1) | [Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.1.6-alpha.1) | [Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.1.6-alpha.1) |
| 0.2.0-rc.2 | [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.2.0-rc.2) | [Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.2.0-rc.2) | [Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.2.0-rc.2) | [Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.2.0-rc.2) |
| 0.2.1-alpha.1 | [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.2.1-alpha.1) | [Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.2.1-alpha.1) | [Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.2.1-alpha.1) | [Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.2.1-alpha.1) |
| 0.2.1-alpha.2 | [CLI](https://registry.npmjs.org/@deepseek-ai/dsh/0.2.1-alpha.2) | [Base](https://registry.npmjs.org/@deepseek-ai/dsh-base/0.2.1-alpha.2) | [Web](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/0.2.1-alpha.2) | [Boot](https://registry.npmjs.org/@deepseek-ai/dsh-app-boot/0.2.1-alpha.2) |

**源码与包的差异：**alpha.2 tag 的 Plan 首句要求用户通过 `exit_plan_mode` 批准或切换模式；npm 归档改为 `exit_plan_mode` 成功或用户切换模式。差异位于 base 的 Plan section，以及 Web standard／ptc／cordis 的同一 section，其他所查 YAML 一致。这是可复核的发行内容差异；没有运行证据证明权限绕过，也未确认构建来源或差异原因。对模型实际提示词的判断应同时注明来源。[tag base][base]、[tag standard][standard]

| 差异归档 | 本轮验证通过的 integrity |
|---|---|
| [dsh-base tgz](https://registry.npmjs.org/@deepseek-ai/dsh-base/-/dsh-base-0.2.1-alpha.2.tgz) | `sha512-/sJRnKbpjKIzgxtU+qpl65njlTMp0Y8s62AhZQnQmXTJMRurcy1PUWNyB1lWHJqLhnQT9JO+xg/jF1C0E3ypiw==` |
| [dsh-web-app tgz](https://registry.npmjs.org/@deepseek-ai/dsh-web-app/-/dsh-web-app-0.2.1-alpha.2.tgz) | `sha512-KJFOxsb9eaNW2DNzLwLbUMKonAHUGVpQlLggr5nLNDeUo4TEjyBM+fzIu2qTw78QzpM+cYNAXyNPtYvqutt83w==` |

**版本记录：**样本包的 package version 与主版本相同，不据此编造独立插件发版史；组件代码以主 tag／commit 固定，包版本只按实际 manifest 记录。早期依赖范围说明仅固定 CLI 版本不足以确定安装后的全部代码；本项目未运行解析，未断言实际安装会选哪个版本。404也不能证明历史上从未发布、被撤回或撤回原因。

## 需要单独区分的产品能力

**出站数据按通道和入口区分。** 除 Session Log、反馈 OTel、包清单外，Desktop 还默认装配产品交互埋点及 exporter；普通 Web 不装配。官方文档排除提示词、模型回复和凭据作为这些事件字段，关闭新采集不会清空 exporter 队列。它不能与会话反馈开关混称。[Desktop 采集][product-analytics]、[exporter][product-exporter] 具体默认出站研究见 [F-01](FINDINGS.md#f-01--默认-session-log-外发需要独立治理)。

**文件能力分三条。** `present` 声明当前源文件并展示卡片，支持侧栏预览与 Host 打开／定位，当前没有“下载到访问者电脑”的内置入口；从首次公开文件卡片版本 v0.1.5-alpha.2 就是这种源文件语义。`/export` 下载会话日志 ZIP，但不携带 present 源文件字节。鉴权 `GET/HEAD /api/file` 则读取组合文件系统可访问的绝对路径内容，并按附件配置限制响应大小；它不是下载按钮，也不代表任意文件可读。网络取文件与 IM 附件收取又是其他能力，不能由这些接口推导。[早期 present][present-first]、[当前决策][present-decision]、[未运行的上游测试][present-test]、[ZIP 响应][zip]、[文件读取][file-api]、[鉴权][connection]

逐项状态和后续问题只维护在 [能力地图](CAPABILITY-MAP.md)。本轮仍未知：历史缺失包的原因、当前源码／归档差异的构建来源、全部平台发行物的一致性、实际插件加载结果和第三方服务可用性。后续优先静态核查这些证据；运行验证需另行确定范围。

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
