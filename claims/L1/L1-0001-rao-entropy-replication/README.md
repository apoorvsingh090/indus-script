# L1-0001 — Rao-2009-style conditional entropy replication

Independent reimplementation from the papers (ronojoy/indus has no code/data —
papers only, MIT). Corpus: public G-scheme `indus_website` (NOT vendored).

## Corpus comparison

| | Rao et al. 2009 (M77) | This replication (G-scheme) |
|---|---|---|
| Texts | 1,548 (deduped, single-line, unambiguous) | 1,918 (exact-deduped of 2,543; all single-line) |
| Tokens | 7,000 | 9,001 |
| Alphabet | L=417 | L=592 |
| Estimator | NSB | ML + Miller-Madow (documented deviation) |
| Log base | L (alphabet size) | L (same convention) |

## Results (base-L normalized)

| Metric | Real | Shuffled null (B=200) | Uniform iid control |
|---|---|---|---|
| H1 (unigram) | 0.7566 (6.968 bits) | identical by construction | 1.0000 |
| C = (H2−H1)/log2 L | **0.4098** | 0.5633 ± 0.0016 (min 0.5593) | 0.4642 |
| Gate | — | PASS (0.4098 < 0.5593, ~97σ) | PASS (0.4098 < 0.4642) |

Sensitivity: reversed reading order gives identical C (bigram joint entropy is
direction-symmetric) — no direction assumption risk at this order.

## What replicates / does not

| Item | Verdict | Note |
|---|---|---|
| Dedup load (~24% exact dups) | replicates (24.6%) | matches planner hygiene note |
| Sequential structure far below shuffled null | replicates (pattern) | 97σ gap, pre-fixed gate |
| Real below uniform-iid control | replicates (pattern) | |
| Numeric match to Rao Fig.1 values | cannot-check | Rao numbers are figure-only; estimator (MM≠NSB) and scheme (G592≠M77) differ |
| Rerun of original code/data | cannot-replicate | ronojoy/indus ships papers only; provenance.csv corrected accordingly |

## Artifacts

- `object/results.json` — real-corpus stats; `baseline_snapshot/nulls.json` — 200 shuffled C values + uniform control.
- `how-we-built-it/`: `fetch_corpus.py` (pinned HF rev + sha), `run_replication.py`, `entropy_lib.py`.
- `check.py` recomputes from the CSV and asserts the gate (currently PASS).
- Status: `verified` (skeptic-task-01, skeptic-task-02 — the counted gate).
  An unsolicited third replication arrived as PR #1 (branch
  `skeptic/l1-0001-skeptic-task-03`, kept off the gate record): bit-identical
  numbers with own seeds/estimators, and two real findings folded in here —
  unquoted `": "` scalars broke YAML parsing repo-wide (fixed by quoting;
  parsed strings verified byte-identical) and the σ figure is seed-dependent
  informality, not a p-value. Note: that branch's quoting commit mojibakes the
  em-dashes (`???`); main's fix preserves them — do not merge PR #1 as-is.
