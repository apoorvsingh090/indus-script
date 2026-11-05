#!/usr/bin/env python3
"""Generator for L4-0010. Run only AFTER the preregistration commit.

Fresh cell #5 -> gate v2 (matched-scale half nulls + token-weighted
guard). Writes object/results.json + baseline_snapshot/gate10.json.
Runtime ~1h45 (54 climbs) single-process. Prints progress.

Usage: python run_l40010.py <splits_dir> <scratch_dir> <claim_dir>
"""
import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
CLAIM = HERE.parent
ROOT = CLAIM.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0002-sumerian-hidden-key" / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0003-bigram-assisted-key-recovery" / "how-we-built-it"))

from sumer_lib import encipher, fetch_zip, indus_lengths, make_key, sign_texts, windows  # noqa: E402
from recover_lib import top10_hits  # noqa: E402
from l40010_lib import (ALPHA, DEV_KEY_SEED, DEV_NREF, GATE_KEYS, K_NULLS, NREF,  # noqa: E402
                        N_WINDOWS, RATIO_COMMITTED, RATIO_KEY, RATIO_TW, V_U10,
                        WIN_CYP10, WIN_REF10, gate_verdict_v2, null_reference,
                        pools, recover_best, ref_bigrams, token_weighted)


def arm(ref, cyp_seqs, vocab, key, alpha=ALPHA, multistart=True):
    cyp, mp = encipher(cyp_seqs, vocab, key)
    inv = {v: k for k, v in mp.items()}
    guess, diag = recover_best(ref, cyp, vocab, alpha, multistart=multistart)
    return {
        "top10_hits": top10_hits(guess, cyp, inv),
        "full": sum(1 for c in vocab if guess.get(c) == inv.get(c)) / len(vocab),
        "token_weighted": token_weighted(cyp_seqs, vocab, guess, inv),
        **diag,
    }


