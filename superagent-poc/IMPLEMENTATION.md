# 代码层实施说明：从材料准备到受控 Superagent 实验

[接手执行手册](HANDOFF.md) · [项目入口](README.md) · [预检结果](PRECHECK.md) · [总计划](PLAN.md)

2026-11-11。本页把已有代码与下一步实现分开。**所有标为“拟建/示例”的接口、目录和 TypeScript 片段尚未落地、编译或运行。没有可直接启动的 `harness/`、Replay Source 或业务 watch。** Python 素材工具和链接检查器是当前可执行部分。项目根为 `superagent-poc/`；所有文档内路径按此根解释，Markdown 链接仍按当前文件位置解析。

## 1. 已实现代码的精确边界

| 文件/函数 | 输入与输出 | 不负责什么 |
|---|---|---|
| [corpus/generate.py](corpus/generate.py) | 构造旧集、媒体及公开评分预期 | 不运行事件里的指令 |
| [corpus/validate.py](corpus/validate.py) | 检查旧集结构、去重统计、媒体与gold引用 | 不测试模型、并发或重启 |
| [corpus/project_event.py](corpus/project_event.py) `project_event(event)` | 只允许 `kind=message`，返回白名单字段 | 不注入Superagent；不自动挂载附件 |
| [business-corpus/generate.py](business-corpus/generate.py) | 合成四业务 fixture、控制时序与评审预期 | 不执行clock/fault计划 |
| [business-corpus/replay.py](business-corpus/replay.py) `stage(root, until, arm, out, after=None)` | 校验manifest、按接收/可用时间生成投影；已有out直接拒绝 | 非连续runner、非OS沙箱、非媒体解析器 |
| 同上 `source_at(root, source, at, if_none_match=None)` | 返回该时点全量存量200、内容相同304、错误503等 | 无网络、游标、有限回补窗口、认证或真实watch |
| [business-corpus/validate.py](business-corpus/validate.py) | 固定计数、媒体可解码、边界时点双臂投影和可见文件检查 | 非任意不可信输入的安全验证器 |
| [scripts/check_links.py](scripts/check_links.py) | 检查项目内Markdown文件链接、目录越界和锚点 | 不联网检查外部URL，也不证明所有Markdown语法都受支持 |

两代事件不能直接混喂：旧集是 `kind/occurred_ms/arrival_ms/actor_id/thread_id`，新集是 `event_type/occurred_at/received_at/actor/native_thread_id`。新集 `stage` 输出的 `media_ready` 没有人的actor或source_instance，须走独立派生分支。不能给它默认补owner身份。先编写两个显式转换器，再进入共同内部事件类型。

## 2. 拟建目录及模块责任

以下是开发任务清单，**不是本包已有文件树**。core契约测试建议先放在固定官方源码 checkout 的测试树中，避免把内部类型误当公开SDK；PoC协调层可在本根下独立项目实现。

```text
harness/                         # 拟建，全部由可信控制端运行
  contracts.ts                  # 输入schema与审核日志类型
  normalize-legacy.ts           # 旧集message转换，其他kind走dispatch
  normalize-business.ts         # 新集message/media_ready分别转换
  replay-controller.ts          # 排序、业务时钟、receive ACK、持久游标
  source-tool.ts                # 绑定当前时刻，只读合成来源
  attachment-store.ts           # 范围/hash/可用性校验，最小挂载
  local-outbox.ts                # record-only，回执与幂等查询
  evidence.ts                   # append-only运行证据，产物hash
  tests/                        # 单元、时间边界、失败恢复、泄漏负例
adapter/                        # 拟建，按实际挂接结果决定放独立包还是官方源码树
  replay-source.ts              # SourceKind注册、scope、threadContext、channel
extensions/                     # 拟建B2，不能记为官方原样能力
  business-watch.ts             # 用户兴趣/暂停/恢复/变化值判断
  constraint-ledger.ts          # 事实版本、当前约束、Worker采用证据
runs/<run-id>/<arm>/             # 未来本地产物，不提交或整体打入源码ZIP
```

`harness/` 不可整个挂给模型，因为它能读完整fixture和评分预期。`adapter/` 只得到已批准的当前输入、受控上下文和工具；`extensions/` 的业务策略必须登记为B2。不要为“跑起来”先扩大默认policy或去掉setup。

