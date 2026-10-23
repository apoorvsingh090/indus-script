# L1-0002 — Positional asymmetry (AS-STORED order): GATE NOT MET (negative)

## Result

| Metric | Real (as-stored) | Shuffled null (B=200) | Gate |
|---|---|---|---|
| n80_begin | 27 | — | — |
| n80_end | 103 | min 69, max 87 | **FAIL** (need < 27 and < 69) |

`check.py` returns FAIL (exit non-zero) as designed. Reported extras (not gated):
rigidity mean-V 0.1634 (Nair ICIT: 0.15), hapax 0.3632 (Nair: 0.33),
Zipf slope −1.4201 (Nair: −1.49). These are in the right neighborhood;
the gated asymmetry is not — see cause below.

## Cause: loader-convention error (builder's, found post-hoc)

The dataset card states: `sign_sequence` is stored left-to-right;
`reading_direction = "L-R"` means **reverse before use**, `"R-L"` means use as stored.
2440/2543 rows are L-R. This claim analyzed as-stored order throughout, so its
begin/end slots are swapped for 96% of texts. The preregistered gate therefore
tested the wrong orientation — a specification error, NOT evidence against the
literature asymmetry.

## Disposition

- This claim stands as a published **negative**: gate not met as specified.
- Corrected-orientation follow-up preregistered as **L1-0002b** (reverse L-R rows).
- Unaffected: L1-0001 (bigram joint entropy is reversal-symmetric — verified by its
  reversed-order sensitivity run, C identical) and L1-0003/L1-0004 metrics
  (reversal-invariant counts). Loader convention noted in their READMEs.
