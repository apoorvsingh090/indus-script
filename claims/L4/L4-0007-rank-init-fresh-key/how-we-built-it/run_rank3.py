#!/usr/bin/env python3
"""Generator for L4-0007. Run AFTER the preregistration commit.

Same Sumerian windows + halves as L4-0002 (window seed 260417835), fresh
sealed key3 (sha committed at prereg, passed via --key). Exact-rank
(rank_init) recovery only, per prereg spec. Writes object/results.json,
object/key3.json (reveal), and baseline_snapshot/recovery.json.
Usage: python run_rank3.py <splits> <scratch> <claim> --key <key3.json>
"""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
CLAIM = HERE.parent
ROOT = CLAIM.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0002-sumerian-hidden-key" / "how-we-built-it"))

from rank_lib import rank_init
from sumer_lib import KEY_SEED, N_WINDOWS, encipher, fetch_zip, indus_lengths, sign_texts, windows

KEY3_SHA256 = "3492a0775fed6bd6cddc120dc33e64fb454fb90ecc7aedde4c60b4bb96d5027d"
KEY3_SEED_BASE = 260417839


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("splits")
    ap.add_argument("scratch")
    ap.add_argument("claim")
    ap.add_argument("--key", required=True)
    a = ap.parse_args()
    claim = Path(a.claim)

    key = json.load(open(a.key))
    assert hashlib.sha256(json.dumps(key).encode()).hexdigest() == KEY3_SHA256, "key3 mismatch"
    assert _recipe(KEY3_SEED_BASE) == key, "key3 != disclosed recipe"

    texts = sign_texts(fetch_zip(a.scratch))
    seqs, _ = windows(texts, indus_lengths(a.splits), N_WINDOWS, KEY_SEED)
    vocab = sorted({t for s in seqs for t in s})
    assert len(vocab) == 370, len(vocab)
    ref, cyp_plain = seqs[:974], seqs[974:]
    cyp, mp = encipher(cyp_plain, vocab, key)
    inv = {v: k for k, v in mp.items()}
    init = rank_init(ref, cyp, vocab, vocab)
    top = [t for t, _ in Counter(t for s in cyp for t in s).most_common(10)]
    hits = sum(1 for c in top if vocab[init[vocab.index(c)]] == inv[c])
    full = sum(1 for i, c in enumerate(vocab) if vocab[init[i]] == inv[c])
    out = {"vocab": len(vocab), "rank_top10": hits, "rank_full": full,
           "key_seed_base": KEY3_SEED_BASE, "window_seed": KEY_SEED,
           "n_windows": len(seqs), "n_ref": len(ref), "n_cipher": len(cyp_plain),
           "pass": bool(hits >= 7)}
    (claim / "object").mkdir(parents=True, exist_ok=True)
    (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
    (claim / "object" / "key3.json").write_text(json.dumps(key))
    (claim / "baseline_snapshot").mkdir(parents=True, exist_ok=True)
    (claim / "baseline_snapshot" / "recovery.json").write_text(json.dumps(
        {"key3_sha256": KEY3_SHA256, "bar": "top10 >= 7", "method": "rank_init only"}, indent=2))
    print(f"rank-init top10={hits}/10 full={full}/370")
    return 0


def _recipe(seed_base):
    import random
    rng = random.Random(seed_base + 370)
    k = list(range(370))
    rng.shuffle(k)
    return k


if __name__ == "__main__":
    sys.exit(main())
