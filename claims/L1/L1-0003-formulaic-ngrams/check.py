#!/usr/bin/env python3
"""Checker for L1-0003 — readable in one sitting.

Recomputes rep3/rep4 and asserts both exceed the shipped null maxima.
Usage: python check.py --corpus <csv> --object <results.json> --baseline <nulls.json>
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "how-we-built-it"))
from ng_lib import load_oriented, repeated_counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args()

    seqs = load_oriented(a.corpus)
    rep3 = repeated_counts(seqs, 3)[0]
    rep4 = repeated_counts(seqs, 4)[0]
    obj = json.loads(Path(a.object).read_text())
    base = json.loads(Path(a.baseline).read_text())

    if (rep3, rep4) != (obj["rep3"], obj["rep4"]):
        print(f"FAIL: recompute {(rep3, rep4)} != shipped {(obj['rep3'], obj['rep4'])}")
        return 1
    ok = rep3 > max(base["rep3_sorted"]) and rep4 > max(base["rep4_sorted"])
    print(f"rep3={rep3} > nullmax={max(base['rep3_sorted'])}; rep4={rep4} > nullmax={max(base['rep4_sorted'])}")
    print("PASS" if ok else "FAIL: gate not met")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
