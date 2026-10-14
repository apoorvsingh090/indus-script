verdict: reproduced

# Skeptic report — L1-0001 Rao-entropy replication (skeptic-task-01)

Independent audit. I did NOT open `how-we-built-it/{entropy_lib,run_replication,fetch_corpus}.py`,
`check.py`, `object/results.json`, or `baseline_snapshot/nulls.json`.
All numbers below come from my own throwaway script:
`C:\Users\Apoorv\AppData\Local\Temp\opencode\skeptic1\skeptic_recompute.py`
(pandas + numpy + stdlib only, own estimator/null implementation, own seeds).

## Environment

- OS: Windows (win32), Python 3.12.10, pandas 2.2.2, numpy 2.4.6
- Raw input: `C:\Users\Apoorv\AppData\Local\Temp\opencode\hf-indus\indus_website_real_corpus.csv`
- Method reference: filenames in `ronojoy-indus/papers/` (not re-derived from papers; the
  statistic definition `C=(H2-H1)/log2(L)` is taken from the claim text itself).

## Estimator (my choice, stated)

- H1 = ML unigram entropy (bits); H2 = ML *joint* entropy of within-inscription
  adjacent pairs (pairs never cross inscription boundaries), bits.
- Miller–Madow correction in bits `(m-1)/(2·N·ln2)` with `m` = observed non-empty bins,
  applied to H1 and H2 separately; `C=(H2-H1)/log2(L)`, `L` = observed vocab size.
- Plain-ML values reported alongside to make the estimator gap explicit.

## Numbers: mine vs theirs

| Metric | Claim | Mine (MM) | Mine (plain ML) | Match? |
|---|---|---|---|---|
| n_texts (exact-dedup) | 1918 | 1918 | — | exact |
| n_tokens | 9001 | 9001 | — | exact |
| vocab L | 592 | 592 | — | exact |
| raw rows / dups | 2543 / 24.6% | 2543 / 625 dups (24.6%) | — | exact |
| corpus SHA256 | 72580755…98598392c8 | identical (`match: True`) | — | exact |
| H1 | 6.968 bits (0.7566 base-L) | 6.9676 bits (0.7566 base-L) | 6.9203 | yes (<0.001) |
| H2 (joint) | ~10.74 bits (implied) | 10.7413 bits | 10.4378 | yes |
| C_real | 0.4098 | **0.4098** (diff 0.0000) | 0.3819 | yes, MM exact to 4dp |
| shuffled null | min 0.5593, mean 0.5633, sd 0.0016 (B=200, seed 260417828) | min 0.5591, mean 0.5633, sd 0.0016 (B=100, **own seed 42**) | — | yes |
| uniform control | 0.4642 | **0.4640** (**own seed 1234**) | — | yes (<0.001) |

- Real C below my null minimum: **True** (gap ≈ 94.5σ under Gaussian sd; gate itself is
  rank-based `C_real < null-min`, so no normality assumption is needed).
- Real C below uniform control: **True**.
- Note: plain-ML C (0.3819) differs from MM C (0.4098) by ~0.028 — inside the 0.05
  tolerance, and expected: with ~7k transitions over 592² bins the bigram MM term
  (~0.30 bits) dominates the unigram term (~0.05 bits). Estimator choice documented,
  not a discrepancy.

## Gate checklist (planner §8 / skeptic-protocol)

- [x] Rebuilt from raw inputs with independently written code — yes (script above, own seeds).
- [x] Same sign scheme + snapshot hash — G-scheme, SHA256 matches exactly.
- [x] Threshold fixed before run — prereg commit `9b9ed88` ("L1-0001 preregister…",
      2026-10-14 18:00:43 +0530) predates results commit `7666f94` (18:01:50 +0530);
      prereg `claim.yaml` has identical hash/scheme/threshold with `result: TBD —
      pipeline not yet run`. Caveat: the gap is only ~67 s (automation-speed
      preregistration); commit ordering is valid but a human skeptic would prefer a
      larger time separation. Method files already existed at prereg time, so this
      verifies threshold-before-*results*, not threshold-before-*code*.
- [x] Null models attached — my own B=100 shuffle null + uniform control both confirm
      the claimed ordering, with moments matching theirs to 4dp despite different seed/B.
- [x] Wording — no overstatement found. Title says "replicates … (structural, with
      nulls)"; limitations explicitly disclaim numeric match to Rao Fig.1, NSB vs MM,
      G592 vs M77 scheme drift, and rerun status. Case-insensitive grep for
      `decipher|solved|translat` over `claim.yaml`+`README.md` hits only the upstream
      repo *name* (`joyboseroy/indus_decipher`), never a decipherment claim. "Replicates
      pattern" is fair; nothing claims "deciphered" or a numeric match.
- [x] Scheme caveat stated — yes, in both `claim.yaml` (`NOT M77/ICIT/P82`) and README
      comparison table.
- [n/a] Degrees of freedom / multiple-comparison correction — single pre-fixed comparison
      against a shuffle distribution; no search over metrics was evident. Rank-based gate
      needs no Gaussian assumption (the "~97σ" phrasing in README is informal effect
      size, mine is ~94.5σ; harmless).
- [n/a] Checker re-run — deliberately not executed (would require opening the forbidden
      `check.py`); my from-scratch recomputation supersedes it.

## Adversarial tests (trying to break it)

1. **Drop all length-1 texts** (11 texts; they feed H1 but no bigrams): C=0.4111 vs own
   B=50 null min 0.5608 — gate still holds. PASS (no fragility).
2. **Keep duplicates (no dedup, n=2543)**: C=0.3861 — *lower* than deduped, so the dedup
   choice is conservative w.r.t. the claimed effect, not inflating it.
3. **Single-site subset (Mohenjo-daro only, n=961 deduped)**: C=0.3870, still below the
   full-corpus null minimum (0.5591) — effect is not a cross-site mixing artifact
   (subset null not recomputed; indicative only).

## Objections / notes (minor, non-blocking)

1. Thin preregistration window (~67 s between prereg and results commits). Ordering is
   correct and content (`result: TBD`) is genuine, but future claims should separate
   preregistration and results by a less automation-trivial interval.
2. "Corpus differs (2543 texts/11280 tokens…)" in prereg limitations looks like a typo
   (11280 vs the 9001/2543-raw actually used); the README table (2543 raw → 1918/9001)
   is the correct one and matches my recomputation. Suggest fixing the stale number.
3. Novelty framing is honest (replication + frozen gate, not a new empirical finding;
   Rao 2009 is the prior art; `ronojoy/indus` is papers-only so no original code could
   be rerun). No objection — just noting the contribution is methodological hygiene.

## Conclusion

Counts exact, hash exact, MM entropy values exact to 4dp, and my fully independent null
(different seed, different B) reproduces their null moments and the gate ordering with
large margin; adversarial variants do not break it. **Reproduced.**
