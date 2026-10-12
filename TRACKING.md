# 跟踪规则与检查状态

## 研究范围

本项目在 [ikxky/dsh-watch](https://github.com/ikxky/dsh-watch) 公开维护 DeepSeek Harness 的中文研究，关注企业 Agent 平台与个人助理的通用适用性。全部发布内容基于公开来源；不包含特定私有项目的源码、历史、试验结果、预算、凭据或内部协作信息。

这是研究文档项目，不安装或运行 dsh、不调用模型、不部署、不修改账户权限或凭据，不向 DeepSeek 上游创建 issue、PR、comment 或 Discussion。运行试验需另行明确范围，不由每周研究自动执行。

提交白名单仅为：

- `README.md`
- `TRACKING.md`
- `OVERVIEW.md`
- `EVOLUTION.md`
- `FINDINGS.md`
- `releases/*.md`

不增加 GitHub Actions、依赖、代码、数据库或单独的空周报。

## 证据与结论写法

| 标记 | 含义 |
|---|---|
| 官方说明 | 固定版本 README、文档、release 或维护方声明；不等同本项目实测 |
| 源码核实 | 在所登记 commit 直接检查了实现、配置或 diff；只证明该代码存在及可读语义 |
| 推断 | 从证据推导企业集成影响，明确前提，不能写成已复现缺陷 |
| 未知／待验证 | 缺少证据、公开入口不可达或必须运行才能确认 |

结论使用五类：**采用**（满足证据与验证要求后采纳具体能力）、**验证**（值得进一步核验）、**借鉴**（采纳设计思路而非引入运行时）、**观察**（持续跟踪成熟度或变化）、**跳过**（当前研究目标不投入）。本轮没有“生产采用”结论，也没有运行实测。

优先级：P1 涉及数据、权限、任务完成或升级兼容；P2 涉及能力边界与成本；P3 为局部体验。没有复现的问题按“约束／风险／验证项”记录，不宣称漏洞。

## 官方来源与版本纪律

主入口为 [产品页](https://www.deepseek.com/en/harness/)，其指向 [官方仓库](https://github.com/deepseek-ai/deepseek-harness)；安装包标识为 `@deepseek-ai/dsh`。以 [Releases 集合 API](https://api.github.com/repos/deepseek-ai/deepseek-harness/releases?per_page=100) 和 [网页列表](https://github.com/deepseek-ai/deepseek-harness/releases) 发现发布，包含 prerelease，不以 `/releases/latest` 代替。

每项版本结论绑定 tag 对应的完整 commit。正文源码链接固定到 commit；线上文档站和 master 仅作发现入口，不代表已发布版本保证。比较对象是前一个已发布 release 的 tag，不是任意前一 git tag。release 标题和正文可被修改，即使 release 标为 immutable，仍需检查正文指纹。

当前公开仓库 metadata 为 `has_issues=false`、`has_discussions=true`；官方 README 指向 [Discussions](https://github.com/deepseek-ai/deepseek-harness/discussions) 接收反馈。合并提交中的 PR 编号不能直接当作可访问的官方 PR：本轮访问官方 `pulls/4394` 返回 404，因此引用实际可核的 commit，不猜测其来源仓库。以后新增 issue/PR 跟踪条目前先验证 URL、标题、状态及与已发布版本的关系。[仓库 metadata](https://api.github.com/repos/deepseek-ai/deepseek-harness)、[版本 README](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/README.zh.md)

## 已登记发布

2026-10-12 查询完整 Releases API：第1页26条，第2页为空；均为 `draft=false`、`prerelease=true`。当前可见最早为 v0.1.0-rc.7，最新为 v0.2.1-alpha.2。完整时间线、各版本覆盖程度和历史六维分析见 [EVOLUTION](EVOLUTION.md)，不把本列表称作稳定版列表。

| 独立分析 | 选择原因与比较范围 |
|---|---|
| [v0.1.0-rc.7](releases/v0.1.0-rc.7.md) | 当前可见最早公开基线；没有可验证的上一条 release |
| [v0.1.3-alpha.1](releases/v0.1.3-alpha.1.md) | 持久化与生命周期边界；对比 v0.1.2-rc.1 |
| [v0.1.6-alpha.1](releases/v0.1.6-alpha.1.md) | 执行环境、协议与日志默认值；对比 v0.1.5-rc.2 |
| [v0.2.0-rc.2](releases/v0.2.0-rc.2.md) | 对比 rc.1；另明确回看 rc.1 相对 v0.1.7-rc.2 的阶段变化 |
| [v0.2.1-alpha.1](releases/v0.2.1-alpha.1.md) | 最新版直接前身、插件与诊断重组；对比 v0.2.0-rc.2 |
| [v0.2.1-alpha.2](releases/v0.2.1-alpha.2.md) | 当前六维基线；对比 alpha.1 |

其余发布已读取 release 并解析 tag。对格式、模型协议、沙箱修复和默认配置等关键转折补充定向源码核查，但不声称每个版本都做了完整全景评估。各专题正文绑定当时 commit；比较基准与补充范围明确区分。

正文指纹算法：API 返回的 `body` 字符串保持原始 CR/LF，UTF-8 编码后计算 SHA-256；不要先做 Markdown 格式化。以下登记全部26条以支持未来发现旧正文修改，公开 release ID 只是上游条目标识。

<details>
<summary>展开全部发布的固定 commit、release ID、更新时间与正文指纹</summary>

| 官方 tag | Peeled commit | Release ID | updated_at UTC | body SHA-256 |
|---|---|---|---|---|
| dsh-v0.1.0-rc.7 | `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca` | 371725157 | 2026-08-17T13:56:33Z | `7abf5f67e36099e3a1730af700a9637b5fe9ca824bf64a93af44d20a212c6a97` |
| dsh-v0.1.0-rc.8 | `141eb6fef83422698aef7a981029e843e8161534` | 373166049 | 2026-08-21T10:12:17Z | `de037765f44f1f062b5d7af5b3233718baf30fe40846c6fd323cccda77169f15` |
| dsh-v0.1.1-rc.1 | `528c682e061696f5a160f363f236ecbf53cbd006` | 374224613 | 2026-08-21T09:04:11Z | `48e4c1b31b2265d86ae0f168a1eb77c53dd587ef18bc2716b2cc99c54c17e0ff` |
| dsh-v0.1.1-rc.2 | `b150a551b8d465e31e418e1b2eaf5e79bbb7d28e` | 374388128 | 2026-08-21T12:35:08Z | `ef952f3bb480334a91d49a354d6c9f72ac15d9b807d9b2837153bd43536d0bd1` |
| dsh-v0.1.2-alpha.1 | `cd5ef8148158c3a752a658978873241fdf8e2bbc` | 377991936 | 2026-08-28T04:37:55Z | `5de483e86edbe905c43209371cf7c543a7d0a7667caffe1d864b7024ca98be59` |
| dsh-v0.1.2-alpha.2 | `0a53fb55bea101816fa226bb964ae2bed71c343b` | 379296034 | 2026-08-30T13:52:14Z | `9e5f42426f58e619d0afebb710f17b8ab54e67913fdcb86e221cc62d0713ef67` |
| dsh-v0.1.2-alpha.3 | `dd6322d604e00eec1ba5e0c8541159906a21094a` | 379884041 | 2026-08-31T16:03:39Z | `ab6badea167b361148021caa57d021205e5793f439453ae71809168a934b4efe` |
| dsh-v0.1.2-alpha.4 | `4e84901e6471b79ec0338099867ebb4606d12bb5` | 380633709 | 2026-09-01T16:56:25Z | `c955bec093419eb893008b296b5259f27b1016b9286dcb37829e1eac0c5108fb` |
| dsh-v0.1.2-alpha.5 | `db6bdc3576c2d4e7c965e8e3ed0c2a731eed87f5` | 381145530 | 2026-09-02T10:02:56Z | `4099cc3bf0899a6ce1f774486dd6a84d56fcfc82eb2ef14c0c71daaf13b08369` |
| dsh-v0.1.2-rc.1 | `a66e4702047846cdaa10c66c9d3df3951f5ea70d` | 381777538 | 2026-09-04T06:10:55Z | `4237c91aa6d803a6a50064c2efb2f91b4bc187e70751c92a51f253980795f050` |
| dsh-v0.1.3-alpha.1 | `d347e703908d0406b7a7ef80e3a0e594d86b2215` | 382677748 | 2026-09-04T11:34:32Z | `31123414e8d164f660f8f6b0fd88e13b802a75bf6942a9b24c9599f8d3a54739` |
| dsh-v0.1.3-alpha.2 | `82a5fd61a7cf5c293cec4bdff68f455398d685e9` | 384129524 | 2026-09-07T15:03:05Z | `ac77756bd7300317339f88a02fe1130b33b5d4768f30400b235bc6f68e9127bd` |
| dsh-v0.1.5-alpha.1 | `5dda764ed3aa172535a7967b06ff95d9cbfe536a` | 384887562 | 2026-09-08T16:16:04Z | `bd36f715f586c4ec67ce602e33924d7d5133b4a52e758dd1e0d5b62f8e9e5d9b` |
| dsh-v0.1.5-alpha.2 | `b2e3b2a0125854567a4a5fcba75782e42fe84901` | 385585674 | 2026-09-09T14:23:10Z | `23f808223ac5a267fb29912e21136e231e8b876fba6e6a038fe9720e863a6338` |
| dsh-v0.1.5-rc.1 | `183f08e9c6dde7e36cd2318eaee70b0da08fb35e` | 385978363 | 2026-09-10T03:42:23Z | `ee91da82dba70b2c044d6ff86fe840f19819ee520e474a0e0c7fe205f84aaf9e` |
| dsh-v0.1.5-rc.2 | `fb2c4b9e698e30edb738bca4cf0618587db7d203` | 386391166 | 2026-09-10T15:09:34Z | `5a1ca0a1e3ffda87ba448f6f2405e98b27ce29fe00c42b104f3a52541cb49198` |
| dsh-v0.1.6-alpha.1 | `0a15e36e7f82b6ed45af6fa9759f29b40dcd965d` | 388877007 | 2026-09-15T04:59:34Z | `3faca4b25599fb6851bd6454b3c30763014968a523928b8272724b29c9d96877` |
| dsh-v0.1.6-alpha.2 | `ddefc45fbc7f8e46dd73185e68295696d1297887` | 390743959 | 2026-09-17T13:30:16Z | `32f2c4dddf98e97b07401cadfffc95315ff97a7ae6b6140de83dbc64f1126f74` |
| dsh-v0.1.7-alpha.1 | `c36a83ff6bb95e3f82cf79f9be7c724270a8aa61` | 393490604 | 2026-09-22T06:16:27Z | `9584c63f77a1cbbb488c039291222bb1951dac1d201353206949db1739b41a33` |
| dsh-v0.1.7-alpha.2 | `00102833dfaee1da9f48a3a8eae9d34005a75218` | 393884772 | 2026-09-22T15:49:49Z | `0833d289d667e231226789ba07f0053a84c551b64b339530af981ae1119e06d3` |
| dsh-v0.1.7-rc.1 | `46a7f68b0922371ce7144b668b90e377d8e799f4` | 394685472 | 2026-09-23T15:36:47Z | `b130c0f1e58497e53a3085fe44e68a00c5affe25b5f2d5946a1c41125c0719b9` |
| dsh-v0.1.7-rc.2 | `477b4f420553e8a52c2fbccc464d7561b239c443` | 395756051 | 2026-09-27T05:51:24Z | `635137ed7cb00741aa4dc8e177d338422d19bf9bf185e692cabf699f76858139` |
| dsh-v0.2.0-rc.1 | `4878cdabd87d4041bdaff61d04c966883b9fd07a` | 398234978 | 2026-09-28T12:36:21Z | `efdc2176149f0c38d14131867f59673f7050cdd7c6f8c9a8a827995b59263973` |
| dsh-v0.2.0-rc.2 | `639ed015397290b3745d163aafe02ffee4aa3f84` | 399005027 | 2026-09-29T09:42:36Z | `bb4304835bbf3e586a20deda114345a09a62ad150ca201cc62ca500e082ffc76` |
| dsh-v0.2.1-alpha.1 | `5badb15009ae1756c3afe0ae0cef1faafc290ccc` | 402371422 | 2026-10-03T06:42:19Z | `f565c7fa851d9f56db4407f320655993d0ec340a52ea61ed9ef810fecef11e5a` |
| dsh-v0.2.1-alpha.2 | `d743267388641bc76f17c45ce8b4c231aed1d32c` | 407834735 | 2026-10-09T15:10:41Z | `057ac7f6b58dd8e1bea00e1da10449b352953c4f8ff885d26eb3c96355640fd3` |

</details>

tag 核验应解析到 commit（例如 `tag^{commit}`），不能把 annotated tag 对象的 SHA 当作源码 commit。当前 alpha.2 的 peeled commit 为 `d743267388641bc76f17c45ce8b4c231aed1d32c`；对象种类不同本身不是 tag 漂移证据。

## 最近检查

- 检查日期：2026-10-12 UTC。
- 结果：当前最新仍为 alpha.2；在已有基线之上完成历史补充，新增五个历史专题及 EVOLUTION。新增文档不代表上游又发布了新版本。
- 已检查：Releases API 全部26条及空的下一页、各条 prerelease／draft／发布时间／正文、全部 tag 的 peeled commit、各 tag 的 Session 格式常量和 Session Log 默认值、代表节点的关键文档与源码。安全公告页已在同日基线检查中查看，本轮未新增运行或漏洞扫描。
- [安全公告页](https://github.com/deepseek-ai/deepseek-harness/security/advisories)：检查时未显示已发布公告；这不能证明无漏洞或无风险。未进行依赖漏洞扫描、二进制验证或安全审计。
- 运行验证：未进行。源码中存在的测试及上游提交自报测试结果不计作本项目通过的测试。
- 来源限制：官方 PR 入口样本返回 404；当前没有已验证、已登记的 issue/PR URL，开放讨论尚未逐条评估。关键事项通过 FINDINGS 中的 commit／文档引用跟踪。
- 交付范围：入口、规则、当前全景、演进、发现五份主文档及六份版本文档，共11份 Markdown；实际提交身份以仓库 Git 历史为准。
- 本轮结果：[演进与完整发布索引](EVOLUTION.md)、[全景](OVERVIEW.md)、[关键发现](FINDINGS.md)、[当前版本增量](releases/v0.2.1-alpha.2.md)。

检查失败、认证中断或来源不可达时，状态写“检查不完整”并保留上次成功基线；不能写成“无变化”。

## 每周机制

目标时间为**每周一北京时间上午 9 点附近（Asia/Shanghai，UTC 01:00）**。由平台 automations 调度，不通过 GitHub Actions；本仓库的 `on: release` 只能响应本仓事件，不能作为监听上游发布的实现。

**状态：每周跟踪已创建并启用。** 采用灵活时间窗口，目标为每周一北京时间上午 9 点附近；首个计划日为 **2026-10-19**。启用状态不代表已有成功运行记录；首次自动运行结果届时登记。

每次执行：

1. 读取本文件和最近版本结论，确认操作目标仍是 ikxky/dsh-watch。
2. 查询完整 release 列表（含预发布，分页直至覆盖已登记基线），识别新增、撤回或改名条目；核 tag→commit、发布时间、prerelease、正文修改和 fingerprint。对本表已登记发布复查正文；区分正文修订、tag 移动与新增 release，不能把 annotated tag 对象与 commit 的差异误报为移动。
3. 检查安全公告、SAFETY 改动和已登记 upstream refs；对真实可访问的 issue/PR 记录其状态、更新时间及相关提交。master 新内容只标为未发布信号。
4. 有实质变化时，按六维定向阅读 release、固定源码及差异，新增 `releases/<version>.md`，同步当前 OVERVIEW、FINDINGS 和 TRACKING；若改变长期趋势、默认值、兼容边界或历史归属，再更新 EVOLUTION。候选版的累计摘要不能当作当次首次引入的证据。现有 release 正文修订则更新对应文档和指纹，不制造新版本名。
5. 只按白名单提交这一个公开研究仓库；提交前检查 diff、引用、凭据和来源边界；push 后回读远端 commit 与文件。失败时不得宣称发布完成。
6. 向用户报告改变判断的事项，优先报告安全、重大兼容、默认外发和执行可靠性变化；附来源与文档链接。一般 UI 微调只有改变本项目结论时才报告。

“无实质变化”指没有新发布、重大正文修订、相关安全变化或已登记事项的实质状态变化。此时只更新本文件的检查时间、覆盖范围与结果，允许提交这项状态更新；不新增 release 报告，不发送例行空通知。来源不可达等导致机制失效的事项属于运行异常，应简短报告，不按静默成功处理。

## 下一步

1. 首次每周自动检查计划于 2026-10-19 执行，届时更新检查状态；无实质变化保持通知静默。
2. 优先核验 F-01 日志外发配置、F-02 完成与恢复语义、F-03 Team 升级语义，并关注日志格式、协议和插件兼容承诺。历史趋势以 EVOLUTION 为入口，避免每次复制全量全景；当前仅进行公开资料与源码研究。
3. 如另行开展运行验证，在隔离环境使用非敏感样本，单独记录平台、精确版本、配置、输入和失败证据；不把源码测试的存在写成本项目测试通过。
