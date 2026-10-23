#!/usr/bin/env python3
"""Checker for L0-0001 — readable in one sitting.

Compares joyboseroy cisi CSV sequences against mayig source JSONs.
Gate: 179/179 exact side-sequence matches.
Usage: python check.py --mayig <clone dir> --cisi <csv> --object <results.json> --baseline <counts.json>
"""
import argparse
import csv
import glob
import json
import os
import sys
from pathlib import Path


def load_joy(path):
    out = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["inscription_id"]] = (row.get("sign_sequence") or "").split()
    return out


def mayig_sides(path):
    doc = json.load(open(path, encoding="utf-8"))
    items = doc if isinstance(doc, list) else doc.get("sides", [doc])
    sides, iid = [], None
    for side in items:
        if isinstance(side, dict) and side.get("id", "").startswith(("M-", "H-")) and iid is None:
            iid = side["id"]
        if isinstance(side, dict) and "graphemes" in side:
            sides.append([g["id"] for g in side["graphemes"]])
        elif isinstance(side, list):
            sides.append([g.get("id", g) if isinstance(g, dict) else g for g in side])
    return iid or os.path.basename(path).replace(".json", ""), sides


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mayig", required=True)
    ap.add_argument("--cisi", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args()

    joy = load_joy(a.cisi)
    files = sorted(glob.glob(os.path.join(a.mayig, "corpus", "*", "*.json")))
    match, total, mism = 0, 0, []
    for f in files:
        iid, sides = mayig_sides(f)
        if iid not in joy:
            continue
        total += 1
        if any(s == joy[iid] for s in sides):
            match += 1
        else:
            mism.append(iid)
    obj = {"matched": match, "total": total, "mismatches": mism}
    Path(a.object).write_text(json.dumps(obj, indent=2))
    Path(a.baseline).write_text(json.dumps(
        {"mayig_files": len(files), "joy_rows": len(joy)}, indent=2))
    print(f"matched {match}/{total} (mayig files {len(files)}, joy rows {len(joy)})")
    ok = total == 179 and match == total == 179
    print("PASS" if ok else "FAIL: gate not met")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
