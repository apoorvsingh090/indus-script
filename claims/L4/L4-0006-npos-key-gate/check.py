#!/usr/bin/env python3
"""Checker for L4-0006 — readable in one sitting.

Rebuilds fresh cell #3, re-derives alpha* by the dev rule, recomputes the
strengthened gated arms (identical gate to L4-0005) with the
position-resolved positional term, and asserts (a) recomputation matches
object/results.json on every gated cell and (b) the gate outcome.
Full recompute ~2h (51 climbs) if alpha* exists, ~50 min otherwise.

Usage: python check.py --splits <dir> --scratch <dir> --object <results.json> --baseline <gate6.json>
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

from sumer_lib import encipher, fetch_zip, indus_lengths, make_key, sign_texts, windows  # noqa: E402
from l40006_lib import (ALPHA_GRID, DEV_KEY_SEED, DEV_NREF, GATE_KEYS, KEY_SHAS, K_NULLS,  # noqa: E402
                        N_WINDOWS, NREF, V_U6, WIN_CYP6, WIN_REF6, null_reference, pools,
                        recover_best)
from recover_lib import top10_hits  # noqa: E402


def hits_full(ref, cyp_seqs, vocab, key, alpha, multistart=True):
    cyp, mp = encipher(cyp_seqs, vocab, key)
    inv = {v: k for k, v in mp.items()}
    guess, _ = recover_best(ref, cyp, vocab, alpha, multistart=multistart)
    return (top10_hits(guess, cyp, inv),
            sum(1 for c in vocab if guess.get(c) == inv.get(c)) / len(vocab))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args()

    o = json.loads(Path(a.object).read_text())
    base = json.loads(Path(a.baseline).read_text())
    if base.get("key_shas") != KEY_SHAS or base.get("v_union") != V_U6:
        print("FAIL: baseline does not pin the committed keys/V_U6")
        return 1
    for name, seed in list(GATE_KEYS.items()) + [("dev", DEV_KEY_SEED)]:
        k = make_key(V_U6, seed)
        if hashlib.sha256(json.dumps(k).encode()).hexdigest() != KEY_SHAS[name]:
            print(f"FAIL: {name} key does not match commitment")
            return 1

    texts = sign_texts(fetch_zip(a.scratch))
    poolA, poolB = pools(texts)
    lens = indus_lengths(a.splits)
    ref_all, _ = windows(poolA, lens, N_WINDOWS, WIN_REF6)
    cyp_seqs, _ = windows(poolB, lens, N_WINDOWS, WIN_CYP6)
    vocab = sorted({t for s in ref_all + cyp_seqs for t in s})
    if len(vocab) != V_U6:
        print(f"FAIL: union vocab {len(vocab)} != {V_U6}")
        return 1
    ref = ref_all[:NREF]

    alpha_star = None
    for al in ALPHA_GRID:
        h, _ = hits_full(ref[:DEV_NREF], cyp_seqs, vocab, make_key(V_U6, DEV_KEY_SEED), al)
        if h >= 7:
            alpha_star = al
            break
    if alpha_star != o["dev"]["alpha_star"]:
        print(f"FAIL: alpha* recompute {alpha_star} != shipped {o['dev']['alpha_star']}")
        return 1
    if alpha_star is None:
        gate, same = False, True
        main_hits, main_full, nulls = {}, {}, []
    else:
        main_hits, main_full = {}, {}
        for kname, kseed in GATE_KEYS.items():
            main_hits[kname], main_full[kname] = hits_full(
                ref, cyp_seqs, vocab, make_key(V_U6, kseed), alpha_star)
        committed_key = make_key(V_U6, GATE_KEYS["committed"])
        sub_hits = {}
        for half_name, half in (("A", cyp_seqs[:487]), ("B", cyp_seqs[487:])):
            sub_hits[half_name], _ = hits_full(ref, half, vocab, committed_key, alpha_star)
        nulls = []
        for i in range(K_NULLS):
            _, full = hits_full(null_reference(ref, i), cyp_seqs, vocab,
                                committed_key, alpha_star, multistart=False)
            nulls.append(full)
        null_max = max(nulls)
        same = (all(main_hits[k] == o["main"][k]["top10_hits"] for k in main_hits)
                and all(sub_hits[h] == o["sampling_arm"][h]["top10_hits"] for h in sub_hits)
                and abs(main_full["committed"] - o["main"]["committed"]["full"]) < 1e-12
                and abs(null_max - o["nulls"]["null_max"]) < 1e-12)
        n8 = sum(1 for h in main_hits.values() if h >= 8)
        gate = (main_hits["committed"] >= 8 and n8 >= 2
                and main_full["committed"] > null_max and main_full["committed"] >= 1.5 * null_max
                and sub_hits["A"] >= 6 and sub_hits["B"] >= 6)
    gate_same = gate == o["gate"]["pass"]
    print(f"alpha*={alpha_star} committed={main_hits.get('committed', '-')}/10 "
          f"full={main_full.get('committed', '-')} null_max={max(nulls) if nulls else '-'} "
          f"recompute={'match' if same else 'DIFF'} gate={'PASS' if gate else 'FAIL'}")
    print("PASS" if same and gate_same else "FAIL")
    return 0 if same and gate_same else 1


if __name__ == "__main__":
    sys.exit(main())
