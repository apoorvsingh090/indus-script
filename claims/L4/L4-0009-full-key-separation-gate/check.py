#!/usr/bin/env python3
"""Checker for L4-0009 — readable in one sitting.

Rebuilds fresh cell #4, recomputes the full-key-separation grid at the
frozen alpha=0.5, and asserts (a) every gated number matches
object/results.json and (b) the gate outcome. Top-10 is recomputed for
completeness but does not gate.
Full recompute ~68 min (36 climbs).

Usage: python check.py --splits <dir> --scratch <dir> --object <results.json> --baseline <gate9.json>
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
from recover_lib import top10_hits  # noqa: E402
from l40009_lib import (ALPHA, DEV_KEY_SEED, DEV_NREF, GATE_KEYS, KEY_SHAS, K_NULLS,  # noqa: E402
                        N_WINDOWS, NREF, V_U9, WIN_CYP9, WIN_REF9, gate_verdict,
                        null_reference, pools, recover_best)


def hits_full(ref, cyp_seqs, vocab, key, alpha, multistart=True):
    cyp, mp = encipher(cyp_seqs, vocab, key)
    inv = {v: k for k, v in mp.items()}
    guess, diag = recover_best(ref, cyp, vocab, alpha, multistart=multistart)
    return (top10_hits(guess, cyp, inv),
            sum(1 for c in vocab if guess.get(c) == inv.get(c)) / len(vocab), diag)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args()

    o = json.loads(Path(a.object).read_text())
    base = json.loads(Path(a.baseline).read_text())
    if base.get("key_shas") != KEY_SHAS or base.get("v_union") != V_U9 or base.get("alpha") != ALPHA:
        print("FAIL: baseline does not pin keys/V_U9/alpha")
        return 1
    for name, seed in list(GATE_KEYS.items()) + [("dev", DEV_KEY_SEED)]:
        if hashlib.sha256(json.dumps(make_key(V_U9, seed)).encode()).hexdigest() != KEY_SHAS[name]:
            print(f"FAIL: {name} key does not match commitment")
            return 1

    texts = sign_texts(fetch_zip(a.scratch))
    poolA, poolB = pools(texts)
    lens = indus_lengths(a.splits)
    ref_all, _ = windows(poolA, lens, N_WINDOWS, WIN_REF9)
    cyp_seqs, _ = windows(poolB, lens, N_WINDOWS, WIN_CYP9)
    vocab = sorted({t for s in ref_all + cyp_seqs for t in s})
    if len(vocab) != V_U9:
        print(f"FAIL: union vocab {len(vocab)} != {V_U9}")
        return 1
    ref = ref_all[:NREF]

    main_full, main_hits = {}, {}
    for kname, kseed in GATE_KEYS.items():
        h, full, _ = hits_full(ref, cyp_seqs, vocab, make_key(V_U9, kseed), ALPHA)
        main_hits[kname], main_full[kname] = h, full
    committed_key = make_key(V_U9, GATE_KEYS["committed"])
    sub_full, sub_hits = {}, {}
    for half_name, half in (("A", cyp_seqs[:487]), ("B", cyp_seqs[487:])):
        h, full, _ = hits_full(ref, half, vocab, committed_key, ALPHA)
        sub_hits[half_name], sub_full[half_name] = h, full
    nulls = []
    for i in range(K_NULLS):
        _, full, _ = hits_full(null_reference(ref, i), cyp_seqs, vocab,
                               committed_key, ALPHA, multistart=False)
        nulls.append(full)
    null_max = max(nulls)
    gate, checks, keys_replicated = gate_verdict(main_full, null_max, sub_full)

    same = (
        all(abs(main_full[k] - o["main"][k]["full"]) < 1e-12 for k in main_full)
        and all(main_hits[k] == o["main"][k]["top10_hits"] for k in main_hits)
        and all(abs(sub_full[h] - o["sampling_arm"][h]["full"]) < 1e-12 for h in sub_full)
        and all(sub_hits[h] == o["sampling_arm"][h]["top10_hits"] for h in sub_hits)
        and abs(null_max - o["nulls"]["null_max"]) < 1e-12
        and sorted(round(x, 12) for x in nulls) == sorted(round(x, 12) for x in o["nulls"]["full_accuracies"])
    )
    gate_same = gate == o["gate"]["pass"] and checks == o["gate"]["checks"]
    print(f"alpha={ALPHA} committed_full={main_full['committed']:.6f} "
          f"null_max={null_max:.6f} keys_replicated={keys_replicated} "
          f"halves={sub_full['A']:.6f}/{sub_full['B']:.6f} "
          f"recompute={'match' if same else 'DIFF'} gate={'PASS' if gate else 'FAIL'}")
    print("PASS" if same and gate_same else "FAIL")
    return 0 if same and gate_same else 1


if __name__ == "__main__":
    sys.exit(main())
