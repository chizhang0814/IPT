# -*- coding: utf-8 -*-
"""
脱敏管线：eicd_snapshot → eicd_anon.db（确定性假名化，可重跑）
用法: python etl/anonymize.py [--src data/eicd_snapshot_20260812.db] [--dst data/eicd_anon.db]
产出: 脱敏库 + etl/mapping_anonymize.json(映射表,不入库不交付) + docs/脱敏报告.md
"""
import sqlite3, re, json, argparse, sys, io
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GENERIC_JUNK = {"", "-", "/", "NA", "N/A", "TBD", "无", "待定"}
GENERIC_PROJECT_NAMES = {"测试", "总装测试"}  # 过于通用，不进全文替换（列级已处理）


def letter(i):  # 0->A, 1->B ... 25->Z, 26->AA
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(ROOT / "data/eicd_snapshot_20260812.db"))
    ap.add_argument("--dst", default=str(ROOT / "data/eicd_anon.db"))
    args = ap.parse_args()

    cfg = yaml.safe_load(open(ROOT / "etl/anonymize_config.yaml", encoding="utf-8"))

    # 1. 复制快照
    src = sqlite3.connect(args.src)
    Path(args.dst).unlink(missing_ok=True)
    dst = sqlite3.connect(args.dst)
    src.backup(dst)
    src.close()
    db = dst
    db.row_factory = sqlite3.Row
    report = {"replacements": {}, "maps": {}}

    # 2. 构建映射 ----------------------------------------------------------
    # 2.1 项目
    projects = db.execute("SELECT id, name FROM projects ORDER BY id").fetchall()
    project_map = {}  # 原名 -> 假名
    for i, p in enumerate(projects):
        project_map[p["name"]] = cfg["project_name_map_prefix"] + letter(i)
    report["maps"]["projects"] = len(project_map)

    # 2.2 人员：users + 各列中的 6 位工号
    users = db.execute("SELECT id, username, name, display_name FROM users ORDER BY id").fetchall()
    generic = set(cfg["generic_accounts"])
    eid_map, name_map = {}, {}
    n_eid = n_name = 0
    for u in users:
        un = u["username"]
        if un not in generic:
            n_eid += 1
            eid_map[un] = f'{cfg["eid_prefix"]}{n_eid:03d}'
        for nm in {u["name"], u["display_name"]} - {None, ""}:
            if nm not in name_map:
                n_name += 1
                name_map[nm] = f'{cfg["person_name_prefix"]}{n_name:03d}'
    # 库内散落的工号（设备负责人等列）并入
    for table, cols in cfg["eid_columns"].items():
        for col in cols:
            try:
                vals = [r[0] for r in db.execute(
                    f'SELECT DISTINCT "{col}" FROM "{table}" WHERE "{col}" IS NOT NULL')]
            except sqlite3.OperationalError:
                continue
            for v in vals:
                v = str(v)
                if re.fullmatch(r"\d{6}", v) and v not in eid_map:
                    n_eid += 1
                    eid_map[v] = f'{cfg["eid_prefix"]}{n_eid:03d}'
                elif v and v not in eid_map and not re.fullmatch(r"\d{6}", v) \
                        and v not in generic and v not in GENERIC_JUNK and len(v) >= 2 \
                        and re.search(r"[一-鿿]", v) and v not in name_map:
                    n_name += 1
                    name_map[v] = f'{cfg["person_name_prefix"]}{n_name:03d}'
    report["maps"]["eids"] = len(eid_map)
    report["maps"]["person_names"] = len(name_map)

    # 2.3 供应商
    sup_vals = set()
    for table, cols in cfg["supplier_columns"].items():
        for col in cols:
            try:
                sup_vals |= {str(r[0]) for r in db.execute(
                    f'SELECT DISTINCT "{col}" FROM "{table}" WHERE "{col}" IS NOT NULL')}
            except sqlite3.OperationalError:
                pass
    sup_vals -= GENERIC_JUNK
    supplier_map = {v: f'{cfg["supplier_prefix"]}{i+1:02d}'
                    for i, v in enumerate(sorted(sup_vals))}
    report["maps"]["suppliers"] = len(supplier_map)

    # 3. 列级替换 ----------------------------------------------------------
    def col_update(table, col, mapping):
        n = 0
        for old, new in mapping.items():
            cur = db.execute(f'UPDATE "{table}" SET "{col}"=? WHERE "{col}"=?', (new, old))
            n += cur.rowcount
        if n:
            report["replacements"][f"{table}.{col}"] = n

    for old, new in project_map.items():
        db.execute("UPDATE projects SET name=? WHERE name=?", (new, old))
    col_update("permission_requests", "project_name", project_map)

    for table, cols in cfg["supplier_columns"].items():
        for col in cols:
            try:
                col_update(table, col, supplier_map)
            except sqlite3.OperationalError:
                pass

    person_map_all = {**eid_map, **name_map}
    for table, cols in {**cfg["eid_columns"], **cfg["username_ref_columns"]}.items():
        for col in cols:
            try:
                col_update(table, col, person_map_all)
            except sqlite3.OperationalError:
                pass

    # users 表本体
    for u in users:
        un = u["username"]
        db.execute(
            "UPDATE users SET username=?, name=?, display_name=?, password=? WHERE id=?",
            (eid_map.get(un, un),
             name_map.get(u["name"], None) if u["name"] else None,
             name_map.get(u["display_name"], None) if u["display_name"] else None,
             cfg["password_placeholder"], u["id"]))

    # 整列清空
    for table, colmap in cfg.get("blank_columns", {}).items():
        for col, val in colmap.items():
            db.execute(f'UPDATE "{table}" SET "{col}"=?', (val,))

    # 4. 全文本替换 --------------------------------------------------------
    # token 集：型号token + 项目名变体 + 人名 + 长供应商名；工号单独一个 \b 正则
    tokens = dict(cfg["model_tokens"])
    for old, new in project_map.items():
        if old in GENERIC_PROJECT_NAMES:
            continue
        tokens[old + "机"] = new + "机"
        tokens[old] = new
    for old, new in name_map.items():
        tokens[old] = new
    for old, new in supplier_map.items():
        if len(old) >= cfg["min_supplier_len_for_freetext"]:
            tokens[old] = new

    def guarded(tok):
        pat = re.escape(tok)
        if re.match(r"[0-9A-Za-z]", tok):
            pat = r"(?<![0-9A-Za-z])" + pat
        if re.search(r"[0-9A-Za-z]$", tok):
            pat = pat + r"(?![0-9A-Za-z])"
        return pat

    ordered = sorted(tokens, key=len, reverse=True)
    tok_re = re.compile("|".join(guarded(t) for t in ordered)) if ordered else None
    # 最长优先：re 交替按书写顺序取先匹配者，已按长度降序
    lookup = dict(tokens)
    # 全文工号替换仅限 6 位数字工号；"158"等短账号只做列级替换，避免误伤技术编号
    # 注意不能用 \b：汉字属于 \w，"600509信号表" 中 \b 不成立；统一用字母数字环视
    eids_ft = [e for e in eid_map if re.fullmatch(r"\d{6}", e)]
    eid_re = re.compile(r"(?<![0-9A-Za-z])(" + "|".join(map(re.escape, eids_ft))
                        + r")(?![0-9A-Za-z])") if eids_ft else None

    def scrub(text):
        n = 0
        if tok_re:
            def _r(m):
                nonlocal n
                n += 1
                return lookup[m.group(0)] if m.group(0) in lookup else m.group(0)
            # group(0) 可能因 guard 不在 lookup（不会：guard 是零宽断言），直接替换
            text = tok_re.sub(_r, text)
        if eid_re:
            def _e(m):
                nonlocal n
                n += 1
                return eid_map[m.group(1)]
            text = eid_re.sub(_e, text)
        return text, n

    for table, cols in cfg["freetext_columns"].items():
        for col in cols:
            try:
                rows = db.execute(
                    f'SELECT rowid, "{col}" FROM "{table}" WHERE "{col}" IS NOT NULL AND "{col}"!=""').fetchall()
            except sqlite3.OperationalError:
                continue
            total = 0
            for r in rows:
                new, n = scrub(str(r[1]))
                if n:
                    db.execute(f'UPDATE "{table}" SET "{col}"=? WHERE rowid=?', (new, r[0]))
                    total += n
            if total:
                report["replacements"][f"{table}.{col}(freetext)"] = total

    # 兜底：generic_eid_columns 中任意 6 位数字一律假名化。
    # 已知工号走 eid_map；其余（可能是上传者工号，也可能是文档/信号编号）用独立 F 序号，
    # 不并入工号表——避免把技术编号当敏感串全库扩散（历史教训：420001 信号编号误判）。
    any6 = re.compile(r"(?<![0-9A-Za-z])\d{6}(?![0-9A-Za-z])")
    file_token_map = {}
    for table, cols in cfg.get("generic_eid_columns", {}).items():
        for col in cols:
            try:
                rows = db.execute(
                    f'SELECT rowid, "{col}" FROM "{table}" WHERE "{col}" IS NOT NULL AND "{col}"!=""').fetchall()
            except sqlite3.OperationalError:
                continue
            total = 0
            for r in rows:
                s = str(r[1])

                def _g(m):
                    nonlocal total
                    v = m.group(0)
                    if v in eid_map:
                        total += 1
                        return eid_map[v]
                    if v not in file_token_map:
                        file_token_map[v] = f"F{len(file_token_map)+1:03d}"
                    total += 1
                    return file_token_map[v]
                new = any6.sub(_g, s)
                if new != s:
                    db.execute(f'UPDATE "{table}" SET "{col}"=? WHERE rowid=?', (new, r[0]))
            if total:
                report["replacements"][f"{table}.{col}(generic-eid)"] = total

    db.commit()
    db.execute("VACUUM")
    db.close()

    # 5. 落映射与报告 ------------------------------------------------------
    mapping = {"projects": project_map, "eids": eid_map, "names": name_map,
               "suppliers": supplier_map, "file_tokens": file_token_map}
    (ROOT / "etl/mapping_anonymize.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = ["# 脱敏报告", "", f"- 源库: {args.src}", f"- 脱敏库: {args.dst}", "",
             "## 映射规模", ""]
    for k, v in report["maps"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## 替换计数（表.列 → 次数）", ""]
    for k, v in sorted(report["replacements"].items()):
        lines.append(f"- {k}: {v}")
    (ROOT / "docs/脱敏报告.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
