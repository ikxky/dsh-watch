# dsh-watch

DeepSeek Harness 的独立公开长期研究项目，服务于企业 Agent 平台与个人助理的技术判断。这里保存可追溯的产品、架构与版本研究，不承载业务源码、运行环境或上游贡献。

当前基线：**v0.2.1-alpha.2**，官方 tag `dsh-v0.2.1-alpha.2`，检查日期 **2026-10-12**。本轮仅进行官方资料阅读、固定提交源码检查和版本差异分析；未安装或运行 dsh，未调用模型，也未验证性能、安全性或端到端功能。

| 从哪里开始 | 内容 |
|---|---|
| [OVERVIEW.md](OVERVIEW.md) | 六个维度的当前产品、架构、能力与适用边界 |
| [FINDINGS.md](FINDINGS.md) | 少量关键问题与机会，以及证据和后续验证条件 |
| [本次版本增量](releases/v0.2.1-alpha.2.md) | 相对上一已发布版本 alpha.1 的实质变化 |
| [TRACKING.md](TRACKING.md) | 来源、版本登记、检查状态、每周机制及下一步 |

当前判断以**借鉴、验证、观察**为主：事件日志与插件组合值得研究；完成语义、日志外发与权限边界需要单独验证。当前不采用 dsh 作为生产或多租户运行时。官方明确将其定位为尚未安全审计的开发者预览，不能把沙箱或审批视为隔离保证。[版本 README](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/README.zh.md)、[安全说明](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/SAFETY.zh.md)

官方入口：[DeepSeek Harness 产品页](https://www.deepseek.com/en/harness/)、[源码仓库](https://github.com/deepseek-ai/deepseek-harness)、[完整 Releases 列表](https://github.com/deepseek-ai/deepseek-harness/releases)、[npm 包](https://www.npmjs.com/package/@deepseek-ai/dsh)。

研究采用轻量治理：每周检查，有实质变化才形成增量结论；没有变化仅更新检查状态并保持通知静默。每周跟踪已启用，周期与范围见 [TRACKING.md](TRACKING.md)。
