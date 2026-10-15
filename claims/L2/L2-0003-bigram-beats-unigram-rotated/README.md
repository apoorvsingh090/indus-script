# L2-0003 — Rotation: bigram beats unigram on Mohenjo-daro held-out: GATE PASS

Same frozen pipeline as L2-0001 (no new modeling code), splits v2
(`6996368c…`): train Harappa+rest (1133/4533), test Mohenjo-daro (1126/5625).

## Gated result (TEST)

| Model | Accuracy |
|---|---|
| Unigram | 0.1086 |
| Bigram α=0.001 | **0.1979** |
| Positional (reported) | 0.1088 |

Diff = **0.0892**, CI95 **[0.0805, 0.0978]** → PASS (wider margin than v1's +5.8pp).

## Notes

- Generality holds across rotation: the bigram advantage is not a Harappa quirk.
- Positional ≈ unigram here (0.1088 vs 0.1086), underperformed on v1 test —
  slot marginals carry no predictive edge either way. Recorded as found.
- Path fix (`parents[3]`→`[2]` in the driver) committed separately; threshold
  text untouched throughout.
