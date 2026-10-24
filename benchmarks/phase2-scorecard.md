# Scorecard — what replicates, what does not, under which scheme

Date: 2026-10-14, extended 2026-10-15 (rows 16–25: L0/L2/L4). Working corpus: `indus_website` (joyboseroy/indus_decipher @47e8616d,
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
| 16 | mayig→joy cisi fidelity | 179/179 exact, bijection | derivation pipeline | P-codes | verified (L0-0001); Wells tails + M77 bridge dropped in derivation |
| 17 | P/W/M/V concordance v0.1 | 227 clean-1:1 / 80 multi / 89 unmapped / 13 contested-M | mayig features (MIT) | P/W/M/V type-level | verified (L0-0002); G unbridged |
| 18 | Next-sign, Harappa held-out | bigram 0.174 vs unigram 0.116 (+5.8pp, CI clear) | structural baseline | G-592, splits v1 | verified (L2-0001); log-loss disagrees as found |
| 19 | Next-sign, rotated (M-daro) | bigram 0.198 vs unigram 0.109 (+8.9pp) | structural baseline | G-592, splits v2 | verified (L2-0003); not a Harappa quirk |
| 20 | Methods on English-like synth | all pass @1948; N_min ENT≤250/L2=500/panel=1000 | known generator | SYNTH words | verified (L4-0001); robust floor 1000 |
| 21 | Methods on emblem synth | ENT+REP pass, L2 negative throughout | Nair-style heraldic | SYNTH templates | verified (L4-0001); L2 bar discriminates here |
| 22 | Methods on real Sumerian | ENT+L2(+15.4pp)+REP pass @1948 | known script (ETCSRI, CC0) | SUMER signs | verified-gates (L4-0002); sensitivity beyond English |
| 23 | Sealed substitution-key recovery | rank mapping 5/10 < 7 | hidden key (sha-committed) | SUMER signs | CONFIRMED NEGATIVE (L4-0002); tolerance alone insufficient |
| 24 | Fuls books as data source | reference-only | ICIT 4660/5644/17957 + concordances Ch.2.4/2.5 | ICIT/M77/P82 | blocked (© + ICIT deferred); facts banked in provenance |
| 25 | HimanshuAttri PNGs / Berkmen PDF | n/a | glyph images / reading claims | n/a | rejected (no license; unfalsifiable) |
| 26 | Bigram hill-climb key recovery (L4-0003) | 4/10 @α=0.001 (3/3 keys) < 7; rank-only 5/10 | Jakobsen-1995-style cryptanalysis | SUMER windows (L4-0002 pipeline) | verified-negative 2/2 — CONFIG-SCOPED: α≥0.2 → 10/10 (sk3-B); full-corpus ref → 10/10 (sk3-A); α-calibrated rerun = fresh prereg |
| 27 | α-calibrated recovery, disjoint pools + N_ref grid (L4-0004) | reaches bar @974 (7/7/7, zero slack); 2-4/10 @≤250; α*=0.2 dev rule | same method class | SUMER disjoint pools (V_U=368) | verified-pass 2/2 (bounded: top-10 bar passes 17% of structureless controls; joint pattern carries it; L3 needs strengthened gate) |

## Loader-convention finding (cross-cutting)

`sign_sequence` is stored L-to-R; `reading_direction == "L-R"` (2440/2543 rows)
means reverse-before-use (dataset card). Order-sensitive analyses MUST orient
first. Reversal-symmetric metrics (block entropy, repeat counts up to selective
shift) are robust; positional metrics are not. L1-0002 is the standing warning.

## Scheme-debt list (blocks numeric comparison)

- P/W/M/V v0.1 exists (L0-0002) but is type-level and provisional; G-scheme and
  the authoritative Fuls concordances remain unbridged (Phase 1 item still open).
- Estimators differ per study (NSB vs MM vs ML vs Chao-Shen) — absolute values
  compared only within-study; cross-study verdicts are pattern-level.
