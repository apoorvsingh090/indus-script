# L1-0003 — Formulaic repetition: GATE PASS

Corrected order, post-orient dedup (1948 texts). repK = distinct length-K
substrings in ≥2 distinct inscriptions.

## Gated result

| Metric | Real | Shuffled null max (B=200, seed 260417830) | Gate |
|---|---|---|---|
| rep3 | **576** | 111 | **PASS** |
| rep4 | **189** | 4 | **PASS** |

## Cross-version vs Nair 2026 (ICIT 1916/584/11110)

| Metric | Ours (G-592) | Nair ICIT | Note |
|---|---|---|---|
| Repeated len-3 phrases | 576 | 565 | near-exact despite version drift |
| Repeated len-4 phrases | 189 | 187 | near-exact |
| Bigram top-3 successor coverage (own def.) | 0.456 | cal. range 0.319–0.884 (median 0.594) | inside range |

Top repeated len-3 phrases (G-codes): see `object/results.json` (`top_rep3`).

## Evidentiary note

Counts are reversal-invariant (global reversal is a bijection on phrases), so the
L1-0002 loader issue cannot favor this gate; corrected order used regardless.
First run executed pre-prereg-commit due to a workdir slip; artifacts deleted and
re-run fresh after pure-prereg `903d2af` — deterministic seeds, identical numbers.
