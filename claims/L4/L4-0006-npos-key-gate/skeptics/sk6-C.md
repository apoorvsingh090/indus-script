# sk6-C — fresh-context reproduction of L4-0006

**Verdict: reproduced** (all gate-bearing numbers, the dev `alpha*`, all
main/half/null numbers, and the overall FAIL verdict match the object).
One report-only field diverges by 2/372 (see Discrepancies) and is
non-gating.

- Skeptic: sk6-C (fresh context)
- Date: 2026-11-03
- Environment: Windows, Python 3.12.10, stdlib only
- Scratch: `C:\Users\Apoorv\AppData\Local\Temp\opencode\sk6-C\`
- Corpus: cached `etcsri.zip`, sha256 `66991601…54d6`, 13,197,377 bytes,
  1,456 nonempty texts (verified by rebuild, not downloaded)
- Wallclock: **2295 s (~38.3 min)** for the full grid (51 climbs / 4
  workers); individual climbs 102–545 s (best-of-3 tasks report the sum).

## Blind compliance

Before my grid run completed I read only: L4-0006 `claim.yaml`/`README.md`;
L4-0002..0005 `claim.yaml`/`README.md`; `benchmarks/splits/v1/*`;
`agents/skeptic-protocol.md`; and
`claims/L4/L4-0002-sumerian-hidden-key/how-we-built-it/sumer_lib.py`.
I did **not** read `check.py`, `how-we-built-it/*` of L4-0006, the other
claims' method code, `object/*.json`, or `baseline_snapshot/*.json` until
after `results_C.json` was written. The object, the L4-0006 generator,
`recover_lib.py`, and `nmin_lib.py` were opened only afterwards, for the
discrepancy check.

**Pipeline used:** the frozen L4-0002 `sumer_lib.py` for
`sign_texts`, `indus_lengths`, `windows`, `make_key` (and the encipher
convention). **Own code** for all statistics (reference/cipher bigram and
position counts), the joint objective, the exact swap-delta, the climb,
the three starts, the null permutation, and the top-10/full-key
accounting — written from the `claim.yaml` prose, not copied from the
generator.

**Deviations disclosed:**

1. I shuffled the text list directly with `Random(260417835+8000)` rather
   than shuffling an index list first. These are provably the same
   permutation (Fisher–Yates uses the same RNG stream and the objects are
   distinct), and the resulting pools match: wrap rates 0.059548 /
   0.103696, mean lengths 4.583 / 4.634, `V_U6 = 372`.
2. The claim's design-input phrase "positions >=8 = 8.9% of tokens" is
   imprecise: **8.88% is the fraction of windows with length >= 8**; the
   token fraction at index >= 7 is 4.02%. This changes nothing in the
   method (`pos = min(index, 7)`), but it is a wording error worth noting.
3. For the two report-only best-of-3 nulls I reused control seeds
   777000000 and 777000001 with the full three starts; the shipped object
   records exactly those two values, so this matches.

## Input verification (before the climb)

| item | claim | reproduced |
|---|---|---|
| nonempty texts | 1456 | 1456 |
| V_U6 | 372 | 372 |
| wrap ref / cyp | 0.0595 / 0.1037 | 0.059548 / 0.103696 |
| mean len ref / cyp | 4.58 / 4.63 | 4.583 / 4.634 |
| committed key sha | aa855349…425d8 | match |
| alt1 sha | 5e17e7ba…0fe8 | match |
| alt2 sha | 56ac6216…01b | match |
| dev sha | d0d78100…e3e | match |

(Key shas are `sha256(json.dumps(key))`; all four match exactly.)

## Dev alpha table (dev key, N_ref=500, best-of-3)

| alpha | top-10 | full acc | start used |
|---|---|---|---|
| 0.001 | 4/10 | 0.053763 | 2 |
| 0.01 | 4/10 | 0.064516 | 2 |
| 0.1 | 4/10 | 0.059140 | 2 |
| 0.2 | 3/10 | 0.083333 | 0 |
| 0.5 | **9/10** | 0.102151 | 0 |
| 1.0 | 7/10 | 0.115591 | 0 |

`alpha* = 0.5` (smallest alpha with >=7/10). Restarts won the three
lowest-alpha columns (start 2), as the claim states.

## Main grid at alpha* = 0.5, N_ref=974

| key | top-10 | full acc | best start | swaps |
|---|---|---|---|---|
| committed | **2/10** | **0.075269** | 0 | 265 |
| alt1 | **3/10** | 0.051075 | 0 | 265 |
| alt2 | **5/10** | 0.059140 | 2 | 311 |

`keys_ge8 = 0`.

## Cipher halves (committed key, 487 windows each)

| half | top-10 | full acc | best start |
|---|---|---|---|
| A (windows 0–486) | **6/10** | 0.088710 | 0 |
| B (windows 487–973) | **3/10** | 0.059140 | 0 |

## Nulls (within-window permuted reference, committed key, 974 ref)

Single-start full-key accuracies for seeds 777000000..777000011:

```
0.029570 0.013441 0.037634 0.029570 0.032258 0.026882
0.024194 0.018817 0.037634 0.016129 0.024194 0.018817
```

`null_max = 0.037634`. Best-of-3 spot checks (seeds 777000000,
777000001): 0.029570, 0.013441 — unchanged from their rank-init
single-start values, so the main full-key margin is **not** a
best-of-3-versus-single-start search artifact.

## Gate verdict

| condition | result | pass |
|---|---|---|
| (a) alpha* exists | 0.5 | yes |
| (b) committed >= 8/10 @974 | 2/10 | **no** |
| (c) >=2/3 gate keys >= 8/10 | 0/3 | **no** |
| (d) full > null_max and >= 1.5× | 0.075269 > 0.037634 and ratio 2.00 | yes |
| (e) both halves >= 6/10 | 6, 3 | **no** |

**Gate = FAIL**, exactly as filed: dev calibrates to 9/10 but the gate
arms collapse (2/3/5), the sampling arm B fails, while the structureless
full-key separation condition clears at ~2.0× the null maximum.

## Discrepancy vs the shipped object

Everything in `object/results.json` matches **exactly** except one
report-only field:

- dev `alpha=0.001`, `full = 0.053763` (2/372 higher than the shipped
  `0.048387`). Top-10 (4/10) and start used (2) are identical, as are the
  other five dev rows and every main/half/null value and swap count.

This is the known float-tie non-portability at very heavy smoothing:
at alpha=0.001 the objective surface is nearly flat and a different
floating-point accumulation order in the exact `swap_delta` selects a
different but objective-equivalent key pair. It touches no gate field
(the dev rule consumes top-10 hits, not full accuracy). All 12 null
values, both multistart nulls, both halves, and all three main arms are
byte-identical.

## Mechanism concerns

1. **The dev rule is the weak link, confirmed.** The gate uses far more
   reference data (974 vs 500) yet recovers far fewer top-10 signs
   (2–5 vs 9). That is a genuine dev→gate reversal on isomorphic keys,
   i.e. calibration-by-dev-500 does not transport to 974. This is the
   claim's own headline methodological negative and is reproduced.
2. **The full-key arm is real but under-powered as a gate.** Measured
   separation is 2.0× the single-start null max, and the two best-of-3
   nulls did not rise, so the separation is not merely the extra search
   in the main arm. But with only 12 nulls and ~28/372 correct signs,
   the absolute margin (28 vs 14 correct) is small; the 1.5× margin is
   doing a lot of work.
3. **Top-10 gate remains variance-dominated.** The same committed key
   scores 2/10 at 974 but 6/10 on half A and 3/10 on half B; the
   dev-500 dev key scores 9/10. These differences are not interpretable
   as key difficulty and the claim does not over-read them.
4. **Deterministic-constant transparency holds.** Key shas, pools,
   windows, wraps and V all rebuild; there is no hidden randomness in the
   input pipeline, only in the disclosed restarts/null permutations.
5. **Minor wording error:** "8.9% of tokens" is really 8.9% of windows
   (token fraction 4.0%). No effect on method or result.

**Bottom line:** I independently rebuilt the frozen numbers from the raw
zip and the preregistration. The claim's negative verdict and nearly all
reported numbers reproduce exactly; the single 2/372 dev-0.001 full-key
difference is a non-gating float-tie artifact already covered by the
claim's portability limitation.
