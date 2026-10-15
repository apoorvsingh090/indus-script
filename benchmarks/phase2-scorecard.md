# Phase 2 scorecard — what replicates, what does not, under which scheme

Date: 2026-10-14. Working corpus: `indus_website` (joyboseroy/indus_decipher @47e8616d,
G-scheme, 592 signs; 2543 raw → 1918 as-stored-dedup / 1948 corrected-dedup).
Literature columns: Rao 2009 (M77: 1548 texts/7000 tokens/417 signs, NSB),
Adhikari et al. n-gram paper (M77-EBUDS), Nair 2026 arXiv:2604.17828
(ICIT/Yajnadevam: 1916/584/11110; code NOT public — "upon request").

| # | Property | Ours (G-592) | Literature | Scheme match? | Verdict |
|---|---|---|---|---|---|
| 1 | Dedup load ~24% | 24.6% exact dups | planner hygiene note ~24% | same corpus family | replicates |
| 2 | C_real << shuffled null | 0.41 vs 0.56 (97σ, MM) | Rao Fig.1 pattern (NSB) | NO (G≠M77, MM≠NSB) | replicates (pattern-level) |
| 3 | Numeric Rao Fig.1 values | 3.77 bits (H2−H1, MM) | 3.23 bits (Nair, ICIT) | NO | cannot-check numerically; same ballpark |
| 4 | Beginner/ender asymmetry | 107 vs 32 (corrected) | 82 vs 23 (EBUDS) | NO | replicates (direction + ratio) |
| 5 | As-stored (unoriented) | 27 vs 103, gate FAIL | — (spec error, not literature) | n/a | confirmed negative (L1-0002) |
| 6 | Rigidity mean-V top-10 | 0.156 | 0.15 (Nair) | NO | replicates (near-exact) |
| 7 | Site-V M/H | 0.168/0.132 | 0.160/0.153 (Nair) | NO | replicates (direction) |
| 8 | Hapax rate | 0.363 | 0.33 (Nair) | NO | replicates (ballpark) |
| 9 | Zipf slope | −1.42 (OLS) | −1.49 (Nair) | NO | replicates (ballpark) |
| 10 | Mean length | 4.66 | 4.42 (Nair) | NO | replicates (ballpark; revision drift) |
| 11 | Repeated len-3 / len-4 | 576 / 189 | 565 / 187 (Nair) | NO | replicates (near-exact) |
| 12 | Successor coverage | 0.456 | 0.319–0.884 range (Nair cal.) | NO (own def.) | inside range |
| 13 | iid-Zipf distinguishable | d=0.27 (C-alone matches!) | Rao's reply: unigram+bigram differ markedly | n/a (new measurement) | supports Rao's reply; C-alone caution to Sproat's side |
| 14 | Nair synthetic generators | not rerun | heraldic/admin baselines | n/a | cannot-replicate (code upon-request, not public) |
| 15 | ronojoy/indus code rerun | n/a | planner assumed code existed | n/a | cannot-replicate (papers only; corrected in provenance) |

## Loader-convention finding (cross-cutting)

`sign_sequence` is stored L-to-R; `reading_direction == "L-R"` (2440/2543 rows)
means reverse-before-use (dataset card). Order-sensitive analyses MUST orient
first. Reversal-symmetric metrics (block entropy, repeat counts up to selective
shift) are robust; positional metrics are not. L1-0002 is the standing warning.

## Scheme-debt list (blocks numeric comparison)

- No M77/P82/ICIT↔G concordance exists yet (Phase 1 item still open).
- Estimators differ per study (NSB vs MM vs ML vs Chao-Shen) — absolute values
  compared only within-study; cross-study verdicts are pattern-level.
