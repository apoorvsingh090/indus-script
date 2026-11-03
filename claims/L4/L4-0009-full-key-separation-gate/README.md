# L4-0009 — Full-key-separation gate on fresh cell #4 (PREREGISTERED)

Status: **preregistered, results TBD.** This file and `claim.yaml` were
committed before any recovery, dev sweep, or null ran on cell #4.

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

## Result

TBD. The generator (`how-we-built-it/run_l40009.py`) writes
`object/results.json` and `baseline_snapshot/gate9.json`; `check.py`
recomputes the full grid (~68 min, 36 climbs) and must print `PASS`.

## Evidentiary notes

- Preregistered before any recovery on this cell; design inputs (V, wrap,
  meanlen, pos-tail, key shas) measured pre-prereg and disclosed.
- The design lineage runs through the L4-0006 **draft** object, which has
  two matching recomputes but not yet the ≥2 fresh-context skeptics; that
  is disclosed in `claim.yaml` and in the limitations.
- License caution as L4-0002..0006: ORACC/ETCSRI CC0-per-file, attribute,
  never vendor.
