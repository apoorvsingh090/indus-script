# L4-0006 — Position-resolved method vs the strengthened gate: CONFIRMED NEGATIVE, with the failure structure inverted

Runs the strongest known formulation from the [L4-0005](../L4-0005-strengthened-key-gate/README.md)
review — position-resolved positional term ln P(t|pos), pos bucketed 0–7,
plus best-of-3 restarts — against the **unchanged** strengthened gate on
**fresh cell #3** (seeds +8000/+8100/+8200, V_U6=372; the full gated grid
had never been run under any position-resolved reading).

## Gated result — FAIL (but differently than L4-0005)

| Arm | Result | Bar | Verdict |
|---|---|---|---|
| dev key @ N_ref=500 | **9/10** (α\*=0.5) | ≥7/10 | PASS |
| committed @ 974 | **2/10** | ≥8/10 | FAIL |
| alt1 / alt2 @ 974 | 3/10, 5/10 | ≥8, ≥2-of-3 | FAIL (keys_ge8=0) |
| full-key @ 974 | **0.075 vs null-max 0.038** | > max, ≥1.5× | **PASS** |
| cipher halves | 6/10, 3/10 | ≥6 both | FAIL (B) |

## What this establishes

- **The method extracts genuine signal.** Full-key accuracy runs ~2× the
  structureless-null maximum — the first cell where the separation
  condition clears. The position-resolved term + restarts are doing real
  work (dev 9/10; restarts winning low-α cells).
- **But top-10 recovery collapses dev→gate**: 9/10 at half-reference on
  the dev key becomes 2–5/10 at full reference on all three gate keys.
  The problems are isomorphic across keys — this is tie-break/landscape
  variance plus a real dev→gate reversal, not key difficulty.
- **The dev-rule calibration is unreliable at this scale.** Dev-bar
  performance does not predict gate performance — a methodological
  negative for the α\*-by-dev-rule design itself (and a retroactive
  caveat on L4-0004's α\* framing), independent of which positional
  formulation is used.

## Consequence for the ladder

Third fresh cell, strongest known formulation, gate still uncleared — L3
stays shut. The constructive output: **full-key separation, not the
top-10 bar, is the informative recovery metric** (this method achieves
the former; the latter is variance-dominated). Any future L4 gate should
be built on full-key separation vs a structureless null — sk4-B's
original recommendation, now empirically grounded.

## Skeptic confirmation (2/2)

sk6-C and sk6-D rebuilt the frozen grid from the prereg prose with their
own code (only the audited `sumer_lib` input pipeline shared). Both
reproduce the negative verdict and every gate-bearing number: dev
4/4/4/3/9/7 → α\*=0.5; committed/alt1/alt2 2/3/5 top-10 (keys_ge8=0);
halves 6/3; null_max 14/372; full-key 27-28/372. Qualifications folded:

- The **~2× full-key separation is metric-specific**: it holds for
  unweighted type accuracy only. Token-weighted, committed 0.3325 vs
  null_max 0.2625 = **1.27×**, below the 1.5× margin; the top-frequency
  band actually favors the nulls.
- **Bucket-edge sensitivity**: `posmax=6` gives 18/372 (<1.5× null),
  `posmax=8` gives 30/372 — a standalone full-key gate is fragile to the
  positional boundary.
- The prereg phrase "8.9% of tokens" is really **8.9% of windows** with
  length ≥ 8 (4.0% of tokens sit at index ≥ 7).
- Tie and bucket variants never lift committed top-10 near 8/10; the
  top-10 negative is robust.

## Recompute (2026-11-03)

The shipped checker (`recompute=match`, gate FAIL) and a from-prose
independent rebuild (sharing only the frozen `sumer_lib` input pipeline)
reproduce the object field-for-field, including all start indices and swap
counts. This is **not** the skeptic gate: the subagent backend was
unreachable, so no fresh-context skeptics ran and the claim stays `draft`.
Details: [skeptics/RECOMPUTE-2026-11-03.md](skeptics/RECOMPUTE-2026-11-03.md).

## Evidentiary notes

- Prereg `8c88ee5` pushed before any recovery ran on this cell; design
  inputs (pools, windows, V_U6=372, key shas, pos-tail 8.9%) measured
  pre-prereg and disclosed; V_U6 coincides with L4-0005's V_U5 by chance
  (key shas coincide accordingly — cells differ by pools/windows).
- Variant lineage (sk5-A position-resolved; sk5-B npos K=8) scouted only
  on the L4-0005 cell at dev-500; disclosed at prereg.
- One infrastructure note: the first pipeline run was killed ~8h in by a
  cancelled monitoring command after "main committed"; the deterministic
  rerun reproduced every prior line exactly and completed the grid.
- License caution as L4-0002..0005: ORACC/ETCSRI CC0-per-file, attribute,
  never vendor.
