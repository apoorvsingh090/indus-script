#!/usr/bin/env python3
"""Checker for L4-0002 — readable in one sitting.

Recomputes Sumerian windows, all three gates, and hidden-key recovery from
scratch; asserts key-sha commitment, shipped equality, and gate passage.
Usage: python check.py --splits <dir> --scratch <dir> --object <results.json> --baseline <sumer.json> --key <revealed key.json>
"""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
CLAIM = HERE
ROOT = CLAIM.parents[3]
sys.path.insert(0, str(HERE / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "benchmarks" / "baselines"))
sys.path.insert(0, str(ROOT / "claims" / "L1" / "L1-0001-rao-entropy-replication" / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L1" / "L1-0003-formulaic-ngrams" / "how-we-built-it"))

import models
from entropy_lib import corpus_stats, shuffled_C
from ng_lib import null_rep, repeated_counts
from sumer_lib import (KEY_SEED, KEY_SHA256, N_WINDOWS, encipher, fetch_zip, indus_lengths,
                       load_key, recover_topk, sign_texts, windows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--key", required=True)
    a = ap.parse_args()

    key = load_key(a.key)
    if hashlib.sha256(json.dumps(key).encode()).hexdigest() != KEY_SHA256:
        print("FAIL: key does not match preregistered commitment")
        return 1
    texts = sign_texts(fetch_zip(a.scratch))
    seqs, _ = windows(texts, indus_lengths(a.splits), N_WINDOWS, KEY_SEED)
    vocab = sorted({t for s in seqs for t in s})
    if len(vocab) != 370:
        print(f"FAIL: windowed vocab {len(vocab)} != committed V=370 (key would not fit)")
        return 1
    st = corpus_stats(seqs, len(vocab))
    nulls = sorted(shuffled_C(seqs, len(vocab), seed=KEY_SEED + 1, b=100))
    half, other = seqs[:974], seqs[974:]
    uni = models.Unigram()
    uni.fit([{"signs": s} for s in half])
    bg = models.Bigram(alpha=0.001)
    bg.fit([{"signs": s} for s in half])
    acc_u, pu = models.accuracy(uni, [{"signs": s} for s in other])
    acc_b, pb = models.accuracy(bg, [{"signs": s} for s in other])
    w = [len(s) for s in other]
    lo, hi, diff = models.paired_bootstrap_ci(pb, pu, w, seed=KEY_SEED + 2, b=1000)
    rep3 = repeated_counts(seqs, 3)[0]
    rep4 = repeated_counts(seqs, 4)[0]
    n3 = sorted(null_rep(seqs, 3, seed=KEY_SEED + 3, b=100))
    n4 = sorted(null_rep(seqs, 4, seed=KEY_SEED + 4, b=100))
    cyp, mp = encipher(seqs[974:], vocab, key)
    guess = recover_topk(seqs[:974], cyp)
    inv = {v: k for k, v in mp.items()}
    top = [t for t, _ in Counter(t for s in cyp for t in s).most_common(10)]
    hits = sum(1 for c in top if guess.get(c) == inv.get(c))

    o = json.loads(Path(a.object).read_text())
    same = (abs(st["C_cond_norm"] - o["ent"]["C"]) < 1e-9 and abs(diff - o["l2"]["diff"]) < 1e-9
            and rep3 == o["rep"]["rep3"] and rep4 == o["rep"]["rep4"]
            and hits == o["hidden_key"]["top10_hits"])
    gate = (st["C_cond_norm"] < nulls[0] and lo > 0 and diff > 0.01
            and rep3 > n3[-1] and rep4 > n4[-1] and hits >= 7)
    print(f"ENT {st['C_cond_norm']:.3f}<{nulls[0]:.3f} L2 d={diff:.4f} [{lo:.4f},{hi:.4f}] "
          f"REP {rep3}/{rep4} vs {n3[-1]}/{n4[-1]} KEY {hits}/10 recompute={'match' if same else 'DIFF'}")
    print("PASS" if same and gate else "FAIL")
    return 0 if same and gate else 1


if __name__ == "__main__":
    sys.exit(main())
