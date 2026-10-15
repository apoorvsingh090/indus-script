#!/usr/bin/env python3
"""Checker for L2-0001 — readable in one sitting.

Refits all models from the frozen splits and asserts the preregistered gate:
paired-bootstrap 95% CI lower bound > 0 AND point diff > 0.01 on TEST.
Usage: python check.py --splits <dir> --object <results.json> --baseline <unigram.json>
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "benchmarks" / "baselines"))
from models import ALPHAS, Bigram, Positional, Unigram, accuracy, load_split, paired_bootstrap_ci


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args()

    sp = Path(a.splits)
    train, val, test = (load_split(sp / f"{n}.jsonl") for n in ("train", "val", "test"))
    uni = Unigram()
    uni.fit(train)
    scored = []
    for al in ALPHAS:
        bg = Bigram(alpha=al)
        bg.fit(train)
        acc, _ = accuracy(bg, val)
        scored.append((acc, al))
    best = min([s for s in scored if s[0] == max(x[0] for x in scored)], key=lambda s: s[1])
    bg = Bigram(alpha=best[1])
    bg.fit(train)
    acc_u, pu = accuracy(uni, test)
    acc_b, pb = accuracy(bg, test)
    w = [len(r["signs"]) for r in test]
    lo, hi, diff = paired_bootstrap_ci(pb, pu, w)

    obj = json.loads(Path(a.object).read_text())
    base = json.loads(Path(a.baseline).read_text())
    ship = obj["comparison"]
    if abs(diff - ship["diff_bigram_minus_unigram"]) > 1e-9 or best[1] != ship["alpha_selected"]:
        print("FAIL: recompute differs from shipped (diff or alpha)")
        return 1
    if abs(acc_u - base["test_acc"]) > 1e-12:
        print("FAIL: unigram baseline differs")
        return 1
    ok = lo > 0 and diff > 0.01
    print(f"unigram={acc_u:.4f} bigram(a={best[1]})={acc_b:.4f} diff={diff:.4f} CI=[{lo:.4f},{hi:.4f}]")
    print("PASS" if ok else "FAIL: gate not met")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
