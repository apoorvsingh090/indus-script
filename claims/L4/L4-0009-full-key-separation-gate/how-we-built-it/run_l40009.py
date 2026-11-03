#!/usr/bin/env python3
"""Generator for L4-0009. Run only AFTER the preregistration commit.

Fresh cell #4 -> alpha FROZEN at 0.5 -> full-key-separation gate.
Writes object/results.json + baseline_snapshot/gate9.json.
Runtime ~68 min (36 climbs) single-process. Prints progress.

Usage: python run_l40009.py <splits_dir> <scratch_dir> <claim_dir>
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
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0003-bigram-assisted-key-recovery" / "how-we-built-it"))

from sumer_lib import encipher, fetch_zip, indus_lengths, make_key, sign_texts, windows  # noqa: E402
from recover_lib import top10_hits  # noqa: E402
from l40009_lib import (ALPHA, DEV_KEY_SEED, DEV_NREF, GATE_KEYS, KEY_SHAS, K_NULLS,  # noqa: E402
                        N_WINDOWS, NREF, V_U9, WIN_CYP9, WIN_REF9, gate_verdict,
                        null_reference, pools, recover_best)


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
        k = make_key(V_U9, seed)
        got = hashlib.sha256(json.dumps(k).encode()).hexdigest()
        assert got == KEY_SHAS[name], f"{name} key sha {got} != commitment"

    texts = sign_texts(fetch_zip(a.scratch))
    poolA, poolB = pools(texts)
    lens = indus_lengths(a.splits)
    ref_all, wrap_r = windows(poolA, lens, N_WINDOWS, WIN_REF9)
    cyp_seqs, wrap_c = windows(poolB, lens, N_WINDOWS, WIN_CYP9)
    vocab = sorted({t for s in ref_all + cyp_seqs for t in s})
    assert len(vocab) == V_U9, f"union vocab {len(vocab)} != {V_U9}"
    ref = ref_all[:NREF]

    dev_h, dev_full, _ = hits_full(ref[:DEV_NREF], cyp_seqs, vocab,
                                   make_key(V_U9, DEV_KEY_SEED), ALPHA)
    print(f"dev (report-only) alpha={ALPHA}: top10 {dev_h}/10 full {dev_full:.4f}", flush=True)

    main_ = {}
    for kname, kseed in GATE_KEYS.items():
        h, full, diag = hits_full(ref, cyp_seqs, vocab, make_key(V_U9, kseed), ALPHA)
        main_[kname] = {"top10_hits": h, "full": full, "start": diag["start_used"],
                        "swaps": diag["accepted_swaps"]}
        print(f"main {kname}: top10 {h}/10 full {full:.4f} "
              f"(start {diag['start_used']}, swaps {diag['accepted_swaps']})", flush=True)

    committed_key = make_key(V_U9, GATE_KEYS["committed"])
    sub = {}
    for half_name, half in (("A", cyp_seqs[:487]), ("B", cyp_seqs[487:])):
        h, full, _ = hits_full(ref, half, vocab, committed_key, ALPHA)
        sub[half_name] = {"top10_hits": h, "full": full}
        print(f"sub {half_name}: top10 {h}/10 full {full:.4f}", flush=True)

    nulls = []
    for i in range(K_NULLS):
        _, full, _ = hits_full(null_reference(ref, i), cyp_seqs, vocab, committed_key,
                               ALPHA, multistart=False)
        nulls.append(full)
        print(f"null {i}: full {full:.4f}", flush=True)
    null_ms = []
    for i in (0, 1):
        _, full, _ = hits_full(null_reference(ref, i), cyp_seqs, vocab, committed_key,
                               ALPHA, multistart=True)
        null_ms.append(full)
        print(f"null-ms {i}: full {full:.4f}", flush=True)
    null_max = max(nulls)

    main_full = {k: main_[k]["full"] for k in main_}
    sub_full = {h: sub[h]["full"] for h in sub}
    gate, checks, keys_replicated = gate_verdict(main_full, null_max, sub_full)

    out = {
        "cell": {"pool_texts": [len(poolA), len(poolB)], "v_union": V_U9,
                 "wrap_ref": wrap_r, "wrap_cyp": wrap_c},
        "method": {"alpha": ALPHA, "alpha_policy": "frozen from prior cells; no dev sweep on this cell",
                   "restarts": 3, "objective": "bigram LL + position-resolved positional LL (pos 0..7)"},
        "dev_report_only": {"key": "dev", "n_ref": DEV_NREF, "top10_hits": dev_h, "full": dev_full},
        "main": main_,
        "sampling_arm": sub,
        "nulls": {"full_accuracies": nulls, "null_max": null_max,
                  "multistart_spot_check": null_ms},
        "gate": {"bar": "committed>null_max & >=1.5x & >=0.060 AND >=2/3 keys>=1.25x AND both halves>=1.25x",
                 "checks": checks, "keys_replicated": keys_replicated,
                 "null_max": null_max, "pass": gate},
    }
    (claim / "object").mkdir(exist_ok=True)
    (claim / "baseline_snapshot").mkdir(exist_ok=True)
    (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
    (claim / "baseline_snapshot" / "gate9.json").write_text(
        json.dumps({"key_shas": KEY_SHAS, "v_union": V_U9, "alpha": ALPHA,
                    "k_nulls": K_NULLS}, indent=2))
    print(f"alpha={ALPHA} committed full {main_full['committed']:.4f} "
          f"null_max {null_max:.4f} keys_replicated {keys_replicated} "
          f"halves {sub_full['A']:.4f}/{sub_full['B']:.4f} "
          f"gate={'PASS' if gate else 'FAIL'} checks={checks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
