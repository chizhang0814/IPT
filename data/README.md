# data/ — 数据库不入 git，clone 后此目录只有本文件

| 文件 | 大小 | 从哪获取 | 能否传给同事 |
|---|---|---|---|
| `eicd_anon.db` | 123MB | 数据负责人内网拷贝，或用管线重新生成 | ✅ 可以（脱敏库，团队内部使用） |
| `eicd_snapshot_YYYYMMDD.db` | 187MB | 由 EICD 平台 `eicd.db` 快照生成 | ❌ **禁止**（脱敏前原始数据，仅数据负责人本机保存） |

同样不入库的还有 `etl/mapping_anonymize.json`（脱敏映射表，持有即可反推真名，**永不出数据负责人本机**）。

## clone 之后想跑通全流程

1. 向数据负责人索取 `eicd_anon.db`，放入本目录；
2. 索取 `graph/nodes.jsonl`、`graph/edges.jsonl` 放入 `graph/`（或自己跑 `python etl/build_graph.py` 用脱敏库现场生成，约 2 分钟）；
3. `eval/generate_eval.py`、`etl/build_graph.py` 此时均可运行；
4. `etl/anonymize.py` 与 `etl/verify_anonymize.py` 依赖原始快照/映射表，**只能在数据负责人机器上运行**——脱敏是否干净的证明见 `docs/脱敏残留清单.md`（286 探针零命中记录）。
