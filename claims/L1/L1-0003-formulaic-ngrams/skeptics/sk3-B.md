verdict: reproduced

# sk3-B — Independent skeptic audit of L1-0003 (formulaic n-grams)

Own code: `C:\Users\Apoorv\AppData\Local\Temp\opencode\sk3B\sk3b_main.py`
(own seed 777, B=200 global token shuffles preserving text lengths).
Forbidden files not read (`how-we-built-it/*.py`, `check.py`,
`object/results.json`, `baseline_snapshot/nulls.json`, `skeptics/*.md`).
`check.py` executed last, blind (only `--help` + run), result below.

## Environment

- Python 3.12.10 (MSC v.1943 64-bit AMD64), Windows-11-10.0.26200-SP0
- stdlib only (`csv`, `hashlib`, `collections`, `random`, `json`)
- Raw corpus: `C:\Users\Apoorv\AppData\Local\Temp\opencode\hf-indus\indus_website_real_corpus.csv`
  (2543 rows, 592 distinct G-tokens, `damaged` all False, no filtering applied)

## 1. SHA256 + orient + dedup

- `Get-FileHash` SHA256 = `7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8`
  — matches `claim.yaml:corpus_snapshot_sha256` exactly (case-insensitive). **PASS**
- Corrected order reimplemented from claim wording alone:
  reverse token list iff `reading_direction == 'L-R'`, else keep.
- Exact-dedup on post-orienting token tuples: **1948** (from 2543 raw). **Matches claim.**
- Reference: as-stored (no reversal) dedup = 1918; raw distinct strings = 1918.
  Orientation changes dedup (+30), as expected for a partial reversal.

## 2. Main recomputation (corrected order, deduped 1948)

- `repK` = distinct length-K substrings with document frequency ≥ 2
  (per-text dedup of n-grams, counted over distinct inscriptions).
- **rep3 = 576, rep4 = 189 — exact match to claim.**
- Own nulls: global token-pool permutation, re-chunked by original fixed
  lengths, B=200, seed 777 (theirs: B=200, seed 260417830):
  - rep3 null-max **116** (mean 92.3; top-5: 116,114,113,112,112) vs claimed 111
  - rep4 null-max **7** (mean 1.66; top-5: 7,6,5,5,5) vs claimed 4
  - Small differences are expected sampling variation from a different seed;
    gate margin is enormous either way.
- Gate with own nulls: **576 > 116 AND 189 > 7 → PASS. Confirmed.**

## 3. Successor coverage (reimplemented from task definition)

- Definition used: top-10 signs by total token frequency in the corrected
  deduped corpus; per sign, `share = (top-3 successor bigram counts) /
  (total outgoing bigrams, i.e. non-final occurrences)`; report macro
  (unweighted) mean over the 10 signs.
- Result: **0.456005 → ≈0.456. Exact match to claim.**
- Per-sign (sign: freq, share): G740: 974, 0.5563; G2: 506, 0.1838;
  G220: 235, 0.3257; G32: 227, 0.4528; G400: 211, 0.6098; G240: 194, 0.2169;
  G390: 173, 0.5588; G520: 170, 0.4706; G60: 166, 0.2744; G861: 156, 0.9110.
- Note: definition is the authors' own (not gated); reproduced as specified.
  Nair 0.319–0.884 range not independently verified here (no ICIT access).

## 4. Adversarials

### (a) LOADER-INVARIANCE — ⚠️ FLAG: counts are NOT identical

- As-stored order (no reversal), own dedup: rep3 **579**, rep4 **192**
  (dedup 1918) vs corrected **576 / 189** (dedup 1948).
- **Difference: +3 / +3. NOT identical — README's
  "Counts are reversal-invariant … so the L1-0002 loader issue cannot favor
  this gate" is wrong as applied.** Global-reversal invariance is real
  (I confirm: as-stored 579/192 == all-texts-reversed 579/192, and
  corrected 576/189 == reverse-R-L-only 576/189 — the bijection holds for
  *global* reversal), but the loader fix reverses only the L-R subset
  (2440/2543 rows), i.e. a *partial* reversal, to which the bijection
  argument does not apply.
