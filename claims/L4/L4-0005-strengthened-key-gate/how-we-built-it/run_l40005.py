#!/usr/bin/env python3
"""Generator for L4-0005. Run AFTER the preregistration commit.

Fresh disjoint-pool cell -> alpha* by the dev rule -> strengthened gated
arms (8/10 bar, full-key vs structureless-null max x1.5, cipher-half
sampling arm). Writes object/results.json + baseline_snapshot/gate5.json.
Runtime ~2h (51 hill-climbs); prints progress.

Usage: python run_l40005.py <splits_dir> <scratch_dir> <claim_dir>
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

from sumer_lib import encipher, fetch_zip, indus_lengths, make_key, sign_texts, windows  # noqa: E402
from l40005_lib import (ALPHA_GRID, DEV_KEY_SEED, DEV_NREF, GATE_KEYS, KEY_SHAS, K_NULLS,  # noqa: E402
                        N_WINDOWS, NREF, V_U5, WIN_CYP5, WIN_REF5, null_reference, pools,
                        recover_best)
from recover_lib import top10_hits  # noqa: E402


def hits_full(ref, cyp_seqs, vocab, key, alpha, multistart=True):
    cyp, mp = encipher(cyp_seqs, vocab, key)
    inv = {v: k for k, v in mp.items()}
    guess, diag = recover_best(ref, cyp, vocab, alpha, multistart=multistart)
    h = top10_hits(guess, cyp, inv)
    full = sum(1 for c in vocab if guess.get(c) == inv.get(c)) / len(vocab)
    return h, full, diag


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("splits")
    ap.add_argument("scratch")
    ap.add_argument("claim")
    a = ap.parse_args()
    claim = Path(a.claim)

    for name, seed in list(GATE_KEYS.items()) + [("dev", DEV_KEY_SEED)]:
        k = make_key(V_U5, seed)
        assert hashlib.sha256(json.dumps(k).encode()).hexdigest() == KEY_SHAS[name], name

    texts = sign_texts(fetch_zip(a.scratch))
    poolA, poolB = pools(texts)
    lens = indus_lengths(a.splits)
    ref_all, wrap_r = windows(poolA, lens, N_WINDOWS, WIN_REF5)
    cyp_seqs, wrap_c = windows(poolB, lens, N_WINDOWS, WIN_CYP5)
    vocab = sorted({t for s in ref_all + cyp_seqs for t in s})
    assert len(vocab) == V_U5, f"union vocab {len(vocab)} != {V_U5}"
    ref = ref_all[:NREF]

    # --- dev rule -> alpha* (best-of-3 method) ---
    dev_key = make_key(V_U5, DEV_KEY_SEED)
    dev_table = {}
    alpha_star = None
    for al in ALPHA_GRID:
        h, full, diag = hits_full(ref[:DEV_NREF], cyp_seqs, vocab, dev_key, al)
        dev_table[str(al)] = {"top10_hits": h, "full": full, "start": diag["start_used"]}
        print(f"dev alpha={al}: {h}/10 full {full:.3f} (start {diag['start_used']})", flush=True)
        if alpha_star is None and h >= 7:
            alpha_star = al
    if alpha_star is None:
        out = {"cell": {"v_union": V_U5, "wrap_ref": wrap_r, "wrap_cyp": wrap_c},
               "dev": {"table": dev_table, "alpha_star": None},
               "gate": {"pass": False, "reason": "no alpha reaches 7/10 on the dev cell"}}
        (claim / "object").mkdir(exist_ok=True)
        (claim / "baseline_snapshot").mkdir(exist_ok=True)
        (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
        (claim / "baseline_snapshot" / "gate5.json").write_text(
            json.dumps({"key_shas": KEY_SHAS, "v_union": V_U5, "alpha_star": None}, indent=2))
        print("dev cell: no alpha clears 7/10 -> negative filing")
        return 0

    # --- gated main arms (best-of-3) ---
    main = {}
    for kname, kseed in GATE_KEYS.items():
        h, full, diag = hits_full(ref, cyp_seqs, vocab, make_key(V_U5, kseed), alpha_star)
        main[kname] = {"top10_hits": h, "full": full, "start": diag["start_used"],
                       "swaps": diag["accepted_swaps"]}
        print(f"main {kname}: {h}/10 full {full:.3f} (start {diag['start_used']})", flush=True)

    # --- sampling arm: two disjoint cipher halves, committed key ---
    committed_key = make_key(V_U5, GATE_KEYS["committed"])
    sub = {}
    for half_name, half in (("A", cyp_seqs[:487]), ("B", cyp_seqs[487:])):
        h, full, diag = hits_full(ref, half, vocab, committed_key, alpha_star)
        sub[half_name] = {"top10_hits": h, "full": full}
        print(f"sub {half_name}: {h}/10 full {full:.3f}", flush=True)

    # --- structureless nulls: rank-init single-start, K=12 + 2 at best-of-3 ---
    nulls = []
    for i in range(K_NULLS):
        nref = null_reference(ref, i)
        _, full, diag = hits_full(nref, cyp_seqs, vocab, committed_key,
                                  alpha_star, multistart=False)
        nulls.append(full)
        print(f"null {i}: full {full:.3f}", flush=True)
    null_ms = []
    for i in (0, 1):
        nref = null_reference(ref, i)
        _, full, diag = hits_full(nref, cyp_seqs, vocab, committed_key,
                                  alpha_star, multistart=True)
        null_ms.append(full)
        print(f"null-ms {i}: full {full:.3f}", flush=True)
    null_max = max(nulls)

    at974 = {k: main[k]["top10_hits"] for k in main}
    n8 = sum(1 for h in at974.values() if h >= 8)
    full_c = main["committed"]["full"]
    gate = (alpha_star is not None and at974["committed"] >= 8 and n8 >= 2
            and full_c > null_max and full_c >= 1.5 * null_max
            and sub["A"]["top10_hits"] >= 6 and sub["B"]["top10_hits"] >= 6)

    out = {
        "cell": {"pool_texts": [len(poolA), len(poolB)], "v_union": V_U5,
                 "wrap_ref": wrap_r, "wrap_cyp": wrap_c},
        "dev": {"rule": "smallest alpha with >=7/10 dev key at N_ref=500 (best-of-3)",
                "grid": ALPHA_GRID, "table": dev_table, "alpha_star": alpha_star},
        "main": main,
        "sampling_arm": sub,
        "nulls": {"full_accuracies": nulls, "null_max": null_max,
                  "multistart_spot_check": null_ms},
        "gate": {"bar": "a* exists AND committed>=8/10 AND >=2/3 keys>=8 AND "
                        "full>1.5*null_max AND both cipher halves>=6/10",
                 "committed_at_974": at974["committed"], "keys_ge8": n8,
                 "full_committed": full_c, "null_max": null_max, "pass": bool(gate)},
    }
    (claim / "object").mkdir(exist_ok=True)
    (claim / "baseline_snapshot").mkdir(exist_ok=True)
    (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
    (claim / "baseline_snapshot" / "gate5.json").write_text(
        json.dumps({"key_shas": KEY_SHAS, "v_union": V_U5, "alpha_star": alpha_star,
                    "k_nulls": K_NULLS}, indent=2))
    print(f"alpha*={alpha_star} committed {at974['committed']}/10 keys_ge8={n8} "
          f"full {full_c:.3f} vs null_max {null_max:.3f} sub {sub['A']['top10_hits']}/{sub['B']['top10_hits']} "
          f"gate={'PASS' if gate else 'FAIL'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
