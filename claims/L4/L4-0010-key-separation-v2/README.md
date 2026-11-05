# L4-0010 — Full-key-separation gate v2 on fresh cell #5 (PREREGISTERED)

Status: **preregistered, results TBD.** This file and `claim.yaml` were
committed before any recovery, dev sweep, or null ran on cell #5.

## Why this claim exists

L4-0009 (verified negative 2/2, sk9-A/sk9-B) found committed full-key
0.1725 (64/371) vs null 0.0674 — 2.56x, all 3 gate keys replicating —
but the gate failed because cipher half B sat at 1.00x the null max.
Two skeptic findings shaped this successor:

1. **Calibration** (sk9-B): (c) compared 487-window halves against a
   974-window null. Half-specific nulls max at 19/371 on BOTH halves;
   half B would have been 1.32x under its own scale. v2 adds
   **matched-scale half nulls** (permuted 974 reference + the half's
   487 cipher subset — the arm's true data scale), and keeps the
   original full-scale reading as a second required condition.
2. **Metric specificity** (sk6-D/sk9-B on L4-0006/L4-0009): unweighted
   separation survives token weighting only weakly (cell #4: 1.45x).
   v2 makes a **token-weighted guard** a required condition.

## Design (frozen; method unchanged byte-for-byte from L4-0009)

- **Cell #5** (never measured before prereg, cell-level inputs only):
  pools `Random(260407835+12000)`, windows `+12100/+12200`, 974 per
  side, `V_U10=377`, keys `+13000..+13003` (shas in claim.yaml).
- **Alpha frozen at 0.5**, best-of-3 restarts (seeds 42000001/42000002).
- **Gate v2** (all required): (a) committed > null_max_full, >=1.5x,
  >=0.060; (b) >=2/3 keys >=1.25x null_max_full; (c1)/(c2) each half
  >=1.25x its **matched-scale** half-null max; (c3) both halves
  >=1.25x null_max_full (the L4-0009 reading, known fragile — kept so
  a pass is robust under both calibrations); (d) token-weighted
  committed >=1.25x max token-weighted null.
- **Band policy**: pass-margins < 3/377 flagged band-adjacent
  (cross-implementation float band, ±1–3/371 established by skeptics).

Runtime ~1h45 single-process (54 climbs): 3 gate keys (best-of-3),
committed halves x3, dev, 12 full nulls + 24 half nulls (single-start).

## Interpretation rules (frozen in advance)

- PASS on the full v2 gate → the separation license survives
  matched-scale calibration; L3 escalation consideration.
- PASS on (a,b,c1,c2,d) but FAIL on (c3) → separation exists at the
  interpretable scale but depends on composition; L4 verdict recorded
  per the frozen gate (fail), with the calibration split documented as
  the finding.
- FAIL everywhere → decisive: the method counts high-frequency
  structure only.

## Evidentiary notes

- Preregistered before any recovery on this cell; design inputs
  (pools, windows, V, wrap, meanlen, pos-tail, key shas) measured
  pre-prereg at cell level only.
- Design lineage through VERIFIED claims L4-0006 and L4-0009 (both
  negative, both 2/2 skeptics); thresholds carried unchanged.
- License caution: ORACC/ETCSRI CC0 per-file, attribute, never vendor.
