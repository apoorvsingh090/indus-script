#!/usr/bin/env python3
"""Generator for L4-0004. Run AFTER the preregistration commit.

Builds the disjoint-pool cell (pool B cipher windows under the gate keys,
pool A reference prefixes), derives alpha* by the frozen dev rule
(smallest alpha in grid reaching >=7/10 on the dev key at N_ref=500),
then evaluates the gated N_ref x key grid at frozen alpha* and writes
object/results.json + baseline_snapshot/nmin.json.

Usage: python run_l40004.py <splits_dir> <scratch_dir> <claim_dir>
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
CLAIM = HERE.parent
ROOT = CLAIM.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0002-sumerian-hidden-key" / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0003-bigram-assisted-key-recovery" / "how-we-built-it"))

from sumer_lib import encipher, fetch_zip, indus_lengths, make_key, sign_texts, windows  # noqa: E402
from nmin_lib import (ALPHA_GRID, DEV_KEY_SEED, DEV_NREF, GATE_KEYS, KEY_SHAS, NREF_GRID,  # noqa: E402
                      N_WINDOWS, V_U, WIN_CYP, WIN_REF, key_sha, pools, recover_at)
from recover_lib import top10_hits  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("splits")
    ap.add_argument("scratch")
    ap.add_argument("claim")
    a = ap.parse_args()
    claim = Path(a.claim)

    for name, seed in list(GATE_KEYS.items()) + [("dev", DEV_KEY_SEED)]:
        assert key_sha(seed) == KEY_SHAS[name], f"key sha mismatch for {name}"

    texts = sign_texts(fetch_zip(a.scratch))
    poolA, poolB = pools(texts)
    lens = indus_lengths(a.splits)
    ref_all, wrap_r = windows(poolA, lens, N_WINDOWS, WIN_REF)
    cyp_seqs, wrap_c = windows(poolB, lens, N_WINDOWS, WIN_CYP)
    vocab = sorted({t for s in ref_all + cyp_seqs for t in s})
    assert len(vocab) == V_U, f"union vocab {len(vocab)} != {V_U}"

    # --- dev cell: fix alpha* by the frozen rule ---
    dev_key = make_key(V_U, DEV_KEY_SEED)
    dev_ref = ref_all[:DEV_NREF]
    dev_cyp, dev_mp = encipher(cyp_seqs, vocab, dev_key)
    dev_inv = {v: k for k, v in dev_mp.items()}
    dev_table = {}
    alpha_star = None
    for al in ALPHA_GRID:
        guess, swaps = recover_at(dev_ref, dev_cyp, vocab, al)
        hits = top10_hits(guess, dev_cyp, dev_inv)
        dev_table[str(al)] = {"top10_hits": hits, "accepted_swaps": swaps}
        print(f"dev alpha={al}: {hits}/10 (swaps {swaps})", flush=True)
        if alpha_star is None and hits >= 7:
            alpha_star = al

    out = {
        "cell": {"pool_texts": [len(poolA), len(poolB)], "n_windows": N_WINDOWS,
                 "v_union": V_U, "wrap_ref": wrap_r, "wrap_cyp": wrap_c,
                 "mean_len_ref": sum(len(s) for s in ref_all) / N_WINDOWS,
                 "mean_len_cyp": sum(len(s) for s in cyp_seqs) / N_WINDOWS},
        "dev": {"rule": "smallest alpha in grid with >=7/10 on dev key at N_ref=500",
                "grid": ALPHA_GRID, "table": dev_table,
                "alpha_star": alpha_star},
    }

    if alpha_star is None:
        out["gate"] = {"bar": "alpha* exists AND committed@974 >=7 AND >=2/3 keys >=7 at N_ref=974",
                       "pass": False, "reason": "no alpha in grid reaches 7/10 on the dev cell"}
        (claim / "object").mkdir(exist_ok=True)
        (claim / "baseline_snapshot").mkdir(exist_ok=True)
        (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
        (claim / "baseline_snapshot" / "nmin.json").write_text(json.dumps(
            {"key_shas": KEY_SHAS, "v_union": V_U, "nref_grid": NREF_GRID}, indent=2))
        print("dev cell: no alpha clears 7/10 -> negative filing, gate FAIL")
        return 0

    # --- gated grid at frozen alpha* ---
    grid = {}
    for kname, kseed in GATE_KEYS.items():
        k = make_key(V_U, kseed)
        cyp, mp = encipher(cyp_seqs, vocab, k)
        inv = {v: kk for kk, v in mp.items()}
        for nref in NREF_GRID:
            guess, swaps = recover_at(ref_all[:nref], cyp, vocab, alpha_star)
            hits = top10_hits(guess, cyp, inv)
            full = sum(1 for c in vocab if guess.get(c) == inv.get(c)) / V_U
            grid[f"{kname}@{nref}"] = {"top10_hits": hits, "full_key_acc": full, "accepted_swaps": swaps}
            print(f"{kname}@{nref}: {hits}/10 full {full:.3f} (swaps {swaps})", flush=True)

    at974 = {k: grid[f"{k}@974"]["top10_hits"] for k in GATE_KEYS}
    n_keys_ge7 = sum(1 for h in at974.values() if h >= 7)
    n_min = next((n for n in NREF_GRID if grid[f"committed@{n}"]["top10_hits"] >= 7), None)
    gate_pass = at974["committed"] >= 7 and n_keys_ge7 >= 2 and n_min is not None

    out["grid"] = grid
    out["gate"] = {"bar": "alpha* exists AND committed@974 >=7 AND >=2/3 keys >=7 at N_ref=974 AND N_min exists",
                   "committed_at_974": at974["committed"], "keys_ge7_at_974": n_keys_ge7,
                   "n_min": n_min, "pass": bool(gate_pass)}
    (claim / "object").mkdir(exist_ok=True)
    (claim / "baseline_snapshot").mkdir(exist_ok=True)
    (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
    (claim / "baseline_snapshot" / "nmin.json").write_text(json.dumps(
        {"key_shas": KEY_SHAS, "v_union": V_U, "nref_grid": NREF_GRID, "alpha_star": alpha_star}, indent=2))
    print(f"alpha*={alpha_star} N_min={n_min} committed@974={at974['committed']}/10 "
          f"keys_ge7={n_keys_ge7} gate={'PASS' if gate_pass else 'FAIL'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
