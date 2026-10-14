verdict: reproduced

# Skeptic report — L1-0001 Rao-entropy replication (skeptic-task-03)

Independent reimplementation from the recipe in `skeptics/HOW_TO_REPRODUCE.md`,
run 2026-10-14.

**Independence disclosure (exact order of what I opened):**

1. Read first: repo `README.md`, claim `README.md`, `claim.yaml`, `agents/skeptic-protocol.md`,
   `skeptics/HOW_TO_REPRODUCE.md` (the recipe — sanctioned for skeptics), and
   `how-we-built-it/fetch_corpus.py` (step 2 explicitly prescribes the fetch script).
2. Fetched the CSV (pinned HF rev 47e8616d), verified SHA256 with `Get-FileHash`.
3. Wrote and ran **my own script from the recipe only** — at that point I had seen
   neither `how-we-built-it/entropy_lib.py`, `how-we-built-it/run_replication.py`,
   `object/results.json`, `baseline_snapshot/nulls.json`, nor `skeptics/skeptic-task-0{1,2}.md`.
4. Only after my numbers existed: ran `check.py` (step 4), then read the shipped
   `object/` + `baseline_snapshot/` artifacts for the comparison table, then the two
   prior skeptic reports.
5. `entropy_lib.py` / `run_replication.py` source: **never opened** (check.py imports
   entropy_lib at run time — unavoidable for step 4 — but I did not read its source;
   my own recompute is the independent path).

Own throwaway code (nothing else in the repo touched):

- `C:\Users\Apoorv\AppData\Local\Temp\opencode\skeptic3\skeptic3_rep.py` → `skeptic3_numbers.json`
- `C:\Users\Apoorv\AppData\Local\Temp\opencode\skeptic3\skeptic3_cs_null.py` → `skeptic3_cs.json`
- Seeds (mine): null shuffle **8675309**, alt-seed null **20261015**, uniform **31337**, CS-null **8675309 / 424242**.

## Environment

- OS: Microsoft Windows 11 Pro (win32), PowerShell 5.1
- Python 3.12.10 (CPython), **stdlib only** (`csv, math, random, collections, hashlib, json, pathlib`)
- Corpus: `C:\Users\Apoorv\AppData\Local\Temp\indus_website_real_corpus.csv`
  (downloaded from joyboseroy/indus_decipher @ HF rev `47e8616dff4d1ff62343bd74f3eeefc4afbfd4d8`)
- SHA256 recomputed twice (fetch script + `Get-FileHash -Algorithm SHA256`):
  `7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8` — **matches
  `claim.yaml:corpus_snapshot_sha256` exactly**.

## Method (my implementation, stated)

1. Parse CSV, take `sign_sequence`, split on whitespace, drop empty rows; keep stored order.
2. Exact dedup on the raw sequence string (keep first occurrence).
3. Unigram ML entropy in bits; Miller–Madow in bits `(m−1)/(2·N·ln2)` added to H1 and H2
   separately (`m` = observed non-empty bins of that distribution).
4. Ordered bigrams **within each inscription only** (pairs never cross boundaries);
   H2 = ML(+MM) joint entropy of bigram types; `N2 = Σ(len−1) = 9001 − 1918 = 7083`.
5. `C = (H2 − H1)/log2(L)`, `L` = observed vocab (592 on the full corpus).
6. Null: pool all 9001 tokens, `random.Random(8675309).shuffle`, re-chunk to the original
   1918 lengths, recompute C; B=200 (recipe floor: ≥50). Repeated with seed 20261015.
7. Uniform control: iid `randrange(592)` at the same lengths, B=100, seed 31337.
8. Extra estimators for break-it: plain ML and Chao–Shen (literal Horvitz–Thompson form
   `H = −Σ p·log2(p)/(1−(1−p)^N)`).

## Counts (mine vs claim)

| Item | Claim | Mine | Match |
|---|---|---|---|
| Raw rows | 2543 | 2543 | ✓ |
| Raw tokens | 11280 | 11280 | ✓ |
| Exact-dedup texts | 1918 | 1918 | ✓ |
| Deduped tokens | 9001 | 9001 | ✓ |
| Vocab L | 592 | 592 | ✓ |
| Dedup rate | ~24.6% | 625/2543 = 24.58% | ✓ |
| All single-line | yes | 2543/2543 `line_count==1` | ✓ |
| len-1 texts | — | 11 | (new) |
| Distinct bigrams (real) | — | 2981 | (new) |

## Entropy numbers (mine vs shipped)

