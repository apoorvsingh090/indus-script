#!/usr/bin/env python3
"""Checker for L1-0002 — readable in one sitting.

Recomputes n80_begin/n80_end from the corpus CSV and asserts the preregistered gate:
n80_end < n80_begin AND n80_end < min of shipped shuffle null.
Usage: python check.py --corpus <csv> --object <results.json> --baseline <nulls.json>
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "how-we-built-it"))
from pos_lib import load_sequences, pos_stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args()

    st = pos_stats(load_sequences(a.corpus))
    obj = json.loads(Path(a.object).read_text())
    base = json.loads(Path(a.baseline).read_text())

    if (st["n80_begin"], st["n80_end"]) != (obj["n80_begin"], obj["n80_end"]):
        print(f"FAIL: recompute {(st['n80_begin'], st['n80_end'])} != shipped {(obj['n80_begin'], obj['n80_end'])}")
        return 1
    null_min = min(base["n80_end_sorted"])
    ok = st["n80_end"] < st["n80_begin"] and st["n80_end"] < null_min
    print(f"n80 begin/end = {st['n80_begin']}/{st['n80_end']} null_min = {null_min}")
    print("PASS" if ok else "FAIL: gate not met")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
