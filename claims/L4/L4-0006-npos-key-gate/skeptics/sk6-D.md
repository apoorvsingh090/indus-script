# sk6-D — fresh-context adversarial skeptic report for L4-0006

**Claim:** L4-0006, "Position-resolved positional term ... vs the full strengthened key gate on fresh cell #3"
**Verdict: `reproduced`** (negative conclusion and every gate-relevant number reproduced; minor
per-cell full-key counts differ by 1–2/372 from the object due to floating-point search-path
divergence, never the gate outcome).

Environment: Windows 10/11, Python 3.12.10, stdlib only, multiprocessing at ≤4 workers.
Scratch: `C:\Users\Apoorv\AppData\Local\Temp\opencode\sk6-D` (only this directory written
plus this report). Ran 2026-11-03/04.

---

## 1. Compliance and deviations

**Input pipeline.** I used the frozen `claims/L4/L4-0002-sumerian-hidden-key/how-we-built-it/sumer_lib.py`
for `sign_texts`, `indus_lengths`, `windows`, `make_key`, `encipher` (explicitly allowed). Everything
else — cell assembly, counts, objective, steepest-ascent search, scoring, nulls, adversarial variants —
is my own code (`D_core.py`, `D_run.py`, `D_maps.py`, `D_variants.py`). I did not copy method code.

**Pre-run verification (matched exactly):**

| item | reproduced |
|---|---|
| zip sha256 | `66991601…c9d54d6` (13 197 377 bytes) |
| non-empty texts | 1456 |
| pools `Random(260417835+8000)` | 728 / 728 |
| wrap ref / cyp | 0.05955 / 0.10370 (claim 0.0595 / 0.1037) |
| mean length ref / cyp | 4.5832 / 4.6345 (claim 4.58 / 4.63) |
| V_U6 union types | **372** |
| key shas committed/alt1/alt2/dev | `aa8553…` / `5e17e7…` / `56ac62…` / `d0d781…` — all four match |

**Deviations (disclosed):**
1. **Blind-protocol deviation.** While enumerating `claims/L4/` I printed `claim.yaml` for
   L4-0001/0007/0008/0009, which are outside the allowed set. L4-0009's lineage text repeats
   L4-0006's already-allowed rounded result (full 0.0753, null_max 0.0376, top-10 2/10). No
   `object/*.json`, `check.py`, or any `how-we-built-it` method code was read before my grid
   completed. This is a real protocol slip and is reported as such; it did not expose the object
   table or method implementation.
2. The scratch dir already contained files `sk6d_core.py`, `sk6d_run.py`, `sk6d_results.json`, etc.
   from a prior attempt. I did not read or execute them; my run used only my `D_*` files.
3. "positions >=8 = 8.9% of tokens" is a labeling error in the prereg: 8.88% is the fraction of
   **windows with length ≥ 8** (i.e., windows that have an index-7 slot); tokens at index ≥ 7 are
   only ~4.0%, at index ≥ 8 ~2.1%. The unambiguous formula `pos = min(index,7)` was implemented.
   Note bucket 7 therefore contains index 7 *and* index ≥8, so "positions ≥8 pooled" is imprecise.
4. Adversarial bucket variants (`posmax` 6 and 8) were run at frozen alpha=0.5 without a fresh
   dev sweep (report-only; see §6). The tie variant is a within-spec tie-break alternate.

---

## 2. Dev alpha table (dev key +9002, N_ref=500, best-of-3)

My table (top-10 hits / full-of-372), with winning start:

| alpha | top-10 | full | start |
|---|---|---|---|
| 0.001 | 4/10 | 17 | 2 |
| 0.01  | 4/10 | 22 | 2 |
| 0.1   | 4/10 | 22 | 2 |
| 0.2   | 3/10 | 31 | 0 |
| **0.5** | **9/10** | **38** | **0** |
| 1.0   | 7/10 | 45 | 0 |

