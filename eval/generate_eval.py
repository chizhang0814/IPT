# -*- coding: utf-8 -*-
"""
评测集生成器（骨架版 v0）：从脱敏库采样实体 → 按模板生成题目，金标答案由 SQL 现算。
用法: python eval/generate_eval.py [--db data/eicd_anon.db] [--n 20] [--out eval/gold/auto_eval_v0.jsonl]
每条: {id, skill, template, question, gold, gold_sql, source}
确定性采样（固定 seed），同库两次生成结果一致。
后续扩展：每个 Skill 一组模板，目标 150–200 条（W2 完成）。
"""
import sqlite3, json, argparse, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = 20260812


def sample(db, sql, n, seed_offset=0):
    rows = db.execute(sql).fetchall()
    rnd = random.Random(SEED + seed_offset)
    return rnd.sample(rows, min(n, len(rows)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(ROOT / "data/eicd_anon.db"))
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--out", default=str(ROOT / "eval/gold/auto_eval_v0.jsonl"))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    db.row_factory = sqlite3.Row
    per = max(1, args.n // 8)
    items = []

    # T1 结构计数：设备的连接器数（S01 问答 / S08 体检共用）
    for r in sample(db, """
        SELECT d.id, d.设备编号, d.project_id, COUNT(c.id) AS n
        FROM devices d JOIN connectors c ON c.device_id=d.id
        GROUP BY d.id HAVING n>0""", per, 1):
        items.append({
            "skill": "S01", "template": "device_connector_count",
            "question": f"项目ID {r['project_id']} 中，设备 {r['设备编号']} 有多少个设备端连接器？",
            "gold": r["n"],
            "gold_sql": f"SELECT COUNT(*) FROM connectors WHERE device_id={r['id']}",
            "source": {"table": "devices", "id": r["id"]}})

    # T2 信号端点落位：信号两端在哪些设备（S03 链路追踪基础题）
    for r in sample(db, """
        SELECT s.id, s.unique_id FROM signals s
        WHERE s.unique_id IS NOT NULL AND EXISTS
          (SELECT 1 FROM signal_endpoints e WHERE e.signal_id=s.id AND e.device_id IS NOT NULL)
        """, per, 2):
        golds = sorted({row[0] for row in db.execute(
            "SELECT DISTINCT d.设备编号 FROM signal_endpoints e "
            "JOIN devices d ON d.id=e.device_id WHERE e.signal_id=?", (r["id"],))})
        items.append({
            "skill": "S03", "template": "signal_endpoint_devices",
            "question": f"信号 {r['unique_id']} 的端点分布在哪些设备上？（列出设备编号）",
            "gold": golds,
            "gold_sql": ("SELECT DISTINCT d.设备编号 FROM signal_endpoints e "
                         f"JOIN devices d ON d.id=e.device_id WHERE e.signal_id={r['id']}"),
            "source": {"table": "signals", "id": r["id"]}})

    # T3 系统归属：设备属于哪个 ATA 子系统（S01）
    for r in sample(db, """
        SELECT id, 设备编号, "设备部件所属系统（4位ATA）" AS ata FROM devices
        WHERE ata IS NOT NULL AND ata NOT IN ('','-')""", per, 3):
        items.append({
            "skill": "S01", "template": "device_ata",
            "question": f"设备 {r['设备编号']} 属于哪个系统（4位ATA）？",
            "gold": r["ata"],
            "gold_sql": ("SELECT \"设备部件所属系统（4位ATA）\" FROM devices "
                         f"WHERE id={r['id']}"),
            "source": {"table": "devices", "id": r["id"]}})

    # T4 物理实现：信号由哪些导线实现（S03/S09 逻辑-物理对齐题）
    for r in sample(db, """
        SELECT s.id, s.unique_id FROM signals s
        WHERE s.unique_id IS NOT NULL AND EXISTS
          (SELECT 1 FROM wires w WHERE w.signal_id=s.id)""", per, 4):
        golds = sorted(row[0] for row in db.execute(
            "SELECT wire_no FROM wires WHERE signal_id=?", (r["id"],)))
        items.append({
            "skill": "S03", "template": "signal_wires",
            "question": f"信号 {r['unique_id']} 由哪些物理导线实现？（列出线号）",
            "gold": golds,
            "gold_sql": f"SELECT wire_no FROM wires WHERE signal_id={r['id']}",
            "source": {"table": "signals", "id": r["id"]}})

    # T5 系统清单：某 ATA 子系统下的设备（S01 问答 / S07 构型对比基础）
    for r in sample(db, """
        SELECT project_id, "设备部件所属系统（4位ATA）" AS ata, COUNT(*) AS n
        FROM devices WHERE ata IS NOT NULL AND ata NOT IN ('','-')
        GROUP BY project_id, ata HAVING n BETWEEN 2 AND 30""", per, 5):
        golds = sorted(row[0] for row in db.execute(
            'SELECT 设备编号 FROM devices WHERE project_id=? AND "设备部件所属系统（4位ATA）"=?',
            (r["project_id"], r["ata"])))
        items.append({
            "skill": "S01", "template": "ata_device_list",
            "question": f"项目ID {r['project_id']} 中，{r['ata']} 子系统包含哪些设备？（列出设备编号）",
            "gold": golds,
            "gold_sql": (f"SELECT 设备编号 FROM devices WHERE project_id={r['project_id']} "
                         f"AND \"设备部件所属系统（4位ATA）\"='{r['ata']}'"),
            "source": {"table": "devices", "id": None}})

    # T6 线束归属：信号的实现导线在哪个线束（S03 物理侧）
    for r in sample(db, """
        SELECT s.id, s.unique_id FROM signals s WHERE s.unique_id IS NOT NULL AND EXISTS
          (SELECT 1 FROM wires w WHERE w.signal_id=s.id AND w.harness_id IS NOT NULL)""", per, 6):
        golds = sorted({row[0] for row in db.execute(
            "SELECT h.harness_no FROM wires w JOIN harnesses h ON h.id=w.harness_id "
            "WHERE w.signal_id=?", (r["id"],))})
        items.append({
            "skill": "S03", "template": "signal_harness",
            "question": f"信号 {r['unique_id']} 的实现导线归属哪些线束？（列出线束号）",
            "gold": golds,
            "gold_sql": ("SELECT DISTINCT h.harness_no FROM wires w "
                         f"JOIN harnesses h ON h.id=w.harness_id WHERE w.signal_id={r['id']}"),
            "source": {"table": "signals", "id": r["id"]}})

    # T7 变更历史计数：实体被改过多少次（S04 影响分析 / S10 溯源基础）
    for r in sample(db, """
        SELECT d.id, d.设备编号, COUNT(c.id) AS n FROM devices d
        JOIN change_logs c ON COALESCE(c.entity_table,c.table_name)='devices'
          AND COALESCE(c.entity_id,c.data_id)=d.id
        GROUP BY d.id HAVING n>0""", per, 7):
        items.append({
            "skill": "S04", "template": "device_change_count",
            "question": f"设备 {r['设备编号']} 共有多少条变更记录？",
            "gold": r["n"],
            "gold_sql": ("SELECT COUNT(*) FROM change_logs WHERE "
                         "COALESCE(entity_table,table_name)='devices' "
                         f"AND COALESCE(entity_id,data_id)={r['id']}"),
            "source": {"table": "devices", "id": r["id"]}})

    # T8 针孔属性：指定针孔的端接尺寸（S08 质量体检基础）
    for r in sample(db, """
        SELECT p.id, p.针孔号, p.端接尺寸, c.设备端元器件编号 AS conn, d.设备编号 AS dev
        FROM pins p JOIN connectors c ON c.id=p.connector_id JOIN devices d ON d.id=c.device_id
        WHERE p.端接尺寸 IS NOT NULL AND p.端接尺寸 NOT IN ('','-')""", per, 8):
        items.append({
            "skill": "S08", "template": "pin_termination",
            "question": f"设备 {r['dev']} 连接器 {r['conn']} 的针孔 {r['针孔号']} 端接尺寸是多少？",
            "gold": r["端接尺寸"],
            "gold_sql": f"SELECT 端接尺寸 FROM pins WHERE id={r['id']}",
            "source": {"table": "pins", "id": r["id"]}})

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for i, it in enumerate(items, 1):
            it["id"] = f"auto-{i:04d}"
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"generated {len(items)} items -> {out}")


if __name__ == "__main__":
    main()