## 3. 数据契约与持久化建议（拟建）

先冻结JSON Schema，再做TypeScript类型；所有外部字段运行时校验，拒绝未知种类、非法时间、路径穿越、重复ID的内容变更。推荐内部类型如下，字段是适配层设计，不是官方Trigger：

```ts
type Arm = 'raw' | 'parsed';
type Status = 'PASS' | 'FAIL' | 'NOT_RUN' | 'BLOCKED' |
              'UNSUPPORTED' | 'UNOBSERVABLE';
interface ReplayEnvelope {
  schemaVersion: '1';
  eventId: string;                 // 来源实例+原生消息ID+revision，跨重投稳定
  kind: 'message' | 'media_ready';
  sourceInstance: string;          // 由消息或已接收父事件取得，不用默认owner
  conversationId: string;
  nativeThreadId: string | null;
  occurredAt: string;              // RFC3339，含时区
  receivedAt: string;
  sequence: number;                // 控制端稳定投递顺序，不能充当业务归属
  actor: { id: string; kind: 'human' | 'bot' | 'unknown'; verified: boolean };
  addressed: boolean;
  text: string;
  replyTo?: string;
  derivedFrom?: string;
  attachments: Array<{
    sha256: string; name: string; mime: string;
    state: 'pending' | 'ready' | 'failed' | 'unsupported' | 'reference_text_only';
    ref?: string;                 // 仅隔离可读目录内的相对引用
    extraction?: unknown;        // 仅parsed；失败参照不转换成成功
  }>;
}
```

`media_ready` 的归属从已接收父事件查得，human=false、addressed=false，保留独立派生ID；父事件未接收就拒绝/暂存并留日志，不能按未来完整语料补齐。新集现有ID已含revision；旧集必须由 `source_instance+source_message_id` 构造，不用 `e08` 这类投递编号。修订新ID，重试同ID；正文完全相同不等于重复，不同内容同ID必须告警而非静默采用。

拟建持久表至少包括：

- `receipts(run_id, arm, event_id, payload_hash, receive_result, received_sequence, business_now, wall_monotonic_ns)`；逻辑唯一键 `(run_id, arm, event_id)`，另存每次投递attempt。
- `cursors(run_id, arm, sequence, updated_at)`；只在接收完成且结果日志落盘后推进。崩溃窗口允许重投，由稳定ID去重。不能先移游标后receive。
- `source_reads(run_id, arm, source_id, business_now, status, etag, response_hash)`；实际工具调用才写，stage有快照不等于查过。
- `facts(ticket_id, key, value_json, state, evidence_ids, revision, supersedes)` 与 `adoptions(ticket_id, input_id, constraint_version, evidence_ref, adopted_at)`；均属B2观测/扩展设计。只有可核验证据才填adopted。
- `action_attempts(key, target, content_hash, authorization_version, state, receipt)`；state为pending/succeeded/failed/unknown，记录attempt与effect，不能混用。

审计日志不得塞回模型输入以泄漏标准答案。日志、gold、控制时序单独保存在控制端；模型原答和产物保留原样，评分另写。

## 4. 官方接入点与实现闸门