Smallest alpha with ≥7/10 → **alpha\* = 0.5**, exactly as claimed. Start-winner pattern
(start 2 for alpha ≤0.1, start 0 thereafter) matches the object exactly.

Object comparison: top-10 is identical in all six cells; full differs only at 0.001 (18 vs 17),
0.01 (24 vs 22), 1.0 (43 vs 45); 0.1/0.2/0.5 match (22/31/38).

---

## 3. Gate grid at N_ref=974, alpha\*=0.5 (my numbers)

| arm | top-10 | full/372 | full frac |
|---|---|---|---|
| committed | **2/10** | **27** | 0.07258 |
| alt1 | 3/10 | 19 | 0.05108 |
| alt2 | 5/10 | 22 | 0.05914 |
| half A (first 487) | **6/10** | 33 | 0.08871 |
| half B (last 487) | **3/10** | 23 | 0.06183 |
| null_max (K=12, single-start) | — | **14** | 0.03763 |
| best-of-3 nulls (seeds 0,1) | — | 10, 5 | 0.02688, 0.01344 |

Null full counts (seeds 777000000..777000011):
`[13, 5, 14, 9, 12, 9, 9, 7, 13, 6, 9, 8]`, max 14, mean 9.5.

**Gate verdict reproduced: FAIL.**
- (a) alpha\* exists → PASS (0.5).
- (b) committed ≥8/10 → **FAIL** (2/10).
- (c) ≥2 of 3 keys ≥8/10 → **FAIL** (keys_ge8 = 0; 2,3,5).
- (d) committed full > null_max and ≥1.5× → **PASS** (27 > 14; 1.93×; claim 28/14 ≈ 2.0×).
- (e) both halves ≥6/10 → **FAIL** (A 6, B 3).

All top-10 numbers (2/3/5, 6/3) and `null_max = 14/372 = 0.03763` match the object exactly.
Full-key values differ only at committed (27 vs object 28) and half B (23 vs object 22); alt1 (19)
and alt2 (22) and half A (33) match the object. This is consistent with the object's accepted-swap
counts differing by ≤6 (committed 265 vs 270 here), i.e. a float-summation-order path divergence,
not a different method. The gate verdict is unchanged.

---

## 4. Null construction: is `null_max` an artifact?

Report-only probes, all at alpha 0.5, N_ref=974, committed key, rank-init single start:

| null reference construction | full/372 (4 seeds shown) | max |
|---|---|---|
| frozen: within-window permutation, seeds 0–19 | 20 seeds, max **14** | 14 |
| global token shuffle (window lengths fixed), seeds 0–3 | 6, 8, 4, 3 | 8 |
| position-bucket-preserving shuffle (shuffle tokens across windows at each position), seeds 0–3 | 8, 5, 10, 8 | 10 |
| frozen, best-of-3 (2 controls) | 10, 5 | 10 |

Extending to 20 within-window seeds does **not** raise null_max above 14; two alternative
structureless constructions give *lower* maxima. So `null_max = 14/372` is not an artifact of an
unusually weak null, and the single-start vs best-of-3 asymmetry does not inflate it (the two
best-of-3 nulls are well below the committed 27). Condition (d) is robust.

---

## 5. Adversarial: token-weighted and per-frequency-band full-key readings

The gate's condition (d) uses *unweighted* full-key accuracy (each of 372 types counts once). I
rescored the saved mappings (committed and the 12 gate nulls) with the same committed-key truth:

- **Token-weighted full-key accuracy:** committed **0.3325**; null max **0.2625** (null seed 8) →
  ratio **1.27×**, i.e. **below the 1.5× margin**. The “~2×” separation does **not** survive
  token weighting.
- **Per-frequency-band accuracy** (cipher types ranked by cipher frequency; committed / null max):

| band | committed | null max (12) |
|---|---|---|
| 1–10 | 0.20 | **0.40** |
| 11–50 | 0.40 | 0.175 |
| 51–100 | 0.14 | 0.10 |
| 101–200 | 0.01 | 0.05 |
| 201–372 | 0.00 | 0.013 |

