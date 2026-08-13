# -*- coding: utf-8 -*-
"""
脱敏残留验证：扫描 eicd_anon.db 全部 TEXT 列，确认已映射的敏感串零残留。
用法: python etl/verify_anonymize.py [--db data/eicd_anon.db]
退出码: 0=零残留, 1=有残留（明细落 docs/脱敏残留清单.md）
"""
import sqlite3, re, json, argparse, sys, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(ROOT / "data/eicd_anon.db"))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    mapping = json.load(open(ROOT / "etl/mapping_anonymize.json", encoding="utf-8"))

    probes = list(mapping["names"])
    probes += [k for k in mapping["eids"] if re.fullmatch(r"\d{6}", k)]
    probes += [p for p in mapping["projects"] if p not in ("测试", "总装测试")]
    probes += [s for s in mapping["suppliers"]
               if len(s) >= 4 and not s.replace(" ", "").isdigit()]
    probes += ["CE-25", "CE25A"]

    def guard(p):
        pat = re.escape(p)
        if re.match(r"[0-9A-Za-z]", p):
            pat = r"(?<![0-9A-Za-z])" + pat
        if re.search(r"[0-9A-Za-z]$", p):
            pat += r"(?![0-9A-Za-z])"
        return pat

    big = re.compile("|".join(guard(p) for p in sorted(probes, key=len, reverse=True)))
    tables = [r[0] for r in db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
    hits = []
    for t in tables:
        for c in db.execute(f'PRAGMA table_info("{t}")').fetchall():
            col, typ = c[1], (c[2] or "TEXT").upper()
            if typ not in ("TEXT", ""):
                continue
            try:
                rows = db.execute(
                    f'SELECT "{col}" FROM "{t}" WHERE "{col}" IS NOT NULL AND "{col}"!=""').fetchall()
            except sqlite3.OperationalError:
                continue
            for (v,) in rows:
                m = big.search(str(v))
                if m:
                    hits.append((t, col, m.group(0), str(v)[:80]))

    lines = [f"# 脱敏残留清单（probes={len(probes)}, hits={len(hits)}）", ""]
    for k, n in collections.Counter((h[0], h[1], h[2]) for h in hits).most_common(50):
        lines.append(f"- {k[0]}.{k[1]} 残留 `{k[2]}` × {n}")
    (ROOT / "docs/脱敏残留清单.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"probes={len(probes)} hits={len(hits)}")
    sys.exit(0 if not hits else 1)


if __name__ == "__main__":
    main()
