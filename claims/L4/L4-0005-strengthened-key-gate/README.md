# L4-0005 — Strengthened key gate on a fresh cell: CONFIRMED NEGATIVE (2/2 skeptics, re-scoped per review)

Implements the strengthened gate the [L4-0004](../L4-0004-key-recovery-nmin/README.md)
skeptics specified (sk4-A/sk4-B: structureless-null arm, raised bar,
sampling arm) with a method package answering the diagnosed failure modes
(positional likelihood term + best-of-3 multi-start), evaluated on a
**fresh disjoint-pool cell** (new pool/window/key seeds, V_U5=372) so the
outcome would be genuinely open.

It was: **the dev cell fails under the frozen implementation.** No α in
[0.001, 0.01, 0.1, 0.2, 0.5, 1.0] reaches the 7/10 dev bar at N_ref=500
(hits 2/3/4/4/4/4; best full 0.1075 at α=1.0) — so α\*=None and the
strengthened gate fails at condition (a) before any gated arm runs.
Filed per the frozen rule. Reproduced by sk5-A and sk5-B (own code,
blind checkers, prereg chains byte-identical).

## What this establishes

- **The feasibility boundary is real, and we are on it.** L4-0004 passed
  7/10 with zero slack on one cell draw; the identical protocol with a
  fresh draw and a stronger method does not clear the *dev* bar at half
  the reference. Key recovery at Indus scale (~4.5k cipher tokens,
  V≈370) is not reliably inside the feasible region — it is a boundary
  phenomenon whose pass/fail flips with the corpus draw.
- **The mechanism is search/data-size, not the objective** (sk5-B): the
  true key outscores everything the search finds at every α
  (S_true − S_best = +209…+1011 nats). Over-smoothing artifacts
  (recovered outscoring true) appear only in the strongest reading at
  α≥0.5 (sk5-A).

## Skeptic qualifications (2/2 reproduced; folded in, two readings withdrawn)

- **Reading-conditional at the dev stage** (sk5-A, material): the frozen
  3-class positional term is nearly inert; sk5-A's position-resolved
  variant *with restarts at high α* clears the dev bar (α\*=0.5, up to
  10/10) — so "no α reaches 7/10" belongs to the frozen reading, not the
  method family. sk5-B's position-resolved variants (rank-init) do not
  clear it (best 6/10). Implementations diverge at the dev bar.
- **The gate fails under every reading tried**: full-reference probes
  top out at 6/10 (sk5-A, all starts) and 5/10 (sk5-B) against the 8/10
  bar — and the L4-0003-style reference-scope rescue does **not**
  transfer to this cell.
- **Withdrawn as over-strong** (with thanks): "random restarts do not
  help" (holds in the frozen reading, falsified in sk5-A's strong-reading
  family) and "positional augmentation did not rescue" (conditional on
  the inert reading).
- Report-only `full` fields are float-tie non-portable across
  implementations (±1–2/372); the bigram-denominator convention differs
  legitimately (the 0.1-cell band gap); 9 duplicate-content texts
  straddle the pools (~1%).

## Consequence for the ladder

The L3 gate stays shut: the only L4 key-recovery pass (L4-0004) is now
bracketed by a fresh-cell failure under a stronger method and stricter
gate. Any future L3 consideration requires a method that clears the
strengthened gate *on a preregistered fresh cell* — until then,
substitution-recovery calibration supports no reading claims. The named
follow-up: a preregistered normalized-position positional term (the dev
bar is near-reachable at 6/10, sk5-B).

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
