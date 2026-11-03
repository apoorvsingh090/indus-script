"""L4-0009 — full-key-separation gate on fresh cell #4.

Frozen design (preregistered in ../claim.yaml before any recovery ran on
this cell):

Cell (never measured before prereg): 1456 ETCSRI sign_texts shuffled
Random(KEY_SEED+10000); pool A = first 728 (reference), pool B = rest
(cipher); 974 windows each (seeds +10100/+10200), splits/v1 lengths;
V_U9=371 union types. Keys: committed=KEY_SEED+11000, alt1=+11001,
alt2=+11002, dev=+11003 (shas in claim.yaml). Fresh against every prior
cell (+7000/+8000, +7100..+8200, key bases <= +9002).

Method: the L4-0006 position-resolved joint objective, alpha FROZEN at
0.5 (no dev sweep on this cell). Alpha 0.5 was the L4-0006 dev optimum
and the strongest-reading setting from the L4-0005 review; L4-0006's
dev-rule calibration is known unreliable, so this claim tests the metric
it showed to be informative instead of re-running alpha selection.

GATE — full-key separation (all required):
  (a) committed full-key @ N_ref=974 > null_max AND >= 1.5*null_max;
  (b) >= 2 of the 3 gate keys full-key @974 >= 1.25*null_max;
  (c) both disjoint 487-window cipher halves (committed key) full-key
      >= 1.25*null_max;
  (d) committed full-key @974 >= 0.060 absolute floor (22x chance
      1/371; ~1.6x the L4-0006 null max, disclosed derivation).
null_max = max full-key over K=12 within-window permuted references
(committed key, rank-init single-start; 2 best-of-3 nulls report-only).
Top-10 hits are computed and shipped report-only, not gated.
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

POOL9 = KEY_SEED + 10000
WIN_REF9 = KEY_SEED + 10100
WIN_CYP9 = KEY_SEED + 10200
V_U9 = 371
N_WINDOWS = 974
NREF = 974
DEV_NREF = 500
ALPHA = 0.5
GATE_KEYS = {"committed": KEY_SEED + 11000, "alt1": KEY_SEED + 11001, "alt2": KEY_SEED + 11002}
DEV_KEY_SEED = KEY_SEED + 11003
KEY_SHAS = {
    "committed": "d602af01cbaa8680363c211e60fab0af1484610799ad27d4c3c6051374bc50c3",
    "alt1": "c3d4afee57f4d378896368499bd07bf671fbfd4ec281ce2eeefb076a63f4c670",
    "alt2": "2690391603c3b7e8df04f920e030fe517d121e92c5aabede953455823839d88d",
    "dev": "31355b77a67beb466bd6ffac6416c9a021f05479bed02c73a9cc63308b797a57",
}
NPOS = 8
K_NULLS = 12
NULL_BASE = 777_000_000
RESTART_BASE = 42_000_000
RATIO_COMMITTED = 1.5
RATIO_KEY = 1.25
ABS_FLOOR = 0.060


def pools(texts):
    rng = random.Random(POOL9)
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


def gate_verdict(main_full, null_max, sub_full):
    keys_replicated = sum(1 for k in GATE_KEYS if main_full[k] >= RATIO_KEY * null_max)
    checks = {
        "committed_gt_null_max": main_full["committed"] > null_max,
        "committed_ge_1.5x": main_full["committed"] >= RATIO_COMMITTED * null_max,
        "committed_ge_abs_floor": main_full["committed"] >= ABS_FLOOR,
        "keys_replicated_ge_2": keys_replicated >= 2,
        "halves_both_ge_1.25x": all(sub_full[h] >= RATIO_KEY * null_max for h in ("A", "B")),
    }
    return bool(all(checks.values())), checks, keys_replicated
