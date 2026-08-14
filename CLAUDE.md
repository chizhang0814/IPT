# 电气接口智能体（IPT）— Claude Code 项目指引

电动飞机全机电气接口（EICD）场景智能体项目：基于脱敏后的 EICD 数据库构建知识图谱与内网可部署的智能体服务。

> **接手开发？** 你的任务全在 [`docs/开发任务书-内网部署版智能体.md`](docs/开发任务书-内网部署版智能体.md)——按 T1→T5 顺序执行，那份文档自包含（背景/架构/任务分解/接口契约/验收标准/预估工时）。本文件是每次会话的速查参考。

## 当前状态（2026-08-14）

- ✅ W1 已交付：本体、脱敏管线、知识图谱 v0（210,640 节点/401,938 关系）、评测集 48 条
- 🔨 进行中：**T1–T5 内网独立部署版智能体**（8/25 交付，见开发任务书）
- ⏳ 后续：T6 评测跑分 → T7 MCP 化（9 月初）→ T8 Claw 适配（拿到规范才做）

## 开工前置（一次性，缺了先解决再开发）

1. `data/eicd_anon.db`（123MB）不在 git 里——向数据负责人（张弛）索取，放入 `data/`；
2. 验证环境：`python etl/build_graph.py`（约 2 分钟，成功即环境+数据都通）；
3. 开发分支：`dev/agent-v1`，每完成一个任务提交一次。

## 三条铁律

1. **零第三方依赖**：只用 Python 3.8+ 标准库（目标机器无 pip）。现有代码全部如此，新代码同样；
2. **数据库只读**：`sqlite3.connect("file:...?mode=ro", uri=True)`；任何写库都是 bug；
3. **数据红线**：只用脱敏库 `eicd_anon.db`。`eicd_snapshot_*.db` 与 `etl/mapping_anonymize.json` 永不引用、永不提交、永不外传。

## 仓库地图

```
docs/开发任务书-内网部署版智能体.md   ← 开发任务全集（T1–T8）
docs/schema摸底.md                    ← 49 表全列结构（写 SQL 前必查）
ontology/ontology.yaml|.md            ← 本体：22 类/28 关系及源表映射
etl/                                  ← 脱敏+图谱管线（数据负责人维护，你只读）
graph/stats.md                        ← 图谱权威统计；jsonl 生成物不入库
eval/gold/auto_eval_v0.jsonl          ← 48 条金标（question/gold/gold_sql）＝你的验收标准
eval/generate_eval.py                 ← 金标生成器（确定性，可复现）
agent/reference/                      ← ★ 你的主战场：server.py/eicd_tools.py/skills.py/llm.py/ui/
mcp/                                  ← T7 阶段填充
0814会议准备材料/                     ← 汇报材料（含本体地图/链路走查可视化，可当业务学习材料）
```

## 常用命令

```powershell
python etl/build_graph.py           # 脱敏库 → 图谱 jsonl + stats.md（确定性可重跑）
python eval/generate_eval.py        # 重新生成 48 条金标
python graph/adapters/export_neo4j.py   # 图谱 → Neo4j CSV
# T3 完成后：
python agent/reference/server.py --db data/eicd_anon.db --port 8087
```

## 领域速查（写工具/Skill 必备）

- **数据主链**：`devices → connectors → pins`；`signals → signal_endpoints`（端点落到 device+pin）；`signal_edges`（端点↔端点逻辑边）；`wires → wire_ends`（端接到 pin 或 interconnect_pin）；`interconnect_pin_pairs`（分离面 R/P 面贯通）。图形化理解看 `0814会议准备材料/05-本体与图谱浏览器.html`；
- **S03 链路自测样例**：信号 `N240279-340014` → 端点 U-2403（应急配电盘箱）→ 2U-341（甚高频设备2），导线 W3303-34023-14/34024-14，分离面 D33002-A1/D33004-A2。追踪结果对不上这个就是有 bug；
- **端接尺寸唯一事实在 `pins.端接尺寸`**（`signal_endpoints.端接尺寸` 已废弃勿读）；
- 一个信号可有 >2 端点、可被多根导线实现；屏蔽线（`wires.is_shield=1`）无独立信号，按 `cable_no` 跟随芯线；
- 参考实现（业务逻辑金标，TS→Python 移植不重写规则）：`D:\Downloads\MBSE综合管理平台\server\src\shared\chat-tools.ts`、`llm-adapter.ts`、`sql-sandbox.ts`；导电网并查集在同仓库 `scripts/relink-wire-signals.py`。

## 常见坑

1. 中文列名含中文括号（`"设备部件所属系统（4位ATA）"`）——SQL 一律双引号包裹；
2. Windows 控制台打中文 GBK 乱码——调试输出写 UTF-8 文件再 Read，别信 print；
3. `\b` 正则在中文边界失效（汉字算 `\w`）——要边界用 `(?<![0-9A-Za-z])`；
4. 金标核对是最快的自检：写完一个工具就拿 `eval/gold/` 对应模板的 6 条题跑一遍。

## 验收

- 每个工具/Skill：金标逐条核对全绿（T6 的 `eval/score.py` 固化此流程，目标 ≥85%，实际应 100%）；
- S03/S04 另有指定样例断言（见开发任务书 T2 验收栏）；
- 8/25 演示故事线：查链路（S03）→ 看影响（S04）→ 体检（S08），在纯内网环境走通。

## 协作

- 数据刷新/脱敏口径/评测金标扩充：张弛负责，你不动 `etl/`；
- 内网模型地址、Claw 规范：张弛对外协调，到手后按任务书 T4/T8 接入；
- 提交规范：中文 commit message，说清做了什么和验收结果。
