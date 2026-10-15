# L2-0003 — Rotation: bigram beats unigram on Mohenjo-daro held-out: GATE PASS

Same frozen pipeline as L2-0001 (no new modeling code), splits v2
(`6996368c…`): train Harappa+rest (1133/4533), test Mohenjo-daro (1126/5625).

## Gated result (TEST)

| Model | Accuracy | Log-loss (bits) |
|---|---|---|
| Unigram | 0.1086 | 7.1736 |
| Bigram α=0.001 | **0.1979** | 7.7352 |
| Positional (reported) | 0.1088 | 6.7571 |

Diff = **0.0892**, CI95 **[0.0805, 0.0978]** → PASS (wider margin than v1's +5.8pp).

## Notes

- Generality holds across rotation: the bigram advantage is not a Harappa quirk.
- Positional model spec (same canonical rule as L2-0001): slot(pos, len) =
  begin iff pos == 0; end iff pos == len−1 AND len > 1; else middle; len-1
  counts as begin ONLY; ties count-desc/sign-asc. Skeptic variants using other
  bucketings get 0.10–0.12 — the number is spec-sensitive, rule stated here.
- Metric disagreement as on v1 (recorded as found): accuracy favors bigram,
  log-loss favors unigram (7.17 vs 7.74) at gated α; positional wins log-loss
  (6.76) while tying accuracy. Accuracy is the gated metric.
- Path fix (`parents[3]`→`[2]` in the driver) committed separately; threshold
  text untouched throughout.