| Lens | Metric | Shipped claim | Mine (own code, own seeds) | Match |
|---|---|---|---|---|
| MM | H1 (bits) | 6.968 (0.7566 base-L) | 6.967617 (0.756572) | ✓ to 4dp |
| MM | H2 (bits) | 10.7413 (implied) | 10.741259 | ✓ to 6dp |
| MM | **C_real** | **0.4098** | **0.40975741041323926** | ✓ identical digits vs `object/results.json` |
| MM | shuffled null | mean 0.5633, sd 0.0016, min 0.5593 (B=200, seed 260417828) | mean 0.56351, sd 0.00176, **min 0.55905** (B=200, **seed 8675309**) | ✓ |
| MM | shuffled null, alt seed | — | mean 0.56343, min 0.56001 (B=200, seed 20261015) | ✓ |
| MM | uniform control | 0.4642 | **0.464203** (B=100, seed 31337; shipped value 0.464202) | ✓ to 1e-6 |
| ML | C_real / null min / uniform | — | 0.381946 / 0.513676 (mean 0.51773) / 0.391821 | — |
| Chao–Shen | C_real / null min | — | 0.621810 / 0.93470 & 0.93283 (B=50 × 2 seeds) | — |

- Gate (my numbers): C_real 0.40976 < my null min 0.55905 (**z ≈ 87σ** of my null sd) and
  < my uniform 0.46420 → **PASS**; also below the *max* of both my null and my uniform.
- The shipped `object/results.json` C and my C are bit-identical to all 17 printed digits —
  two independent implementations agreeing at machine precision.

## Step 4 — repo checker

```
> python claims\L1\...\check.py --corpus <csv> --object ...\object\results.json --baseline ...\baseline_snapshot\nulls.json
C_real=0.4098 p0.5=0.5593 uniform=0.4642
PASS   (exit 0)
```

## Preregistration order (step 5 checklist item)

```
9b9ed88 2026-10-14 18:00:43 +0530  L1-0001 preregister: ... (threshold fixed, results TBD)
7666f94 2026-10-14 18:01:50 +0530  L1-0001 results: C=0.4098 ...
```

- At `9b9ed88` the file reads `result: TBD — pipeline not yet run at preregistration commit`,
  `skeptics: []`, `status: draft`.
- `git diff 9b9ed88 7666f94 -- claim.yaml`: **only** `result:` / `status:` changed —
  `preregistered_threshold` is byte-identical (threshold not retro-edited).
- Same caveat as skeptic-1: the prereg→results gap is only ~67 s (automation-speed);
  ordering and content are correct, but a human skeptic would prefer a wider window.

## Break-it variants (all run, none broke it)

| # | Variant | Result | Verdict |
|---|---|---|---|
| 1 | Null, own seed 8675309, B=200 | min 0.55905 vs real 0.40976 | holds |
| 2 | Null, second own seed 20261015, B=200 | min 0.56001 vs real 0.40976 | holds |
| 3 | Estimator = plain ML | real 0.38195 < null min 0.51368 **and** < uniform 0.39182 (thin, Δ≈0.0099 ≈ 24 uniform-sd) | holds (thin leg) |
| 4 | Estimator = Chao–Shen | real 0.62181 < null min 0.93283 (both CS seeds) | holds |
| 5 | Drop all len-1 texts (n=1907) | C 0.41110 vs own B=50 null min 0.56075 | holds |
| 6 | Keep duplicates (no dedup, n=2543) | C 0.38612 — **lower** than deduped 0.40976 → dedup is conservative; own null min 0.57797 | holds |
| 7 | Per-site (within-site B=100 shuffle nulls, MM) | Mohenjo-daro 0.38698 vs 0.53125; Harappa 0.36649 vs 0.49092; Dholavira 0.24190 vs 0.26738 | holds at every site (Dholavira narrowest, ~5σ) |
| 8 | Reading-order reversal | C identical to all digits (0.40975741041323926) — bigram joint entropy is direction-symmetric | confirms README note |
| 9 | Prereg order / threshold integrity | see above | holds |

## Gate checklist (`agents/skeptic-protocol.md`)

- [x] Rebuilt from raw inputs in a fresh context with independently written code — yes
      (script above; stdlib only; own estimator/null implementation).
- [x] Same sign scheme + corpus snapshot hash — G-scheme; SHA256 recomputed and matched.
- [x] Threshold and split fixed before the run — `git log`/`git diff` proof above
      (threshold line byte-identical from prereg to results commit).
- [x] Null models and calibration attached — my own B=200 shuffle null (2 seeds) +
      B=100 uniform + B=100 within-site nulls + CS/ML estimator nulls.
- [x] Degrees of freedom counted; multiple-comparison correction — the gated claim is a
      single pre-fixed comparison (real vs null-min, real vs uniform); my variant sweep
      (5 estimators/seeds/subsets) was run *after* the gate and is reported as robustness,
      not as extra gates. No multiplicity issue for the pre-fixed claim.
