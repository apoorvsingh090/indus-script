#!/usr/bin/env python3
"""Checker for L4-0008 - readable in one sitting.

Rebuilds the 1948 Sumerian windows (same protocol as L4-0002, no key),
recomputes n80_begin / n80_end (definitions identical to L1-0002b pos_lib),
regenerates the B=200 paired token-shuffle null (seed 260417840), and gates:
|n80_begin - n80_end| > null max of the same asymmetry index.
Usage: python check.py --splits <dir> --scratch <dir> --object <results.json> --baseline <nulls.json>
"""
import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
CLAIM = HERE
ROOT = CLAIM.parents[2]
sys.path.insert(0, str(HERE / "how-we-built-it"))
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
    for x in ("splits", "scratch", "object", "baseline"):
        ap.add_argument("--" + x, required=True)
    a = ap.parse_args()

    texts = sign_texts(fetch_zip(a.scratch))
    seqs, _ = windows(texts, indus_lengths(a.splits), N_WINDOWS, KEY_SEED)
    vocab = sorted({t for s in seqs for t in s})
    if len(vocab) != 370:
        print(f"FAIL: vocab {len(vocab)} != 370")
        return 1
    st = pos_stats(seqs)
    n80_begin, n80_end, n80_all = st["n80_begin"], st["n80_end"], st["n80_all"]
    gap = abs(n80_begin - n80_end)
    d_list, b_list, e_list = null_battery(seqs, POS_NULL_SEED, B)
    d_max = max(d_list)

    o = json.loads(Path(a.object).read_text())
    same = (o["n80_begin"] == n80_begin and o["n80_end"] == n80_end
            and o["n80_all"] == n80_all and o["null_D_max"] == d_max)
    ok = same and gap > d_max
    print(f"n80 begin={n80_begin} end={n80_end} all={n80_all} gap={gap} "
          f"null_D_max={d_max} recompute={'match' if same else 'DIFF'}")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
