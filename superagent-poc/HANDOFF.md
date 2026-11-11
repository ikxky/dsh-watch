# Superagent PoC 同事接手执行手册

[返回唯一入口 README](README.md) · [代码层实施说明](IMPLEMENTATION.md) · [本轮预检记录](PRECHECK.md)

更新：2026-11-11。先完成本页的离线检查，再按代码实施说明开发缺失部分。**本次交付不是已安装的 Superagent 服务。**

## 1. 五分钟看清现状

| 层次 | 已有内容 | 当前结论 |
|---|---|---|
| 官方固定版本 | `deepseek-ai/dsh-superagent-prototype@8c32a9dc5d72c033816c6a8110b37f40cf94fba4` 的源码审阅 | 有 Engine、Intake、Ticket/Worker、Source、持久化 effects/outbox 等机制；未在本项目运行 |
| 旧机制语料 | `corpus/`，41条消息/控制事件，10批，38个唯一源ID | 生成、校验、单消息白名单投影已实现；不是连续注入器 |
| 四业务语料 | `business-corpus/`，48条业务投递，47个唯一源消息，16批，15附件 | 固定14天窗口；时点 stage、200/304/503 来源查询与材料校验已实现 |
| 本轮新增 | 本手册、代码任务/接口说明、相对链接检查器、预检记录 | 可以复核材料并据此开发；示例 TypeScript 不等于已编译实现 |
| 待开发 | Replay Source、连续 controller、模型/Worker 观测、业务 watch、record-only 收件箱、OS 隔离 | 尚无可启动的完整 PoC；不能声称持续执行、业务通过率或性能已测 |

两套语料独立使用，不合并统计。旧集包含 tool/worker/fault 控制事件，不能把41条全当用户消息；新集每臂严格增量回放还有1条 `media_ready`，它不是新的用户请求。原始与预解析两臂不是两个不同业务世界，后者仅用于定位媒体链路差异。

## 2. 根路径与阅读顺序

**文档、目录树及命令所说的“项目根目录”均指 `superagent-poc/`，不是 dsh-watch 仓库根、系统 `/` 或官方原型目录。** ZIP 解压后进入其中的 `superagent-poc/`；Git checkout 用户从 dsh-watch 进入该子目录。

```sh
cd superagent-poc
pwd
# 应能看到 README.md、HANDOFF.md、corpus/、business-corpus/
```

除明确标注“官方源码目录”的命令外，下面所有命令都在此根目录执行。文内如 `business-corpus/replay.py` 也是根相对路径。

Markdown **链接按当前文档位置相对解析**：根文档用 `business-corpus/README.md`，该子目录回入口用 `../README.md`。它们解析后必须仍在 `superagent-poc/` 内。不要写 `/PLAN.md` 或 `superagent-poc/PLAN.md` 作为跨文档链接，前者会变成网站/文件系统根，后者在本目录重复一层。项目外的 DSH 研究/官方源码使用固定版本 HTTPS 链接，离线不保证可打开。

推荐顺序：

1. **本手册**：现状、立即可跑的命令、接手分工及交付物。
2. [IMPLEMENTATION.md](IMPLEMENTATION.md)：接口、数据结构、Source 挂接、时钟、watch、隔离、测试断言和开发顺序。
3. [BUSINESS-REPLAY-PLAN.md](BUSINESS-REPLAY-PLAN.md)：业务情境、时序和评估逻辑；[业务语料说明](business-corpus/README.md)查看材料字段。
4. [PLAN.md](PLAN.md)：原型证据、完整实验矩阵、B0/B1/B2 归因、真实渠道适配限制；[旧语料说明](corpus/README.md)查机制用例。
5. [PRECHECK.md](PRECHECK.md)：本轮实际执行记录；[历史业务 QA](business-corpus/QA.md)是2026-11-10材料检查，勿混作本轮实测。

## 3. 现在就能做的离线检查

已有 fixture 可直接用，**不需要重新生成，不需要模型 Key，不需要 GitHub/飞书账号**。Python 3.12；validator 的媒体依赖见两份语料说明。本轮版本/结果以预检记录为准。缺依赖时如实记 BLOCKED，不能忽略失败。

