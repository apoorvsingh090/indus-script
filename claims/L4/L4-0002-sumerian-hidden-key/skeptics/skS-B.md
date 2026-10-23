verdict: reproduced

# skS-B — L4-0002 audit (mechanism + tolerance angle)

Independent skeptic. Own code only (`C:\Users\Apoorv\AppData\Local\Temp\opencode\skS-B\skSB_audit.py`,
stdlib only). Read ONLY `claim.yaml`, `README.md`, `agents/skeptic-protocol.md`
before analysis. Never opened `how-we-built-it/*.py`, `check.py` (executed once,
unread, at the end), `object/results.json`, or `skeptics/*.md`.
`object/key.json` opened ONLY after all analysis, for sha/permutation check.

## Environment

- Windows, Python 3.12.10, no third-party packages.
- Raw inputs: `etcsri.zip` sha256 `214fd724…db60c3` (13,186,059 B; local copy
  verified byte-identical to the zip the builder's `check.py` fetched fresh at
  build during this audit) + Indus splits-v1 lengths (2364 seqs, pool mean 4.557).
- Own reconstruction of windows protocol from claim/README text: recursive
  `gdl_sign` extraction from per-text ORACC JSON; N=1948 contiguous excerpts,
  token-weighted text choice, modular wrap; lengths resampled w/ replacement
  from the Indus pool. GEN=260417835 primary + 2 variant seeds.

## Rebuild (own estimators)

| seed | V_win (cl.370) | meanlen (4.61) | wrap% (7.3) | ENT C<nullmin | L2 loglike@0.001 | L2 acc-gain | REP r3/r4 vs nullmax |
|---|---|---|---|---|---|---|---|
| 260417835 | 400 | 4.586 | 8.4 | 0.515<0.661 PASS | 0.005 [-0.09,0.10] FAIL | +0.225 | 575/286 vs 226/35 PASS |
| 260417836 | 403 | 4.578 | 8.0 | 0.515<0.665 PASS | 0.190 [0.09,0.28] PASS | +0.233 | 557/286 vs 227/32 PASS |
| 999001 | 401 | 4.607 | 9.4 | 0.518<0.668 PASS | 0.116 [0.03,0.21] PASS | +0.222 | 560/270 vs 232/31 PASS |

Corpus parse (own): 1457 zip members, 1456 non-empty texts (matches
`baseline_snapshot/sumer.json` `texts_available: 1456`), corpus-wide V=619
(claim: 569; the 1458-text / 370-windowed-V deltas are parse-filter differences,
see objections — qualitative gates unaffected). 974/974 halves in generation order.

## Mechanism check (main job): rank stability on halves

| seed | member /10 (cl.9) | exact /10 (cl.5) | tol ±1 /10 | tol ±2 /10 | keyed hits ×3 own keys |
|---|---|---|---|---|---|
| 260417835 | 7 | 4 | 4 | **7** | 4,4,4 |
| 260417836 | 10 | 5 | **8** | **8** | 3,6,4 |
| 999001 | 8 | 3 | 6 | 6 | 3,3,3 |

Reverse direction (ref=second half) identical in all seeds. Keyed-attack hits
equal cross-half exact agreement by construction (key-independent), as theory predicts.

- (a) Membership: 7–10/10 across seeds; claim's 9/10 inside range but above my
  GEN-seed value (7/10). Directionally stable, quantitatively softer.
- (b) Exact-rank: 3–5/10, always <7 — the FAIL reproduces in every seed,
  including the builder's exact number (5/10) on a variant seed.
- Mid-rank near-ties CONFIRMED as the cause: GEN top-10 counts
  177,168,158,153,141,120,107,99,98,90 — adjacent gaps (9,10,5,12,21,13,8,1,8,
  incl. a 1-count gap and a 0-gap tie elsewhere) are almost all below Poisson
  sqrt-noise (~10–13). Shuffling of ranks 1–9 across halves is statistically
  expected, not a fluke. Builder's examples (LUGAL/MU/GA/KID moves) are the
  same phenomenon I see (e.g. NA 2→3, LUGAL 3→1, AN 7→12 on GEN).
