#!/usr/bin/env python3
"""Checker for L1-0001 — readable in one sitting.

Recomputes C_real from the corpus CSV and asserts the preregistered gate:
C_real < p0.5 percentile of the shipped shuffled null AND C_real < C_uniform.
Usage: python check.py --corpus <csv> --object <results.json> --baseline <nulls.json>
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "how-we-built-it"))
from entropy_lib import corpus_stats, load_sequences


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args()

    seqs, vocab = load_sequences(a.corpus)
    real = corpus_stats(seqs, vocab)
    obj = json.loads(Path(a.object).read_text())["real"]
    base = json.loads(Path(a.baseline).read_text())

    if abs(real["C_cond_norm"] - obj["C_cond_norm"]) > 1e-9:
        print(f"FAIL: recompute {real['C_cond_norm']:.6f} != shipped {obj['C_cond_norm']:.6f}")
        return 1
    p05 = sorted(base["C_sorted"])[0]  # B=200 -> min ~= 0.5th percentile
    ok = real["C_cond_norm"] < p05 and real["C_cond_norm"] < base["C_uniform"]
    print(f"C_real={real['C_cond_norm']:.4f} p0.5={p05:.4f} uniform={base['C_uniform']:.4f}")
    print("PASS" if ok else "FAIL: gate not met")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
