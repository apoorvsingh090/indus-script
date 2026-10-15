# baselines/ — L2 v1 reference models (fit on train only)

- `models.py`: `Unigram`, `Bigram(alpha)`, `Positional`, plus `accuracy`
  (top-1 next-sign, all positions), `mean_logloss` (bits), `paired_bootstrap_ci`.
- Smoothing selection: bigram α from {0.001, 0.01, 0.1, 1.0} by VAL accuracy,
  ties → smallest α. Position-0 prediction backs off to unigram top.
- Frozen inputs: `../splits/v1/` (splits-sha `0398a16b…`).
- L2-0001 (`claims/L2/L2-0001-bigram-beats-unigram`) is the first scored claim.
