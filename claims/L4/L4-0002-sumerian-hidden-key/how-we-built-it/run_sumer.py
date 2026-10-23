#!/usr/bin/env python3
"""Generator for L4-0002. Run AFTER the preregistration commit.

Builds Sumerian sign windows, runs the three frozen gates at N=1948, then the
hidden-key test (key from --key: builder-local pre-reveal path; sha committed
at prereg). Writes object/results.json (+ object/key.json reveal) and
baseline_snapshot/sumer.json.
Usage: python run_sumer.py <splits> <scratch> <claim> --key <key.json>
"""
import hashlib
import json
import sys
from collections import Counter
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
from ng_lib import null_rep, repeated_counts
from sumer_lib import (KEY_SEED, KEY_SHA256, N_WINDOWS, encipher, fetch_zip, indus_lengths,
                       load_key, recover_topk, sign_texts, windows)


def main() -> int:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("splits")
    ap.add_argument("scratch")
    ap.add_argument("claim")
    ap.add_argument("--key", required=True)
    a = ap.parse_args()
    splits, claim = Path(a.splits), Path(a.claim)

    key = load_key(a.key)
    assert hashlib.sha256(json.dumps(key).encode()).hexdigest() == KEY_SHA256, "key mismatch"
    texts = sign_texts(fetch_zip(a.scratch))
    lens = indus_lengths(splits)
    seqs, wrap_rate = windows(texts, lens, N_WINDOWS, KEY_SEED)
    vocab = sorted({t for s in seqs for t in s})

    st = corpus_stats(seqs, len(vocab))
    nulls = sorted(shuffled_C(seqs, len(vocab), seed=KEY_SEED + 1, b=100))
    ent_pass = st["C_cond_norm"] < nulls[0]
    half, other = seqs[:974], seqs[974:]
    uni = models.Unigram()
    uni.fit([{"signs": s} for s in half])
    # Halves double as train/test (no val split on the real-script cell);
    # alpha fixed to the L2-0001 production value 0.001 (stated deviation).
    bg = models.Bigram(alpha=0.001)
    bg.fit([{"signs": s} for s in half])
    acc_u, pu = models.accuracy(uni, [{"signs": s} for s in other])
    acc_b, pb = models.accuracy(bg, [{"signs": s} for s in other])
    w = [len(s) for s in other]
    lo, hi, diff = models.paired_bootstrap_ci(pb, pu, w, seed=KEY_SEED + 2, b=1000)
    l2_pass = lo > 0 and diff > 0.01
    rep3 = repeated_counts(seqs, 3)[0]
    rep4 = repeated_counts(seqs, 4)[0]
    n3 = sorted(null_rep(seqs, 3, seed=KEY_SEED + 3, b=100))
    n4 = sorted(null_rep(seqs, 4, seed=KEY_SEED + 4, b=100))
    rep_pass = rep3 > n3[-1] and rep4 > n4[-1]

    half_a, half_b = seqs[:974], seqs[974:]
    cyp, mp = encipher(half_b, vocab, key)
    guess = recover_topk(half_a, cyp)
    inv = {v: k for k, v in mp.items()}
    top_cyp = [t for t, _ in Counter(t for s in cyp for t in s).most_common(10)]
    hits = sum(1 for c in top_cyp if guess.get(c) == inv.get(c))
    key_pass = hits >= 7

    out = {
        "n_texts": len(seqs), "vocab": len(vocab), "wrap_rate": wrap_rate,
        "mean_len": sum(len(s) for s in seqs) / len(seqs),
        "ent": {"C": st["C_cond_norm"], "null_min": nulls[0], "pass": ent_pass},
        "l2": {"acc_u": acc_u, "acc_b": acc_b, "diff": diff, "ci": [lo, hi], "pass": bool(l2_pass)},
        "rep": {"rep3": rep3, "rep4": rep4, "null3_max": n3[-1], "null4_max": n4[-1], "pass": rep_pass},
        "hidden_key": {"top10_hits": hits, "pass": bool(key_pass)},
    }
    (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
    (claim / "object" / "key.json").write_text(json.dumps(key))
    (claim / "baseline_snapshot" / "sumer.json").write_text(json.dumps(
        {"key_sha256": KEY_SHA256, "n": N_WINDOWS, "texts_available": len(texts)}, indent=2))
    print(f"vocab={len(vocab)} meanlen={out['mean_len']:.2f} wrap={wrap_rate:.3f}")
    print(f"ENT {out['ent']['C']:.3f}<{out['ent']['null_min']:.3f} L2 d={diff:.4f} [{lo:.4f},{hi:.4f}] "
          f"REP {rep3}/{rep4} vs {n3[-1]}/{n4[-1]} KEY {hits}/10")
    return 0


if __name__ == "__main__":
    sys.exit(main())
