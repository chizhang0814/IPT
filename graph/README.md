# graph/ — 图谱数据文件不入 git

`nodes.jsonl`（60MB，210,640 节点）与 `edges.jsonl`（29MB，401,938 关系）是 ETL 生成物，不入库；权威统计见同目录 `stats.md`（入库）。

获取方式二选一：

1. **向数据负责人索取**两个 jsonl 文件放入本目录；
2. **自己生成**：拿到 `data/eicd_anon.db` 后运行 `python etl/build_graph.py`（约 2 分钟，确定性输出，同库两次运行逐字节一致）。
