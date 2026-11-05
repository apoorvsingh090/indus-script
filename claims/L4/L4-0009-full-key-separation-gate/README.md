# L4-0009 — Full-key-separation gate on fresh cell #4: CONFIRMED NEGATIVE at condition (c)

Status: **verified negative 2/2** (sk9-A, sk9-B). Preregistered before
any recovery on the cell.

## Why this claim exists

[L4-0006](../L4-0006-npos-key-gate/README.md) ran the strongest known
position-resolved formulation against the top-10-style strengthened gate
on fresh cell #3. Top-10 collapsed (committed 2/10; `keys_ge8=0`), but
full-key accuracy cleared the structureless-null condition for the first
time: **0.0753 vs null_max 0.0376 (~2x)**. Its conclusion: the top-10 bar
is variance-dominated at this scale; full-key separation is the
informative metric. This claim tests that conclusion on a **fourth fresh
cell**, with the metric and margins frozen in advance.

## Design (frozen)

- **Cell #4** (never measured before prereg): pools `Random(260417835+10000)`,
  windows `+10100/+10200`, 974 windows per side, `V_U9=371`, keys
  `+11000/+11001/+11002` (+11003 dev). All four key shas are new.
- **Method**: L4-0006 joint bigram + position-resolved objective,
  best-of-3 restarts.
- **Alpha frozen at 0.5** — no alpha selection on this cell. 0.5 was the
  L4-0006 dev optimum and the strongest-reading threshold from the
  L4-0005 review; L4-0006 showed dev-rule calibration is unreliable, so
  the claim tests the endpoint instead.
- **Nulls**: K=12 within-window permuted references, committed key,
  rank-init single start; 2 best-of-3 nulls report-only.

## Gate (all required)

| # | Condition |
|---|---|
| a | committed full-key @974 > null_max **and** ≥ 1.5×null_max |
| b | ≥ 2 of 3 gate keys full-key @974 ≥ 1.25×null_max |
| c | both 487-window cipher halves ≥ 1.25×null_max |
| d | committed full-key @974 ≥ 0.060 absolute floor |

Threshold derivation is disclosed: 1.5× and 0.060 come from the L4-0006
draft separation (0.075 vs 0.038); 1.25× is a weaker replication margin
for the other keys and the halves. Top-10 hits are computed and shipped
report-only.

## Result — FAIL at condition (c)

| Arm | Result | Check |
|---|---|---|
| committed full @974 | **0.1725** (64/371) vs null_max 0.0674 | (a) PASS — 2.56×, > floor |
| gate keys full @974 | 0.1725 / 0.1429 / 0.1536 | (b) PASS — 3/3 ≥ 1.25× |
| halves A / B full | 0.1294 / **0.0674** | (c) **FAIL** — B = 1.00× null_max |
| committed full floor | 0.1725 ≥ 0.060 | (d) PASS |
| report-only top-10 | committed 10/10, alt1 10/10, alt2 7/10 | not gated |
| dev (report-only) | top-10 9/10, full 0.1590 | not gated |

The gate fails **only** on the half-replication condition: cipher half A
keeps 1.92× the null max, while half B lands at ~1.0×. This is the first
cell with a large multi-key full-key separation and a top-10 performance
that would clear the old 8/10 bar on two of three keys — but the
advantage does not replicate on half B, so the frozen gate fails and L3
stays shut.

## Skeptic gate (2/2)

Both skeptics rebuilt the frozen grid from the prereg prose with their
own method code (shared: the audited `sumer_lib` input pipeline).

- **Reproduced**: verdict FAIL at (c); sk9-B got committed/alt1/alt2 and
  null_max **bit-exact** (64/53/57 and 25 of 371), all other arms within
  the ±1–3/371 cross-implementation float band; a float-faithful re-run
  then reproduced every shipped field, including swap counts.
- **Prereg ambiguity resolved**: restart seeds are 42000001/42000002.
- **Calibration caveat (sk9-B)**: (c) compares 487-window halves against
  a 974-window null. Half-specific nulls (K=12) max at 19/371 on *both*
  halves — under half-scale calibration half B would be 1.32× and clear
  the 1.25× margin. The frozen verdict stands as written, but successor
  half-split gates must preregister half-scale nulls.
- **Half B is a composition outlier** (2–3 pp lower reference-bigram
  coherence), not a generic small-sample effect: alternate 487-window
  splits recover 46/47/52/58 of 371.
- **Token-weighted**: half B (0.293) sits below the largest null (0.445);
  committed (0.645) far above.
- The ±1–3/371 float-path band now touches gate-bearing numbers; current
  margins absorb it — a future gate passing by <3/371 would not be
  cross-implementation reproducible.

## Evidentiary notes

- Preregistered before any recovery on this cell; design inputs (V, wrap,
  meanlen, pos-tail, key shas) measured pre-prereg and disclosed.
- The design lineage runs through the L4-0006 **draft** object, which has
  two matching recomputes but not yet the ≥2 fresh-context skeptics; that
  is disclosed in `claim.yaml` and in the limitations.
- License caution as L4-0002..0006: ORACC/ETCSRI CC0-per-file, attribute,
  never vendor.
