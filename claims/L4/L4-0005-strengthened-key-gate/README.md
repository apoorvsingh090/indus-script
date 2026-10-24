# L4-0005 — Strengthened key gate on a fresh cell: CONFIRMED NEGATIVE (dev-cell failure)

Implements the strengthened gate the [L4-0004](../L4-0004-key-recovery-nmin/README.md)
skeptics specified (sk4-A/sk4-B: structureless-null arm, raised bar,
sampling arm) with a method package answering the diagnosed failure modes
(positional likelihood term + best-of-3 multi-start), evaluated on a
**fresh disjoint-pool cell** (new pool/window/key seeds, V_U5=372) so the
outcome would be genuinely open.

It was: **the dev cell alone fails.** No α in
[0.001, 0.01, 0.1, 0.2, 0.5, 1.0] reaches the 7/10 dev bar at N_ref=500
(hits 2/3/4/4/4/4; best full-key 0.108 at α=1.0) — so α\*=None and the
strengthened gate fails at condition (a) before any gated arm runs.
Filed per the frozen rule.

## What this establishes

- **The feasibility boundary is real, and we are on it.** L4-0004 passed
  7/10 with zero slack on one cell draw; the identical protocol with a
  fresh draw and a stronger method does not even clear the *dev* bar at
  half the reference. Key recovery at Indus scale (~4.5k cipher tokens,
  V≈370) is not reliably inside the feasible region — it is a boundary
  phenomenon whose pass/fail flips with the corpus draw.
- **Multi-start does not help here:** the rank-init start beat both fixed
  random restarts at every α (best-of-3 always selected start 0) — at
  this data size random restarts land in worse basins, not better ones.
- **Positional augmentation was not the binding constraint** on this
  cell — the L1-0002b positional structure is real, but adding it to the
  objective did not move the dev hits.

## Consequence for the ladder

The L3 gate stays shut: the only L4 key-recovery pass (L4-0004) is now
bracketed by a fresh-cell failure under a stronger method and stricter
gate. Any future L3 consideration requires a method that clears the
strengthened gate *on a preregistered fresh cell* — until then,
substitution-recovery calibration supports no reading claims.

## Evidentiary notes

- Prereg `4cc930c` pushed before any recovery ran on this cell; design
  inputs (pools, windows, V_U5=372, four key shas) measured pre-prereg
  and disclosed.
- The gate thresholds were review-motivated (L4-0004 skeptics) — that is
  the claim's purpose; the fresh cell is the openness guarantee, and it
  resolved the question in the negative direction.
- Checker recomputes the dev sweep (18 climbs, ~50 min) and asserts
  α\*=None reproduces; negative filed by design. Exit-convention note:
  this checker exits 0 when the recomputation matches the filed negative
  (the printed `gate=FAIL` line carries the gate outcome) — unlike
  L4-0003/0004 whose exit 1 signals gate failure; disclosed here.
- License caution as L4-0002/0003/0004: ORACC/ETCSRI CC0-per-file,
  attribute, never vendor.