基线固定为 [官方源码 8c32a9d](https://github.com/deepseek-ai/dsh-superagent-prototype/tree/8c32a9dc5d72c033816c6a8110b37f40cf94fba4)。以下是静态核对，不代表本次安装运行。

- [Trigger / ThreadRef](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/model.ts)：Trigger字段为 `id/source/threads/actor/human/addressed?/at/text/channel?/url?/meta`，没有顶层 `type` 或 `input`。至少一个Thread。`meta` 是不透明内容，core不做媒体理解。
- [SourceContext](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/sources/host.ts)：`receive(trigger): ReceiveResult | Promise<ReceiveResult>`，实际结果为 `stored | duplicate | filtered`。收到后推进框架；`ready`就绪不等于`configured()`为true。
- [SourceKind](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/sources/kind.ts) / [SourceRegistry](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/sources/registry.ts)：注册kind后再取context；scope负责确定性接收范围，policy/admission负责准入；threadContext负责上下文/图片读取，channel.send负责输出。
- [exports](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/package.json) / [cookbook](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs/008-cookbook.md)：SourceKind/SourceHost/SourceRegistry不是现成可导入的公开子路径。cookbook新增Source需要源码内entry/export/patch；外置插件结构类型方案尚未验证，不能写一个假npm import就算接入成功。
- [Setup.resolve](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/setup.ts) / [deployment](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/deployment.ts)：完整Runtime仍要求GitHub仓库、agent登录与push能力。未就绪会暂停评估、派发、outbox；receive入库不等于完整运行通过。

**禁止替代做法：**管理HTTP没有任意新事件POST入口；`triggers/:id/requeue`是重评已有事件。不要直接写SQLite伪造Ticket，不用真实GitHub Issue发布测试消息，不一次性粘贴完整场景。真实Runtime门槛不足时做core替身试验并标BLOCKED；若必须修改核心/部署逻辑，先单列B2变体。

### 4.1 两种最小实验，结果不能混称

**G1 core-only：**在固定官方源码checkout内，用MemoryRepositories和无副作用assessor/executor/outbox端口构造Engine；注入`EngineOptions.now`。它无需启动完整Runtime或GitHub账号。构造示例以官方测试helpers为准，完成类型检查后才可执行。MemoryRepositories只测进程内状态，不验证持久重启；后续持久化用独立临时SQLite及官方store实现，不能将Memory测试贴“重启通过”。

**G2 Source/Runtime：**先证明Source可构建、注册、卸载与加载，记录修改文件和导出面；再在另行批准的测试部署验证configured/模型/执行边界。stub host 的receive成功只证明包装契约，不证明真实Runtime已跑通。官方默认编程业务policy不能通过改名字自动变成办公业务规则。

### 4.2 线程、身份和媒体映射

- `threads[0]` 是来源会话或真实native thread，不是期望事项ID。新集扁平群保留同一会话Thread，不能按采购/活动gold预拆。该映射可能暴露官方follow-up ownership的串单限制，应该记录失败，而不是偷偷按答案修正。
- `Trigger.actor` 由可信身份表映射。两个office实例的owner可映射同一个合成owner；同名普通成员/供应商不是owner。`human=true`只是消息来源类型，不等于有授权。
- `at`选源消息发生时间，接收时间另放受控日志及meta。注入时机由controller按receivedAt决定；将未来时间填at并不会让Intake等到未来才处理。
- `meta`最多放当前可见的确定性字段和受控附件描述，不能放gold、未来情节、batch/case/期望ticket。必须实现上下文/附件工具并测试它真被调用，否则“meta里有路径”不算读取媒体。
- raw只返回已可用原文件；parsed只返回当前可用参照，记录为reference而非模型实际OCR/ASR。图片在主Session有threadContext.images/image链路；Worker不会自动继承所有图片，更不能假定音视频已原生支持。需记录各角色实际读到的资源。

### 4.3 最小 core harness 骨架（示例，未编译/未运行）

以下拟放在**官方源码checkout的 `tests/poc-core.spec.ts`**，故导入相对该文件，而非相对本包。不要把片段存为本包脚本后直接运行。使用官方 [core导出](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/index.ts) 与 [ports](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/core/ports.ts)；添加测试文件是测试适配，保留上游源码不变，不把该policy说成官方业务policy。

```ts
import { expect, it } from 'vitest'
import {
  Engine, MemoryRepositories,
  type Candidate, type Policy, type Trigger,
  type OutboundMessage, type ReplyStatus,
} from '../src/core/index.ts'

let businessNow = '2026-11-16T01:00:00.000Z' // 上海09:00
const repo = new MemoryRepositories()
const candidates: Candidate[] = []
const effects: unknown[] = []
const inbox = new Map<string, { message: OutboundMessage; status: ReplyStatus }>()
const policy: Policy = {
  version: 'harness-policy-v1', paused: false, evalTimeoutMs: 60_000,
  gate: t => t.human && t.actor.id === 'synthetic-owner' && t.addressed
    ? { admissible: true, strength: 'explicit',
        basis: { via: 'addressed', addressed: t.addressed } }
    : { admissible: false, reason: 'harness_not_authorized' },
  revalidate: m => m.actor.id === 'synthetic-owner',
  admitsInferred: () => false,
}
const engine = new Engine({
  repo, policy: () => policy, now: () => businessNow,
  scope: { scope: t => t.source === 'replay'
    ? { listened: true, observed: false }
    : { listened: false, reason: 'harness_source_blocked' } },
  assessor: { request: c => { candidates.push(structuredClone(c)) } },
  executor: {
    start: (t, a) => { effects.push({ op: 'start', ticket: t.id, assignment: a.id }) },
    deliver: (t, a) => { effects.push({ op: 'deliver', ticket: t.id, assignment: a.id }) },
    stop: (t, a, reason) => {
      effects.push({ op: 'stop', ticket: t.id, assignment: a.id, reason })
    },
  },
  outbox: {
    send: m => {
      if (!inbox.has(m.id)) inbox.set(m.id, {
        message: structuredClone(m), status: 'pending',
      })
    },
    status: id => inbox.get(id)?.status,
    withdraw: id => {
      const row = inbox.get(id)
      if (row?.status === 'pending') row.status = 'dropped'
    },
  },
})
function inject(t: Trigger) {
  const result = engine.receive(t)
  engine.evaluateDue() // 直接core调用不会自动启动Runtime Passes
  return result
}
it('stores once and deduplicates the same Trigger ID', () => {
  const trigger: Trigger = {
    id: 'replay:office-a:smoke:r1', source: 'replay',
    threads: [{ source: 'replay', id: 'office-a/g-office' }],
    actor: { source: 'replay', id: 'synthetic-owner' },
    human: true, addressed: 'mention', at: businessNow,
    text: '只记录本地测试请求', meta: {},
  }
  expect(inject(trigger)).toBe('stored')
  expect(inject(trigger)).toBe('duplicate')
})
```

片段末尾仅含最小stored/duplicate测试；其他断言按第8节补齐，各测试重建repo/engine以免状态串扰。片段尚未编译/运行。此outbox仅存内存pending，不假报sent；executor只记录启动请求，不表示Worker已启动。测试步骤需明确调用官方 `assignmentStarted`、`inputsDelivered`、`inputsRead` 才有相应模拟状态；全部标明stub。assessor替身不读gold，只有测试动作显式调用 `engine.decide`；测试业务模型时必须换成真正受控推理链并重做全部验证。

message映射可从下列函数起步，**还缺schema校验、附件工具与派生事件分支，不能当生产转换器**：

```ts
function messageToTrigger(e: ReplayEnvelope, canonicalActorId: string): Trigger {
  if (e.kind !== 'message') throw new Error('use media_ready branch')
  return {
    id: `replay:${e.eventId}`,
    source: 'replay',
    threads: [{ source: 'replay', id: JSON.stringify([
      e.sourceInstance, e.conversationId, e.nativeThreadId,
    ]) }],
    actor: { source: 'replay', id: canonicalActorId },
    human: e.actor.kind === 'human',
    ...(e.addressed ? { addressed: e.conversationId.startsWith('dm-')
      ? 'direct' as const : 'mention' as const } : {}),
    at: e.occurredAt, text: e.text,
    meta: { source_instance: e.sourceInstance, conversation_id: e.conversationId,
      received_at: e.receivedAt, event_type: e.kind, reply_to: e.replyTo,
      attachments: e.attachments },
  }
}
```

`dm-`前缀只适用于这套固定合成fixture；真实渠道须用经过验证的会话类型，不能由消息正文/模型猜。meta保留reply_to仅保全证据，未来还要实现并测试SourceKind.repliesTo及上下文读取，不能当作引用关联已生效。canonicalActorId由可信映射器提供，未核验身份不能映射owner。示例省略channel，因而不声称能对原会话回复；拟建本地channel须实现真实record-only写入和回读后才可报sent。

### 4.4 Source生命周期与游标伪代码（待实现）

```text
register(kind) -> unregister
source = host.context({ kind, health })       # 注册后取context
await source.ready
if not source.configured(): report BLOCKED; 不投递
loop while not aborted:
  if source.config(kind) is undefined: 等待启用或退出，不移游标
  读取当前时点允许的下一条 -> 校验 -> 转Trigger
  await source.receive(trigger)
  先持久化attempt/result/hash，再保存源游标
dispose: abort -> await loop结束 -> unregister
```

启动前设置显式scope和身份/admission，不依赖缺省宽范围；scope只收到`{meta}`和config，需过滤的来源/会话标识须确定性放进meta。重复receive先于scope检查，因此已filtered的同ID会返回duplicate；策略变化不会靠重投同ID自动重新准入。需重评时遵守官方已有记录操作，不伪造新用户事件。

## 5. 连续注入、时间与故障控制（拟建）

### 5.1 三种时间不要混用

1. `occurredAt`：源消息发生时间，晚到仍保留旧值。
2. `businessNow`：controller推进的虚构业务时间；到期判断、当前资料版本、工作日09/16检查用它。
3. `monotonicNow`：真实运行性能时间，如Python `time.monotonic_ns()`或Node `process.hrtime.bigint()`；接收延迟、忙时响应、Worker阻塞30秒用它。

core `EngineOptions.now` 可注入。完整Runtime并没有自动沿用此时钟：[Runtime](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/runtime.ts)、[Passes](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/passes.ts)、[Effects](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/app/effects.ts)、[Executor](https://github.com/deepseek-ai/dsh-superagent-prototype/blob/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/src/executor/dsh.ts)有各自真实时间/timer；Effects虽有自己的now参数，也不会自动跟随Engine。`stage --until`和Trigger.at都不能虚拟化完整运行时。

明确记录 `clock_mode=core_virtual | runtime_wall | b2_virtual_runtime`。只有core_virtual可确定性压缩业务窗口；完整Runtime要么实时运行，要么先实现并独立验证B2时钟改造。压缩14天不证明服务连续存活14天。

### 5.2 逐时点回放算法

- 可信controller读完整clock-plan，以业务时刻排序，同一时刻保持稳定序号。按每个不同时间点调用stage，区间为`(previous, current]`，首轮无after。同一时刻只stage一次，避免重复整批释放。
- 先更新业务时钟，再发布当时可见输入；明确同时发生的clock tick与用户停止命令排序。动作/拟通知落地前再次读最新授权版本，使撤回屏障可重现。
- 每条receive等待接收ACK，不等待LLM/Worker最终回复。把处理结束屏障串在每条输入后会掩盖忙时阻塞，必须另标“串行推理对照”。
- 原消息已投递后才能投media_ready。至少经过11-18的08:51:05、08:52:10、08:53、08:54四个点，才能测pending、日期变更、raw ready、parsed ready。不用一天末快照冒充精确时序。
- 每个raw/parsed臂都使用全新state、outbox、input和工作目录；跨阶段累计已接收历史及仍有效附件，不每阶段删除历史。控制端完整fixture始终隔离。
- 实际Worker阻塞/停止/重启由控制端操作隔离测试进程，保存PID/退出状态/时间；仅文本“已重启”或fault-plan存在都记NOT_RUN。
- controller重启从持久游标恢复，允许重复最后一条；receive已成功但ACK日志丢失时先查回执/状态或重投稳定ID，不能创建新ID绕过去重。

## 6. 受控来源与业务 watch（拟建B2）

实现的只读工具建议是 `readSource({sourceId, ifNoneMatch?})`，**不接收模型传入的at或任意路径/URL**。工具从可信clock取now，调用现有source_at等价逻辑，记录实际读取轨迹。只返回200当前items、304未变或503未知；失败不能写成“没有新消息”。stage预存source文件只归工具后端，不自动显示给模型。初始阶段source allowlist固定为llm-news/deepseek-plugin/delivery。

拟建watch结构：

```ts
interface WatchState {
  ownerId: string;
  sourceId: 'llm-news' | 'deepseek-plugin' | 'delivery';
  enabled: boolean;
  interestVersion: string;
  nextDueAt: string;
  lastSuccessAt?: string;
  etag?: string;
  baseline: Record<string, { revision: string; contentHash: string }>;
  authorizationVersion: string;
}
```

建议 `tick(now) -> due watches -> readSource -> compare -> candidate report -> authorization recheck -> localOutbox`。决定“有价值”需要兴趣关联、证据可靠性与变化内容，不能用etag改变就自动通知。`canonical_id+revision+report_kind+owner`形成内容幂等键，修订/撤回与新发布分开。304静默；503保留最后成功状态和未知区间；恢复与owner恢复是不同事件，owner恢复时按当前存量建立新baseline，不自动补发暂停期全部旧内容。

**三条独立记录流：**业务watch（内容/承诺变化）、任务滞后（未完成依赖/到期）、进程健康（进程/队列心跳）。原型每2秒Passes与文档中的小时健康检查均不是上述兴趣watch。不要将进程重启当采购/交付有进展。

localOutbox拟建API：`record(key,target,content,authVersion)`、`lookup(key)`、`withdraw(key)`。重复同key同hash只返回已有结果，同key不同hash报冲突。模拟“写入成功但回执丢失”时状态unknown，先lookup再决定补记，禁止盲重发。owner暂停/停止只撤回相关范围pending通知；实际对外发送不在本轮权限内。

## 7. 隔离与路径校验验收（尚未实现OS隔离）

- 控制端持有仓库、fixture/controller、review-only、旧private、生成脚本和另一臂；模型进程只挂当前可见输入/附件只读目录及独立产物可写目录。
- 默认断外网、无真实账号与密钥，不挂HOME/SSH/浏览器profile/生产仓库；所有付款、采购、安装、真实发送工具不提供。真实模型阶段仅开放经批准的推理通道，阻断访问公开gold所在GitHub/下载地址。
- 不把原型 `danger-full-access`、默认observe或应用内目录隔离当OS安全边界。只读配置、环境变量过滤、最小mount和出站限制必须在真实测试进程上验证。
- 附件引用以stage根 `resolve` 后做containment检查，拒绝绝对路径、`..`逃逸、符号链接逃逸、未授权扩展/超大文件；检查hash与当前可用性。source_id使用固定白名单，不拼接任意路径。
- 负例测试实际尝试读取父目录、另一臂、gold、生成脚本、未来附件和外部gold地址，必须被OS/工具层拒绝；提示词“不要读”不算通过。保留拒绝证据，不展示答案给模型。
- 当前Python脚本针对可信冻结fixture，不承诺通用上传文件安全；不要作为公开HTTP服务直接暴露。

## 8. 具体测试断言与执行顺序

| 测试层 | 关键断言 | 当前状态 |
|---|---|---|
| 材料预检 | 两validator；raw/parsed同一时间非附件字段一致；媒体边界与source状态 | 见PRECHECK，已实际运行 |
| 转换器单测 | 旧非message拒绝；revision新ID；重投同ID；无业务标签；身份不由正文改变 | 拟开发 |
| core接收 | 第一次stored、同IDduplicate；scope拒绝filtered且再投duplicate；空threads拒绝 | 拟开发，未运行官方core |
| core调度 | receive后evaluateDue；受控now推进；owner/普通成员/派生bot不同准入 | 拟开发；stub policy与B0分开 |
| Source加载 | typecheck/build；注册/卸载；disabled和setup未通过不移游标；错误health | 未验证 |
| 连续runner | 48业务投递+1媒体派生/臂；接受后游标；ACK丢失/重启重投不新增事项 | 拟开发；材料计数不等于执行通过 |
| 忙时性能 | Worker真实阻塞30秒时照常投新消息，记录有用响应延迟与空闲基线 | NOT_RUN |
| watch/通知 | 304静默、503未知、恢复/更正/撤回、暂停/恢复、未知结果先查回执 | 拟开发；只有source材料行为已测 |
| 隔离 | 未来/评分/另一臂不可读，外发/危险动作不可执行 | NOT_RUN |
| 业务/媒体 | 每checkpoint引用当时证据，raw实际读媒体，产物存在且版本正确 | NOT_RUN |

获得后续安装/运行授权后，在**官方源码目录**核对 `git rev-parse HEAD` 为固定SHA、保留lockfile，并使用仓库packageManager声明的pnpm版本。官方Node要求 `^22.19.0 || >=24.0.0`、packageManager `pnpm@11.7.0`、DSH要求 `^0.2.1-alpha.2`。具体安装命令/依赖来源按官方当前固定文档执行，不在本轮自动安装。

代码改完至少运行官方脚本 `pnpm typecheck`、定向 `pnpm exec vitest run tests/poc-core.spec.ts`、再 `pnpm check`（typecheck+test+build）；本轮均NOT_RUN。定向测试通过不能替代全套检查。Source/Runtime加载测试与模型业务运行仍各自记录。

最终报告分别列B0原样、B1输入适配、B2业务扩展；写清已执行命令、环境、pass/fail/not-run、原始日志与产物位置。安全硬失败不被均分抵消；无足够独立延迟样本不强下p95结论。不要将公开合成集上的通过推广为中文语音、真实渠道、长期稳定性或生产安全结论。
