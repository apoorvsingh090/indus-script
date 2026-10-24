# L4-0004 — α-calibrated key recovery reaches the bar at Indus scale (2/2 skeptics, qualifications folded)

Follow-up to [L4-0003](../L4-0003-bigram-assisted-key-recovery/README.md),
whose skeptics showed the negative was config-scoped (α≥0.2 clears; more
reference data clears). This claim measures the honest version of that
question: **with α fixed by a dev rule and a genuinely disjoint reference
(different underlying texts), does substitution-key recovery reach the bar
at Indus scale, and where?** Reproduced by sk4-A and sk4-B (own code, blind
checker runs `recompute=match gate=PASS`).

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

## Gated result — PASS (reaches the bar at 974; zero slack)

| N_ref | committed | alt1 | alt2 |
|---|---|---|---|
| 100 | 2/10 | 2/10 | 2/10 |
| 250 | 4/10 | **8/10** | 4/10 |
| 500 | 6/10 | 5/10 | 4/10 |
| 974 | **7/10** | **7/10** | **7/10** |

All three keys **reach the bar** at N_ref=974 (never 8 — zero slack);
committed full-key accuracy 0.114 (alt1 0.120, alt2 0.098; skeptic bands
±2–3/368).

## Reading

- Recovery **reaches the bar only at the edge of the corpus**: below ~1000
  disjoint reference windows it collapses (2–4/10). "N_min=974" is a
  one-key zero-slack boundary (committed's final 6→7 step sits inside
  structureless-control noise; rank-10/11 gap one token) — the honest
  statement is *reaches the bar at the full corpus*, with the collapse
  below ~250 robust.
- The L4-0003 negative and this pass are consistent: same method, α=0.001
  vs dev-calibrated α=0.2, and here the reference never overlaps the
  enciphered texts. Smoothing, not search, was the binding constraint.
- Honest limits: full-key accuracy stays ~0.10 (top-10 bar only); alt1's
  curve is non-monotonic (8/10 at 250 — real variance, not tie-noise, per
  sk4-A); pool disjointness holds at object level with 6 duplicate-text
  groups (~0.33% tokens) straddling; genre leakage inherent, disclosed.

## Skeptic qualifications (2/2 reproduced; folded in, gate outcome unchanged)

- **Top-10 bar alone is weakly separated from structureless noise
  (sk4-B, material).** Under within-window-permuted references
  (unigram marginals preserved), the full preregistered gate still passes
  5/30 ≈ 17% of draws. What carries the claim is the joint pattern:
  7/7/7 across keys, full-key 0.095–0.120 vs control max 0.071, and
  committed's 6/10 at N_ref=500 above the entire control band. Future
  key-recovery gates should add a structureless-null arm, gate on
  full-key accuracy, or raise the bar — that is the design note L4-0005+
  must implement.
- **3 keys = relabeling robustness, not sampling robustness (sk4-B).**
  All keys share identical top-10 cipher counts and the same hit pattern
  (ranks 1–7 hit, 8–10 miss). The conjunct rules out key-specific luck,
  not corpus-sampling luck.
- **Zero slack (sk4-A, sk4-B).** All keys sit at exactly 7/10 at 974;
  cells are stable under reversed tie-break and α perturbation, but the
  margin is one hit.
- **α-grid peek-inheritance (sk4-A).** Disclosed at prereg; mitigated by
  the smallest-sufficient rule, dev-key separation, the never-measured
  cell, and α-insensitivity of the gate across 0.2–1.0.
- **Report-only fields not cross-implementation portable** (float
  tie-noise; L4-0003 precedent). Gated cells exact in both audits.

## What this means for the ladder

The hidden-key arm of L4 calibration is now **cleared on this cell** by a
preregistered, dev-calibrated configuration — the first L4 key-recovery
pass (after rank 5/10, tolerance seed-fragile, α=0.001 hill-climb 4/10),
confirmed 2/2. Per the ladder rule, an L3 (reading) claim remains gated on
*the specific method passing L4* — but given the folded qualifications
(top-10 bar weakly separated; zero slack), any L3 attempt from this method
must first clear a **strengthened** key-recovery gate (structureless-null
arm, full-key accuracy, or a raised bar). No Indus sign value is known:
top-10 recovery of a synthetic key on Sumerian transfers nothing to Indus
readings by itself.

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
