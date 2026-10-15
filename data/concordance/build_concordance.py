#!/usr/bin/env python3
"""Build data/concordance/pwm-v01.csv from mayig features/ (type-level P->W/M/V).
Status per P-sign: clean (exactly 1 W and 1 M) | multi (split/merge) | unmapped-W/M.
Usage: python build_concordance.py <mayig-clone> <out-csv>
"""
import glob
import json
import sys
from pathlib import Path


def main() -> int:
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    rows = []
    for f in sorted(glob.glob(str(src / "features" / "P*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        pid = d.get("id")
        ws = d.get("wells_graphemes", [])
        ms = d.get("mahadevan_graphemes", [])
        vs = d.get("parpola_graphemes", [])
        if len(ws) == 1 and len(ms) == 1:
            status = "clean-1:1"
        elif not ws and not ms:
            status = "unmapped-WM"
        elif not ws:
            status = "unmapped-W"
        elif not ms:
            status = "unmapped-M"
        else:
            status = "multi"
        rows.append((pid, "|".join(ws), "|".join(ms), "|".join(vs), status))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("p,w_list,m_list,v_list,status\n")
        for pid, w, m, v, s in rows:
            fh.write(f"{pid},{w},{m},{v},{s}\n")
    from collections import Counter
    print(Counter(s for _, _, _, _, s in rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
