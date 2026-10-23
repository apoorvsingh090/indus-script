"""Bigram-assisted hidden-key recovery for L4-0003.

Frozen method (preregistered in ../claim.yaml before any gated number was
computed):

- Inputs: reference plaintext half and enciphered half of the SAME frozen
  Sumerian windows used by L4-0002 (imported from L4-0002 sumer_lib:
  fetch/sign/window/encipher pipeline, seed 260417835, splits/v1 lengths,
  V=370 asserted, halves 974/974, cipher = second half).
- Init m: unigram rank match — cipher types and reference types each sorted
  by (count desc, sign asc); rank i of cipher maps to rank i of reference.
- Objective: S(m) = sum over adjacent within-window pairs (c_i, c_{i+1}) of
  the cipher half of ln P_ref(m(c_i) -> m(c_{i+1})), where
  P_ref(q|p) = (ref_bigram[p][q] + alpha) / (ref_unigram[p] + alpha*V),
  alpha = 0.001 (the L2/L4-0002 production alpha), natural log.
- Search: deterministic steepest-ascent over pairwise swaps of m. Each step
  scans ALL pairs (a,b), a<b in row-major order, computes the exact score
  delta, keeps the FIRST maximum, and accepts it iff delta > 1e-12. Stops
  when no pair improves or after 2000 accepted swaps. No randomness.
- Gate: >= 7 of the 10 most frequent cipher-half types
  (Counter(...).most_common(10), identical to L4-0002) map exactly to their
  true plaintext types; AND key-seed robustness: >= 2 of the 3 keys
  {committed (sha 3b6a6c1d...), alt1 = Random(260417835+9000+370),
  alt2 = Random(260417835+9001+370)} each satisfy the same 7/10 bar.

Method is the classic bigram hill-climb (Jakobsen 1995-style), stdlib only,
no parameters tuned on the gated data.
"""
import math
from collections import Counter

ALPHA = 0.001
EPS = 1e-12
SWAP_CAP = 2000


def build_objective(ref_seqs, cyp_seqs, vocab):
    """Sparse cipher bigram/col counts + dense reference log-transition matrix."""
    V = len(vocab)
    ix = {s: i for i, s in enumerate(vocab)}
    ref = [[ix[t] for t in s] for s in ref_seqs]
    cyp = [[ix[t] for t in s] for s in cyp_seqs]
    ur = [0] * V
    br = [[0] * V for _ in range(V)]
    for s in ref:
        for t in s:
            ur[t] += 1
        for p, q in zip(s, s[1:]):
            br[p][q] += 1
    logp = [[math.log((br[p][q] + ALPHA) / (ur[p] + ALPHA * V)) for q in range(V)]
            for p in range(V)]
    rows = [dict() for _ in range(V)]
    cols = [dict() for _ in range(V)]
    uc = [0] * V
    for s in cyp:
        for t in s:
            uc[t] += 1
        for p, q in zip(s, s[1:]):
            rows[p][q] = rows[p].get(q, 0) + 1
            cols[q][p] = cols[q].get(p, 0) + 1
    return logp, rows, cols, uc, ur


def rank_init(uc, ur, vocab):
    """Canonical unigram-rank mapping (count desc, sign asc on both sides)."""
    V = len(vocab)
    csort = sorted(range(V), key=lambda i: (-uc[i], vocab[i]))
    rsort = sorted(range(V), key=lambda i: (-ur[i], vocab[i]))
    m = [0] * V
    for r, ci in enumerate(csort):
        m[ci] = rsort[r]
    return m


def swap_delta(a, b, m, rows, cols, logp):
    """Exact S(m') - S(m) for exchanging the plaintext assignments of a and b."""
    x, y = m[a], m[b]
    d = 0.0
    for k, c in rows[a].items():
        if k != a and k != b:
            d += c * (logp[y][m[k]] - logp[x][m[k]])
    for k, c in rows[b].items():
        if k != a and k != b:
            d += c * (logp[x][m[k]] - logp[y][m[k]])
    for k, c in cols[a].items():
        if k != a and k != b:
            d += c * (logp[m[k]][y] - logp[m[k]][x])
    for k, c in cols[b].items():
        if k != a and k != b:
            d += c * (logp[m[k]][x] - logp[m[k]][y])
    caa = rows[a].get(a, 0)
    cbb = rows[b].get(b, 0)
    cab = rows[a].get(b, 0)
    cba = rows[b].get(a, 0)
    d += (caa * (logp[y][y] - logp[x][x]) + cbb * (logp[x][x] - logp[y][y])
          + cab * (logp[y][x] - logp[x][y]) + cba * (logp[x][y] - logp[y][x]))
    return d


def climb(m, rows, cols, logp, cap=SWAP_CAP, eps=EPS):
    """Steepest ascent; first row-major maximum wins ties; one accepted swap per sweep."""
    V = len(m)
    accepted = 0
    while accepted < cap:
        best_d, best_a, best_b = eps, -1, -1
        for a in range(V):
            for b in range(a + 1, V):
                d = swap_delta(a, b, m, rows, cols, logp)
                if d > best_d:
                    best_d, best_a, best_b = d, a, b
        if best_a < 0:
            break
        m[best_a], m[best_b] = m[best_b], m[best_a]
        accepted += 1
    return accepted


def recover(ref_seqs, cyp_seqs, vocab):
    """Full frozen pipeline; returns (mapping dict cipher-sign -> ref-sign, diagnostics)."""
    logp, rows, cols, uc, ur = build_objective(ref_seqs, cyp_seqs, vocab)
    m0 = rank_init(uc, ur, vocab)
    m = m0[:]
    accepted = climb(m, rows, cols, logp)
    guess = {vocab[c]: vocab[m[c]] for c in range(len(vocab))}
    return guess, {"init": m0, "final": m, "accepted_swaps": accepted}


def top10_hits(guess, cyp_seqs, inv_map):
    """Same hit-counting convention as L4-0002 (Counter.most_common(10))."""
    top = [t for t, _ in Counter(t for s in cyp_seqs for t in s).most_common(10)]
    return sum(1 for c in top if guess.get(c) == inv_map.get(c))
