#!/usr/bin/env python3
"""Generator for L4-0003. Run AFTER the preregistration commit.

Rebuilds the frozen L4-0002 key arm inputs bit-exactly (same zip fetch,
sign_texts, 1948 windows @ seed 260417835, splits/v1 lengths, V=370,
974/974 halves), then runs the frozen bigram-assisted recovery
(recover_lib.recover) on the committed key plus the two preregistered
alternate keys, evaluates the 7/10 top-10 bar, and writes
object/results.json + baseline_snapshot/l40003.json.

Usage: python run_l40003.py <splits_dir> <scratch_dir> <claim_dir> --key <key.json>
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
CLAIM = HERE.parent
ROOT = CLAIM.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0002-sumerian-hidden-key" / "how-we-built-it"))

from sumer_lib import KEY_SEED, KEY_SHA256, N_WINDOWS, encipher, fetch_zip, indus_lengths, \
    load_key, make_key, sign_texts, windows
from recover_lib import recover, top10_hits


def arm(seqs, vocab, key):
    """Encipher second half under key, recover from first half, score."""
    half_a, half_b = seqs[:974], seqs[974:]
    cyp, mp = encipher(half_b, vocab, key)
    inv = {v: k for k, v in mp.items()}
    guess, diag = recover(half_a, cyp, vocab)
    hits = top10_hits(guess, cyp, inv)
    full = sum(1 for c in vocab if guess.get(c) == inv.get(c)) / len(vocab)
    return hits, full, diag["accepted_swaps"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("splits")
    ap.add_argument("scratch")
    ap.add_argument("claim")
    ap.add_argument("--key", required=True)
    a = ap.parse_args()
    splits, claim = Path(a.splits), Path(a.claim)

    key = load_key(a.key)
    assert hashlib.sha256(json.dumps(key).encode()).hexdigest() == KEY_SHA256, "key mismatch"
    texts = sign_texts(fetch_zip(a.scratch))
    seqs, wrap_rate = windows(texts, indus_lengths(splits), N_WINDOWS, KEY_SEED)
    vocab = sorted({t for s in seqs for t in s})
    assert len(vocab) == 370, f"windowed vocab {len(vocab)} != 370"

    alt1 = make_key(370, KEY_SEED + 9000)
    alt2 = make_key(370, KEY_SEED + 9001)

    hits_c, full_c, swaps_c = arm(seqs, vocab, key)
    hits_1, full_1, swaps_1 = arm(seqs, vocab, alt1)
    hits_2, full_2, swaps_2 = arm(seqs, vocab, alt2)
    arms = {"committed": hits_c, "alt1": hits_1, "alt2": hits_2}
    n_pass = sum(1 for h in arms.values() if h >= 7)
    gate_pass = hits_c >= 7 and n_pass >= 2

    out = {
        "n_texts": len(seqs), "vocab": len(vocab), "wrap_rate": wrap_rate,
        "committed_key_sha256": KEY_SHA256,
        "recovery": {
            "committed": {"top10_hits": hits_c, "full_key_acc": full_c, "accepted_swaps": swaps_c},
            "alt1": {"top10_hits": hits_1, "full_key_acc": full_1, "accepted_swaps": swaps_1},
            "alt2": {"top10_hits": hits_2, "full_key_acc": full_2, "accepted_swaps": swaps_2},
            "keys_ge7": n_pass,
        },
        "gate": {"bar": ">=7/10 top-10 exact on committed AND >=2 of 3 keys >=7",
                 "pass": bool(gate_pass)},
        "l4_0002_baseline_top10_hits": 5,
    }
    (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
    (claim / "baseline_snapshot" / "l40003.json").write_text(json.dumps(
        {"key_sha256": KEY_SHA256, "n": N_WINDOWS, "l4_0002_rank_only_top10_hits": 5}, indent=2))
    print(f"committed {hits_c}/10 (full {full_c:.3f}, swaps {swaps_c}) "
          f"alt1 {hits_1}/10 alt2 {hits_2}/10 -> keys_ge7={n_pass} "
          f"gate={'PASS' if gate_pass else 'FAIL'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
