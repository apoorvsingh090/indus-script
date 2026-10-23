verdict: reproduced

# sk3-A — independent skeptic audit of L1-0003 (formulaic n-grams)

## Environment
- Machine: Windows, Python 3.12.10 (MSC v.1943 64-bit), stdlib only (`csv`, `hashlib`, `json`, `random`, `collections`)
- Own code: `C:\Users\Apoorv\AppData\Local\Temp\opencode\sk3A\recompute.py` (written fresh, no repo code read)
- Own seed: 555, B=150 (claim used seed 260417830, B=200 — different seed/B by design)
- Raw corpus: `C:\Users\Apoorv\AppData\Local\Temp\opencode\hf-indus\indus_website_real_corpus.csv`
- Full independent output: `C:\Users\Apoorv\AppData\Local\Temp\opencode\sk3A\results.json`
- Forbidden files were not read (no `how-we-built-it/*.py`, `check.py` source, `object/results.json`,
  `baseline_snapshot/nulls.json`, or prior `skeptics/*.md`). `check.py` executed only as a
  black box at the end (`--help` + one conformance run).

## 1. SHA256 + orient/dedup
- SHA256(raw csv) = `7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8` — MATCHES `claim.yaml`.
- Raw rows: 2543. Orientation rule applied independently from claim text: reverse token order
  of `reading_direction == 'L-R'` rows, keep `R-L` as-is.
- After orienting, exact-dedup → **1948** texts — CONFIRMED.
- (Side note: raw as-stored dedup without orienting gives 1918; orientation changes dedup count
  by +30. Dedup-after-orienting, as claimed, is the correct order of operations.)

## 2. rep3/rep4 recompute + own shuffle nulls (fixed lengths)
- Definition used (from claim text): repK = distinct length-K substrings occurring in
  ≥2 distinct inscriptions, counted once per inscription (document frequency, not token frequency).
- Deduped oriented corpus: **rep3 = 576, rep4 = 189** — EXACT match to claim.
- Own nulls: global token-pool permutation re-chunked to the same 1948 inscription lengths
  (fixed lengths, unigram frequencies preserved, order/association destroyed), seed 555, B=150:
  - rep3 null: range 69–111, mean 89.8, **max 111** (coincidentally identical to claim's null-max 111)
  - rep4 null: range 0–6, mean 1.57, **max 6** (claim: max 4, B=200 — same order, tiny sampling noise)
  - Gate with my nulls: 576 > 111 AND 189 > 6 → **PASS** with enormous margin (real ≈ 5× / 30× null max).

## 3. Adversarials (both done)
(a) Stricter recurrence (≥3 distinct inscriptions), same corpus, same nulls at same threshold:
  - Real: rep3_3 = 242, rep4_3 = 51.
  - Null max (B=150): rep3_3 = 25 (mean 13.9), rep4_3 = 1 (mean 0.03).
  - 242 > 25 AND 51 > 1 → signal survives comfortably; not a ≥2-threshold artifact.
(b) UNDEDUPED corpus (2543 oriented texts, duplicates kept):
  - rep3 = 734 (+158 vs deduped, +27%), rep4 = 322 (+133, +70%).
  - Exact-duplicate texts materially inflate the counts — so the claim's choice to dedup is the
    conservative, correct one. Gate on undeduped would still pass trivially (734 ≫ 111, 322 ≫ 6),
    but the reported 576/189 are the honest (lower) numbers.

## 4. Git order + wording
- `903d2af` "L1-0003 preregister" (2026-10-14 18:16:24 +0530) touches only `check.py`, `claim.yaml`,
  `how-we-built-it/{ng_lib,run_ng}.py` — threshold fixed, results TBD. `f8bf348` "L1-0003 results"
  (18:17:56, +92 s) adds `README.md`, `object/results.json`, `baseline_snapshot/nulls.json`.
  Prereg-before-results order is clean at commit level. The README's admission of a pre-prereg
  trial run (workdir slip, artifacts deleted, re-run after `903d2af` with identical numbers) is
  taken on trust — deletion itself is unverifiable from git, but the committed order is proper
  and determinism (my exact-number match with independent code) supports the re-run story.
- Wording: title says "repeated len-3/len-4 phrases beat shuffled nulls" — matches what was shown.
  No "deciphered/solved" stretch. Cross-version Nair comparison (565/187) is explicitly labeled
  cross-version-only in `claim.yaml`; I did not verify Nair's numbers (no ICIT access), so that
  row is unchecked but also non-gated. `succ-cov 0.456` is explicitly non-gated ("own definition").

## 5. Checker conformance (black box, run last)
- `python check.py --corpus … --object … --baseline …` → stdout
  `rep3=576 > nullmax=111; rep4=189 > nullmax=4` / `PASS`, exit 0. Conformance green.

## Objections / caveats (none gate-breaking)
1. (Minor, wording) README's "counts are reversal-invariant … so the L1-0002 loader issue cannot
   favor this gate" overstates slightly: invariance holds for *global* reversal (I verified:
   globally reversed deduped corpus gives exactly 576/189), whereas the correction reverses only
   the L-R subset. I checked the material point directly: as-stored deduped corpus gives
   rep3/rep4 = 579/192 vs corrected 576/189 — orientation shifts counts by +3/+3, negligible
   against margins of ~465/~185. The conclusion stands; suggest rewording to "orientation changes
   counts by 3 (verified), far below the margin."
2. (Minor, documentation) `succ-cov 0.456` is not reproducible from the published text: none of
   micro-averaged top-3/head (0.555), macro (0.880), distinct-type (0.345), global-top-3 (0.041),
   per-tail (0.488), or undeduped-micro (0.602) variants I tried recover 0.456. It is non-gated
   and my micro value (0.555) is also inside the quoted Nair range, but the exact definition
   should be pinned in the README for verifiability.
3. Null choice sensitivity: I used global-pool shuffle; within-text permutation would be a stricter
   null (preserves per-text multisets). Given the margin (rep4 real 189 vs null max single digits
   under either scheme), the gate is not null-choice-sensitive, so I did not run the second scheme.
   Noted for completeness.

## Bottom line
Independent code + independent seed/B reproduces 1948 texts and 576/189 exactly; gate passes by a
wide margin; stricter-threshold and undeduped adversarials both behave as a real signal should
(survives / conservative reporting). Checker PASS. No blocking objections.