The unweighted advantage is concentrated in mid/low-frequency types; on the highest-frequency
band the nulls actually beat the committed key. This does not change the gate (d) result under the
frozen metric, but it materially weakens the claim's interpretation that the method “extracts
genuine signal ~2× the structureless null”: that headline is metric-specific, and token-weighted
or high-frequency-band readings are at or below the null band.

---

## 6. Adversarial: tie/start and positional-bucket-edge variants

| variant | committed top-10 | full/372 | changes gate verdict? |
|---|---|---|---|
| frozen (first strict max, ties→earlier start) | 2/10 | 27 | — |
| tie-to-last swap (accept `≥1e-12`, later max wins; best-of-3 ties→later start) | 2/10 | 27 | **No** (same hits/full; path differs: 276 vs 270 swaps) |
| positional buckets 0..6 (`pos=min(i,6)`, pool ≥7) | 5/10 | 18 | **No** (5 < 8); note (d) would flip to FAIL if null unchanged (18/14=1.29×) |
| positional buckets 0..8 (`pos=min(i,8)`, pool ≥9) | 5/10 | 30 | **No** (5 < 8) |

Start-handling ties are moot in practice: winning-vs-runner-up objectives differ by hundreds of
nats at every dev alpha and gate arm. Bucket-edge variants move full-key accuracy substantially
(18↔30) but never lift the committed top-10 anywhere near the 8/10 bar, so **no variant changes the
FAIL verdict**. The bucket-edge sensitivity is a caution for using the (d) full-key arm as a
standalone gate: it can flip with a one-position change to the positional pooling rule.

---

## 7. Runtime and scale

| phase | wall (4 workers) | climbs |
|---|---|---|
| dev alpha sweep (6 α × 3 starts) | 621.5 s | 18 |
| gate grid (3 keys + 2 halves + 12 nulls + 2 bo3 nulls) | 1289.9 s | 33 |
| mapping/extra-null runs (adversarial) | 992.1 s | 31 |
| tie + bucket variants | 423.2 s | 9 |
| **total** | **≈55 min** | **91** |

Single climb ≈80–90 s, consistent with the ~110 s/climb budget stated in the task.

---

## 8. Concerns

1. **Reproduced verdict.** The failed strengthened gate is real: on a third fresh cell the strongest
   position-resolved formulation reaches 2/5/3/… top-10 hits, far below 8/10; dev→gate reversal is
   confirmed. I concur with the claim's headline and with its “dev-rule calibration is unreliable”
   conclusion.
2. **Full-key interpretation is metric-sensitive.** The claim's emphasized “~2× null” separation
   holds only for unweighted type accuracy. Token-weighted accuracy (1.27×) is below the prereg's
   own 1.5× margin, and the top-frequency band favors the nulls. The claim should qualify
   “genuine signal” accordingly.
3. **Positional bucket edge.** Changing the pooling boundary from index 7 to index 6 drops committed
   full from 27 to 18 (<1.5×null), while index 8 raises it to 30. A full-key-separation gate built
   on this positional term is therefore fragile to an arbitrary boundary choice; this supports the
   claim's broader caution rather than its positive separation language.
4. **Minor numeric non-portability.** Report-only/derived full-key counts differ by 1–2/372 in a
   few cells (committed 27 vs 28; half B 23 vs 22; some dev/null cells) because my swap-delta
   summation order differs from the shipped code's; accepted-swap counts differ by ≤6. All
   gate-relevant top-10 cells and `null_max` match exactly, so this is float path noise, not a
   method discrepancy.
5. **Cosmetic prereg error.** “positions ≥8 = 8.9% of tokens” is actually 8.88% of *windows* with
   length ≥8; token fractions are ~2–4%. Does not affect the implemented `min(index,7)` rule.

No repo files other than this report were modified.