```sh
# 标准库检查：全部项目内 Markdown 相对链接
python scripts/check_links.py
# 这两项校验的是材料，不启动 Superagent
python corpus/validate.py
python business-corpus/validate.py

# 新建临时输出，保存已有证据，不复用 stage 目录
RUN_DIR="$(mktemp -d)"
python business-corpus/replay.py stage \
  --until 2026-11-16T09:02:11+08:00 --arm raw --out "$RUN_DIR/stage-01"
python business-corpus/replay.py stage \
  --after 2026-11-16T09:02:11+08:00 \
  --until 2026-11-16T09:02:31+08:00 --arm raw --out "$RUN_DIR/stage-02"
python business-corpus/replay.py source \
  --at 2026-11-18T16:00:00+08:00 --source deepseek-plugin
python business-corpus/replay.py source \
  --at 2026-11-19T09:00:00+08:00 --source deepseek-plugin
# 旧集只投影 message；事件ID不是生产去重键
python corpus/project_event.py corpus/generated/events.raw.jsonl --event e01
```

以上 stage 分别应为4条、2条输入；source 示例应分别为503、200。实际 CLI 是 `--after`，没有 `--since`。`--fixture` 是顶层选项，若使用须放在 `stage`/`source` 前。完整语料生成器只在独立临时副本运行，不覆盖已提交 fixture；跨依赖版本不保证媒体字节相同。

`stage` 只输出时点材料：`inbox.jsonl`、`clock.json`、`identity-map.json`、`sources/` 快照及当前 raw 附件。它没有调用 receive、推进 Worker、运行 watch 或发通知。输出整个目录也不是最终安全挂载配置：来源快照应藏在可信只读工具之后，不能因 stage 有文件就让模型自由遍历所有源。

## 4. 按这个顺序开发，逐关交接

负责人由接手团队分配，以下是职责，不代表任何人已承诺工期。

| 关卡 | 建议责任 | 必须提交的产物 | 出口标准 |
|---|---|---|---|
| G0 材料基线 | 测试/评审 | 源码SHA、fixture hash、依赖版本、本轮命令日志 | 两个validator及相对链接通过；任何失败保留 |
| G1 core契约 | 框架工程 | 官方测试树内的 core harness、转换器、去重/权限单测 | 替身端口、注入时钟；不调用模型，不产生外部副作用；不称Runtime通过 |
| G2 Source可加载 | 集成工程 | 注册/卸载、构建导出、作用域/身份配置验证 | 分清 stub host 与真实Runtime；无法过setup时停在BLOCKED，先解决授权/环境 |
| G3 连续回放 | 测试工程 | controller、分臂目录、事件接收日志、受控来源工具、故障屏障 | 不泄漏未来/答案；按到达顺序；有重投恢复、媒体pending→ready证据 |
| G4 业务对照 | 业务评审+工程 | 原答、事实/产物版本、采用证据、逐项评分 | 取得模型/运行权限后再执行；B0/B1/B2和raw/parsed分开；无严重越权 |
| G5 真实输入 | 渠道工程 | 只读渠道适配、游标恢复、映射差异报告 | 另行批准具体测试账号/群和范围；对外发送仍单独限制 |

优先 G1，不要先做全功能UI。遇到挂接只能修改核心/默认prompt/业务policy时，记录为B2独立变体；不要覆盖B0原样目录。完整Runtime的GitHub setup与agent push权限门槛仍在，不因输入名叫replay而消失。

## 5. 运行证据与停止条件

每次未来运行使用独立 `run_id`，记录配置/源码/材料hash、实验标签、raw/parsed、业务时间、单调运行时间、原事件ID、Trigger ID、接收结果、实际工具读取、Worker采用证据、产物hash、拟通知回读和评分。详细建议结构在实施说明中。不要把模型说“已完成”当产物存在，不把“receive成功”当Worker已采用。

结果枚举固定为：`PASS`、`FAIL`、`NOT_RUN`、`BLOCKED`、`UNSUPPORTED`、`UNOBSERVABLE`。未运行不填0%或PASS；性能时钟不用压缩后的业务时钟。一个固定剧本重复100次不等于100个独立样本。

出现未来/评分答案泄漏、真实外发/付款/生产写入尝试、身份被文本篡改、停止后继续动作、结果未知时盲重试，立即保留证据并停止相应运行。`observe` 不关闭显式任务，不能替代OS/网络/工具层隔离。

本包含公开合成评分文件 `corpus/private/expected.json` 和 `business-corpus/review-only/checkpoints.json`，为了同事评审而保留；名称里的 private/review-only 不是秘密，也不是访问控制。它们不得挂给被测模型。本包不包含真实账号、群记录、密钥或运行数据库。
