"""Disjoint-pool key-recovery cell + N_min grid for L4-0004.

Frozen design (preregistered in ../claim.yaml before any recovery ran on
this cell):

- Pools: the 1456 ETCSRI sign_texts shuffled with Random(KEY_SEED+5555);
  pool A = first 728 texts (reference pool), pool B = rest (cipher pool).
  Disjoint underlying texts => reference plaintext can never contain the
  enciphered material (no oracle contamination by construction).
- Windows: 974 from pool A @ seed KEY_SEED+6100 (reference pool; N_ref
  grid takes prefixes in generation order: 100/250/500/974), 974 from
  pool B @ seed KEY_SEED+6000 (cipher arm), lengths from Indus splits/v1,
  same windowing protocol as L4-0002/L4-0003.
- Vocab: union of both window sets, V_U = 368 (asserted). The recovery
  mapping is a permutation over V_U (types absent on a side have zero
  counts; smoothing carries them).
- Keys over V_U via sumer_lib.make_key: gate_committed = make_key(368,
  KEY_SEED) [sha 73d42c4b...], alt1 = +9000, alt2 = +9001, dev = +9002.
- Objective: same form as L4-0003 but with alpha a free parameter fixed
  by the dev rule: P_ref(q|p) = (ref_bigram[p][q]+alpha)/(ref_unigram[p]
  +alpha*V_U), natural log, transitions only.
- Dev rule (fixes alpha*): on the dev key with reference = first 500
  pool-A windows, sweep alpha in [0.001, 0.01, 0.1, 0.2, 0.5, 1.0];
  alpha* = SMALLEST alpha whose dev top-10 hits >= 7/10. If none reaches
  7/10, alpha* = null and the claim files as negative.
- Gated evaluation (alpha* frozen): top-10 exact hits for keys
  {committed, alt1, alt2} at each N_ref in {100, 250, 500, 974}.

Grid values for alpha are disclosed as informed by sk3-B's L4-0003 peek
(alpha >= 0.2 cleared there); the evaluation cell (disjoint pools, new
windows, new key basis V_U=368) has never been measured — the gate is
genuinely open.
"""
import hashlib
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0002-sumerian-hidden-key" / "how-we-built-it"))
sys.path.insert(0, str(ROOT / "claims" / "L4" / "L4-0003-bigram-assisted-key-recovery" / "how-we-built-it"))

from sumer_lib import KEY_SEED, indus_lengths, make_key  # noqa: E402
from recover_lib import climb, rank_init, top10_hits  # noqa: E402

POOL_SEED = KEY_SEED + 5555
WIN_REF = KEY_SEED + 6100
WIN_CYP = KEY_SEED + 6000
N_WINDOWS = 974
V_U = 368
ALPHA_GRID = [0.001, 0.01, 0.1, 0.2, 0.5, 1.0]
NREF_GRID = [100, 250, 500, 974]
DEV_NREF = 500
GATE_KEYS = {"committed": KEY_SEED, "alt1": KEY_SEED + 9000, "alt2": KEY_SEED + 9001}
DEV_KEY_SEED = KEY_SEED + 9002
KEY_SHAS = {
    "committed": "73d42c4b9d2fde2cc999c7e3cf2c842a4222d5c4df3f2b094cc35b82cb309da3",
    "alt1": "a50b4c8271c8971ec10f4e200a5a79ca05334ab3e1189aa09e276d15cbfbc249",
    "alt2": "d704e187974531bb21fe110a1182a06e38d0049276e1c23bcabb928a3f1abf5e",
    "dev": "733cebcc478939bfeb0289e8bfa41237ef95c1bc69351a84a6d661021471b614",
}


def pools(texts):
    rng = random.Random(POOL_SEED)
    idx = list(range(len(texts)))
    rng.shuffle(idx)
    h = len(idx) // 2
    return [texts[i] for i in idx[:h]], [texts[i] for i in idx[h:]]


def build_stats(ref_seqs, cyp_seqs, vocab, alpha):
    """Dense reference log-transitions + sparse cipher rows/cols (alpha-parameterized)."""
    V = len(vocab)
    ix = {s: i for i, s in enumerate(vocab)}
    ur = [0] * V
    br = [[0] * V for _ in range(V)]
    for s in ref_seqs:
        ss = [ix[t] for t in s]
        for t in ss:
            ur[t] += 1
        for p, q in zip(ss, ss[1:]):
            br[p][q] += 1
    logp = [[math.log((br[p][q] + alpha) / (ur[p] + alpha * V)) for q in range(V)] for p in range(V)]
    rows = [dict() for _ in range(V)]
    cols = [dict() for _ in range(V)]
    uc = [0] * V
    for s in cyp_seqs:
        ss = [ix[t] for t in s]
        for t in ss:
            uc[t] += 1
        for p, q in zip(ss, ss[1:]):
            rows[p][q] = rows[p].get(q, 0) + 1
            cols[q][p] = cols[q].get(p, 0) + 1
    return logp, rows, cols, uc, ur


def recover_at(ref_seqs, cyp_seqs, vocab, alpha):
    """Rank init + frozen climb at the given alpha; returns (guess dict, hits-helper data)."""
    logp, rows, cols, uc, ur = build_stats(ref_seqs, cyp_seqs, vocab, alpha)
    m = rank_init(uc, ur, vocab)
    swaps = climb(m, rows, cols, logp)
    guess = {vocab[c]: vocab[m[c]] for c in range(len(vocab))}
    return guess, swaps


def key_sha(seed_base):
    k = make_key(V_U, seed_base)
    return hashlib.sha256(json.dumps(k).encode()).hexdigest()
