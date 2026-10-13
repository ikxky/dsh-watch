# dsh-watch

DeepSeek Harness 的独立公开长期研究项目，服务于企业 Agent 平台与个人助理的技术判断。这里保存可追溯的产品、架构与版本研究，不承载业务源码、运行环境或上游贡献。

当前基线：**v0.2.1-alpha.2**，官方 tag `dsh-v0.2.1-alpha.2`，最近核查日期 **2026-10-13**。已登记26次公开发布，全部为 prerelease；完成五个历史专题、插件演进和36项能力地图。本轮仅进行官方资料阅读、固定提交源码检查、版本差异与发行归档静态核验；未安装或运行 dsh，未调用模型，也未验证性能、安全性或端到端功能。

| 从哪里开始 | 内容 |
|---|---|
| [CAPABILITY-MAP.md](CAPABILITY-MAP.md) | 唯一逐项能力地图：支持状态、实现归属、证据程度与下一步问题 |
| [OVERVIEW.md](OVERVIEW.md) | 六个维度的当前产品、架构、能力与适用边界 |
| [PLUGINS.md](PLUGINS.md) | 默认组成、随附关闭／按需安装的区分、插件演进与发行包证据 |
| [EVOLUTION.md](EVOLUTION.md) | 完整发布索引、六维演进、历史迁移成本与反复出现的主题 |
| [FINDINGS.md](FINDINGS.md) | 少量关键问题与机会，以及证据和后续验证条件 |
| [本次版本增量](releases/v0.2.1-alpha.2.md) | 相对上一已发布版本 alpha.1 的实质变化 |
| [TRACKING.md](TRACKING.md) | 来源、版本登记、检查状态、每周机制及下一步 |

当前判断以**借鉴、验证、观察**为主：事件日志与插件组合值得研究；完成语义、日志外发与权限边界需要单独验证。当前不采用 dsh 作为生产或多租户运行时。官方明确将其定位为尚未安全审计的开发者预览，不能把沙箱或审批视为隔离保证。[版本 README](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/README.zh.md)、[安全说明](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/SAFETY.zh.md)

官方入口：[DeepSeek Harness 产品页](https://www.deepseek.com/en/harness/)、[源码仓库](https://github.com/deepseek-ai/deepseek-harness)、[完整 Releases 列表](https://github.com/deepseek-ai/deepseek-harness/releases)、[npm 包](https://www.npmjs.com/package/@deepseek-ai/dsh)。

历史专题：[最早可见基线](releases/v0.1.0-rc.7.md) → [Session 持久化边界](releases/v0.1.3-alpha.1.md) → [执行环境与默认值](releases/v0.1.6-alpha.1.md) → [0.2 交付与可靠性](releases/v0.2.0-rc.2.md) → [插件产品化](releases/v0.2.1-alpha.1.md)。

研究采用轻量治理：每周检查，有实质变化才形成增量结论；没有变化仅更新检查状态并保持通知静默。每周跟踪已启用，周期与范围见 [TRACKING.md](TRACKING.md)。
