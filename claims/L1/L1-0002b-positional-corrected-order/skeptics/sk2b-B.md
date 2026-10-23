verdict: reproduced

# sk2b-B — Independent skeptic-B audit of L1-0002b (positional, loader-corrected order)

Role: INDEPENDENT SKEPTIC B. Fresh context. Own code only, different seed/choices
from the original replication. Forbidden files were not opened
(`how-we-built-it/*.py`, `check.py` source, `object/results.json`,
`baseline_snapshot/nulls.json`, `skeptics/*.md`). Only `claim.yaml`,
`README.md`, and `agents/skeptic-protocol.md` were read. `check.py` was
executed once at the end via `--help`/`--corpus/--object/--baseline`
without reading its source.

## Environment
- OS: Windows (win32), PowerShell 5.1
- Python 3.12.10, numpy 2.4.6, scipy 1.15.3, pandas 2.2.2
- Repo HEAD at audit time: `bf4b49d` (2026-10-14); claim commits verified below
- Raw corpus: `C:\Users\Apoorv\AppData\Local\Temp\opencode\hf-indus\indus_website_real_corpus.csv`
- Own code: `C:\Users\Apoorv\AppData\Local\Temp\opencode\sk2bB\recompute_b.py`
  (seed **20260704**, **B=150** token-shuffles, fixed lengths; artifacts
  `summary.json`, `null_dist.json`, `undedup_null.json` in same dir)

## 1. SHA256 / orient / dedup — confirmed exactly
- SHA256(raw) = `7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8`
  — matches `claim.yaml:corpus_snapshot_sha256` (case-insensitive). PASS.
- Columns: inscription_id, sign_sequence, site, object_type, line_count,
  damaged, reading_direction, motif, cisi_number. Raw rows = **2543**,
  `L-R` = **2440**, `R-L` = **103** — matches README (2440/2543).
- Orient rule reimplemented from spec: reverse token list iff
  `reading_direction == "L-R"`, else keep as stored. No empty sequences.
  Length histogram: len1=19, len2=450, len3=482, len4=502, len5=444,
  max len 19.
- Exact-dedup AFTER orienting (tuple equality, keep first in file order):
  **1948** texts. As-stored dedup (no orient) = **1918**. Both match README
  (1948 vs 1918; orientation changes dup identity). PASS.
- Tokens post-dedup: **9080**, mean len **4.6612** (9080/1948) vs claimed
  4.66. Vocab **592** distinct G-codes. PASS.
- Site counts post-dedup (global-dedup-keeps-first-site): Mohenjo-daro **970**,
  Harappa **660**, Dholavira 67, Lothal 59, Chanhujo-daro 43, Kalibangan 40,
  rest small. M/H n matches README `n=970/660` exactly, confirming the
  keep-first-site rule reimplementation. Raw pre-dedup was M=1202/H=970, so
  dedup removed 232 M + 310 H texts.

## 2. n80 begin/end + own shuffle null — gate PASS with margin
- Position convention reimplemented: begin = index 0 (all texts); end =
  index len-1 only for len>1 (19 len-1 texts contribute begin only);
  middle = interior indices for len>2.
- Corrected-order deduped: **n80_begin=107** (nb=1948),
  **n80_end=32** (ne=1937). Top beginners G820(116)/G861(108)/G817(102);
  top enders G740(654)/G400(170)/G520(136). Matches claimed 107/32 exactly.
