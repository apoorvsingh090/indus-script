# L2-0001 — Bigram beats unigram on site-held-out next-sign: GATE PASS

Splits v1 (`0398a16b…`): train Mohenjo-daro+rest (1365/6527), val
Lothal/Dholavira/Kalibangan (185/846), test Harappa (814/3400, 156
train-overlapping seqs excluded). Top-1 next-sign accuracy, all positions.

## Gated result (TEST)

| Model | Accuracy | Log-loss (bits) |
|---|---|---|
| Unigram (baseline) | 0.1162 | 7.1193 |
| Bigram α=0.001 (val-selected; all 4 α tied on val) | **0.1738** | 7.6121 |
| Positional (reported) | 0.1029 | 6.9064 |

Diff bigram−unigram = **0.0576**, paired-bootstrap 95% CI **[0.0453, 0.0698]**
(B=2000, seed 260417833, length-weighted) → lower bound > 0 and diff > 0.01:
**PASS**.

## Notes

- Positional model spec (previously code-only — stated here after skeptic
  feedback): slot(pos, len) = begin iff pos == 0; end iff pos == len−1 AND
  len > 1; else middle. Length-1 inscriptions count as begin ONLY, never end.
  Prediction = argmax P(sign|slot) fit on train; ties broken canonically
  (count desc, sign asc), verified PYTHONHASHSEED-independent. Under this exact
  rule the reported 0.1029 reproduces (skeptic-A confirmed).
- Positional UNDERPERFORMS unigram (0.1029 < 0.1162): slot marginals alone are a
  weaker predictor than global frequency on unseen-site data, despite real
  positional rigidity (L1-0002b). Description ≠ prediction — recorded as found.
- Unigram 11.6% ≈ top-sign prior: most prediction mass sits on a few frequent signs.
- Implementation incident (pre-results, fixed): bigram argmax iterated a `set`
  (hash-order nondeterminism across processes — caught by the checker
  disagreeing with the generator). Fixed to sorted-order tie-break; numbers above
  reproduce under `PYTHONHASHSEED=99`.
- Test ≈ 3400 predictions: unpaired SE ≈ 0.7pp; observed +5.8pp with CI fully
  clear of zero — well-powered (see power_note in claim.yaml).
- Metric disagreement (skeptic-B, recorded as found): at gated α=0.001 accuracy
  favors bigram (0.1738 vs 0.1162) but LOG-LOSS favors unigram (7.12 vs 7.61
  bits) — tiny α leaves unseen bigrams near-zero mass and punishes misses;
  bigram wins log-loss only at heavier smoothing. Accuracy is the gated metric;
  log-loss direction is reported, not gated. (Positional wins log-loss at 6.91
  while losing accuracy — description ≠ prediction again.)
