#!/usr/bin/env python3
"""Checker for L1-0004 — readable in one sitting.

Recomputes real + synthetic (seeded) points and asserts d >= 0.05
(Sproat-style iid-Zipf counterexample distinguishable).
Usage: python check.py --corpus <csv> --object <results.json> --baseline <real_point.json>
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "how-we-built-it"))
from zipf_lib import load_oriented, mm_point, synth_zipf, zipf_s_ols


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args()

    seqs, vocab = load_oriented(a.corpus)
    h1r, cr = mm_point(seqs, vocab)
    obj = json.loads(Path(a.object).read_text())
    base = json.loads(Path(a.baseline).read_text())["real"]

    if abs(h1r - base["H1n"]) > 1e-9 or abs(cr - base["C"]) > 1e-9:
        print("FAIL: real-point recompute differs from shipped baseline")
        return 1
    s = zipf_s_ols(seqs)
    syn = synth_zipf([len(x) for x in seqs], vocab, s)
    h1z, cz = mm_point(syn, vocab)
    d = max(abs(h1z - h1r), abs(cz - cr))
    if abs(d - obj["d"]) > 1e-9:
        print(f"FAIL: recompute d={d:.6f} != shipped {obj['d']:.6f}")
        return 1
    print(f"s={s:.4f} real=({h1r:.4f},{cr:.4f}) synth=({h1z:.4f},{cz:.4f}) d={d:.4f}")
    print("PASS: distinguishable" if d >= 0.05 else "FAIL: gate not met (counterexample succeeds)")
    return 0 if d >= 0.05 else 1


if __name__ == "__main__":
    sys.exit(main())
