# L4-0010 — Full-key-separation gate v2 on fresh cell #5: FAIL at condition (c3) only

Status: **draft** (results in, awaiting >=2 fresh-context skeptics and checker confirm). This file and `claim.yaml` were
committed before any recovery on the cell (amended once, pre-recovery).

## Why this claim exists

L4-0009 (verified negative 2/2, sk9-A/sk9-B) found committed full-key
0.1725 (64/371) vs null 0.0674 — 2.56×, all 3 gate keys replicating —
but the gate failed because cipher half B sat at 1.00× the null max.
Two skeptic findings shaped this successor:

1. **Calibration** (sk9-B): (c) compared 487-window halves against a
   974-window null. Half-specific nulls max at 19/371 on BOTH halves;
   half B would have been 1.32× under its own scale. v2 adds
   **matched-scale half nulls** (permuted 974 reference + the half's
   487 cipher subset — the arm's true data scale), and keeps the
   original full-scale reading as a second required condition.
2. **Metric specificity** (sk6-D/sk9-B on L4-0006/L4-0009): unweighted
   separation survives token weighting only weakly (cell #4: 1.45×).
   v2 makes a **token-weighted guard** a required condition.

## Design (frozen; method unchanged byte-for-byte from L4-0009)

- **Cell #5** (never measured before prereg, cell-level inputs only):
  pools `Random(260417835+12000)`, windows `+12100/+12200`, 974 per
  side, `V_U10=353`, keys `+13000..+13003` (shas in claim.yaml).
- **Alpha frozen at 0.5**, best-of-3 restarts (seeds 42000001/42000002).
- **Gate v2** (all required): (a) committed > null_max_full, ≥1.5×,
  ≥0.060; (b) ≥2/3 keys ≥1.25× null_max_full; (c1)/(c2) each half
  ≥1.25× its **matched-scale** half-null max; (c3) both halves
  ≥1.25× null_max_full (the L4-0009 reading, known fragile — kept so
  a pass is robust under both calibrations); (d) token-weighted
  committed ≥1.25× max token-weighted null.
- **Band policy**: pass-margins < 3/353 flagged band-adjacent
  (cross-implementation float band, ±1–3/353 this cell).

Runtime ~1h45 single-process (54 climbs): 3 gate keys (best-of-3),
committed halves ×3, dev, 12 full nulls + 24 half nulls (single-start).

## Interpretation rules (frozen in advance)

- PASS on the full v2 gate → the separation license survives
  matched-scale calibration; L3 escalation consideration.
- PASS on (a,b,c1,c2,d) but FAIL on (c3) → separation exists at the
  interpretable scale but depends on composition; L4 verdict recorded
  per the frozen gate (fail), with the calibration split documented as
  the finding.
- FAIL everywhere → decisive: the method counts high-frequency
  structure only.

## Result — FAIL, single check (c3)

| Condition | Value | Check |
|---|---|---|
| (a) committed @974 | **0.0850** (30/353) vs null_max_full 16/353 | PASS (1.88×, > 0.060 floor) |
| (b) keys | 28 / 30 / 64 of 353 | PASS (3/3 ≥ 1.25×) |
| (c1) half A vs matched half-null | 10/353 vs 8/353 | PASS **at exact equality** (1.25×8 = 10; margin 0.0 types — band-adjacent) |
| (c2) half B vs matched half-null | 39/353 vs 11/353 | PASS (by 25.25 types) |
| (c3) both halves vs full null | A 0.625×, B 2.44× | **FAIL** (the legacy L4-0009 reading) |
| (d) token-weighted | 0.0856 vs null TW max 0.0521 | PASS (1.65×) |

Reading: the v2 **matched-scale** calibration supports separation on
both halves of this cell — A only by integer luck (a 9/353 null would
have failed it), B decisively. The legacy **full-scale** half reading
fails again, this time on half A. Two consecutive fresh cells now show
a *different* fragile half each (cell #4: B; cell #5: A), and
decoded-bigram-coherence tracks recovery direction per cell
(cell #4: A 0.5718 > B 0.5488 with A recovering 48 vs B 25 of 371;
cell #5: B 0.6741 > A 0.6627 with B recovering 39 vs A 10 of 353).
The frozen verdict stands: the gate as written fails and L3 stays
shut; the calibration finding from L4-0009 is confirmed and sharpened.

Report-only diagnostic correction: first-shipped coherence values were
computed on plaintext arms (generator bug, diag fields only); the
shipped object carries ciphertext-arm values; no recovery/gate field
is affected. Checker revalidates.

## Evidentiary notes

- Preregistered before any recovery on this cell; design inputs
  (pools, windows, V, wrap, meanlen, pos-tail, key shas) measured
  pre-prereg at cell level only.
- Design lineage through VERIFIED claims L4-0006 and L4-0009 (both
  negative, both 2/2 skeptics); thresholds carried unchanged.
- License caution: ORACC/ETCSRI CC0 per-file, attribute, never vendor.
