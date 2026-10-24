#!/usr/bin/env python3
"""Checker for L4-0004 — readable in one sitting.

Rebuilds the disjoint-pool cell, re-derives alpha* by the frozen dev rule,
recomputes the gated N_ref x key grid, and asserts (a) recomputation
matches object/results.json on every gated cell and (b) the gate outcome.
Full recompute takes ~30-60 min (18 hill-climbs at V=368).

Usage: python check.py --splits <dir> --scratch <dir> --object <results.json> --baseline <nmin.json>
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0002-sumerian-hidden-key" / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0003-bigram-assisted-key-recovery" / "how-we-built-it"))

from sumer_lib import encipher, fetch_zip, indus_lengths, make_key, sign_texts, windows  # noqa: E402
from nmin_lib import (ALPHA_GRID, DEV_KEY_SEED, DEV_NREF, GATE_KEYS, KEY_SHAS, NREF_GRID,  # noqa: E402
                      N_WINDOWS, V_U, WIN_CYP, WIN_REF, key_sha, pools, recover_at)
from recover_lib import top10_hits  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args()

    o = json.loads(Path(a.object).read_text())
    base = json.loads(Path(a.baseline).read_text())
    if base.get("key_shas") != KEY_SHAS or base.get("v_union") != V_U:
        print("FAIL: baseline snapshot does not pin the committed keys/V_U")
        return 1
    for name, seed in list(GATE_KEYS.items()) + [("dev", DEV_KEY_SEED)]:
        if key_sha(seed) != KEY_SHAS[name]:
            print(f"FAIL: {name} key does not match commitment")
            return 1

    texts = sign_texts(fetch_zip(a.scratch))
    poolA, poolB = pools(texts)
    lens = indus_lengths(a.splits)
    ref_all, _ = windows(poolA, lens, N_WINDOWS, WIN_REF)
    cyp_seqs, _ = windows(poolB, lens, N_WINDOWS, WIN_CYP)
    vocab = sorted({t for s in ref_all + cyp_seqs for t in s})
    if len(vocab) != V_U:
        print(f"FAIL: union vocab {len(vocab)} != {V_U}")
        return 1

    # dev rule -> alpha*
    dev_key = make_key(V_U, DEV_KEY_SEED)
    dev_cyp, dev_mp = encipher(cyp_seqs, vocab, dev_key)
    dev_inv = {v: k for k, v in dev_mp.items()}
    alpha_star = None
    for al in ALPHA_GRID:
        guess, _ = recover_at(ref_all[:DEV_NREF], dev_cyp, vocab, al)
        if top10_hits(guess, dev_cyp, dev_inv) >= 7:
            alpha_star = al
            break
    if alpha_star != o["dev"]["alpha_star"]:
        print(f"FAIL: alpha* recompute {alpha_star} != shipped {o['dev']['alpha_star']}")
        return 1

    grid = {}
    for kname, kseed in GATE_KEYS.items():
        k = make_key(V_U, kseed)
        cyp, mp = encipher(cyp_seqs, vocab, k)
        inv = {v: kk for kk, v in mp.items()}
        for nref in NREF_GRID:
            guess, _ = recover_at(ref_all[:nref], cyp, vocab, alpha_star)
            grid[f"{kname}@{nref}"] = top10_hits(guess, cyp, inv)

    same = all(grid[c] == o["grid"][c]["top10_hits"] for c in grid)
    at974 = {k: grid[f"{k}@974"] for k in GATE_KEYS}
    n_ge7 = sum(1 for h in at974.values() if h >= 7)
    n_min = next((n for n in NREF_GRID if grid[f"committed@{n}"] >= 7), None)
    gate = alpha_star is not None and at974["committed"] >= 7 and n_ge7 >= 2 and n_min is not None
    gate_same = gate == o["gate"]["pass"]
    print(f"alpha*={alpha_star} N_min={n_min} committed@974={at974['committed']}/10 "
          f"keys_ge7={n_ge7} recompute={'match' if same else 'DIFF'} gate={'PASS' if gate else 'FAIL'}")
    print("PASS" if same and gate_same else "FAIL")
    return 0 if same and gate_same else 1


if __name__ == "__main__":
    sys.exit(main())