def window_flags(texts, lens, seed, n):
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("splits")
    ap.add_argument("scratch")
    ap.add_argument("claim")
    a = ap.parse_args()
    claim = Path(a.claim)

    for name, seed in list(GATE_KEYS.items()) + [("dev", DEV_KEY_SEED)]:
        k = make_key(V_U10, seed)
        got = hashlib.sha256(json.dumps(k).encode()).hexdigest()
        assert got == KEY_SHAS[name], f"{name} key sha {got} != commitment"

    texts = sign_texts(fetch_zip(a.scratch))
    poolA, poolB = pools(texts)
    lens = indus_lengths(a.splits)
    ref_all, wrap_r = windows(poolA, lens, N_WINDOWS, WIN_REF10)
    cyp_seqs, wrap_c = windows(poolB, lens, N_WINDOWS, WIN_CYP10)
    vocab = sorted({t for s in ref_all + cyp_seqs for t in s})
    assert len(vocab) == V_U10, f"union vocab {len(vocab)} != {V_U10}"
    ref = ref_all[:NREF]
    ref_bi = ref_bigrams(ref)
    my_c, my_f = window_flags(poolB, lens, WIN_CYP10, N_WINDOWS)
    assert my_c == cyp_seqs, "window mirror diverged"
    flagsA, flagsB = my_f[:487], my_f[487:]

    committed_key = make_key(V_U10, GATE_KEYS["committed"])
    _, mp_committed = encipher(cyp_seqs, vocab, committed_key)
    inv_committed = {v: k for k, v in mp_committed.items()}

    def coherence(name, cyp_arm, flags):
        pairs, hits, unw_pairs, unw_hits = 0, 0, 0, 0
        for s, wr in zip(cyp_arm, flags):
            arm_pairs = list(zip(s, s[1:]))
            pairs += len(arm_pairs)
            hits += sum(1 for p, q in arm_pairs if (inv_committed[p], inv_committed[q]) in ref_bi)
            if not wr:
                unw_pairs += len(arm_pairs)
                unw_hits += sum(1 for p, q in arm_pairs
                                if (inv_committed[p], inv_committed[q]) in ref_bi)
        return {"arm": name, "windows": len(cyp_arm), "wrapped_windows": sum(1 for f in flags if f),
                "tokens": sum(len(s) for s in cyp_arm),
                "bigram_coherence_decoded_committed": round(hits / pairs, 4),
                "bigram_coherence_unwrapped": round(unw_hits / unw_pairs, 4)}

    main_ = {}
    for kname, kseed in GATE_KEYS.items():
        main_[kname] = arm(ref, cyp_seqs, vocab, make_key(V_U10, kseed))
        m = main_[kname]
        print(f"main {kname}: top10 {m['top10_hits']}/10 full {m['full']:.4f} "
              f"tw {m['token_weighted']:.4f} (start {m['start_used']}, swaps {m['accepted_swaps']})",
              flush=True)

    sub = {}
    for half_name, half in (("A", cyp_seqs[:487]), ("B", cyp_seqs[487:])):
        sub[half_name] = arm(ref, half, vocab, committed_key)
        s = sub[half_name]
        print(f"sub {half_name}: top10 {s['top10_hits']}/10 full {s['full']:.4f} "
              f"tw {s['token_weighted']:.4f} (start {s['start_used']}, swaps {s['accepted_swaps']})",
              flush=True)

    dev = arm(ref[:DEV_NREF], cyp_seqs, vocab, make_key(V_U10, DEV_KEY_SEED))
    print(f"dev (report-only) alpha={ALPHA}: top10 {dev['top10_hits']}/10 full {dev['full']:.4f} "
          f"tw {dev['token_weighted']:.4f}", flush=True)

    nulls, tw_nulls = [], []
    half_nulls = {"A": [], "B": []}
    tw_half_nulls = {"A": [], "B": []}
    for i in range(K_NULLS):
        nref = null_reference(ref, i)
        n_full = arm(nref, cyp_seqs, vocab, committed_key, multistart=False)
        nulls.append(n_full["full"])
        tw_nulls.append(n_full["token_weighted"])
        print(f"null {i} full: {n_full['full']:.4f} tw {n_full['token_weighted']:.4f}", flush=True)
        for half_name, half in (("A", cyp_seqs[:487]), ("B", cyp_seqs[487:])):
            n_half = arm(nref, half, vocab, committed_key, multistart=False)
            half_nulls[half_name].append(n_half["full"])
            tw_half_nulls[half_name].append(n_half["token_weighted"])
            print(f"null {i} half {half_name}: {n_half['full']:.4f}", flush=True)

    null_max_full = max(nulls)
    null_half_max = {h: max(v) for h, v in half_nulls.items()}
    tw_null_max = max(tw_nulls)
    tw_committed = main_["committed"]["token_weighted"]
    gate, checks, keys_replicated = gate_verdict_v2(
        {k: main_[k]["full"] for k in main_}, {h: sub[h]["full"] for h in sub},
        null_max_full, null_half_max, tw_committed, tw_null_max)

    sub_full = {h: sub[h]["full"] for h in sub}
    margins_counts = {
        "committed_vs_1.5x_full_counts": (main_["committed"]["full"] - RATIO_COMMITTED * null_max_full) * V_U10,
        "weakest_key_vs_1.25x_counts": (min(main_[k]["full"] for k in main_) - RATIO_KEY * null_max_full) * V_U10,
        "halfA_vs_half_null_counts": (sub_full["A"] - RATIO_KEY * null_half_max["A"]) * V_U10,
        "halfB_vs_half_null_counts": (sub_full["B"] - RATIO_KEY * null_half_max["B"]) * V_U10,
        "weakest_half_vs_full_null_counts": (min(sub_full.values()) - RATIO_KEY * null_max_full) * V_U10,
        "tw_committed_vs_1.25x_null_counts": (tw_committed - RATIO_TW * tw_null_max) * len(vocab),
    }
    band = {k: round(v, 2) for k, v in margins_counts.items()}
    band_flags = {k: band[k] < 3.0 for k in band}

    out = {
        "cell": {"pool_texts": [len(poolA), len(poolB)], "v_union": V_U10,
                 "wrap_ref": wrap_r, "wrap_cyp": wrap_c},
        "method": {"alpha": ALPHA,
                   "alpha_policy": "frozen from prior cells; no dev sweep on this cell",
                   "restarts": 3,
                   "objective": "bigram LL + position-resolved positional LL (L4-0006 objective, unchanged)"},
        "dev_report_only": {"key": "dev", "n_ref": DEV_NREF, "top10_hits": dev["top10_hits"],
                            "full": dev["full"], "token_weighted": dev["token_weighted"]},
        "main": main_,
        "sampling_arm": sub,
        "nulls": {"full_accuracies": nulls, "full_token_weighted": tw_nulls,
                  "null_max_full": null_max_full, "tw_null_max": tw_null_max,
                  "half_accuracies_A": half_nulls["A"], "half_accuracies_B": half_nulls["B"],
                  "null_max_half": null_half_max,
                  "half_token_weighted": {"A": tw_half_nulls["A"], "B": tw_half_nulls["B"]}},
        "diagnostics": {"committed_key_decode": [
            coherence("A", cyp_seqs[:487], flagsA),
            coherence("B", cyp_seqs[487:], flagsB),
            coherence("full", cyp_seqs, my_f)],
            "note": "report-only; coherence decoded with committed key; wrap flags RNG-mirrored"},
        "band_margins": band,
        "band_flags": band_flags,
        "gate": {"bar": "(a) committed>null_max_full & >=1.5x & >=0.060; (b) >=2/3 keys >=1.25x null_max_full; "
                        "(c1) halfA >= 1.25x half-null; (c2) halfB >= 1.25x half-null; "
                        "(c3) both halves >= 1.25x null_max_full; (d) token-weighted >= 1.25x null TW",
                 "checks": checks, "keys_replicated": keys_replicated,
                 "null_max_full": null_max_full, "null_max_half": null_half_max,
                 "tw_committed": tw_committed, "tw_null_max": tw_null_max, "pass": gate},
    }
    (claim / "object").mkdir(exist_ok=True)
    (claim / "baseline_snapshot").mkdir(exist_ok=True)
    (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
    (claim / "baseline_snapshot" / "gate10.json").write_text(
        json.dumps({"key_shas": KEY_SHAS, "v_union": V_U10, "alpha": ALPHA,
                    "k_nulls": K_NULLS, "ratios": {"committed": RATIO_COMMITTED,
                    "key": RATIO_KEY, "tw": RATIO_TW, "floor": 0.060}}, indent=2))
    print(f"committed full {main_['committed']['full']:.4f} tw {tw_committed:.4f} "
          f"null_max_full {null_max_full:.4f} tw {tw_null_max:.4f} "
          f"halves {sub_full['A']:.4f}/{sub_full['B']:.4f} "
          f"half-null max {null_half_max['A']:.4f}/{null_half_max['B']:.4f} "
          f"gate={'PASS' if gate else 'FAIL'} checks={checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
