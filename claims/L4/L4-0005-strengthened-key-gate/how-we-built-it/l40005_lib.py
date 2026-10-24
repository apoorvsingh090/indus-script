"""L4-0005 — strengthened key-recovery gate on a FRESH disjoint-pool cell.

Frozen design (preregistered in ../claim.yaml before any recovery ran):

Cell (never measured before prereg; all seeds fresh vs L4-0004):
- 1456 ETCSRI sign_texts shuffled Random(KEY_SEED+7000); pool A = first 728
  (reference), pool B = rest (cipher). 974 windows each (seeds +7100/+7200),
  splits/v1 lengths, L4-0002 windowing protocol. V_U5 = 372 union types.
- Keys over V_U5 via make_key: committed=KEY_SEED, alt1=+9000, alt2=+9001,
  dev=+9002 (shas committed in claim.yaml).

Method (best-of-3 positional-augmented bigram hill-climb):
- Objective = bigram log-likelihood + positional log-likelihood (no free
  weight: both are proper likelihood components at the same alpha):
    bigram:   sum over adjacent within-window cipher pairs of
              ln P_ref(q|p), P_ref(q|p)=(Br[p][q]+a)/(Ur[p]+a*V)
    position: sum over cipher tokens of ln P_ref(cls|m(tok)),
              P(cls|p)=(Pr[p][cls]+a)/(Ur[p]+3a), cls in {begin,end,middle}
              (L1-0002b convention: pos 0 = begin; last pos with len>1 =
              end; len-1 windows begin-only).
- Search: steepest-ascent pairwise swaps (full sweep per step, first
  row-major maximum, accept iff delta > 1e-12, cap 2000), same as
  L4-0003/0004, with swap delta = bigram delta (recover_lib.swap_delta)
  + positional delta.
- Multi-start R=3: rank-init + 2 fixed random permutations
  (Random(42_000_000+i).shuffle, i=1,2); keep the final mapping with the
  highest exact total objective; ties -> earlier start.
- alpha* by the L4-0004 dev rule: smallest alpha in
  [0.001,0.01,0.1,0.2,0.5,1.0] reaching >=7/10 top-10 on the dev key at
  N_ref=500 (Counter.most_common(10) of cipher types).

Strengthened GATE (all required):
  (a) alpha* exists;
  (b) committed key top-10 >= 8/10 at N_ref=974;
  (c) >= 2 of 3 gate keys >= 8/10 at 974;
  (d) committed full-key accuracy at 974 > null_max AND >= 1.5*null_max,
      where null_max = max full-key accuracy over K=12 structureless
      controls (within-window permutation of the reference, unigram
      marginals preserved; seeds 777_000_000+i; rank-init single-start
      climb — method asymmetry disclosed, the 1.5x margin covers it;
      2 extra nulls at full best-of-3 are report-only);
  (e) sampling arm: the two disjoint 487-window halves of the cipher
      corpus (committed key) each reach top-10 >= 6/10 (scaled bar).

Gate design is informed by L4-0004 skeptic review (that is its purpose);
the fresh cell keeps the outcome open. No recovery ran on this cell
before the prereg commit.
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
from nmin_lib import build_stats  # noqa: E402  (alpha-parameterized bigram stats)

POOL5 = KEY_SEED + 7000
WIN_REF5 = KEY_SEED + 7100
WIN_CYP5 = KEY_SEED + 7200
V_U5 = 372
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
K_NULLS = 12
NULL_BASE = 777_000_000
RESTART_BASE = 42_000_000
CLS = 3  # 0=begin, 1=middle, 2=end


def pools(texts):
    rng = random.Random(POOL5)
    idx = list(range(len(texts)))
    rng.shuffle(idx)
    h = len(idx) // 2
    return [texts[i] for i in idx[:h]], [texts[i] for i in idx[h:]]


def pos_class(i, L):
    if i == 0:
        return 0
    if i == L - 1 and L > 1:
        return 2
    return 1


def cipher_pos_counts(cyp_seqs, vocab):
    """pc[cipher_type][cls] + dense positional log-probs from reference."""
    V = len(vocab)
    ix = {s: i for i, s in enumerate(vocab)}
    pc = [[0] * CLS for _ in range(V)]
    for s in cyp_seqs:
        L = len(s)
        for i, t in enumerate(s):
            pc[ix[t]][pos_class(i, L)] += 1
    return pc


def ref_pos_logp(ref_seqs, vocab, alpha):
    """LP[cls][plain] = ln P_ref(cls | plain), begin/middle/end."""
    V = len(vocab)
    ix = {s: i for i, s in enumerate(vocab)}
    ur = [0] * V
    pr = [[0] * CLS for _ in range(V)]
    for s in ref_seqs:
        L = len(s)
        for i, t in enumerate(s):
            ur[ix[t]] += 1
            pr[ix[t]][pos_class(i, L)] += 1
    LP = [[math.log((pr[p][c] + alpha) / (ur[p] + alpha * CLS)) for p in range(V)] for c in range(CLS)]
    return LP, ur


def pos_delta(a, b, m, pc, LP):
    x, y = m[a], m[b]
    d = 0.0
    for c in range(CLS):
        if pc[a][c]:
            d += pc[a][c] * (LP[c][y] - LP[c][x])
        if pc[b][c]:
            d += pc[b][c] * (LP[c][x] - LP[c][y])
    return d


def total_score(m, rows, pc, logp, LP):
    s = sum(cnt * logp[m[i]][m[k]] for i, r in enumerate(rows) for k, cnt in r.items())
    s += sum(pc[i][c] * LP[c][m[i]] for i in range(len(m)) for c in range(CLS) if pc[i][c])
    return s


def climb_joint(m, rows, cols, logp, pc, LP, cap=2000, eps=1e-12):
    V = len(m)
    accepted = 0
    while accepted < cap:
        best_d, best_a, best_b = eps, -1, -1
        for a in range(V):
            for b in range(a + 1, V):
                d = swap_delta(a, b, m, rows, cols, logp) + pos_delta(a, b, m, pc, LP)
                if d > best_d:
                    best_d, best_a, best_b = d, a, b
        if best_a < 0:
            break
        m[best_a], m[best_b] = m[best_b], m[best_a]
        accepted += 1
    return accepted


def starts(vocab, uc, ur):
    """Rank-init + 2 fixed random restarts (deterministic)."""
    out = [rank_init(uc, ur, vocab)]
    V = len(vocab)
    for i in (1, 2):
        rng = random.Random(RESTART_BASE + i)
        m = list(range(V))
        rng.shuffle(m)
        out.append(m)
    return out


def recover_best(ref_seqs, cyp_seqs, vocab, alpha, multistart=True):
    """Frozen pipeline. Returns (guess dict, diagnostics)."""
    logp, rows, cols, uc, ur = build_stats(ref_seqs, cyp_seqs, vocab, alpha)
    pc = cipher_pos_counts(cyp_seqs, vocab)
    LP, _ = ref_pos_logp(ref_seqs, vocab, alpha)
    best_m, best_s, best_i, best_sw = None, -math.inf, -1, 0
    for si, m0 in enumerate(starts(vocab, uc, ur) if multistart else [rank_init(uc, ur, vocab)]):
        m = m0[:]
        sw = climb_joint(m, rows, cols, logp, pc, LP)
        s = total_score(m, rows, pc, logp, LP)
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
