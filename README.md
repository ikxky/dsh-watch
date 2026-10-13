# dsh-watch

DeepSeek Harness 的独立公开长期研究项目。我们关注一个产品问题：**把工作交给 Agent 之后，用户能否看懂过程、保持控制、拿到成果，并在出错后接着做。** 研究服务于企业 Agent 平台与个人助理的选型和设计，不承载业务源码或运行环境。

dsh 提供工作区、会话和工具执行，也能供其他应用调用。当前值得借鉴和验证的是委派、监督、续接与插件扩展；生产可靠性、组织权限、成果保留和整项任务费用仍需单独确认。官方仍将其标为未经安全审计的开发者预览，本项目暂无生产运行时采用结论。[官方说明](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/README.zh.md)、[安全声明](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/SAFETY.zh.md)

## 从产品问题开始阅读

1. **[它适合承担什么工作](OVERVIEW.md)**：先看产品定位、适合场景、原生与上层平台的分工，以及当前采用判断。
2. **[一项任务怎样从委派走到验收](CAPABILITY-MAP.md)**：沿入口、进度、人工决定、资源、交付、续接、恢复与协作阅读；36项能力的版本与证据可按需展开。
3. **[插件能增加哪些能力](PLUGINS.md)**：按找回历史、持续工作、协作、输入阅读和外部系统等需要选择；默认配置和发行证据放在后半部。
4. **[哪些发现会改变接入判断](FINDINGS.md)**：聚焦日志外发、完成语义、恢复、权限与版本一致性。

需要追溯版本时，读[历史演进](EVOLUTION.md)和[当前版本增量](releases/v0.2.1-alpha.2.md)；来源登记、检查状态与每周规则见[跟踪记录](TRACKING.md)。历史专题保留各版本当时的判断，不用当前能力倒推过去。

## 这份研究目前确认到哪里

当前基线为 **v0.2.1-alpha.2**，官方 tag `dsh-v0.2.1-alpha.2`；最近资料核查 **2026-10-13**。已登记26次公开发布，均为预发布；完成五个历史专题、当前增量、插件研究和能力地图。

所有结论来自公开官方资料、固定提交源码、版本比较与发行归档静态核验。没有安装或运行 dsh、调用模型，或实测性能、安全与任务效果。本次按产品阅读路径重构文档，保留既有能力 ID、证据及未确认项。

每周跟踪已启用，目标为周一北京时间上午9点附近。有实质变化才更新判断并报告；没有变化只登记检查状态、保持通知静默。完整规则见 [TRACKING](TRACKING.md)。

官方入口：[产品页](https://www.deepseek.com/en/harness/)、[源码仓库](https://github.com/deepseek-ai/deepseek-harness)、[完整 Releases](https://github.com/deepseek-ai/deepseek-harness/releases)、[npm](https://www.npmjs.com/package/@deepseek-ai/dsh)。