- Own null: B=150 independent shuffles, token-multiset permutation
  re-chunked to identical fixed lengths, seed 20260704 (different from
  claimant's B=200/seed 260417832). n80_end null: **min 69, max 84,
  mean 76.6** (sorted tails [69,69,71,...] / [...82,83,84,84]); n80_begin
  null 71–88. Claimant reported min 67 / max 85 — same range within
  Monte-Carlo noise (my min is 2 higher with fewer replicates).
- Gate: 32 < 107 AND 32 < 69 → **PASS with margin 37 below null-min**.
  Result is not a near-miss.

## 3. FOCUS metrics — all confirmed to claimed precision
Cramer's V reimplemented **from the Nair-2026 paper description only**
(2×3 table per sign: {sign vs rest} × {begin,middle,end}, chi2 without
correction, V=sqrt(chi2/n) since min(r,c)=2; mean over top-10 most frequent
signs; site splits use top-10 *within that site* and site-local marginals).
No claim code consulted.

| Metric | Mine (B) | Claimed | Verdict |
|---|---|---|---|
| Rigidity mean-V top-10 (all, n=1948, 9080 tok) | **0.1560** | 0.1560 (Nair 0.15) | exact to 4dp |
| Site V Mohenjo-daro (n=970 texts, 4960 tok) | **0.1683** | 0.168 (Nair 0.160) | match |
| Site V Harappa (n=660 texts, 2710 tok) | **0.1320** | 0.132 (Nair 0.153) | exact to 3dp |
| Hapax rate | **215/592 = 0.3632** | 0.3632 (Nair 0.33) | exact |
| Zipf log-log OLS slope | **−1.4236** (intercept 8.954, R² 0.961) | −1.4236 (Nair −1.49) | exact to 4dp |

Per-sign V (all): G740 0.391, G400 0.223, G520 0.198, G2 0.191, G861 0.154,
G60 0.111, others <0.09 — heavy-tail rigidity driven by a few terminal signs,
as expected. Site top-10 sets differ (M includes G820/G861; H includes
G400/G0/G33), consistent with per-site top-10 rather than global top-10 —
and this choice reproduces the claimed numbers exactly, corroborating it.
M > H ordering reproduced (0.168 > 0.132), same direction as Nair (0.160 vs
0.153), though my H gap to Nair (0.021) is larger than M gap (0.008).

## 4. ADVERSARIAL
### 4a. UNDEDUPED corrected-order corpus (2543 texts, no dedup)
- n80_begin=**93** (nb=2543), n80_end=**24** (ne=2524).
- Own null B=150 seed 20260704+1: n80_end min **68**, max **82**.
- Gate: 24 < 93 AND 24 < 68 → **still PASS, by a larger margin (44)**.
- Conclusion: **dedup is NOT load-bearing.** Removing dedup makes enders
  *more* concentrated (24 < 32), consistent with duplicates being
  formulaic/ender-heavy. The gate does not depend on the dedup choice.

### 4b. Top-20 (not top-10) mean V — sign-set widening
- All: 0.1560 → **0.1186**; M: 0.1683 → **0.1279**; H: 0.1320 → **0.1041**.
- M > H ordering **survives** (0.128 > 0.104); both remain above the Nair
  heraldic-generator band (~0.08±0.01), though H-top-20 (0.104) is closer
  to its upper edge. Magnitude is k-sensitive (rarer signs are less
  positionally constrained — expected dilution), but the rigidity-direction
  conclusion (rigid; same grammar across sites) survives widening. No
  sign-flip. Report k=10 as preregistered-style stability choice is
  reasonable but should be disclosed as a degree of freedom (it is: Nair
  paper states top-10 explicitly).

## 5. Git order + wording checks
- Log (graph): `e41920f` (L1-0002 prereg) → `c2e006f` (L1-0002 negative,
  as-stored gate not met) → **`cac214e` (L1-0002b prereg, result TBD,
  threshold fixed)** → `903d2af`/`d7c6b4c` (other claims) →
  **`f991376` (L1-0002b results)**. Prereg precedes results. PASS.
- `git show cac214e:claim.yaml` has full `preregistered_threshold` text
  with `result: TBD`; `git diff cac214e f991376 -- claim.yaml` changes
  **only** `result:` (TBD → numbers) and `status:` (draft →
  under-skeptic-review). Threshold text byte-identical. No moving of
  goalposts. PASS. (README evidentiary note about an early workdir-error
  run + `git reset` to `e41920f` is consistent with this graph; deterministic
  seeds make the repair credible, and my independent seeds reproduce the
  numbers anyway.)
- Wording: title says "loader-corrected reading order (enders
  concentrated)"; claim.yaml limitations explicitly state (i) sign IDs not
  comparable to M77 without concordance — direction/count pattern only,
  (ii) "Corrected" = loader convention only, not a true-reading-direction
  claim, (iii) V/cross-site/hapax/Zipf reported not gated. README mirrors
  this ("scheme-specific — no M77 concordance yet"). No "solved"/decipherment
  stretch. PASS.
- Degrees of freedom: gate is single (n80_end vs begin + null-min); no
  multiple-comparison correction required for the gate. V top-10 is a
  reported comparison metric with k fixed by Nair precedent. Noted in §4b.

## 6. Checker conformance (run last, source never read)
- `python check.py --help` showed `--corpus/--object/--baseline` args.
- `python check.py --corpus <hf csv> --object object/results.json
  --baseline baseline_snapshot/nulls.json` → stdout:
  `corrected order: n80 begin/end = 107/32 null_min = 67` + `PASS`.
  **Checker green from scratch.** (Null-min 67 is the claimant's B=200
  baseline; my B=150 null-min 69 is consistent Monte-Carlo variation.)

## Objections / caveats (none blocking)
1. H site-V (0.132 vs Nair 0.153) matches the claim but sits 0.021 below
   Nair — larger drift than M. Acceptable as "same direction/ballpark"
   given different sign scheme (G-592 vs ICIT-584) and site-n differences,
   but a future concordance should revisit.
2. Top-k choice (k=10) is a real degree of freedom; magnitude drops at
   k=20. Ordering survives. Claim does not overstate this (reported, not
   gated; Nair precedent cited).
3. Null range depends on B/seed (67–85 claimed vs 69–84 mine) — gate margin
   (~37) dwarfs this noise. No calibration concern.
4. Novelty check: searched Nair 2026 ("How Non-Linguistic Is the Indus Sign
   System?", arXiv 2604.17828) for the V/hapax/Zipf/site-V definitions and
   confirmed the claim's comparison values (0.15, 0.160/0.153, 0.33,
   −1.49) appear there; M77-EBUDS 82-vs-23 cited as structural mirror only
   with explicit no-concordance hedge. No prior-art contradiction found.

## Reproduction log
All numbers above produced by `sk2bB/recompute_b.py` (seed 20260704, B=150)
in one run; see `sk2bB/summary.json`. Corpus hash, counts, n80, null, V,
hapax, Zipf, site-n, undeduped, and top-20 branches all logged to stdout.
