# L1-0004 — Zipfian-iid control: DISTINGUISHABLE (d=0.27 ≥ 0.05, PASS)

Sproat-style counterexample (iid draws, Zipf exponent fit from the corpus itself,
s = 1.4236) vs real Indus, MM estimator, base-592 logs, corrected order.

## Result

| Point | H1n (unigram) | C (conditional) |
|---|---|---|
| Real (1948 texts) | 0.7561 | 0.4167 |
| iid-Zipf synthetic (seed 260417831) | 0.4816 | 0.4189 |
| d = max Δ | **0.2746** | gate d ≥ 0.05 **PASS** |

## The interesting nuance (reported as found)

On **C alone** the counterexample matches almost exactly (0.4189 vs 0.4167) —
at the single-metric level Sproat's caution is vindicated. Separation comes from
the **joint (H1, C) profile**: H1n differs by 0.27. This is precisely Rao's reply
point ("unigram AND bigram entropies are markedly different"), now measured on an
independent corpus with a self-fit exponent. Both sides of the debate get something:
single-metric entropy does not discriminate; the 2-D profile does — for this
counterexample family.

## Cross-checks

- Own-fit s = 1.4236 vs Nair 1.46/1.49 (same ballpark, no borrowed constants).
- Real C here (0.4167) vs L1-0001 (0.4098): shift from corrected-order dedup set
  (1948 vs 1918 texts) — expected, same estimator.
- One family only (iid Zipf); does not close the broader rebuttal.