- TOLERANCE TEST (builder's causal story: strictness is the problem): ±2 lifts
  hits by exactly +3 in every seed (4→7, 5→8, 3→6). It clears 7/10 on 2/3 seeds
  (7 and 8) but FAILS on the third (6/10); ±1 clears only 1/3 (8 on GEN+1).
  All tolerant scores beat a rank-permutation null (p≈0.003–0.10), but the ±2
  null mean is already ~3–4.4/10, so the criterion is lax AND still seed-fragile.

## Step 3 — key commitment (opened last, analysis already frozen)

`object/key.json` file-bytes sha256 = `3b6a6c1d…c517`, matches `claim.yaml`
exactly. Content is a JSON list of length 370 and a valid permutation of
`range(370)`. No analysis was designed around its contents (all rank work used
halves + own keys).

## Step 4 — git order, wording, checker

- `git log`: prereg `1da3312` (claim.yaml + check.py + builder code, no results)
  precedes results `3ef214d` (README, baseline, key.json, results.json, small
  check.py/claim.yaml amendments = disclosed `parents[]` path fixes). Tree clean.
- No `TROPHY_CASE.md` entry for L4-0002 (correct for a draft negative); sealed
  registry has no L4-0002 row (registry currently example-only).
- Builder `check.py` executed unread (args learned via `--help` only), scratch
  outside repo: `ENT 0.447<0.627 L2 d=0.1540 [0.1405,0.1687] REP 612/317 vs 83/4
  KEY 5/10 recompute=match` → `FAIL`. Checker FAILs on the key arm as designed;
  builder numbers are self-consistent (`recompute=match`).

## Mechanism verdict

Mid-rank shuffling CONFIRMED as the failure mechanism (near-tied counts ⇒ rank
instability ⇒ exact-rank mapping fails every seed). But the builder's implied
remedy story ("tolerance will fix it") is NOT confirmed: ±2 tolerance clears the
7/10 bar in only 2/3 of my seeds and 6/10 on the third, while being a lax
criterion against null (~4/10 free). Tolerance alone is unlikely sufficient;
the L4-0003 candidate will need bigram assistance and/or a stricter-than-±2
criterion, as the README hedges but the mechanism section undersells.

## Objections / notes (none fatal to the negative claim)

1. Parse deltas: corpus V 619 vs 569; windowed V ~400 vs 370; zip members 1457
   vs "1458 texts" (non-empty 1456 matches baseline). Likely sign-filter
   differences in the builder pipeline; qualitative conclusions unaffected, but
   exact-number reproduction needs their filter, which I correctly could not use.
2. L2 exact number NOT reproduced with a standard per-token loglike estimator at
   α=0.001 (GEN: 0.007 vs claimed 0.1540; CI includes 0). It passes on variant
   seeds and at α≥0.01, and argmax-accuracy gain is +0.22–0.23 on all seeds, so
   sequential structure is real — but the L2 statistic as specified is
   estimator- and seed-fragile (tiny α ⇒ huge unseen-bigram penalties). The
   claim text underspecifies the statistic; add a sensitivity note.
3. Membership 7/10 (GEN) and 8/10 (999001) below the claimed 9/10; exact 4 and 3
   vs claimed 5 on two seeds. All within sampling variation (variant seed gives
   10/10 and 5/10), and the FAIL verdict reproduces everywhere — but the README
   mechanism numbers should be presented as one draw, not typical values.
4. Wording: `claim.yaml` title ("recovered 7+/10 by rank mapping") reads like a
   positive in listings; the negative lives only in `result:`/README. Suggest
   retitling to include "bar not cleared (5/10)". README itself is exemplary.
5. Null-scale mismatch (my REP nullmax 226/35 vs builder 83/4; my ENT nullmin
   0.66 vs 0.627) further shows null construction matters; both pass either way.

## Bottom line

The partial negative STANDS: gates pass (sensitivity real), exact-rank recovery
fails (<7/10) in 3/3 independent reconstructions, checker FAILs as designed,
commitment verifies. Mechanism (mid-rank shuffling) is real and quantified, but
tolerance alone does not robustly recover 7/10 — future-work claim needs a
stronger recipe. No evidence of peeking or misrepresentation; minor
quantitative softness and one fragile estimator (L2@0.001) noted above.
