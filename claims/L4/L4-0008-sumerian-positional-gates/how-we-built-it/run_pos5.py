#!/usr/bin/env python3
"""Generator for L4-0008. Run AFTER the preregistration commit.

Same 1948 Sumerian windows as L4-0002 (window seed 260417835, both halves
pooled, no key). n80 machinery imported unchanged from the verified
L1-0002b pos_lib. Paired B=200 token-shuffle null (seed 260417840) mirroring
pos_lib.null_n80_end, extended to compute begin and end per draw.
Writes object/results.json and baseline_snapshot/nulls.json.
Usage: python run_pos5.py <splits> <scratch> <claim>
"""
import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
CLAIM = HERE.parent
ROOT = CLAIM.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0002-sumerian-hidden-key" / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L1" / "L1-0002b-positional-corrected-order" / "how-we-built-it"))

from pos_lib import n80, pos_stats
from sumer_lib import KEY_SEED, N_WINDOWS, fetch_zip, indus_lengths, sign_texts, windows

POS_NULL_SEED = 260417840
B = 200


def null_battery(seqs, seed, b):
    rng = random.Random(seed)
    lens = [len(s) for s in seqs]
    pool = [t for s in seqs for t in s]
    d_list, b_list, e_list = [], [], []
    for _ in range(b):
        rng.shuffle(pool)
        it = iter(pool)
        sh = [[next(it) for _ in range(k)] for k in lens]
        beg = Counter(s[0] for s in sh)
        end = Counter(s[-1] for s in sh if len(s) > 1)
        nb, ne = n80(beg), n80(end)
        b_list.append(nb)
        e_list.append(ne)
        d_list.append(abs(nb - ne))
    return d_list, b_list, e_list


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("splits")
    ap.add_argument("scratch")
    ap.add_argument("claim")
    a = ap.parse_args()
    claim = Path(a.claim)

    texts = sign_texts(fetch_zip(a.scratch))
    seqs, _ = windows(texts, indus_lengths(a.splits), N_WINDOWS, KEY_SEED)
    vocab = sorted({t for s in seqs for t in s})
    assert len(vocab) == 370, len(vocab)
    st = pos_stats(seqs)
    gap = abs(st["n80_begin"] - st["n80_end"])
    d_list, b_list, e_list = null_battery(seqs, POS_NULL_SEED, B)
    out = {"n_texts": st["n_texts"], "vocab": st["vocab"], "n_tokens": sum(len(s) for s in seqs),
           "n80_all": st["n80_all"], "n80_begin": st["n80_begin"], "n80_end": st["n80_end"],
           "asym_gap": gap, "null_D_max": max(d_list), "null_D_min": min(d_list),
           "null_begin_min": min(b_list), "null_begin_max": max(b_list),
           "null_end_min": min(e_list), "null_end_max": max(e_list),
           "top_begin": st["top_begin"], "top_end": st["top_end"],
           "null_seed": POS_NULL_SEED, "window_seed": KEY_SEED, "b": B,
           "pass": bool(gap > max(d_list))}
    (claim / "object").mkdir(parents=True, exist_ok=True)
    (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
    (claim / "baseline_snapshot").mkdir(parents=True, exist_ok=True)
    (claim / "baseline_snapshot" / "nulls.json").write_text(json.dumps(
        {"method": "permute tokens across fixed window lengths (pooled halves, no key)",
         "B": B, "seed": POS_NULL_SEED,
         "D_sorted": sorted(d_list), "n80_begin_sorted": sorted(b_list),
         "n80_end_sorted": sorted(e_list)}, indent=2))
    print(f"n80 begin={st['n80_begin']} end={st['n80_end']} all={st['n80_all']} "
          f"gap={gap} null_D_max={max(d_list)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
