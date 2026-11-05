#!/usr/bin/env python3
"""POST-HOC composition diagnostic for L4-0009 half B (archivist, 2026-11-05).

Driven by the two fresh-context skeptics (sk9-A, sk9-B) and folded into the
verified-negative claim as an exploratory addendum. This script does NOT
re-run recovery and does NOT alter the frozen verdict in any way; it only
measures *composition* statistics of cipher half B vs half A to explain
why the committed key's decoded bigrams support recovery less well on B.

Cell #4 is rebuilt exactly as in run_l40009.py (same seeds, same vocab
assert, committed key sha asserted). Window wrap flags are recovered by
mirroring the sumer_lib.windows() RNG stream deterministically (asserted
against the real output).

All cipher-arm metrics are computed on the ENCRYPTED windows (as in the
recovery), decoded with the committed key's inverse map:
  - distinct/covered types are decoded (plaintext-side) types
  - ref-bigram coherence: share of decoded adjacent token pairs that occur
    anywhere in the reference bigrams, counted per pair occurrence
  - per-window coherence mean / median / q1 / q3
  - coherence restricted to non-wrapped windows (wrap flags inherited from
    the 1:1 plaintext-ciphertext window correspondence)

Usage: python diag_half_b_composition.py <splits_dir> <scratch_dir> <claim_dir>
"""
import hashlib
import json
import random
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
CLAIM = HERE.parent
ROOT = CLAIM.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0002-sumerian-hidden-key" / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0003-bigram-assisted-key-recovery" / "how-we-built-it"))

from sumer_lib import encipher, fetch_zip, indus_lengths, make_key, sign_texts, windows  # noqa: E402
from l40009_lib import GATE_KEYS, NREF, N_WINDOWS, V_U9, WIN_CYP9, WIN_REF9, pools  # noqa: E402

HALF = 487
COMMITTED_SHA = "d602af01cbaa8680363c211e60fab0af1484610799ad27d4c3c6051374bc50c3"


def window_flags(texts, lens, seed, n):
    """Mirror sumer_lib.windows() RNG exactly; return (seqs, wrapped_flags)."""
    rng = random.Random(seed)
    weights = [len(t) for t in texts]
    total = sum(weights)
    seqs, flags = [], []
    for _ in range(n):
        x = rng.randrange(total)
        acc, ti = 0, 0
        for i, w in enumerate(weights):
            acc += w
            if x < acc:
                ti = i
                break
        t = texts[ti]
        L = lens[rng.randrange(len(lens))]
        off = rng.randrange(len(t))
        seqs.append([t[(off + k) % len(t)] for k in range(L)])
        flags.append(off + L > len(t))
    return seqs, flags


def bigrams(ref_seqs):
    return {(p, q) for s in ref_seqs for p, q in zip(s, s[1:])}


