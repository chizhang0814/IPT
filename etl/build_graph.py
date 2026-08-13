# -*- coding: utf-8 -*-
"""
图谱生成：eicd_anon.db → graph/nodes.jsonl + graph/edges.jsonl + graph/stats.md
本体定义见 ontology/ontology.yaml；节点带 source_table/source_id 回溯键。
用法: python etl/build_graph.py [--db data/eicd_anon.db] [--out graph]
确定性、可重跑：输出按 (type, id) 排序，同库两次运行逐字节一致。
"""
import sqlite3, json, argparse, sys
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent


def norm(v):
    if v is None:
        return None
    s = str(v).strip()
    return s if s not in ("", "-", "/", "TBD", "N/A", "NA") else None


class Graph:
    def __init__(self):
        self.nodes = {}   # id -> dict
        self.edges = []   # list of dict

    def node(self, nid, ntype, label, props=None, table=None, sid=None):
        if nid in self.nodes:
            return nid
        d = {"id": nid, "type": ntype, "label": label}
        if props:
            d["props"] = {k: v for k, v in props.items() if norm(v) is not None}
        if table:
            d["source_table"] = table
            d["source_id"] = sid
        self.nodes[nid] = d
        return nid

    def edge(self, src, dst, etype, props=None):
        # 不在插入时校验端点（节点可能后建），输出前统一校验并报告丢弃数
        d = {"src": src, "dst": dst, "type": etype}
        if props:
            d["props"] = {k: v for k, v in props.items() if norm(v) is not None}
        self.edges.append(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(ROOT / "data/eicd_anon.db"))
    ap.add_argument("--out", default=str(ROOT / "graph"))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(exist_ok=True)

    db = sqlite3.connect(args.db)
    db.row_factory = sqlite3.Row
    g = Graph()

    # ---------- 产品定义层 ----------
    for r in db.execute("SELECT * FROM projects"):
        g.node(f"project:{r['id']}", "Project", r["name"], {"name": r["name"]},
               "projects", r["id"])

    for r in db.execute("SELECT * FROM regions"):
        g.node(f"region:{r['id']}", "Region", r["region_name"],
               {"region_code": r["region_code"]}, "regions", r["id"])
    for r in db.execute("SELECT * FROM subregions"):
        g.node(f"subregion:{r['id']}", "Subregion", r["subregion_name"],
               {"subregion_code": r["subregion_code"]}, "subregions", r["id"])
        g.edge(f"region:{r['region_id']}", f"subregion:{r['id']}", "HAS_SUBREGION")

    # 设备 + 派生 ATA / EDZ
    ata_col = "设备部件所属系统（4位ATA）"
    for r in db.execute("SELECT * FROM devices"):
        did = g.node(f"device:{r['id']}", "Device", r["设备编号"], {
            "设备编号": r["设备编号"], "设备中文名称": r["设备中文名称"],
            "设备英文名称": r["设备英文名称"], "设备英文缩写": r["设备英文缩写"],
            "设备DAL": r["设备DAL"], "设备安装位置": r["设备安装位置"],
            "设备装机构型": r["设备装机构型"], "设备装机架次": r["设备装机架次"],
            "设备壳体接地方式": r["设备壳体接地方式"],
            "设备正常工作电压范围（V）": r["设备正常工作电压范围（V）"],
            "status": r["status"]}, "devices", r["id"])
        g.edge(f"project:{r['project_id']}", did, "HAS_DEVICE")
        ata = norm(r[ata_col])
        if ata:
            sub = g.node(f"ata:{ata}", "ATASubsystem", ata, {"code": ata})
            g.edge(did, sub, "BELONGS_TO_SYSTEM")
            ch = ata[:2]
            chn = g.node(f"atach:{ch}", "ATAChapter", f"ATA{ch}", {"chapter": ch})
            g.edge(sub, chn, "PART_OF_CHAPTER")
        edz = norm(r["EDZ"])
        if edz:
            ez = g.node(f"edz:{r['project_id']}:{edz}", "EDZ", edz,
                        {"edz_code": edz, "project_id": r["project_id"]})
            g.edge(did, ez, "LOCATED_IN_EDZ")
        owner = norm(r["设备负责人"])
        if owner:
            pn = g.node(f"person:{owner}", "Person", owner, {"anon_name": owner})
            g.edge(pn, did, "RESPONSIBLE_FOR")

    for r in db.execute("SELECT * FROM connectors"):
        cid = g.node(f"connector:{r['id']}", "Connector", r["设备端元器件编号"], {
            "设备端元器件编号": r["设备端元器件编号"],
            "设备端元器件名称及类型": r["设备端元器件名称及类型"],
            "设备端元器件件号类型及件号": r["设备端元器件件号类型及件号"],
            "触件型号": r["触件型号"], "尾附件件号": r["尾附件件号"],
            "status": r["status"]}, "connectors", r["id"])
        g.edge(f"device:{r['device_id']}", cid, "HAS_CONNECTOR")

    for r in db.execute("SELECT * FROM pins"):
        pid = g.node(f"pin:{r['id']}", "Pin", r["针孔号"], {
            "针孔号": r["针孔号"], "端接尺寸": r["端接尺寸"],
            "屏蔽类型": r["屏蔽类型"], "status": r["status"]}, "pins", r["id"])
        g.edge(f"connector:{r['connector_id']}", pid, "HAS_PIN")

    # 信号 + 派生 电源/接地/分组
    for r in db.execute("SELECT * FROM signals"):
        sid = g.node(f"signal:{r['id']}", "Signal", r["unique_id"] or f"sig-{r['id']}", {
            "unique_id": r["unique_id"], "连接类型": r["连接类型"],
            "信号ATA": r["信号ATA"], "推荐导线线规": r["推荐导线线规"],
            "推荐导线线型": r["推荐导线线型"], "独立电源代码": r["独立电源代码"],
            "余度代码": r["余度代码"], "接地代码": r["接地代码"],
            "功能代码": r["功能代码"], "电磁兼容代码": r["电磁兼容代码"],
            "额定电压": r["额定电压"], "额定电流": r["额定电流"],
            "是否成品线": r["是否成品线"], "协议标识": r["协议标识"],
            "signal_group": r["signal_group"], "twist_group": r["twist_group"],
            "status": r["status"]}, "signals", r["id"])
        pj = r["project_id"]
        pw = norm(r["独立电源代码"])
        if pw:
            g.edge(sid, g.node(f"power:{pw}", "PowerSource", pw, {"code": pw}), "POWERED_BY")
        gc = norm(r["接地代码"])
        if gc:
            g.edge(sid, g.node(f"ground:{gc}", "GroundClass", gc, {"code": gc}), "GROUNDED_AS")
        grp = norm(r["signal_group"])
        if grp:
            gn = g.node(f"group:{pj}:{grp}", "SignalGroup", grp,
                        {"group_name": grp, "project_id": pj})
            g.edge(sid, gn, "IN_GROUP")
        sa = norm(r["信号ATA"])
        if sa:
            sub = g.node(f"ata:{sa}", "ATASubsystem", sa, {"code": sa})
            g.edge(sid, sub, "SIGNAL_OF_SYSTEM")

    for r in db.execute("SELECT * FROM signal_group_types"):
        g.node(f"grouptype:{r['id']}", "SignalGroupType", r["name"], {
            "name": r["name"], "connection_type": r["connection_type"],
            "prefix": r["prefix"], "count": r["count"], "protocols": r["protocols"]},
            "signal_group_types", r["id"])

    # 分组→组建规则（前缀匹配，同项目）
    gt_by_proj = defaultdict(list)
    for r in db.execute("SELECT id, project_id, prefix FROM signal_group_types"):
        gt_by_proj[r["project_id"]].append((r["prefix"], r["id"]))
    for nid, nd in list(g.nodes.items()):
        if nd["type"] != "SignalGroup":
            continue
        pj = nd["props"]["project_id"]
        name = nd["props"]["group_name"]
        for prefix, gtid in sorted(gt_by_proj.get(pj, []), key=lambda x: -len(x[0])):
            if name.startswith(prefix):
                g.edge(nid, f"grouptype:{gtid}", "GROUP_RULE")
                break

    for r in db.execute("SELECT * FROM signal_endpoints"):
        eid = g.node(f"endpoint:{r['id']}", "SignalEndpoint",
                     r["信号名称"] or f"ep-{r['id']}", {
            "信号名称": r["信号名称"], "信号定义": r["信号定义"],
            "endpoint_index": r["endpoint_index"], "input": r["input"],
            "output": r["output"], "推荐导线线规": r["推荐导线线规"]},
            "signal_endpoints", r["id"])
        g.edge(f"signal:{r['signal_id']}", eid, "HAS_ENDPOINT")
        if r["device_id"]:
            g.edge(eid, f"device:{r['device_id']}", "AT_DEVICE")
        if r["pin_id"]:
            g.edge(eid, f"pin:{r['pin_id']}", "AT_PIN")

    for r in db.execute("SELECT * FROM signal_edges"):
        g.edge(f"endpoint:{r['from_endpoint_id']}", f"endpoint:{r['to_endpoint_id']}",
               "SIGNAL_EDGE", {"direction": r["direction"], "edge_id": r["id"]})

    # 线束 / 导线 / 互联点
    for r in db.execute("SELECT * FROM harnesses"):
        hid = g.node(f"harness:{r['id']}", "Harness", r["harness_no"], {
            "harness_no": r["harness_no"], "alias": r["alias"], "zone": r["zone"]},
            "harnesses", r["id"])
        g.edge(hid, f"project:{r['project_id']}", "HARNESS_OF")

    for r in db.execute("SELECT it.*, t.name AS ic_type_name FROM interconnects it "
                        "LEFT JOIN ic_types t ON t.id = it.ic_type_id"):
        icid = g.node(f"ic:{r['id']}", "Interconnect", r["label"], {
            "label": r["label"], "sub_kind": r["sub_kind"], "edz": r["edz"],
            "ground_class": r["ground_class"], "stage": r["stage"],
            "ic_type_name": r["ic_type_name"]}, "interconnects", r["id"])
        edz = norm(r["edz"])
        if edz:
            ez = g.node(f"edz:{r['project_id']}:{edz}", "EDZ", edz,
                        {"edz_code": edz, "project_id": r["project_id"]})
            g.edge(icid, ez, "IC_IN_EDZ")
        gc = norm(r["ground_class"])
        if gc:
            g.edge(icid, g.node(f"ground:{gc}", "GroundClass", gc, {"code": gc}),
                   "IC_GROUND_CLASS")
        ac = norm(r["arrangement_code"])
        if ac:
            g.edge(icid, f"arr:{ac}", "USES_ARRANGEMENT")

    for r in db.execute("SELECT * FROM interconnect_pins"):
        ipid = g.node(f"icpin:{r['id']}", "InterconnectPin", r["pin_num"], {
            "pin_num": r["pin_num"], "face": r["face"],
            "contact_size": r["contact_size"], "shield_type": r["shield_type"],
            "signal_name": r["signal_name"]}, "interconnect_pins", r["id"])
        g.edge(f"ic:{r['interconnect_id']}", ipid, "HAS_ICPIN")

    for r in db.execute("SELECT * FROM interconnect_pin_pairs"):
        g.edge(f"icpin:{r['pin_r_id']}", f"icpin:{r['pin_p_id']}", "THROUGH_PAIR")

    for r in db.execute("SELECT * FROM wires"):
        wid = g.node(f"wire:{r['id']}", "Wire", r["wire_no"], {
            "wire_no": r["wire_no"], "cable_no": r["cable_no"],
            "is_shield": r["is_shield"], "gauge_awg": r["gauge_awg"],
            "wire_type": r["wire_type"], "color": r["color"],
            "length_mm": r["length_mm"], "stage": r["stage"], "source": r["source"]},
            "wires", r["id"])
        if r["signal_id"]:
            g.edge(wid, f"signal:{r['signal_id']}", "IMPLEMENTS")
        if r["harness_id"]:
            g.edge(wid, f"harness:{r['harness_id']}", "IN_HARNESS")

    for r in db.execute("SELECT * FROM wire_ends"):
        props = {"end_idx": r["end_idx"], "kind": r["kind"]}
        if r["pin_id"]:
            g.edge(f"wire:{r['wire_id']}", f"pin:{r['pin_id']}", "END_AT_PIN", props)
        if r["interconnect_pin_id"]:
            g.edge(f"wire:{r['wire_id']}", f"icpin:{r['interconnect_pin_id']}",
                   "END_AT_ICPIN", props)

    # ---------- 规则层 ----------
    for r in db.execute("SELECT * FROM arrangements"):
        g.node(f"arr:{r['arrangement_code']}", "Arrangement", r["arrangement_code"], {
            "arrangement_code": r["arrangement_code"], "shell_size": r["shell_size"],
            "shell_letter": r["shell_letter"], "family": r["family"],
            "total_contacts": r["total_contacts"],
            "contact_distribution": r["contact_distribution"]},
            "arrangements", r["arrangement_code"])
    for r in db.execute("SELECT * FROM arrangement_positions"):
        apid = g.node(f"arrpos:{r['arrangement_code']}:{r['label']}",
                      "ArrangementPosition", r["label"], {
            "label": r["label"], "position_index": r["position_index"],
            "contact_std": r["contact_std"], "is_special": r["is_special"]},
            "arrangement_positions", f"{r['arrangement_code']}+{r['label']}")
        g.edge(f"arr:{r['arrangement_code']}", apid, "HAS_POSITION")

    # ---------- 过程层 ----------
    users = {r["id"]: r for r in db.execute("SELECT * FROM users")}
    for uid, r in users.items():
        nm = r["name"] or r["username"]
        g.node(f"person:{nm}", "Person", nm,
               {"anon_name": nm, "role": r["role"]}, "users", uid)

    ent_prefix = {"devices": "device", "connectors": "connector", "pins": "pin",
                  "signals": "signal", "wires": "wire", "interconnects": "ic",
                  "signal_endpoints": "endpoint", "harnesses": "harness"}
    for r in db.execute("SELECT * FROM change_logs"):
        cid = g.node(f"chg:{r['id']}", "ChangeEvent", f"chg-{r['id']}", {
            "entity_table": r["entity_table"] or r["table_name"],
            "entity_id": r["entity_id"] if r["entity_id"] is not None else r["data_id"],
            "reason": (r["reason"] or "")[:120] or None, "status": r["status"],
            "batch_id": r["batch_id"], "created_at": r["created_at"]},
            "change_logs", r["id"])
        et = (r["entity_table"] or r["table_name"] or "")
        eid_v = r["entity_id"] if r["entity_id"] is not None else r["data_id"]
        if et in ent_prefix and eid_v is not None:
            g.edge(cid, f"{ent_prefix[et]}:{eid_v}", "CHANGED")
        u = users.get(r["changed_by"])
        if u:
            g.edge(cid, f"person:{u['name'] or u['username']}", "CHANGED_BY")

    uname2person = {r["username"]: f"person:{r['name'] or r['username']}"
                    for r in users.values()}
    ent_prefix2 = {"device": "device", "connector": "connector", "pin": "pin",
                   "signal": "signal", "devices": "device", "signals": "signal"}
    for r in db.execute("SELECT * FROM approval_requests"):
        aid = g.node(f"apr:{r['id']}", "ApprovalEvent", f"apr-{r['id']}", {
            "action_type": r["action_type"], "entity_type": r["entity_type"],
            "entity_id": r["entity_id"], "status": r["status"],
            "current_phase": r["current_phase"], "created_at": r["created_at"]},
            "approval_requests", r["id"])
        et = (r["entity_type"] or "").lower()
        if et in ent_prefix2 and r["entity_id"] is not None:
            g.edge(aid, f"{ent_prefix2[et]}:{r['entity_id']}", "APPROVAL_FOR")
        p = uname2person.get(r["requester_username"])
        if p:
            g.edge(aid, p, "REQUESTED_BY")

    # ---------- 输出 ----------
    node_list = sorted(g.nodes.values(), key=lambda n: (n["type"], n["id"]))
    dropped = Counter()
    valid_edges = []
    for e in g.edges:
        if e["src"] in g.nodes and e["dst"] in g.nodes:
            valid_edges.append(e)
        else:
            dropped[e["type"]] += 1
    if dropped:
        print("WARN dropped edges (dangling endpoint):",
              json.dumps(dict(dropped), ensure_ascii=False), file=sys.stderr)
    edge_list = sorted(valid_edges, key=lambda e: (e["type"], e["src"], e["dst"]))
    with open(out / "nodes.jsonl", "w", encoding="utf-8") as f:
        for n in node_list:
            f.write(json.dumps(n, ensure_ascii=False, default=str) + "\n")
    with open(out / "edges.jsonl", "w", encoding="utf-8") as f:
        for e in edge_list:
            f.write(json.dumps(e, ensure_ascii=False, default=str) + "\n")

    nc, ec = Counter(n["type"] for n in node_list), Counter(e["type"] for e in edge_list)
    lines = ["# 知识图谱统计（v0）", "",
             f"- 数据源: {Path(args.db).name}（脱敏库）",
             f"- 节点总数: **{len(node_list):,}**",
             f"- 关系总数: **{len(edge_list):,}**", "", "## 节点分类型", "",
             "| 类型 | 数量 |", "|---|---|"]
    lines += [f"| {t} | {c:,} |" for t, c in nc.most_common()]
    lines += ["", "## 关系分类型", "", "| 类型 | 数量 |", "|---|---|"]
    lines += [f"| {t} | {c:,} |" for t, c in ec.most_common()]
    if dropped:
        lines += ["", "## 完整性说明", "",
                  "以下悬挂边在输出前被丢弃（目标实体已从库中删除，属正常历史演进；"
                  "ChangeEvent/ApprovalEvent 节点自身保留 entity_table/entity_id 供追溯）：", ""]
        lines += [f"- {t}: {c:,} 条" for t, c in dropped.most_common()]
    (out / "stats.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"nodes={len(node_list)} edges={len(edge_list)}")
    print(json.dumps(dict(nc), ensure_ascii=False))


if __name__ == "__main__":
    main()
