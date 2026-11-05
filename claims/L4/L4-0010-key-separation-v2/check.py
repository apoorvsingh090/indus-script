#!/usr/bin/env python3
"""Checker for L4-0010 — readable in one sitting.

Rebuilds fresh cell #5, recomputes the gate-v2 grid at the frozen
alpha=0.5 (54 climbs), and asserts (a) every gated number matches
object/results.json and (b) the gate outcome. Top-10 and the report-only
diagnostics are recomputed for completeness.
Full recompute ~1h45.

Usage: python check.py --splits <dir> --scratch <dir> --object <results.json> --baseline <gate10.json>
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
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0003-bigram-assisted-key-recovery" / "how-we-built-it"))

from sumer_lib import encipher, fetch_zip, indus_lengths, make_key, sign_texts, windows  # noqa: E402
from recover_lib import top10_hits  # noqa: E402
from l40010_lib import (ALPHA, DEV_KEY_SEED, DEV_NREF, GATE_KEYS, KEY_SHAS, K_NULLS,  # noqa: E402
                        NREF, N_WINDOWS, RATIO_COMMITTED, RATIO_KEY, RATIO_TW, V_U10,
                        WIN_CYP10, WIN_REF10, bigram_coherence, gate_verdict_v2,
                        null_reference, pools, recover_best, ref_bigrams,
                        token_weighted)


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


def close(a, b):
    return abs(a - b) < 1e-12


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args()

    o = json.loads(Path(a.object).read_text())
    base = json.loads(Path(a.baseline).read_text())
    if base.get("key_shas") != KEY_SHAS or base.get("v_union") != V_U10 or base.get("alpha") != ALPHA:
        print("FAIL: baseline does not pin keys/V_U10/alpha")
        return 1
    for name, seed in list(GATE_KEYS.items()) + [("dev", DEV_KEY_SEED)]:
        if hashlib.sha256(json.dumps(make_key(V_U10, seed)).encode()).hexdigest() != KEY_SHAS[name]:
            print(f"FAIL: {name} key does not match commitment")
            return 1

    texts = sign_texts(fetch_zip(a.scratch))
    poolA, poolB = pools(texts)
    lens = indus_lengths(a.splits)
    ref_all, _ = windows(poolA, lens, N_WINDOWS, WIN_REF10)
    cyp_seqs, _ = windows(poolB, lens, N_WINDOWS, WIN_CYP10)
    vocab = sorted({t for s in ref_all + cyp_seqs for t in s})
    if len(vocab) != V_U10:
        print(f"FAIL: union vocab {len(vocab)} != {V_U10}")
        return 1
    ref = ref_all[:NREF]
    committed_key = make_key(V_U10, GATE_KEYS["committed"])
    _, mp_committed = encipher(cyp_seqs, vocab, committed_key)
    inv_committed = {v: k for k, v in mp_committed.items()}
    ref_bi = ref_bigrams(ref)

    main_full, main_tw = {}, {}
    for kname, kseed in GATE_KEYS.items():
        m = arm(ref, cyp_seqs, vocab, make_key(V_U10, kseed))
        main_full[kname], main_tw[kname] = m["full"], m["token_weighted"]
    sub_full, sub_tw = {}, {}
    for half_name, half in (("A", cyp_seqs[:487]), ("B", cyp_seqs[487:])):
        s = arm(ref, half, vocab, committed_key)
        sub_full[half_name], sub_tw[half_name] = s["full"], s["token_weighted"]

    nulls, tw_nulls = [], []
    half_nulls = {"A": [], "B": []}
    tw_half_nulls = {"A": [], "B": []}
    for i in range(K_NULLS):
        nref = null_reference(ref, i)
        n1 = arm(nref, cyp_seqs, vocab, committed_key, multistart=False)
        nulls.append(n1["full"])
        tw_nulls.append(n1["token_weighted"])
        for half_name, half in (("A", cyp_seqs[:487]), ("B", cyp_seqs[487:])):
            n2 = arm(nref, half, vocab, committed_key, multistart=False)
            half_nulls[half_name].append(n2["full"])
            tw_half_nulls[half_name].append(n2["token_weighted"])

    null_max_full = max(nulls)
    null_half_max = {h: max(v) for h, v in half_nulls.items()}
    tw_null_max = max(tw_nulls)
    gate, checks, keys_replicated = gate_verdict_v2(
        main_full, sub_full, null_max_full, null_half_max, main_tw["committed"], tw_null_max)

    coherence = {}
    for name, arm_seqs in (("A", cyp_seqs[:487]), ("B", cyp_seqs[487:]), ("full", cyp_seqs)):
        coherence[name] = round(bigram_coherence(arm_seqs, inv_committed, ref_bi), 4)

    same = (
        all(close(main_full[k], o["main"][k]["full"]) for k in main_full)
        and all(main_tw[k] == o["main"][k]["token_weighted"] for k in main_tw)
        and all(close(sub_full[h], o["sampling_arm"][h]["full"]) for h in sub_full)
        and sorted(round(x, 12) for x in nulls)
            == sorted(round(x, 12) for x in o["nulls"]["full_accuracies"])
        and sorted(round(x, 12) for x in tw_nulls)
            == sorted(round(x, 12) for x in o["nulls"]["full_token_weighted"])
        and all(close(null_half_max[h], o["nulls"]["null_max_half"][h]) for h in half_nulls)
        and sorted(round(x, 12) for x in half_nulls["A"])
            == sorted(round(x, 12) for x in o["nulls"]["half_accuracies_A"])
        and sorted(round(x, 12) for x in half_nulls["B"])
            == sorted(round(x, 12) for x in o["nulls"]["half_accuracies_B"])
        and sorted(round(x, 12) for x in tw_half_nulls["A"])
            == sorted(round(x, 12) for x in o["nulls"]["half_token_weighted"]["A"])
        and sorted(round(x, 12) for x in tw_half_nulls["B"])
            == sorted(round(x, 12) for x in o["nulls"]["half_token_weighted"]["B"])
        and close(tw_null_max, o["nulls"]["tw_null_max"])
        and abs(coherence["A"] - o["diagnostics"]["committed_key_decode"][0]
                ["bigram_coherence_decoded_committed"]) < 1e-9
        and abs(coherence["B"] - o["diagnostics"]["committed_key_decode"][1]
                ["bigram_coherence_decoded_committed"]) < 1e-9
    )
    gate_same = gate == o["gate"]["pass"] and checks == o["gate"]["checks"]
    print(f"alpha={ALPHA} committed={main_full['committed']:.6f} tw={main_tw['committed']:.6f} "
          f"null_max_full={null_max_full:.6f} tw_null={tw_null_max:.6f} "
          f"halves={sub_full['A']:.6f}/{sub_full['B']:.6f} "
          f"half_null={null_half_max['A']:.6f}/{null_half_max['B']:.6f} "
          f"recompute={'match' if same else 'DIFF'} gate={'PASS' if gate else 'FAIL'}")
    print("PASS" if same and gate_same else "FAIL")
    return 0 if same and gate_same else 1


if __name__ == "__main__":
    sys.exit(main())