def arm_stats(name, cyp_arm, flags, inv, ref_bi, ref_count):
    """Cipher-side arm: decode with inv, compare against ref bigrams."""
    tok_n = sum(len(s) for s in cyp_arm)
    dec_types = {inv[t] for s in cyp_arm for t in s}
    per_win = []
    hits = 0
    for s in cyp_arm:
        pairs = list(zip(s, s[1:]))
        h = sum(1 for p, q in pairs if (inv[p], inv[q]) in ref_bi)
        hits += h
        per_win.append(h / len(pairs) if pairs else 0.0)
    unw_hits, unw_pairs = 0, 0
    for s, wr in zip(cyp_arm, flags):
        if not wr:
            pairs = list(zip(s, s[1:]))
            unw_pairs += len(pairs)
            unw_hits += sum(1 for p, q in pairs if (inv[p], inv[q]) in ref_bi)
    qu = statistics.quantiles(per_win, n=4)
    tail = sum(1 for s in cyp_arm for i, _ in enumerate(s) if i >= 7)
    mass = sum(ref_count.get(inv[t], 0) for s in cyp_arm for t in s)
    return {
        "arm": name,
        "windows": len(cyp_arm),
        "wrapped_windows": sum(1 for f in flags if f),
        "mean_len": round(tok_n / len(cyp_arm), 2),
        "tokens": tok_n,
        "distinct_decoded_types": len(dec_types),
        "decoded_types_covered_ge1": sum(1 for t in dec_types if t in ref_count),
        "decoded_types_covered_ge5": sum(1 for t in dec_types if ref_count.get(t, 0) >= 5),
        "bigram_coherence": round(hits / sum(len(s) - 1 for s in cyp_arm), 4),
        "bigram_coherence_unwrapped": round(unw_hits / unw_pairs, 4) if unw_pairs else None,
        "per_window_mean": round(statistics.mean(per_win), 4),
        "per_window_median": round(statistics.median(per_win), 4),
        "per_window_q1": round(qu[0], 4),
        "per_window_q3": round(qu[2], 4),
        "per_window_mean_unwrapped": round(
            statistics.mean(c for c, w in zip(per_win, flags) if not w), 4),
        "tail_share_ge7": round(tail / tok_n, 4),
        "ref_token_mass_per_token": round(mass / tok_n, 2),
    }


if __name__ == "__main__":
    splits, scratch, in_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    key = make_key(V_U9, GATE_KEYS["committed"])
    assert hashlib.sha256(json.dumps(key).encode()).hexdigest() == COMMITTED_SHA

    texts = sign_texts(fetch_zip(scratch))
    poolA, poolB = pools(texts)
    lens = indus_lengths(splits)
    ref_all, wrap_r = windows(poolA, lens, N_WINDOWS, WIN_REF9)
    cyp_plain, wrap_c = windows(poolB, lens, N_WINDOWS, WIN_CYP9)
    vocab = sorted({t for s in ref_all + cyp_plain for t in s})
    assert len(vocab) == V_U9 and wrap_c > 0

    my_cyp, my_flags = window_flags(poolB, lens, WIN_CYP9, N_WINDOWS)
    my_ref, my_rflags = window_flags(poolA, lens, WIN_REF9, N_WINDOWS)
    assert my_cyp == cyp_plain and my_ref == ref_all, "RNG mirror diverged"

    cyp, mp = encipher(cyp_plain, vocab, key)
    inv = {v: k for k, v in mp.items()}
    ref = ref_all[:NREF]
    ref_bi = bigrams(ref)
    ref_count = {}
    for s in ref:
        for t in s:
            ref_count[t] = ref_count.get(t, 0) + 1

    out = {
        "meta": {"post_hoc": True, "purpose": "composition addendum; frozen verdict unchanged",
                 "cell": "4 (V_U9=371)", "key": "committed",
                 "decoded_pairs_checked": "within-window adjacency, as in the recovery objective",
                 "ref_bigram_inventory": len(ref_bi),
                 "note": "cipher arms measured on ENCRYPTED windows decoded by the committed key",
                 "wrap_rates_ref_cyp": [round(wrap_r, 4), round(wrap_c, 4)]},
        "arms": [
            arm_stats("A", cyp[:HALF], my_flags[:HALF], inv, ref_bi, ref_count),
            arm_stats("B", cyp[HALF:], my_flags[HALF:], inv, ref_bi, ref_count),
            arm_stats("full", cyp, my_flags, inv, ref_bi, ref_count),
        ],
        "ref_arm": {"windows": len(ref),
                    "wrapped_windows": sum(1 for f in my_rflags[:NREF] if f)},
    }
    print(json.dumps(out["arms"], indent=2))
    print("mirror OK; ref wrap", round(wrap_r, 4), "cyp wrap", round(wrap_c, 4))
    target = Path(in_dir)
    (target / "object" / "diag_half_b.json").write_text(json.dumps(out, indent=2))
    print("wrote", target / "object" / "diag_half_b.json")
