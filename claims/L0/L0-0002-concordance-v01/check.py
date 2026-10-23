#!/usr/bin/env python3
"""Checker for L0-0002 — readable in one sitting.

Rebuilds pwm-v01.csv from the mayig clone and asserts byte-equality plus the
preregistered status counts and contested-listing rule.
Usage: python check.py --mayig <clone> --object <csv> --baseline <counts.json> [--builder <build_concordance.py>]
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mayig", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--builder", required=True)
    a = ap.parse_args()

    with tempfile.TemporaryDirectory() as td:
        rebuilt = str(Path(td) / "pwm.csv")
        r = subprocess.run([sys.executable, a.builder, a.mayig, rebuilt],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("FAIL: builder error", r.stderr[-500:])
            return 1
        sha_new = hashlib.sha256(open(rebuilt, "rb").read()).hexdigest()
        sha_ship = hashlib.sha256(open(a.object, "rb").read()).hexdigest()
    base = json.loads(Path(a.baseline).read_text())
    ok = sha_new == sha_ship == base["object_sha256"]
    import csv
    counts = Counter()
    contested_m = set()
    m2p = {}
    with open(a.object, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            counts[row["status"]] += 1
            for m in row["m_list"].split("|") if row["m_list"] else []:
                m2p.setdefault(m, set()).add(row["p"])
    contested = {m: p for m, p in m2p.items() if len(p) > 1}
    ok = ok and dict(counts) == base["status_counts"] and len(contested) >= 10
    print(f"sha match={sha_new == sha_ship} counts={dict(counts)} contested-M={len(contested)}")
    print("PASS" if ok else "FAIL: gate not met")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
