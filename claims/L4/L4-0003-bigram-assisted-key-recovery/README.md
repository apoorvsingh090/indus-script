# L4-0003 — Bigram-assisted hidden-key recovery: CONFIRMED NEGATIVE (2/2 skeptics, qualifications folded)

Follow-up to [L4-0002](../L4-0002-sumerian-hidden-key/README.md), which named
bigram-assisted recovery as the L4-0003 candidate after exact-rank mapping
managed only 5/10 (bar ≥ 7/10) and skeptic-B showed ±2-rank tolerance is
seed-fragile (2/3 seeds). Reproduced by sk3-A and sk3-B (own code, own
implementations; checker blind-run `recompute=match`).

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
recovery fails by three routes **as configured here** — exact rank (5/10,
L4-0002), ±2-rank tolerance (seed-fragile, 2/3), bigram hill-climb at
α=0.001 (4/10, all keys) — so the L4 hidden-key arm remains uncleared by
this claim and the L3 gate stays shut for it. This is a statement about the
preregistered configuration, **not** about hill-climbs as a class (see
skeptic qualifications below). Escaping the failure (α-calibrated rerun,
restarts/annealing with the right smoothing, more reference data) requires
a fresh preregistration.

## Skeptic qualifications (2/2 reproduced; folded in, gate unaffected)

- **α-fragility (sk3-B, material).** With everything else frozen, the same
  climb clears the bar at α ≥ 0.2 — α=1.0 gives 10/10 on all three keys
  (full-key 0.26–0.29). α=0.001 was inherited from L4-0002's L2 accuracy
  context, not calibrated for the recovery objective. The negative is
  therefore about the preregistered configuration; an α-calibrated rerun
  must preregister afresh before the hidden-key arm is declared cleared
  or uncleared for hill-climbs generally.
- **Reference scope (sk3-A, sk3-B).** Using the full ~9k-token corpus as
  reference (an oracle bound — illegitimate as decipherment, since it
  includes the target's plaintext), the frozen climb recovers 10/10 top-10
  and ~77% of the full key. The honest scenario — equal-size reference
  half — is the one that fails. Cite the negative with this condition.
- **Cross-implementation portability.** Report-only fields (final LL,
  swap counts, full-key accuracy) differ across implementations by float
  tie-noise on near-tied swaps (84/326 accepted steps have gap < 1e-9);
  quote them as bands (LL −19966…−19995, swaps 309–328). Gated cells are
  stable; the checker compares only those.
- **Adversarial variants (sk3-A).** α 0.01/0.1, first-improvement, 10
  random restarts, 3 annealings, 6 targeted restarts — all ≤ 5/10, none
  clear 7/10 within the preregistered smoothing family.
- **Cosmetic.** `results.json:n_texts` is the number of windows (1948),
  not underlying texts (1456); checker exit 1 means "gate FAIL" (negative
  by design), not "recompute mismatch" (the printed line disambiguates).

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
