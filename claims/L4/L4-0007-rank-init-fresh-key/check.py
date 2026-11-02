#!/usr/bin/env python3
"""Checker for L4-0007 - readable in one sitting.

Recomputes Sumerian windows, cipher, and exact-rank (rank_init) recovery from
scratch; asserts key-sha commitment, recompute-vs-object equality, top10 >= 7.
Usage: python check.py --splits <dir> --scratch <dir> --object <results.json> --baseline <recovery.json> --key <revealed key3.json>
"""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
CLAIM = HERE
ROOT = CLAIM.parents[2]
sys.path.insert(0, str(HERE / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0002-sumerian-hidden-key" / "how-we-built-it"))

from rank_lib import rank_init
from sumer_lib import KEY_SEED, N_WINDOWS, encipher, fetch_zip, indus_lengths, sign_texts, windows

KEY3_SHA256 = "3492a0775fed6bd6cddc120dc33e64fb454fb90ecc7aedde4c60b4bb96d5027d"


def main() -> int:
    ap = argparse.ArgumentParser()
    for x in ("splits", "scratch", "object", "baseline", "key"):
        ap.add_argument("--" + x, required=True)
    a = ap.parse_args()

    key = json.load(open(a.key))
    if hashlib.sha256(json.dumps(key).encode()).hexdigest() != KEY3_SHA256:
        print("FAIL: key3 does not match preregistered commitment")
        return 1
    texts = sign_texts(fetch_zip(a.scratch))
    seqs, _ = windows(texts, indus_lengths(a.splits), N_WINDOWS, KEY_SEED)
    vocab = sorted({t for s in seqs for t in s})
    if len(vocab) != 370:
        print(f"FAIL: vocab {len(vocab)} != 370")
        return 1
    ref, cyp_plain = seqs[:974], seqs[974:]
    cyp, mp = encipher(cyp_plain, vocab, key)
    inv = {v: k for k, v in mp.items()}
    init = rank_init(ref, cyp, vocab, vocab)
    top = [t for t, _ in Counter(t for s in cyp for t in s).most_common(10)]
    hits = sum(1 for c in top if vocab[init[vocab.index(c)]] == inv[c])
    full = sum(1 for i, c in enumerate(vocab) if vocab[init[i]] == inv[c])

    o = json.loads(Path(a.object).read_text())
    same = (hits == o["rank_top10"] and full == o["rank_full"] and o["vocab"] == len(vocab))
    ok = same and hits >= 7
    print(f"rank-init top10={hits}/10 full={full}/370 key-sha=match "
          f"recompute={'match' if same else 'DIFF'}")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
