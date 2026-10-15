#!/usr/bin/env python3
"""Checker for L4-0001 — readable in one sitting.

Full recompute (same seeds) and asserts: shipped cells equal recompute;
linguistic@1948 passes ENT+L2+REP; shipped N_min values match recompute.
Usage: python check.py --splits <dir> --scratch <dir> --object <results.json> --baseline <gates.json>
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "how-we-built-it"))

from run_cal import run_cell
from gen_synth import GEN_SEED, SIZES, build_family, fetch_words, indus_lengths


def n_min(cells):
    for n in SIZES:
        c = cells[str(n)]
        if c["ent"]["pass"] and c["l2"]["pass"] and c["rep"]["pass"]:
            return n
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args()

    words = fetch_words(a.scratch)
    lens = indus_lengths(a.splits)
    ship = json.loads(Path(a.object).read_text())
    ok = True
    for fi, fam in enumerate(("linguistic", "emblem")):
        fams = build_family(fam, words, lens, GEN_SEED + 100 * fi)
        for n in SIZES:
            seqs = fams[n]
            vocab = len({t for s in seqs for t in s})
            cell = run_cell(seqs, vocab, GEN_SEED + 100 * fi + n)
            s = ship[fam][str(n)]
            match = (cell["ent"]["pass"] == s["ent"]["pass"]
                     and abs(cell["ent"]["C"] - s["ent"]["C"]) < 1e-9
                     and cell["l2"]["pass"] == s["l2"]["pass"]
                     and abs(cell["l2"]["diff"] - s["l2"]["diff"]) < 1e-9
                     and cell["rep"]["pass"] == s["rep"]["pass"])
            print(f"{fam} N={n}: ENT={cell['ent']['pass']} L2={cell['l2']['pass']} "
                  f"REP={cell['rep']['pass']} {'OK' if match else 'MISMATCH'}")
            ok = ok and match
    ling = ship["linguistic"]["1948"]
    gate = ling["ent"]["pass"] and ling["l2"]["pass"] and ling["rep"]["pass"]
    print(f"N_min linguistic={n_min(ship['linguistic'])} emblem-profile reported")
    print("PASS" if ok and gate else "FAIL")
    return 0 if ok and gate else 1


if __name__ == "__main__":
    sys.exit(main())
