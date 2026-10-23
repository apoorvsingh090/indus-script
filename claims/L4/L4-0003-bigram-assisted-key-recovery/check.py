#!/usr/bin/env python3
"""Checker for L4-0003 — readable in one sitting.

Rebuilds the frozen L4-0002 key-arm inputs (zip fetch, sign streams, 1948
windows @ seed 260417835 on splits/v1 lengths, V=370, 974/974 halves),
asserts the committed-key sha, runs the frozen bigram-assisted recovery on
the committed + two alternate keys, and asserts (a) recomputation matches
object/results.json exactly and (b) the preregistered gate outcome.

Usage: python check.py --splits <dir> --scratch <dir> --object <results.json> --baseline <l40003.json> --key <key.json>
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0002-sumerian-hidden-key" / "how-we-built-it"))

from sumer_lib import KEY_SEED, KEY_SHA256, N_WINDOWS, encipher, fetch_zip, indus_lengths, \
    load_key, make_key, sign_texts, windows
from recover_lib import recover, top10_hits


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
    base = json.loads(Path(a.baseline).read_text())
    if base.get("key_sha256") != KEY_SHA256 or base.get("l4_0002_rank_only_top10_hits") != 5:
        print("FAIL: baseline snapshot does not pin the L4-0002 chain")
        return 1
    texts = sign_texts(fetch_zip(a.scratch))
    seqs, _ = windows(texts, indus_lengths(a.splits), N_WINDOWS, KEY_SEED)
    vocab = sorted({t for s in seqs for t in s})
    if len(vocab) != 370:
        print(f"FAIL: windowed vocab {len(vocab)} != 370")
        return 1

    hits = {}
    for name, k in (("committed", key), ("alt1", make_key(370, KEY_SEED + 9000)),
                    ("alt2", make_key(370, KEY_SEED + 9001))):
        cyp, mp = encipher(seqs[974:], vocab, k)
        guess, _ = recover(seqs[:974], cyp, vocab)
        hits[name] = top10_hits(guess, cyp, {v: kk for kk, v in mp.items()})

    o = json.loads(Path(a.object).read_text())
    same = all(hits[n] == o["recovery"][n]["top10_hits"] for n in hits) \
        and sum(1 for h in hits.values() if h >= 7) == o["recovery"]["keys_ge7"]
    n_pass = sum(1 for h in hits.values() if h >= 7)
    gate = hits["committed"] >= 7 and n_pass >= 2
    gate_same = gate == o["gate"]["pass"]
    print(f"KEY committed {hits['committed']}/10 alt1 {hits['alt1']}/10 alt2 {hits['alt2']}/10 "
          f"(ge7: {n_pass}) recompute={'match' if same else 'DIFF'} gate={gate}")
    print("PASS" if same and gate_same else "FAIL")
    return 0 if same and gate_same else 1


if __name__ == "__main__":
    sys.exit(main())
