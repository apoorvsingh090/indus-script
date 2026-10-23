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
| Bigram top-3 successor coverage (def. below) | 0.456 | cal. range 0.319–0.884 (median 0.594) | inside range |

Definition (pinned): mean over the 10 most frequent signs of
(top-3 successors' outgoing-transition count / sign's total outgoing transitions).
Per-site top-10 is NOT used here (corpus-global top-10).

Top repeated len-3 phrases (G-codes): see `object/results.json` (`top_rep3`).

## Evidentiary note

CORRECTION (skeptics sk3-A/B): the loader applies SELECTIVE reversal (L-R rows
only), not a global reversal, so counts shift slightly: as-stored 579/192 vs
corrected 576/189 — conservative direction (corrected < as-stored), gate passes
either way with large margin. The "reversal-invariant" phrasing in the first
draft overstated; global-reversal bijection does not cover selective reversal.
First run executed pre-prereg-commit due to a workdir slip; artifacts deleted and
re-run fresh after pure-prereg `903d2af` — deterministic seeds, identical numbers.
