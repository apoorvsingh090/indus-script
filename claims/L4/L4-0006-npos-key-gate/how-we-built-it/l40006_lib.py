"""L4-0006 — position-resolved key recovery vs the strengthened gate, fresh cell #3.

Frozen design (preregistered in ../claim.yaml before any recovery ran):

Cell (never measured before prereg): 1456 ETCSRI sign_texts shuffled
Random(KEY_SEED+8000); pool A = first 728 (reference), pool B = rest
(cipher); 974 windows each (seeds +8100/+8200), splits/v1 lengths;
V_U6=372 union types (equal to L4-0005's V by chance — key shas coincide
with L4-0005's because make_key(V, seed) depends only on V and seed; the
CELLS differ by pools/windows). Keys: committed=KEY_SEED, alt1=+9000,
alt2=+9001, dev=+9002 (shas in claim.yaml).

Method (strongest known formulation per L4-0005 review):
- Joint objective = bigram LL (as L4-0003/4/5) + POSITION-RESOLVED
  positional LL:  sum over cipher tokens of ln P(m(tok) | pos), where
  pos = min(index_within_window, 7)  (positions >=8 pooled; 8.9% of
  tokens), P(t|pos) = (R[t][pos] + alpha) / (T[pos] + alpha*V), R = ref
  counts of type t at pos, T[pos] = total ref tokens at pos.
  Lineage: sk5-A's position-resolved variant (cleared the L4-0005 dev bar
  8-10/10 at alpha>=0.5 with restarts) and sk5-B's npos K=8 variant
  (best 6/10 rank-init); scouted at dev-500 on the L4-0005 cell only.
- Search: steepest-ascent pairwise swaps (full sweep, first row-major
  max, accept iff delta>1e-12, cap 2000), delta = bigram part
  (recover_lib.swap_delta) + positional part.
- Multi-start best-of-3: rank-init (count desc, sign asc) + Random
  (42_000_001/+2) permutations; best exact total objective; ties to
  earlier start (restarts carried: they won at high alpha in the
  strong-reading family).
- alpha* by the L4-0004 dev rule: smallest alpha in
  [0.001,0.01,0.1,0.2,0.5,1.0] with >=7/10 top-10 on the dev key at
  N_ref=500 (Counter.most_common(10) of cipher types).

Strengthened GATE — identical to L4-0005 (all required):
  (a) alpha* exists; (b) committed top-10 >= 8/10 at N_ref=974;
  (c) >= 2 of 3 gate keys >= 8/10 at 974; (d) committed full-key at 974
  > null_max AND >= 1.5*null_max (null_max over K=12 within-window
  permuted references, rank-init single-start; 2 best-of-3 nulls
  report-only); (e) both disjoint 487-window cipher halves (committed
  key) >= 6/10.
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
from recover_lib import rank_init, swap_delta, top10_hits  # noqa: E402
from nmin_lib import build_stats  # noqa: E402

POOL6 = KEY_SEED + 8000
WIN_REF6 = KEY_SEED + 8100
WIN_CYP6 = KEY_SEED + 8200
V_U6 = 372
N_WINDOWS = 974
NREF = 974
DEV_NREF = 500
ALPHA_GRID = [0.001, 0.01, 0.1, 0.2, 0.5, 1.0]
GATE_KEYS = {"committed": KEY_SEED, "alt1": KEY_SEED + 9000, "alt2": KEY_SEED + 9001}
DEV_KEY_SEED = KEY_SEED + 9002
KEY_SHAS = {
    "committed": "aa85534978da75c5b9aa4fe04acfd9bba0ff41d8cad05a48b31b8998a34425d8",
    "alt1": "5e17e7bac36e0087b39bac38f3c7a98e2301c2ecd7f559a1f1bbd66e9d8a0fe8",
    "alt2": "56ac6216a82d3882b7dd65ce2c80f09caefea95c3d7351719ced9cc3158ca01b",
    "dev": "d0d781003f6395112e732eca6a7f7bc7d09c28ec9945c1b69a45ea4b5a72ae3e",
}
NPOS = 8  # positions 0..7, >=8 pooled
K_NULLS = 12
NULL_BASE = 777_000_000
RESTART_BASE = 42_000_000


def pools(texts):
    rng = random.Random(POOL6)
    idx = list(range(len(texts)))
    rng.shuffle(idx)
    h = len(idx) // 2
    return [texts[i] for i in idx[:h]], [texts[i] for i in idx[h:]]


def pos_index(i):
    return i if i < NPOS else NPOS - 1


def cipher_pos_counts(cyp_seqs, vocab):
    """pc[cipher_type][pos] over pos buckets 0..7."""
    V = len(vocab)
    ix = {s: i for i, s in enumerate(vocab)}
    pc = [[0] * NPOS for _ in range(V)]
    for s in cyp_seqs:
        for i, t in enumerate(s):
            pc[ix[t]][pos_index(i)] += 1
    return pc


def ref_pos_logp(ref_seqs, vocab, alpha):
    """LNP[pos][plain] = ln P_ref(plain | pos)."""
    V = len(vocab)
    ix = {s: i for i, s in enumerate(vocab)}
    R = [[0] * NPOS for _ in range(V)]
    T = [0] * NPOS
    for s in ref_seqs:
        for i, t in enumerate(s):
            R[ix[t]][pos_index(i)] += 1
            T[pos_index(i)] += 1
    LNP = [[math.log((R[p][c] + alpha) / (T[c] + alpha * V)) for p in range(V)] for c in range(NPOS)]
    return LNP


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
