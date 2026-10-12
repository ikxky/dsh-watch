# 跟踪规则与检查状态

## 研究范围

本项目在 [ikxky/dsh-watch](https://github.com/ikxky/dsh-watch) 公开维护 DeepSeek Harness 的中文研究，关注企业 Agent 平台与个人助理的通用适用性。全部发布内容基于公开来源；不包含特定私有项目的源码、历史、试验结果、预算、凭据或内部协作信息。

这是研究文档项目，不安装或运行 dsh、不调用模型、不部署、不修改账户权限或凭据，不向 DeepSeek 上游创建 issue、PR、comment 或 Discussion。运行试验需另行明确范围，不由每周研究自动执行。

提交白名单仅为：

- `README.md`
- `TRACKING.md`
- `OVERVIEW.md`
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

| 版本／官方 tag | 发布时间 UTC | 对应 commit | 本项目分析程度 |
|---|---|---|---|
| v0.2.1-alpha.2／dsh-v0.2.1-alpha.2 | 2026-10-09 11:09:26 | `d743267388641bc76f17c45ce8b4c231aed1d32c` | 六维基线与上一版本增量 |
| v0.2.1-alpha.1／dsh-v0.2.1-alpha.1 | 2026-10-03 06:42:19 | `5badb15009ae1756c3afe0ae0cef1faafc290ccc` | 增量比较基准；未独立做全景评估 |
| v0.2.0-rc.2／dsh-v0.2.0-rc.2 | 2026-09-29 09:42:36 | `639ed015397290b3745d163aafe02ffee4aa3f84` | 仅核发布时间、prerelease 与 tag |
| v0.2.0-rc.1／dsh-v0.2.0-rc.1 | 2026-09-28 12:36:21 | `4878cdabd87d4041bdaff61d04c966883b9fd07a` | 仅核发布时间、prerelease 与 tag |

以上四次发布均为 prerelease。当前 alpha.2 release ID 为 `407834735`，`updated_at=2026-10-09T15:10:41Z`；alpha.1 ID 为 `402371422`，`updated_at=2026-10-03T06:42:19Z`。[当前发布](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-alpha.2)、[上一发布](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.1-alpha.1)

正文指纹算法：API 返回的 `body` 字符串保持原始 CR/LF，UTF-8 编码后计算 SHA-256；不要先做 Markdown 格式化。

| tag | body SHA-256 |
|---|---|
| dsh-v0.2.1-alpha.2 | `057ac7f6b58dd8e1bea00e1da10449b352953c4f8ff885d26eb3c96355640fd3` |
| dsh-v0.2.1-alpha.1 | `f565c7fa851d9f56db4407f320655993d0ec340a52ea61ed9ef810fecef11e5a` |

## 最近检查

- 检查日期：2026-10-12 UTC。
- 结果：完成首次基线；发现最新发布 alpha.2，完成与 alpha.1 的固定提交 diff 检查。
- 已检查：Releases 列表及 API 首 10 条、近四次发布 metadata、相应 git tags、关键文档与源码、公开安全公告页。
- [安全公告页](https://github.com/deepseek-ai/deepseek-harness/security/advisories)：检查时未显示已发布公告；这不能证明无漏洞或无风险。未进行依赖漏洞扫描、二进制验证或安全审计。
- 运行验证：未进行。源码中存在的测试及上游提交自报测试结果不计作本项目通过的测试。
- 来源限制：官方 PR 入口样本返回 404；当前没有已验证、已登记的 issue/PR URL，开放讨论尚未逐条评估。关键事项通过 FINDINGS 中的 commit／文档引用跟踪。
- 交付范围：五份白名单 Markdown 文档组成首次基线；实际提交身份以仓库 Git 历史为准。
- 本轮结果：[全景](OVERVIEW.md)、[关键发现](FINDINGS.md)、[版本增量](releases/v0.2.1-alpha.2.md)。

检查失败、认证中断或来源不可达时，状态写“检查不完整”并保留上次成功基线；不能写成“无变化”。

## 每周机制

目标时间为**每周一北京时间上午 9 点附近（Asia/Shanghai，UTC 01:00）**。由平台 automations 调度，不通过 GitHub Actions；本仓库的 `on: release` 只能响应本仓事件，不能作为监听上游发布的实现。

**状态：每周跟踪已创建并启用。** 采用灵活时间窗口，目标为每周一北京时间上午 9 点附近；首个计划日为 **2026-10-19**。启用状态不代表已有成功运行记录；首次自动运行结果届时登记。

每次执行：

1. 读取本文件和最近版本结论，确认操作目标仍是 ikxky/dsh-watch。
2. 查询完整 release 列表（含预发布，分页直至覆盖已登记基线），识别新增、撤回或改名条目；核 tag→commit、发布时间、prerelease、正文修改和 fingerprint。对当前基线及已登记比较基准复查正文。
3. 检查安全公告、SAFETY 改动和已登记 upstream refs；对真实可访问的 issue/PR 记录其状态、更新时间及相关提交。master 新内容只标为未发布信号。
4. 有实质变化时，按六维定向阅读 release、固定源码及差异，新增 `releases/<version>.md`，同步当前 OVERVIEW、FINDINGS 和 TRACKING。现有 release 正文修订则更新对应文档，不制造新版本名。
5. 只按白名单提交这一个公开研究仓库；提交前检查 diff、引用、凭据和来源边界；push 后回读远端 commit 与文件。失败时不得宣称发布完成。
6. 向用户报告改变判断的事项，优先报告安全、重大兼容、默认外发和执行可靠性变化；附来源与文档链接。一般 UI 微调只有改变本项目结论时才报告。

“无实质变化”指没有新发布、重大正文修订、相关安全变化或已登记事项的实质状态变化。此时只更新本文件的检查时间、覆盖范围与结果，允许提交这项状态更新；不新增 release 报告，不发送例行空通知。来源不可达等导致机制失效的事项属于运行异常，应简短报告，不按静默成功处理。

## 下一步

1. 首次每周自动检查计划于 2026-10-19 执行，届时更新检查状态；无实质变化保持通知静默。
2. 优先核验 F-01 日志外发配置、F-02 完成与恢复语义、F-03 Team 升级语义；当前仅进行公开资料与源码研究。
3. 如另行开展运行验证，在隔离环境使用非敏感样本，单独记录平台、精确版本、配置、输入和失败证据；不把源码测试的存在写成本项目测试通过。
