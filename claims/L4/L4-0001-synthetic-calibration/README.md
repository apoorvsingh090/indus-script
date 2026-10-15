# L4-0001 — Synthetic calibration: GATE PASS (linguistic@1948 all three)

Frozen L1/L2 methods rerun on two synthetic families with known generators
(GEN_SEED 260417834, nested sizes, Indus-matched lengths). Null/bootstrap
budgets reduced (B=100/1000) vs production — stated tradeoff.

## Gate: linguistic-like (English excerpts) at N=1948 — PASS all three

| N | ENT C vs null-min | L2 diff [CI] | REP rep3/rep4 vs null-max |
|---|---|---|---|
| 250 | 0.250 < 0.266 PASS | 0.0289 [0.0000, 0.0586] FAIL (touches 0!) | 4/0 vs 2/0 FAIL (rep4 tie) |
| 500 | 0.291 < 0.314 PASS | 0.0266 [0.0049, 0.0482] PASS | 13/1 vs 4/1 FAIL (rep4 tie) |
| 1000 | 0.334 < 0.367 PASS | 0.0363 [0.0196, 0.0538] PASS | 39/3 vs 6/1 PASS |
| 1948 | 0.362 < 0.407 PASS | 0.0490 [0.0376, 0.0603] PASS | 110/7 vs 13/1 PASS |

N_min (sensitivity floor): ENT ≤ 250, L2 = 500, full-panel = 1000.
The N=250 L2 miss (CI lower exactly 0.0000) marks the power cliff honestly.

## Emblem-like profile (reported, not gated) — the discriminator finding

| N=1948 | ENT | L2 | REP |
|---|---|---|---|
| Emblem | 0.615 < 0.705 PASS | −0.0230 [−0.0317, −0.0148] FAIL (bigram *worse*) | 668/98 vs 487/27 PASS |

ENT and REP fire on templates too — they detect structure, not language.
The **L2 bigram-gain bar is the discriminator** in this setup: passes on
linguistic-like at 500+, never on emblem-like (significantly negative).
Real Indus passes all three at N=1948 (L1-0001, L2-0001, L1-0003) — consistent
with the linguistic-like sensitivity profile, and L2-positive against this
emblem family. One family only: no general non-linguistic exclusion claimed.

## Method notes

- Linguistic vocab grows with N (426→1613 types): English words, alphabet
  mismatch accepted; methods are alphabet-agnostic (base-V normalization).
- Emblem test exclusions grow with N (83 at 1948): template collisions across
  random splits — the splits-v1 leakage rule working as designed.
- Transparent-box (generator params committed); hidden-key runs on real scripts
  remain open future work.
