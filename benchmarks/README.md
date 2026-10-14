# benchmarks/

- `splits/` — fixed train/val/held-out splits. Split by **site and object**, not random line (leakage). Each split: `split.json` + `SHA256SUMS` + power analysis.
- `baselines/` — unigram, n-gram, positional model. Each: code + frozen scores on the fixed splits.
- `calibration/` — synthetic Indus-sized scripts from known languages + hidden-key runs on known scripts. Publishes minimum data size for key recovery (L4 gate).
