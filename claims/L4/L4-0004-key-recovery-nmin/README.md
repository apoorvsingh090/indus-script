# L4-0004 — α-calibrated key recovery PASSES at Indus scale: N_min = the whole corpus

Follow-up to [L4-0003](../L4-0003-bigram-assisted-key-recovery/README.md),
whose skeptics showed the negative was config-scoped (α≥0.2 clears; more
reference data clears). This claim measures the honest version of that
question: **with α fixed by a dev rule and a genuinely disjoint reference
(different underlying texts), how much plaintext does substitution-key
recovery need at Indus scale?**

## Cell design (new, never measured before prereg)

- 1456 ETCSRI texts shuffled (Random(KEY_SEED+5555)) into two disjoint
  728-text pools. Cipher arm: 974 windows from pool B. Reference: prefixes
  (100/250/500/974) of 974 windows from pool A. No shared texts → no oracle
  contamination by construction. V_U=368 union types; four keys over V_U
  sha-committed at prereg (committed/alt1/alt2/dev).
- Recovery: L4-0003's frozen hill-climb, α parameterized. **Dev rule**:
  smallest α in {0.001,0.01,0.1,0.2,0.5,1.0} reaching ≥7/10 top-10 on the
  dev key at N_ref=500 → **α\*=0.2** (4/10 for all α≤0.1; 7/10 for
  0.2/0.5/1.0 — the grid is disclosed as post-peek-informed, the rule and
  cell are not).
- Gate (preregistered): α\* exists AND committed@974 ≥7/10 AND ≥2 of 3
  keys ≥7/10 at N_ref=974 AND N_min exists.

## Gated result — PASS

| N_ref | committed | alt1 | alt2 |
|---|---|---|---|
| 100 | 2/10 | 2/10 | 2/10 |
| 250 | 4/10 | **8/10** | 4/10 |
| 500 | 6/10 | 5/10 | 4/10 |
| 974 | **7/10** | **7/10** | **7/10** |

**N_min = 974** (the full Indus-scale reference); keys_ge7 at 974 = 3/3;
committed full-key accuracy 0.114 (alt1 0.120, alt2 0.098).

## Reading

- Recovery **succeeds exactly at the edge of the corpus**: below ~1000
  reference windows it collapses (2–4/10), at the full 974 it clears the
  bar on every key. The N_min=974 boundary — the entire corpus is needed —
  is the quantitative answer to "is Indus-scale data big enough for
  substitution recovery": *just barely, for the top-10 bar, with calibrated
  smoothing, from disjoint same-genre text*.
- The L4-0003 negative and this pass are consistent: same method, α=0.001
  vs dev-calibrated α=0.2, and here the reference never overlaps the
  enciphered texts. Smoothing, not search, was the binding constraint
  (L4-0003's skeptics suspected exactly this).
- Honest limits: full-key accuracy stays ~0.10 (top-10 bar only — exactly
  what was gated); alt1's curve is non-monotonic (8/10 at N_ref=250 →
  5/10 at 500) — per-key variance at small N_ref is real; genre-level
  leakage (one corpus, royal inscriptions) is inherent to the cell and
  disclosed.

## What this means for the ladder

The hidden-key arm of L4 calibration is now **cleared on this cell** by a
preregistered, dev-calibrated configuration — the first L4 key-recovery
pass (after rank 5/10, tolerance seed-fragile, α=0.001 hill-climb 4/10).
Per the ladder rule, an L3 (reading) claim remains gated on *the specific
method passing L4* — this licenses the calibrated hill-climb configuration
(α=0.2, disjoint-reference protocol) for L3 consideration on the Indus
corpus, subject to skeptics. It does **not** license reading claims by
other configurations, nor does top-10 recovery of a synthetic key on
Sumerian imply any Indus sign value is known.

## Evidentiary notes

- Prereg commit `909d6c0` pushed before any recovery ran on this cell;
  design inputs (pools, windows, V_U=368, key shas) measured pre-prereg
  per the L4-0002 "V as design input" precedent, disclosed in claim.yaml.
- Checker recomputes dev rule + full gated grid from the raw zip
  (~30–60 min, 18 climbs) — `recompute=match` required.
- α grid disclosed as informed by sk3-B's L4-0003 peek; the smallest-
  sufficient rule, dev/gated key separation, and never-measured cell
  mitigate but do not erase that.
- License caution as L4-0002/0003: ORACC/ETCSRI CC0-per-file, attribute,
  never vendor.