- Impact assessment: the error is conservative, not gate-flattering —
  corrected counts are slightly *lower* than as-stored, and both beat nulls
  by ~5×/25×+ (as-stored own-null max 117/6 vs 579/192 — also PASS).
  Gate is robust; wording should be corrected from "reversal-invariant,
  orientation cannot favor the gate" to "orientation changes counts by
  <2% and the gate passes under either loader".

### (b) PER-SITE (Mohenjo-daro only) — formulaicity holds, not cross-site mixing

- Mohenjo-daro raw 1202 → corrected + site-internal dedup **1019**.
- Site-internal: rep3 **306**, rep4 **105** vs own site-internal null
  (B=200, seed 7777): rep3 null-max **55** (mean 37.9), rep4 null-max **4**
  (mean 0.59).
- **306 > 55 AND 105 > 4 → gate holds within one site.** No evidence that
  repetition is a cross-site pooling artifact. (Harappa not tested; single
  positive site suffices to reject the mixing hypothesis as sole cause.)

## 5. Git order + wording checks

- `903d2af` (2026-10-14 18:16 +0530): preregisters threshold
  (`rep3_real > max(...) AND rep4_real > max(...)`, B=200, seed 260417830,
  fixed lengths, corrected order, post-orient dedup, repK def) with
  `result: TBD`, `status: draft`. Verified via `git show 903d2af:.../claim.yaml`.
- `f8bf348` (2026-10-14 18:17 +0530, +92 s): fills in results + README +
  nulls/results artifacts only; `git diff 903d2af f8bf348 --stat` shows
  `check.py`/generator untouched between prereg and results. **Order clean.**
- README's "first run pre-prereg due to workdir slip, deleted, re-run after
  903d2af" is disclosed but unverifiable from git (deletion leaves no trace);
  taken at face value — deterministic seeds reproduce the numbers exactly,
  so no evidence of tuning.
- Wording: title "Formulaic repetition above chance" matches what was shown
  (both rep3 and rep4 beat full null maxima; conjunction, no multiplicity
  correction needed). No "solved/deciphered" stretch. "Near-exact" vs Nair
  565/187 (ours 576/189; Δ 11/2) is fair phrasing; drift caveat is stated.
  Successor coverage correctly labeled own-definition, not gated.

## 6. Blind checker run (last step, file never read)

- `python check.py --corpus <hf csv> --object <object/results.json> --baseline <baseline_snapshot/nulls.json>`
- Output: `rep3=576 > nullmax=111; rep4=189 > nullmax=4` / `PASS`, exit 0.
  **Checker green from scratch.**

## Objections / caveats (none gate-breaking)

1. **Loader-invariance wording is technically false** (see 4a) — must be
   reworded; numerically immaterial and conservative.
2. Null-model specification "token shuffles, fixed lengths" is satisfied by
   my global-pool shuffle, but within-text permutation would be a different
   (weaker) null; authors should state the pool scope explicitly. Either way
   the margin here (~460/180 above max) is insensitive to this choice.
3. Nair cross-version numbers (565/187, coverage range) accepted as reported;
   not rechecked against ICIT in this audit.
4. Rep counts exclude length < K texts implicitly and count whole-text
   duplicates only via dedup — matches stated method; no hidden filtering
   (`damaged` uniformly False).

## Summary numbers

| Corpus | dedup | rep3 | rep4 | null-max3 | null-max4 | gate |
|---|---|---|---|---|---|---|
| corrected (claim) | 1948 | 576 | 189 | 111 (theirs) / 116 (mine, seed 777) | 4 / 7 | PASS/PASS |
| as-stored | 1918 | 579 | 192 | 117 (mine) | 6 (mine) | PASS |
| Mohenjo-daro only | 1019 | 306 | 105 | 55 (mine) | 4 (mine) | PASS |

Successor coverage (corrected): **0.456005 ≈ 0.456**. Checker: **PASS**.
