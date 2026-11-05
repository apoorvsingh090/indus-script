"""L4-0010 â€” full-key-separation gate v2 on fresh cell #5.

Successor to the verified-negative L4-0009, preregistered before any
recovery on cell #5. Two skeptic-findings-driven design changes, each
disclosed below; the recovery method is byte-for-byte the L4-0006/
L4-0009 position-resolved joint objective (alpha FROZEN at 0.5,
best-of-3, same restart seeds) so results stay comparable.

Cell: 1456 ETCSRI sign_texts shuffled Random(KEY_SEED+12000); pool A =
first 728 (reference), pool B = rest (cipher); 974 windows each (seeds
+12100/+12200), splits/v1 lengths; V_U10=353 union types. Keys:
committed=KEY_SEED+13000, alt1=+13001, alt2=+13002, dev=+13003 (shas in
claim.yaml). Fresh against every prior cell (pool bases +7000/+8000/
+10000, window bases +7100..+8200/+10100/+10200, key bases <= +11003).

GATE v2 â€” full-key separation (all required):
  (a) committed full-key @974 > null_max_full AND >= 1.5*null_max_full
      AND >= 0.060 absolute floor (unchanged from L4-0009);
  (b) at least 2 of 3 gate keys @974 >= 1.25*null_max_full (unchanged);
  (c1) half A >= 1.25*null_max_half_A   [MATCHED-SCALE nulls: within-
       window permuted FULL 974 reference + the 487-window cipher
       subset, K=12, seeds 777000000+0..11 (same permutations as the
       full battery), committed key, rank-init single-start â€” this is
       the apples-to-apples control for the half arms, fixing the
       calibration flaw sk9-B exposed: L4-0009 compared 487-window arms
       against a 974-window null];
  (c2) half B >= 1.25*null_max_half_B (same construction, other half);
  (c3) both halves >= 1.25*null_max_full â€” the L4-0009-as-filed reading,
       kept as a REQUIRED condition so any PASS is robust under BOTH
       calibrations (disclosed: this condition is already known fragile
       on cell #4); and
  (d) token-weighted committed @974 >= 1.25 * max token-weighted over
      the K=12 full null batteries (metric-specificity guard; fold-in
      of sk6-D/sk9-B: unweighted separation can collapse under token
      weighting; cell #4 measured 0.6452 committed vs null max 0.445 =
      1.45x, margin 1.25 disclosed round-below).
null_max_full = max unweighted full-key over the K=12 full-scale nulls
(as L4-0009). Top-10, dev arm, per-half wrap/coherence/mass diagnostics
and cross-check margins are shipped report-only. The Â±1-3/371 float
band is tracked: every gated comparison is also shipped as a margin in
type-count terms and flagged band-adjacent when < 3.
"""
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0002-sumerian-hidden-key" / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0003-bigram-assisted-key-recovery" / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0004-key-recovery-nmin" / "how-we-built-it"))

from sumer_lib import KEY_SEED, make_key  # noqa: E402
from recover_lib import rank_init, swap_delta  # noqa: E402
from nmin_lib import build_stats  # noqa: E402

POOL10 = KEY_SEED + 12000
WIN_REF10 = KEY_SEED + 12100
WIN_CYP10 = KEY_SEED + 12200
V_U10 = 353
N_WINDOWS = 974
NREF = 974
DEV_NREF = 500
ALPHA = 0.5
HALF = 487
GATE_KEYS = {"committed": KEY_SEED + 13000, "alt1": KEY_SEED + 13001, "alt2": KEY_SEED + 13002}
DEV_KEY_SEED = KEY_SEED + 13003
KEY_SHAS = {
    "committed": "56404ae87e7d6d7d9f6d41584a903525344598419cbf03fda7c730540e6d5605",
    "alt1": "29dd1dfe13012a3603c3c88745ef8e8c765c0e7dc20a68d5626a2474441e3784",
    "alt2": "b63bdb3b98a3b303f2b92bc1f2427870e21ac9e510749a0543eb307c7c7ef8ba",
    "dev": "2745446506bae03bd5a512cc6d852c9913f0521ea64ce35b68cfa810c49eec3c",
}
NPOS = 8
K_NULLS = 12
NULL_BASE = 777_000_000
RESTART_BASE = 42_000_000
RATIO_COMMITTED = 1.5
RATIO_KEY = 1.25
RATIO_TW = 1.25
ABS_FLOOR = 0.060
BAND_COUNTS = 3.0


def pools(texts):
    rng = random.Random(POOL10)
    idx = list(range(len(texts)))
    rng.shuffle(idx)
    h = len(idx) // 2
    return [texts[i] for i in idx[:h]], [texts[i] for i in idx[h:]]


def pos_index(i):
    return i if i < NPOS else NPOS - 1


def cipher_pos_counts(cyp_seqs, vocab):
    V = len(vocab)
    ix = {s: i for i, s in enumerate(vocab)}
    pc = [[0] * NPOS for _ in range(V)]
    for s in cyp_seqs:
        for i, t in enumerate(s):
            pc[ix[t]][pos_index(i)] += 1
    return pc


