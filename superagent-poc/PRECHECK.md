# 2026-11-11 离线预检与交付范围

[项目入口](README.md) · [接手执行手册](HANDOFF.md) · [代码实施细节](IMPLEMENTATION.md)

执行日期：2026-11-11（UTC）。素材基线来自 dsh-watch/main 提交 [`72bb02bf091600d1c1da38bff9a5833973f0510f`](https://github.com/ikxky/dsh-watch/commit/72bb02bf091600d1c1da38bff9a5833973f0510f)，51个原始文件逐个以Git blob SHA核对。未用旧本地副本覆盖远端变化。固定官方原型为 `8c32a9dc5d72c033816c6a8110b37f40cf94fba4`，只做源码回读，**没有安装或运行**。

## 1. 结果汇总

两套既有validator与Python语法检查实际PASS。新增交接检查器也实际运行，结果如下。**这些结果只证明材料和离线准备工具，不是模型业务评测。**

| 检查 | 实际结果 | 解释 |
|---|---|---|
| 旧corpus validator | PASS，退出0 | 41条/10批/38唯一源ID；28 message、3 tool_result、5 worker_result、3 observation、1 fault、1 permission_request；媒体hash/格式及gold引用完整 |
| business validator | PASS，退出0 | 48投递/47唯一源消息/16批/15附件；间隔2–276352秒；180时间边界、360双臂stage；WAV6.765秒、MP4 3秒 |
| Python编译 | PASS | 原有六个脚本及新增两个检查器；编译不表示生成器或TypeScript示例运行 |
| 末时点全量stage | PASS | raw/parsed各48行、47个唯一event_id；保留重投，stage不做业务副作用去重 |
| 逐时点增量stage | PASS | 各臂48条业务投递+1条media_ready；raw为11-18 08:53、parsed为08:54，+08:00；派生事件没有人的actor/text字段 |
| pending/时点隔离 | PASS | 边界前/等/后；pending无ref或提取内容，parsed不复制原媒体；stage文件白名单检查通过 |
| 损坏PDF | PASS（预期负例） | 实际解析抛错；parsed参照status=failed、text=null；日志中的EOF marker not found是预期诊断 |
| 来源快照 | PASS | 200、同etag304、503未知、同版本恢复304、新版200、更正/撤回；补充遍历14个来源时间线状态 |
| 重复与身份元数据 | PASS | d014/d016保留同消息身份/内容；跨实例owner映射同一合成owner，其他成员context-only；native_thread_id全为空 |
| 输出保护 | PASS | 已有输出拒绝覆盖、逆向区间与无时区时间拒绝 |
| `--since` | UNSUPPORTED（未实现），实际退出2 | argparse拒绝该参数。应使用已实现的`--after`，语义为`(after, until]`；不是validator失败 |
| 项目相对链接 | PASS | 检查器验证本包Markdown文件/锚点目标存在且不越出根；外部HTTPS仅保留，不声称离线可用 |
| 真实权限/OS隔离 | NOT_RUN | stage目录不是安全边界；未创建被测进程、mount或网络规则 |
| 原型、模型、Source加载 | NOT_RUN | 未运行Superagent/DSH、编译TypeScript示例或验证真实插件加载 |
| 业务watch/并发/重启/通知 | NOT_RUN | 没有controller、Worker、业务正确率、性能、成本或真实发送结果 |
| 本轮视觉/听辨/生成 | NOT_RUN | 未重新生成fixture、人工看图/听辨或运行OCR/ASR；历史QA不算本轮实测 |

两套validator运行时只处理本地材料及本地ffprobe，不使用账号或外网。生成器只审阅/编译，未重新生成。旧生成器开头的“standard-library-only”说明与实际第三方导入不符，使用者应以依赖列表及import为准；本次保留原脚本。

## 2. 可重复执行的命令

所有命令在 `superagent-poc/` 根目录执行。输出写临时目录，不覆盖fixture；新增 `check_replay.py` 会自行创建并清理临时投影，输出的只是计数/状态摘要，不包含业务评分答案。

```sh
QA_DIR="$(mktemp -d)"
mkdir -p "$QA_DIR/tmp" "$QA_DIR/pycache"
export TMPDIR="$QA_DIR/tmp"
export PYTHONPYCACHEPREFIX="$QA_DIR/pycache"
python corpus/validate.py > "$QA_DIR/corpus-validator.log" 2>&1
python business-corpus/validate.py > "$QA_DIR/business-validator.log" 2>&1
python -m py_compile corpus/*.py business-corpus/*.py scripts/*.py
python scripts/check_replay.py > "$QA_DIR/replay-check.json"
python scripts/check_links.py --self-test > "$QA_DIR/links.log"

# 503失败与200恢复；未传etag时恢复返回200
python business-corpus/replay.py source \
  --at 2026-11-18T16:00:00+08:00 --source deepseek-plugin
python business-corpus/replay.py source \
  --at 2026-11-19T09:00:00+08:00 --source deepseek-plugin

# 负例：应退出2并报告unrecognized arguments；不是支持的用法
python business-corpus/replay.py stage \
  --since 2026-11-16T08:00:00+08:00 \
  --until 2026-11-16T09:02:11+08:00 --arm raw --out "$QA_DIR/invalid-since"
```

每条命令单独记录退出状态；不要因最后一条预期失败而误认整套材料失败，也不要用忽略所有错误的shell脚本掩盖真失败。首次补充检查在独立临时脚本执行；打包前已整理为可复用的[check_replay.py](scripts/check_replay.py)并复跑。

## 3. 本轮环境

- Python 3.12.14
- Pillow 13.0.0；reportlab 4.4.9；pypdf 6.21.4
- ffmpeg/ffprobe 7.1.5-0+deb13u1；NotoSansCJK-Regular.ttc存在

没有安装新依赖。校验依赖齐全；本轮未重新证明flite/libx264生成链路。将来换机器/依赖版本须重新记录，不能把此环境当部署环境。

## 4. 提交与ZIP如何核对

交付通过以最新远端base tree创建单次提交，并用expected head更新main，避免覆盖同期编辑；推送后再次读取main、commit tree及修改文档。ZIP只收该提交的 `superagent-poc/` 文件，逐文件比较Git blob SHA，另校验ZIP CRC、解压及相对链接。提交ID和ZIP SHA256随交付消息提供，避免文件自包含提交ID形成循环。

本包包含公开合成的评审答案以供同事执行评审，不含真实私有材料/凭据。排除`.git`、缓存、临时stage、运行状态数据库、环境文件、依赖目录和无关研究。未进行真实Runtime检查，因此没有此提交的框架CI通过结论；源码/语料离线检查与远端仓库CI状态分开报告。
