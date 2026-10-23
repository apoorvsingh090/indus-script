# L4-0003 — Bigram-assisted hidden-key recovery: CONFIRMED NEGATIVE (3/3 keys)

Follow-up to [L4-0002](../L4-0002-sumerian-hidden-key/README.md), which named
bigram-assisted recovery as the L4-0003 candidate after exact-rank mapping
managed only 5/10 (bar ≥ 7/10) and skeptic-B showed ±2-rank tolerance is
seed-fragile (2/3 seeds).

## Setup (frozen inputs, bit-identical to the L4-0002 key arm)

Same ETCSRI zip (sha256 `66991601…`, L4-0002 checker re-run green on it
before prereg), same 1948 windows @ seed 260417835 on splits/v1 lengths,
V=370 asserted, 974/974 halves, cipher = second half under the SAME
committed key (sha `3b6a6c1d…`, public since the L4-0002 reveal).

Method (Jakobsen-1995-style, preregistered, no tuning on gated data):
unigram-rank init → deterministic steepest-ascent pairwise swaps on
bigram log-likelihood ln P_ref(q|p), α=0.001, first row-major maximum,
accept iff Δ>1e-12, cap 2000 swaps.

## Gated result

| Key | Top-10 exact hits | Bar | Full-key acc | Swaps |
|---|---|---|---|---|
| committed (`3b6a6c1d…`) | **4/10** | ≥7/10 | 0.051 | 326 |
| alt1 (KEY_SEED+9000) | **4/10** | ≥7/10 | 0.051 | 318 |
| alt2 (KEY_SEED+9001) | **4/10** | ≥7/10 | 0.046 | 303 |
| *rank-only init (L4-0002)* | *5/10* | — | — | 0 |

Gate: committed ≥7 AND ≥2 of 3 keys ≥7 → **FAIL (keys_ge7 = 0)**. The
hill-climb is consistent across keys and *underperforms even the rank-only
baseline it was meant to fix*.

## Why (mechanism, probed post-hoc)

- The objective is NOT the problem: LL(true key) = −17157 ≫ LL(init) =
  −29975. The true key is strongly preferred by the likelihood surface.
- The climb converges (326 swaps ≪ cap) at LL = −19981 — it closes ~77% of
  the init→true gap but stalls in a local optimum it cannot leave by
  pairwise swaps at N≈4500 cipher tokens.
- Worse: LL-improving swaps *cost* top-10 accuracy (5→4). With cipher ranks
  2–7 nearly tied (174/160/160/158/156/142 tokens), the greedy search trades
  near-tied top-sign assignments for marginal gains on sparse bigram cells —
  the same flat-mid-rank pathology L4-0002 diagnosed, now shown to mislead
  the likelihood optimum itself, not just rank positions.

## What this means for the ladder

At Indus scale (~9k tokens, V≈370, mean window 4.6), substitution-key
recovery now fails by three independent routes: exact rank (5/10, L4-0002),
±2-rank tolerance (seed-fragile, 2/3), bigram hill-climb (4/10, all keys).
The L4 hidden-key arm remains uncleared — which keeps the L3 gate shut for
methods of this class, exactly as the ladder intends. Escaping local optima
(e.g. restarts/annealing/EM with unigram anchoring) is future work; any
such method must preregister afresh.

## Evidentiary notes

- Prereg committed and pushed (3954eb4) before the gated run; threshold
  byte-identical prereg→results.
- Prereg amendments pre-results, disclosed: (a) generator mkdir fix after a
  first run crashed at the write step (no number written or observed);
  (b) checker exit-code convention aligned to L4-0002 (exit 1 on gate
  failure) — gate itself untouched.
- Toy-prototype (synthetic, unrelated corpus) used only to validate
  `swap_delta` exactness and runtime; never the gated windows.
- Same license caution as L4-0002: CC0 per-file-header, attribute
  ORACC/ETCSRI, never vendored.