def ref_pos_logp(ref_seqs, vocab, alpha):
    V = len(vocab)
    ix = {s: i for i, s in enumerate(vocab)}
    R = [[0] * NPOS for _ in range(V)]
    T = [0] * NPOS
    for s in ref_seqs:
        for i, t in enumerate(s):
            R[ix[t]][pos_index(i)] += 1
            T[pos_index(i)] += 1
    return [[math.log((R[p][c] + alpha) / (T[c] + alpha * V)) for p in range(V)] for c in range(NPOS)]


def pos_delta(a, b, m, pc, LNP):
    x, y = m[a], m[b]
    d = 0.0
    for c in range(NPOS):
        if pc[a][c]:
            d += pc[a][c] * (LNP[c][y] - LNP[c][x])
        if pc[b][c]:
            d += pc[b][c] * (LNP[c][x] - LNP[c][y])
    return d


def total_score(m, rows, pc, logp, LNP):
    s = sum(cnt * logp[m[i]][m[k]] for i, r in enumerate(rows) for k, cnt in r.items())
    s += sum(pc[i][c] * LNP[c][m[i]] for i in range(len(m)) for c in range(NPOS) if pc[i][c])
    return s


def climb_joint(m, rows, cols, logp, pc, LNP, cap=2000, eps=1e-12):
    V = len(m)
    accepted = 0
    while accepted < cap:
        best_d, best_a, best_b = eps, -1, -1
        for a in range(V):
            for b in range(a + 1, V):
                d = swap_delta(a, b, m, rows, cols, logp) + pos_delta(a, b, m, pc, LNP)
                if d > best_d:
                    best_d, best_a, best_b = d, a, b
        if best_a < 0:
            break
        m[best_a], m[best_b] = m[best_b], m[best_a]
        accepted += 1
    return accepted


def starts(vocab, uc, ur):
    out = [rank_init(uc, ur, vocab)]
    V = len(vocab)
    for i in (1, 2):
        rng = random.Random(RESTART_BASE + i)
        m = list(range(V))
        rng.shuffle(m)
        out.append(m)
    return out


def recover_best(ref_seqs, cyp_seqs, vocab, alpha, multistart=True):
    logp, rows, cols, uc, ur = build_stats(ref_seqs, cyp_seqs, vocab, alpha)
    pc = cipher_pos_counts(cyp_seqs, vocab)
    LNP = ref_pos_logp(ref_seqs, vocab, alpha)
    best_m, best_s, best_i, best_sw = None, -math.inf, -1, 0
    for si, m0 in enumerate(starts(vocab, uc, ur) if multistart else [rank_init(uc, ur, vocab)]):
        m = m0[:]
        sw = climb_joint(m, rows, cols, logp, pc, LNP)
        s = total_score(m, rows, pc, logp, LNP)
        if s > best_s:
            best_m, best_s, best_i, best_sw = m, s, si, sw
    guess = {vocab[c]: vocab[best_m[c]] for c in range(len(vocab))}
    return guess, {"start_used": best_i, "score": best_s, "accepted_swaps": best_sw}


def null_reference(ref_seqs, i):
    rng = random.Random(NULL_BASE + i)
    out = []
    for w in ref_seqs:
        w2 = list(w)
        rng.shuffle(w2)
        out.append(w2)
    return out


def token_weighted(cyp_seqs, vocab, guess, inv):
    hits = 0
    total = 0
    for s in cyp_seqs:
        for t in s:
            total += 1
            if guess.get(t) == inv.get(t):
                hits += 1
    return hits / total if total else 0.0


def bigram_coherence(cyp_seqs, inv, ref_bi):
    hits = 0
    pairs = 0
    for s in cyp_seqs:
        for p, q in zip(s, s[1:]):
            pairs += 1
            if (inv[p], inv[q]) in ref_bi:
                hits += 1
    return hits / pairs if pairs else 0.0


def ref_bigrams(ref_seqs):
    return {(p, q) for s in ref_seqs for p, q in zip(s, s[1:])}


def band_flag(value, threshold):
    """Type-count margin below which a PASS is not cross-impl reproducible."""
    return round((value - threshold) * V_U10, 2) < BAND_COUNTS


def gate_verdict_v2(main_full, sub_full, null_max_full, null_half_max, tw_committed, tw_null_max):
    keys_replicated = sum(1 for k in GATE_KEYS if main_full[k] >= RATIO_KEY * null_max_full)
    checks = {
        "committed_gt_null_max_full": main_full["committed"] > null_max_full,
        "committed_ge_1.5x_full": main_full["committed"] >= RATIO_COMMITTED * null_max_full,
        "committed_ge_abs_floor": main_full["committed"] >= ABS_FLOOR,
        "keys_replicated_ge_2": keys_replicated >= 2,
        "halfA_ge_1.25x_half_null": sub_full["A"] >= RATIO_KEY * null_half_max["A"],
        "halfB_ge_1.25x_half_null": sub_full["B"] >= RATIO_KEY * null_half_max["B"],
        "halves_both_ge_1.25x_full_null": all(sub_full[h] >= RATIO_KEY * null_max_full for h in ("A", "B")),
        "token_weighted_ge_1.25x_null_tw": tw_committed >= RATIO_TW * tw_null_max,
    }
    return bool(all(checks.values())), checks, keys_replicated
