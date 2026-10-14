verdict: reproduced

# Skeptic-2 independent audit — L1-0001 Rao-entropy replication

Independent reimplementation from raw CSV. No code from `how-we-built-it/`,
`check.py`, `object/results.json`, `baseline_snapshot/nulls.json`, or
`skeptics/skeptic-task-01.md` was opened. Only `claim.yaml`, `README.md`, and
`agents/skeptic-protocol.md` were read, plus the raw corpus CSV and the
methods papers in `ronojoy-indus/papers/` (method background only).

Throwaway code: `C:\Users\Apoorv\AppData\Local\Temp\opencode\skeptic2\skeptic2_rep.py`
(seed 20261014), numbers dump `skeptic2_numbers.json` in the same dir.
Nothing else in the repo was touched.

## Environment

- OS: Windows-11-10.0.26200-SP0 (win32, PowerShell 5.1)
- Python 3.12.10 (MSC v.1943 64-bit), stdlib only (`csv, math, random, hashlib, collections, json, statistics`)
- Raw corpus: `C:\Users\Apoorv\AppData\Local\Temp\opencode\hf-indus\indus_website_real_corpus.csv`
- Seed: 20261014 (own, differs from claim's 260417828 and from skeptic-1)
- B_global = 150 token-permutation shuffles across fixed lengths (requirement: B>=100 — exceeded)
- B_site = 100 within-site shuffles per top site; B_uniform = 30 iid-uniform controls

## Method (own implementation, stated fully)

1. Load CSV in stored order. Exact dedup on `sign_sequence` string (keep first
   occurrence). Tokenize by whitespace. Alphabet L = #distinct signs in deduped corpus.
2. Within-text ordered bigrams only. N1 = total tokens; N2 = total transitions
   = sum_i (len_i − 1) = N1 − #texts (len-1 texts contribute 0). 11 len-1 texts present.
3. Estimators (both in bits, log2):
   - ML: H_ML = −Σ_i (n_i/N)·log2(n_i/N), applied to unigrams (N1) and bigram-joint (N2).
   - Chao–Shen (Chao & Shen 2003, Horvitz–Thompson form, as specified in task):
     H_CS = −Σ_i [ p_i·log2(p_i) / (1 − (1−p_i)^N) ], p_i = n_i/N (ML proportion),
     denominator = detection probability of type i in N draws.
     Sample coverage C_cov = 1 − f1/N (f1 = #singletons) reported separately for
     unigrams/bigrams. NOTE this is the literal task formula (no extra Good–Turing
     reweighting); it upward-corrects ML and coincides with ML as N→∞ / p_i not tiny.
   - Miller–Madow is NOT reimplemented (different-estimator requirement); the claimed
     MM value C≈0.4098 is quoted for comparison only.
4. Statistic: C = (H2 − H1)/log2(L) (base-L normalized conditional entropy).
5. Null: global token-permutation across fixed lengths — pool all N1 tokens, shuffle,
   re-chunk to original per-text lengths. Preserves unigram counts (H1 identical by
   construction), destroys bigram order. B=150.
6. Uniform control: iid uniform over the observed L-sign alphabet, same lengths, B=30.
7. Site-stratified: split deduped inscriptions by `site`; top-3 by count; per-site C_real
   (ML+CS) plus B=100 shuffles WITHIN each site (pool only that site's tokens).
8. Half-split: SHA256(inscription_id) mod 2 → halves; C on each.

## Numbers

### Gate counts (raw CSV)

| Item | Claimed | Found |
|---|---|---|
| SHA256 CSV | 7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8 | match (recomputed) |
| Raw rows | 2543 | 2543 |
| Raw tokens | 11280 | 11280 |
| Deduped texts (exact `sign_sequence`) | 1918 | 1918 |
| Deduped tokens | 9001 | 9001 |
| L (distinct signs, deduped) | 592 | 592 |
| All `line_count`==1 | all single-line | 2543/2543 == "1" |
| N2 bigram transitions (9001−1918) | ~9k implied | 7083 |
| Distinct bigrams (real) | not stated | 2981 (2083 singletons) |
| Distinct bigrams (one uniform example) | — | 6997 (6912 singletons) |

Gate (c) PASS.

### Global: mine vs claimed (base-L normalized C)

| Lens | C_real (mine) | Null shuffled (mine) | Uniform (mine) | Claimed (MM) |
|---|---|---|---|---|
| ML (plain, no MM) | **0.3819** (H1=6.920, H2=10.438 bits) | mean 0.5177, sd 0.0014, **min 0.5145**, B=150 | mean 0.3917, sd 0.0004, min 0.3908, B=30 | — |
| Chao–Shen | **0.6218** (H1=7.156, H2=12.882 bits) | mean 0.9436, sd 0.0047, **min 0.9327**, B=150 | mean 1.1870, sd 0.0021, min 1.1833, B=30 | — |
| Miller–Madow (claimed) | — | — | — | C_real **0.4098** < null-min 0.5593 (mean 0.5633 sd 0.0016, B=200) and < uniform 0.4642 |

Coverages (mine, global deduped): unigram C_cov = 1−215/9001 = 0.9761; bigram C_cov = 1−2083/7083 = 0.7059.

Gaps:
- ML: real 0.3819 vs null-min 0.5145 → Δ=0.1326, z≈(0.5177−0.3819)/0.0014 ≈ **98σ**. PASS (also < p0.5 percentile trivially).
- Chao–Shen: real 0.6218 vs null-min 0.9327 → Δ=0.3109, z≈ **69σ**. PASS.
- Uniform: ML real 0.3819 < uniform-mean 0.3917 (Δ≈0.010, ~22 uniform-sd) — PASS but **thin**; CS real 0.6218 < uniform-mean 1.1870 — PASS. See Objection O2.

Cross-checks: MM-vs-ML offset explained — H1_MM−H1_ML claimed 6.968−6.920=0.048 bits equals the MM penalty (m−1)/(2N) = 591/18002 nats = 0.0474 bits. Reversed reading order gives identical ML C (0.38194618 vs 0.38194618, diff ~1e-13) — confirms README direction-symmetry note.

### Site-stratified (top-3 sites by deduped count; B=100 within-site shuffles each)

| Site (n deduped) | C_real ML | Null-within-site ML (mean / min) | C_real CS | Null-within-site CS (mean / min) | Holds? |
|---|---|---|---|---|---|
| Mohenjo-daro (961) | 0.3555 | 0.4844 / 0.4788 | 0.6199 | 0.9477 / 0.9339 | yes, both lenses |
| Harappa (639) | 0.3301 | 0.4412 / 0.4360 | 0.6208 | 0.9309 / 0.9150 | yes, both lenses |
| Dholavira (68) | 0.1916 | 0.2207 / 0.2088 | 0.5594 | 0.6686 / 0.6327 | yes, both lenses (smallest margin) |

Effect holds per-site under both estimators — NOT driven by cross-site mixing. Dholavira (n=68) margin is narrowest as expected from small N, but real still below all 100 within-site nulls.

### Half-split stability (hash of inscription_id)

| Half | n | ntok | L_sub | C ML | C CS | cov1 / cov2 |
|---|---|---|---|---|---|---|
| 0 | 976 | 4534 | 446 | 0.3600 | 0.6422 | 0.9618 / 0.6287 |
| 1 | 942 | 4467 | 471 | 0.3557 | 0.6339 | 0.9505 / 0.6173 |
| Global (ref) | 1918 | 9001 | 592 | 0.3819 | 0.6218 | 0.9761 / 0.7059 |

Halves agree with each other within ~0.005 (ML) / ~0.01 (CS) and lie near global — stable. (Level shift vs global is expected: L and N change per half, so C is not directly comparable in absolute value; the point is the two halves coincide.)

## Gate checklist

- (a) Prereg-before-results: PASS. `git log` for `claim.yaml`: `9b9ed88` (2026-10-14 18:00:43 +0530, "preregister … results TBD") → `7666f94` (18:01:50, results C=0.4098) → `5f5a23e` (skeptic-1). At prereg commit the file's `result:` field reads "TBD — pipeline not yet run", `skeptics: []`, `status: draft`; threshold text is already fixed. Order is correct and content confirms no results at prereg.
- (b) Corpus hash: PASS. SHA256 recomputed = `7258…98392c8`, equals `claim.yaml:corpus_snapshot_sha256`.
- (c) Counts 1918/9001/592 after exact dedup: PASS (table above).
- (d) Wording ("deciphered"/numeric-match overstatement): PASS — no overstatement found. Only "decipher" hit in the two allowed files is the dataset filename `indus_decipher`; README explicitly marks "Numeric match to Rao Fig.1 values: cannot-check" and "Rerun of original code/data: cannot-replicate", "Structural comparison only", estimator/scheme deviations documented. No "deciphered/solved/translation" claim.
- Skeptic protocol: fresh context, own seed (20261014), own code (no forbidden files opened), B=150≥100 token-permutation nulls + within-site nulls + uniform + halves, both estimators implemented from formulas. Degrees of freedom: one pre-declared comparison (real vs null) — no multiple-comparison correction needed for the gate; site/halves splits are reported as stability checks, not gated discoveries. Novelty/lit check: ronojoy papers dir contains papers only (no code/data) — consistent with claim's "independent reimplementation, not a rerun"; Rao numbers are figure-only so no numeric comparison is possible (not attempted).

## Objections / limitations (do not overturn verdict, but must ride with the claim)

- O1 (severe bigram undersampling — acknowledged, confirmed): 592²=350,464 bins vs N2=7083 transitions; 2083/2981 distinct bigrams are singletons; bigram coverage only 0.706. Any bigram-entropy number here is a lower-bound-ish estimate, not a population value. The null gap is robust, but absolute C values are estimator-dependent (ML 0.38 vs MM 0.41 vs CS 0.62).
- O2 (uniform-control margin is estimator-fragile): under plain ML, real (0.3819) beats uniform (0.3917) by only ~0.01, vs the claimed MM margin 0.4098 vs 0.4642 (Δ≈0.054). The MM penalty inflates high-dispersion cases (uniform: 6997 distinct bigrams) more than structured ones (real: 2981), so the MM lens flatters the real-vs-uniform gap. The real-vs-shuffled-null gap is huge under every lens; the real-vs-uniform gap is real but small under ML and should not be oversold.
- O3 (Chao–Shen unstable in this regime — use only as robustness check): uniform CS mean C=1.187 exceeds the nominal [0,1] range for a base-L normalized conditional entropy, and null CS means sit at ~0.94. With coverage 0.71 the Horvitz–Thompson 1/(1−(1−p)^N) weights blow up on singletons. Direction (real << null) survives, but absolute CS values are not interpretable as normalized entropies here. Reporting CS as primary would be misleading; ML+MM are the safer lenses.
- O4 (scheme/corpus drift — already disclosed, restated): G-scheme L=592 / 1918 texts / 9001 tokens vs Rao M77 L=417 / 1548 / 7000; estimator MM≠NSB. This is a structural-pattern replication only, not a numeric or code rerun. Any future "verified" label must keep the "structural, with nulls" qualifier and the "values not directly comparable to Rao Fig.1" caveat.
- O5 (dedup definition matters, sensitivity not shown here): exact-`sign_sequence` dedup drops 24.6% (625/2543). Result is conditional on that hygiene choice; near-dup / len-1 handling could shift C. Not tested here beyond the required site/half splits (len-1 texts contribute tokens but no bigrams — negligible at 11/1918).

## Bottom line

Core claim reproduces under two new lenses (ML, Chao–Shen), a new seed, larger-B nulls, per-site nulls, and half-splits: real C sits ~70–100σ below token-permutation nulls, in every site and every half. Gate checks (a)–(d) all pass. Verdict: **reproduced** (structural only, with the estimator/caveat objections above).