- [x] Novelty checked against prior literature — searched: `"Indus script conditional
      entropy Rao 2009 bigram entropy replication"` (2026-10-14). Prior art confirmed:
      Rao et al., *Science* 2009 (conditional-entropy figure is figure-only, no tables of
      values); Sproat 2009/2010 + Liberman (Language Log 2009) show Rao's *language-vs-not*
      conclusion can be mimicked by unigram-matched independent-bigram corpora — i.e. the
      literature already knows conditional entropy alone is not a decipherment/linguistic
      proof. This claim makes only the weaker, structural "beats shuffled/uniform nulls"
      statement, which is not contested by that critique. `ronojoy/indus` = papers only
      (no code/data to rerun), consistent with the claim's "independent reimplementation".
- [x] Claim wording matches what was shown — case-insensitive grep for
      `deciphered|solved|translat|proof` across `claim.yaml`, claim `README.md`,
      `TROPHY_CASE.md`: **no hits**. Limitations disclose NSB≠MM, M77≠G-scheme,
      figure-only Rao values, and estimator-dependent absolutes.
- [x] Checker runs green from scratch — `PASS`, exit 0 (output above).

## Objections / notes (non-blocking, should ride with the claim)

1. **Absolute C is an undersampling artifact — the gate is an ordering test only.**
   My own analysis: an ideal independent-bigram (iid) process at these unigram counts
   would give `C = H1/log2(L) = 0.7566`, but the plug-in estimator over N2=7083
   transitions cannot even reach `log2(7083) = 12.79` bits of bigram entropy, so both the
   real C (0.41) and the shuffle-null C (0.56) are strongly downward-biased absolute
   values. This is *why* the shuffle null is the right design (same N1/N2, same unigram
   marginals, same estimator → bias-matched comparison), and the claim's wording
   ("structural, with nulls", "values not directly comparable to Rao Fig.1") is consistent
   with that. Just never read 0.41 as a population quantity.
2. **Uniform leg is estimator-thin under ML** (0.3819 vs 0.3918, Δ≈0.0099): repeated
   skeptic-2's O2 finding with a third seed/B. The MM uniform margin (0.4098 vs 0.4642)
   is larger because the uniform sample has ~6997 distinct bigrams vs 2981 real, so it
   collects a bigger MM bonus. Under Chao–Shen the direction is not thin at all
   (0.62 vs 1.19). The shuffled-null leg — the scientifically interesting one — is huge
   under every estimator I tried (69–98σ).
3. **"~97σ" in README/TROPHY_CASE** is an informal effect size using the shipped sd;
   with my sd (0.00176) I get 87σ, with theirs ~96σ. Harmless (the gate is rank-based:
   `C_real < null-min`, no normality assumed), but the σ figure is seed/sd-dependent and
   should be read as "large", not as a p-value.
4. **Prereg window ~67 s** (repeat of skeptic-1's objection): ordering verified, but a
   threshold fixed <2 minutes before results by the same automation loop provides much
   weaker protection than an hours/days separation would.
5. Nothing in the claim depends on it, but `TROPHY_CASE.md`'s row shows a large gap
   (97σ) phrasing and reports 2 skeptics — with this report it is 3/3 reproductions;
   TROPHY_CASE is archivist-maintained, so I did not edit it.
6. **Pre-existing CI failure, fixed in this PR (disclosure):** `verify-claim` has been
   red on `main` since `7666f94` (runs 38564512625 / 38564800087 / 38565429072): every
   `claim.yaml` carries plain scalars containing `": "` (`license:` in `corpus_source`,
   `git history:` in `preregistered_threshold`), so `yaml.safe_load` raises
   `ScannerError: mapping values are not allowed here`. I quote the two affected
   **L1-0001** values in a separate commit, asserting the parsed strings are
   **byte-identical** to the raw text at `origin/main` — the threshold wording is
   untouched (encoding-only change). Note `claim.yaml` for L1-0002/0002b/0003/0004 (local
   unpushed commits, not part of this PR) has the same defect and will also need quoting
   before their CI can go green.

## Bottom line

Counts, hash, H1/H2 and C are exact (bit-identical to the shipped object); my null with
two *own* seeds and my uniform with an *own* seed reproduce the shipped moments to
3–6 decimals; the gate passes under MM, ML and Chao–Shen; dedup/len-1/site/direction
variants all preserve the ordering; prereg-before-results is verifiable in git with an
unedited threshold line; `check.py` exits 0/PASS. **Reproduced** — structural claim only,
with objections 1–4 above.
