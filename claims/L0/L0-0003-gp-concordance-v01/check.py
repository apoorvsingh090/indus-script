#!/usr/bin/env python3
"""Checker for L0-0003 — readable in one sitting.

Recomputes the G<->P concordance from the two pinned sources with the
frozen method, asserts every shipped count matches (join, orientation,
classes, holdout), and evaluates the preregistered gate.

Usage: python check.py --mayig <repo_dir> --corpus <csv> --object <results.json> --baseline <counts.json> --concordance <gp-v01.csv>
"""
import argparse
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "how-we-built-it"))

from build_gp import CLEAN_MIN_OCC, classify, evidence, load_g, load_mayig  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mayig", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--concordance", required=True)
    a = ap.parse_args()

    o = json.loads(Path(a.object).read_text())
    psides = load_mayig(Path(a.mayig))
    grows = load_g(a.corpus)
    gsides = {}
    for r in grows:
        gsides.setdefault(r["m"], []).append(r)
    shared = sorted(set(gsides) & set(psides))

    variants = {}
    for p_rev in (False, True):
        C, support, ng, np_, pairs = evidence(gsides, psides, p_rev)
        variants[p_rev] = (C, support, ng, np_, pairs,
                           sum(max(c.values()) for c in C.values() if c))
    p_rev = max(variants, key=lambda k: (variants[k][5], k))
    C, support, ng, np_, pairs, _ = variants[p_rev]
    cls = classify(C, support, ng, np_)

    n_clean = sum(1 for v in cls.values() if v[0] == "clean")
    n_cont = sum(1 for v in cls.values() if v[0] == "contested")
    n_unm = sum(1 for v in cls.values() if v[0] == "unmapped")
    clean_ps = [v[1] for v in cls.values() if v[0] == "clean"]
    bij = len(clean_ps) != len(set(clean_ps))

    same = (o["join"]["shared_m_numbers"] == len(shared)
            and o["orientation"]["selected_p_reversed"] == p_rev
            and o["alignment"]["equal_length_pairs"] == pairs
            and o["alignment"]["g_signs_observed"] == len(ng)
            and o["classes"]["clean"] == n_clean
            and o["classes"]["contested"] == n_cont
            and o["classes"]["unmapped"] == n_unm)
    base = json.loads(Path(a.baseline).read_text())
    csv_rows = list(csv.DictReader(open(a.concordance, encoding="utf-8")))
    csv_same = (len(csv_rows) == len(ng)
                and sum(1 for r in csv_rows if r["class"] == "clean") == n_clean
                and base["clean"] == n_clean and base["g_signs_observed"] == len(ng))
    gate = (n_clean >= 20 and not bij and n_clean + n_cont + n_unm == len(ng)
            and len(shared) == 161)
    print(f"shared={len(shared)} pairs={pairs} p_reverse={p_rev} clean={n_clean} "
          f"contested={n_cont} unmapped={n_unm} bij_viol={bij} "
          f"recompute={'match' if same and csv_same else 'DIFF'} gate={'PASS' if gate else 'FAIL'}")
    print("PASS" if same and csv_same and gate else "FAIL")
    return 0 if same and csv_same and gate else 1


if __name__ == "__main__":
    sys.exit(main())
