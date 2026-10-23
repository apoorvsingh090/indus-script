#!/usr/bin/env python3
"""Sweep runner for L4-0001. Run AFTER the preregistration commit.

Reuses FROZEN repo methods (benchmarks/baselines/models.py, L1-0001 entropy_lib,
L1-0003 ng_lib) on synthetic corpora — this calibrates the actual methods.
Writes object/results.json + baseline_snapshot/gates.json.
Usage: python run_cal.py <splits_dir> <scratch_dir> <claim_dir>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
CLAIM = HERE.parent
ROOT = CLAIM.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "benchmarks" / "baselines"))
sys.path.insert(0, str(ROOT / "claims" / "L1" / "L1-0001-rao-entropy-replication" / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L1" / "L1-0003-formulaic-ngrams" / "how-we-built-it"))

import models
from entropy_lib import corpus_stats, shuffled_C
from gen_synth import GEN_SEED, SIZES, build_family, fetch_words, indus_lengths
from ng_lib import null_rep, repeated_counts

ENT_B, REP_B, BOOT_B = 100, 100, 1000


def split_parts(seqs, seed):
    import random
    rng = random.Random(seed)
    idx = list(range(len(seqs)))
    rng.shuffle(idx)
    n = len(seqs)
    cut1, cut2 = int(0.6 * n), int(0.8 * n)
    get = lambda js: [{"signs": seqs[j]} for j in js]
    train, val, test = get(idx[:cut1]), get(idx[cut1:cut2]), get(idx[cut2:])
    seen = {" ".join(r["signs"]) for r in train}  # same leakage rule as splits v1
    excl = {"val": 0, "test": 0}
    for name, part in (("val", val), ("test", test)):
        keep = []
        for r in part:
            if " ".join(r["signs"]) in seen:
                excl[name] += 1
            else:
                keep.append(r)
        if name == "val":
            val = keep
        else:
            test = keep
    return train, val, test, excl


def run_cell(seqs, vocab, seed_base):
    st = corpus_stats(seqs, vocab)
    nulls = sorted(shuffled_C(seqs, vocab, seed=seed_base, b=ENT_B))
    ent_pass = st["C_cond_norm"] < nulls[0]
    train, val, test, excl = split_parts(seqs, seed_base + 1)
    uni = models.Unigram()
    uni.fit(train)
    scored = []
    for a in models.ALPHAS:
        bg = models.Bigram(alpha=a)
        bg.fit(train)
        acc, _ = models.accuracy(bg, val)
        scored.append((acc, a))
    best = min([s for s in scored if s[0] == max(x[0] for x in scored)], key=lambda s: s[1])
    bg = models.Bigram(alpha=best[1])
    bg.fit(train)
    acc_u, pu = models.accuracy(uni, test)
    acc_b, pb = models.accuracy(bg, test)
    w = [len(r["signs"]) for r in test]
    lo, hi, diff = models.paired_bootstrap_ci(pb, pu, w, seed=seed_base + 2, b=BOOT_B)
    l2_pass = lo > 0 and diff > 0.01
    rep3 = repeated_counts(seqs, 3)[0]
    rep4 = repeated_counts(seqs, 4)[0]
    n3 = sorted(null_rep(seqs, 3, seed=seed_base + 3, b=REP_B))
    n4 = sorted(null_rep(seqs, 4, seed=seed_base + 4, b=REP_B))
    rep_pass = rep3 > n3[-1] and rep4 > n4[-1]
    return {
        "n_texts": len(seqs), "vocab": vocab,
        "l2_excluded": excl,
        "ent": {"C": st["C_cond_norm"], "null_min": nulls[0], "pass": ent_pass},
        "l2": {"acc_u": acc_u, "acc_b": acc_b, "alpha": best[1], "diff": diff,
               "ci": [lo, hi], "pass": bool(l2_pass)},
        "rep": {"rep3": rep3, "rep4": rep4, "null3_max": n3[-1], "null4_max": n4[-1],
                "pass": rep_pass},
    }


def main() -> int:
    splits, scratch, claim = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    words = fetch_words(scratch)
    lens = indus_lengths(splits)
    out = {}
    for fi, fam in enumerate(("linguistic", "emblem")):
        fams = build_family(fam, words, lens, GEN_SEED + 100 * fi)
        out[fam] = {}
        for n in SIZES:
            seqs = fams[n]
            vocab = len({t for s in seqs for t in s})
            cell = run_cell(seqs, vocab, GEN_SEED + 100 * fi + n)
            out[fam][str(n)] = cell
            print(fam, n, {k: cell[k]["pass"] if k != "n_texts" else v
                            for k, v in cell.items() if k in ("ent", "l2", "rep")},
                  flush=True)
    (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
    (claim / "baseline_snapshot" / "gates.json").write_text(json.dumps(
        {"gate": "linguistic@1948 passes ENT+L2+REP; N_min reported; emblem reported",
         "ENT_B": ENT_B, "REP_B": REP_B, "BOOT_B": BOOT_B}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
