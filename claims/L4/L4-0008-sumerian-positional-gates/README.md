# L4-0008 — positional asymmetry on Sumerian windows: NEGATIVE (no signal beyond shuffle noise)

> **Provenance (ported 2026-11-02).** Built and skeptic-closed on a divergent local branch (original ID L4-0005, Oct 18); renumbered L4-0008 here because the canonical line advanced through L4-0006. Object, checker, generator, and both skeptic reports carried over unchanged in substance; the checker was re-run in this location.

Planner's L1/linear-progression machinery (beginner/ender token concentration,
verified on the Indus corpus as L1-0002b) run on the identical 1948 Sumerian
windows as L4-0002 — a calibration of the positional method on a real
known-language script at Indus scale.

## Result

| metric | Sumerian windows | Indus (L1-0002b, 1948 texts) |
|---|---|---|
| n80_all | 72 | — |
| n80_begin | 72 (null range 64–77) | 107 |
| n80_end | 67 (null range 62–76) | 32 |
| asymmetry gap \|begin−end\| | **5** | 75 |
| null gap max (B=200, seed 260417840) | **12** | — |

**PRIMARY GATE FAIL on the shuffle arm, as designed for a negative:**
gap 5 is inside the null range (max 12; 200 draws were as large as |12|).
Both figures sit *inside* their own null ranges (begin 72 ∈ [64,77],
end 67 ∈ [62,76]).

## Reading

1. Sumerian royal-inscription excerpts in line document order show NO
   token-concentration asymmetry between window-initial and window-final
   positions at Indus scale — neither position is special beyond shuffle
   noise.
2. The L1-0002b Indus effect (begin 107 / end 32, end << null-min 67) is
   therefore NOT a generic property of structured real scripts at this data
   size under this window protocol. It is contingent on the Indus
   corpus/genre/loader conventions — which raises the value of the
   structural findings: they are specific, falsifiable facts about the
   Indus material, not tautologies that any real script passes.
3. Top begin/end signs (AN/LUGAL/KI/A…) overlap almost entirely, consistent
   with uniform positional distribution of frequent Sumerian signs (AGOOSE
   determinatives/postpositions appear everywhere).

## Prereg discipline

- n80/n80_all definitions imported UNCHANGED from the twice-audited L1-0002b
  `pos_lib`; shuffle construction mirrors `null_n80_end` exactly, extended to
  a paired (begin, end) draw; seed 260417840; B=200.
- Direction not preregistered (honest two-sided calibration cell).
- Fixed before any Sumerian positional number was computed; no amendments.

## Skeptics

Confirmed 2/2 (`skP5-A`, `skP5-B`):

- Exact replay from raw zip + splits matched the object to the digit
  (V=370, 8985 tokens; n80 72/67/72; gap 5; null gap max 12).
- Null max is seed-stable (auditor seeds: 9-14; observed gap never exceeds
  any seed's band; also fails a softer P95 bar, 5 < 7).
- Within-window composition-preserving shuffle null (auditor-added): gap max
  11 — the negative survives a fairer null, so the pool-shuffle construction
  is not the source of the verdict.
- No metric variant shows signal (JS^1/2 begin-vs-end 0.2635 in null
  [0.239, 0.293]; fractional-n80; first2/last2 — all inside null bands).
- Power: this design reliably detects gap >= ~20 (Indus's own gap 75 clears
  it trivially) — the design was capable of finding the Indus-scale effect
  had it been present.

Erratum note (2026-10-18, per auditors): `object/results.json`'s
`n_texts` field counts WINDOWS (1948), not texts. Kept as-is for history;
checker compares it positionally.
