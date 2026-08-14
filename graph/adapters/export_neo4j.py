# -*- coding: utf-8 -*-
"""
图谱适配导出：nodes.jsonl / edges.jsonl → Neo4j 可导入 CSV
用法: python graph/adapters/export_neo4j.py [--graph graph] [--out graph/adapters/neo4j]
产出: nodes.csv / edges.csv / import.cypher（LOAD CSV 导入脚本样例）
说明: 这是"平台中立图谱 → 目标图数据库"的第一个适配器样例；
      Claw 平台适配器待接入规范到手后按同样模式补充（预计 1–2 天工作量）。
"""
import json, csv, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default=str(ROOT / "graph"))
    ap.add_argument("--out", default=str(ROOT / "graph/adapters/neo4j"))
    args = ap.parse_args()
    gdir, out = Path(args.graph), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    n_nodes = 0
    with open(gdir / "nodes.jsonl", encoding="utf-8") as f, \
         open(out / "nodes.csv", "w", encoding="utf-8-sig", newline="") as fo:
        w = csv.writer(fo)
        w.writerow(["id:ID", ":LABEL", "label", "source_table", "source_id", "props_json"])
        for line in f:
            n = json.loads(line)
            w.writerow([n["id"], n["type"], n.get("label", ""),
                        n.get("source_table", ""), n.get("source_id", ""),
                        json.dumps(n.get("props", {}), ensure_ascii=False)])
            n_nodes += 1

    n_edges = 0
    with open(gdir / "edges.jsonl", encoding="utf-8") as f, \
         open(out / "edges.csv", "w", encoding="utf-8-sig", newline="") as fo:
        w = csv.writer(fo)
        w.writerow([":START_ID", ":END_ID", ":TYPE", "props_json"])
        for line in f:
            e = json.loads(line)
            w.writerow([e["src"], e["dst"], e["type"],
                        json.dumps(e.get("props", {}), ensure_ascii=False)])
            n_edges += 1

    (out / "import.cypher").write_text("""// Neo4j 导入样例（社区版 LOAD CSV 路线；数据量 21 万节点/40 万边，分批提交）
// 1) 建索引
CREATE CONSTRAINT node_id IF NOT EXISTS FOR (n:Entity) REQUIRE n.id IS UNIQUE;
// 2) 导入节点（nodes.csv 放入 Neo4j import 目录）
:auto LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS row
CALL { WITH row
  MERGE (n:Entity {id: row.`id:ID`})
  SET n.type = row.`:LABEL`, n.label = row.label,
      n.source_table = row.source_table, n.source_id = row.source_id,
      n.props = row.props_json
} IN TRANSACTIONS OF 5000 ROWS;
// 3) 导入关系
:auto LOAD CSV WITH HEADERS FROM 'file:///edges.csv' AS row
CALL { WITH row
  MATCH (a:Entity {id: row.`:START_ID`}), (b:Entity {id: row.`:END_ID`})
  CALL apoc.create.relationship(a, row.`:TYPE`, {props: row.props_json}, b) YIELD rel
  RETURN rel
} IN TRANSACTIONS OF 5000 ROWS;
// 无 APOC 时可按 :TYPE 分组用固定关系类型语句导入
""", encoding="utf-8")

    print(f"nodes.csv={n_nodes} edges.csv={n_edges} -> {out}")


if __name__ == "__main__":
    main()
