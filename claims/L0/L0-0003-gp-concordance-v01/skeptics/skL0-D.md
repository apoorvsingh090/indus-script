# skL0-D — skeptic audit of L0-0003 (G↔P type-level concordance v0.1)

verdict: reproduced

## 1. Independence disclosure (what I opened, and when)

Read before any code was written (the only claim files opened pre-numbers):
`claim.yaml`, `README.md` of L0-0003; `planner.md` (§8 plus full file); `agents/skeptic-protocol.md`;
allowed input definitions `claims/L0/L0-0001-mayig-joy-xcheck/claim.yaml`,
`claims/L0/L0-0002-concordance-v01/claim.yaml`, `data/concordance/pwm-v01.csv`.
Raw inputs probed: mayig clone JSONs and `indus_website_real_corpus.csv` (header/shape only).
My implementation (`%TEMP%/skL0D/build.py`, `adversarial.py`) was written from the
`preregistered_threshold` text in claim.yaml alone. Only after my numbers existed did I
execute the shipped `check.py` blind, and only after that did I read `object/results.json`,
`baseline_snapshot/counts.json`, `data/concordance/gp-v01.csv`. I never read the source of
`check.py` or `how-we-built-it/build_gp.py`, never read `skeptics/*` (skL0-C's report and
scratch are untouched), and committed nothing (branch main as-is; my only write is this file).
Interruption disclosure: a transient backend "model concurrency limit exceeded" error hit ~45 s
after launch; I resumed exactly where tool state left off (first-reads and input verification
were already complete), repeated nothing, and no step depended on the failed call.

Input verification: mayig clone `git rev-parse HEAD` = `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb` (clean worktree);
corpus CSV sha256 = `7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8`. Both match claim.yaml.

## 2. Environment

Windows 10 (10.0.26200), Git Bash, Python 3.12.10; scratch `%TEMP%/skL0D`
(`C:\Users\Apoorv\AppData\Local\Temp\skL0D`); mayig used in place (MIT), joy CSV fetch-at-build,
neither vendored. Deterministic run, no network needed for reproduction.

## 3. My implementation (independent)

- Join: G rows `site=='Mohenjo-daro'` with `cisi_number ^M-?\d+[A-Z]?$` (1188 rows, no duplicate
  M-numbers, no letter suffixes on G side) ↔ mayig side ids `^M-?(\d+)` (179 sides, one side per
  JSON, ids like `M-1A`). Join key = numeric M-number.
- G corrected order: tokens reversed when `reading_direction=='L-R'`.
- P orientation: both global variants; score = Σ over G-signs of max_p C[g][p]. As-stored 267,
  reversed 741 → reversed selected (matches the filed convention finding).
- Alignment: all equal-length (G-row, P-side) pairs, positional zip; 140 pairs, 768 positions.
- Classification exactly per prereg: clean iff n_g≥5 ∧ support(g,p1)≥5 texts ∧ C[g][p1]≥0.9·n_g
  ∧ g is p1's top source ∧ C[g][p1]≥0.9·n_p1; contested (n_g≥5, not clean) with reason;
  unmapped n_g<5. Deterministic tie-breaks with all ties logged (7 top-source ties, all at
  count 1, unmapped tail only — no effect on any clean/contested call).

## 4. My numbers vs shipped

| Quantity | Mine | Shipped | Match |
|---|---|---|---|
| shared M-numbers | 161 | 161 | yes |
| mayig sides / G M-daro M-form rows | 179 / 1188 | 179 / 1188 | yes |
| mayig-only M-numbers / G M-form unshared | 18 / 1027 | 18 / 1027 (README) | yes |
| M-daro rows w/o M-form cisi | 14 (all `unknown`) | — (disclosed class) | n/a |
| equal-length pairs / aligned positions | 140 / 768 | 140 / 768 | yes |
| distinct G / P signs at aligned positions | 192 / 164 | 192 / 164 | yes |
| orientation scores (stored / reversed) | 267 / 741 | 267 / 741 | yes |
| clean / contested / unmapped | 22 / 19 / 151 (Σ=192) | 22 / 19 / 151 | yes |
| clean pair set (g→p, c, n_g, support) | all 22 identical, incl. G740→P324 75/76 s75, G2→P122 60/63 s60, G220→P050 27/29 s27, G820→P378 14/15 s13 | same | yes |
| contested set (g, p1, c, n_g, support) | all 19 identical (e.g. G390→P086 25/25 s24, G32→P145 22/23 s21, clusters G861/G817→P385, G803/G806→P364, G900/G920→P154, G550/G798→P230) | same | yes |
| holdout (spec split: every 5th, 33 texts) | 49 positions, 48 correct, 0.980 | 33 / 49 / 0.9796 | yes |
| pwm composition (report-only) | 22/22 clean P in pwm-v01; 15 chain clean-1:1 to M | same | yes |

gp-v01.csv: 192 rows (22 clean + 19 contested + 151 unmapped), clean set byte-level equal to
mine as a set of (g,p,c,n_g,support) tuples. The only divergence anywhere is contested reason
labels (objection O1).

## 5. Blind checker output

```
shared=161 pairs=140 p_reverse=True clean=22 contested=19 unmapped=151 bij_viol=False recompute=match gate=PASS
PASS
EXIT CODE: 0
```

Run blind (source never read), after my numbers existed. Recompute=match, gate=PASS, exit 0 as expected.

## 6. Git prereg audit

- `7e0025d` 2026-10-24T15:23:33+05:30 (prereg: claim.yaml with `result: "TBD — pipeline not yet
  run at preregistration commit"`, plus `check.py` and `how-we-built-it/build_gp.py`) is an
  ancestor of `7861f78` 2026-10-24T20:15:45+05:30 (results: adds README, object, baseline,
  gp-v01.csv; modifies claim.yaml result/status only).
- `preregistered_threshold` line byte-identical at both commits
  (sha256 `fcac9a85ac3291b20fc35b5ad7dfba17754ffe78767d28f9b5d5354da94795df` both).
- `check.py` and `how-we-built-it/` unchanged between the two commits (empty diff).
- Design inputs (shared=161, 140/161 equal-length) disclosed at prereg, before any mapping was
  computed. Worktree clean except untracked `skeptics/` (this report). Chain is clean.

## 7. Adversarial battery

| Attack | Result |
|---|---|
| (a) Permutation control: 200× shuffle of G-sequence→M-number assignment (mayig sides and orientation rule fixed; equal-length filter reapplied) | **0/200 permutations yield a single clean pair** (mean 0.00, max 0; gate ≥20 in 0/200). Max top-pair C among n_g≥5 signs: mean 5.0, max 11, vs 75 in the real run. Coincidental-consistency floor ≈ 0: equal-length alignment on mismatched objects cannot manufacture these pairs. |
| (b) Dedup rerun (evidence = distinct corrected G sequences) | 161/161 shared G sequences are distinct — no exact-duplicate inflation exists; dedup is a no-op: 22/19/151 reproduced identically, 22/22 clean survive. (Formulaic near-duplicates remain by construction; that concern is what (a) quantifies, and it gives 0.) |
| (c) Join validity | 161/161 shared G rows have motif `Bull1:*` (unicorn); 161/161 mayig shared sides are `unicorn I–V seal` — metadata agrees with the same-object premise. 18 mayig-only M-numbers are all unicorn seals too (exclusion not content-driven). 14 M-daro rows lack an M-form cisi (`unknown`). G-side `object_type` is `unknown` everywhere (thin metadata; see O5). |
| (d) Orientation sensitivity | G-corrected+P-reversed: 741 / 22 clean; G-corrected+P-stored: 267 / 0 clean; G-raw+P-stored: 741 / 22; G-raw+P-reversed: 267 / 0. Perfectly symmetric: exactly one global relative orientation works, the wrong one gives zero clean pairs (degrades to nothing, not to noise). G-not-reversed control confirms the rule is doing real work. |
| (e) Threshold sensitivity (support × consistency grid) | Clean counts range 16–28: sup4/0.85→28, sup4/0.90→22, sup4/0.95→19, sup5/0.85→28, 5/0.90→22 (base), 5/0.95→19, 6/0.85→25, 6/0.90→19, 6/0.95→16. Stable core over the four corners (4/6 × 0.85/0.95) = **16 pairs** (incl. G2→P122, G740→P324, G60→P120, G240→P062, G520→P217, G233→P058, G368→P202, G3→P123…). Flips out only at the tail: cons 0.95 drops G220 (27/29), G820 (14/15), G235 (13/14); support 6 drops the 5/5 pairs G65, G503, G415. Loosening cons to 0.85 admits G390, G32, G692, G760, G840, G1 — contested signs with perfect one-way consistency that fail only the two-way/bijection condition (exactly the split-convention story). |
| (f) My own holdout splits (different rule) | every-7th (23 texts): 43/43 = 1.000; seeded random 20% (32 texts, seed 42): 61/61 = 1.000. The filed 0.980 is, if anything, conservative. |
| (g) Wording grep `-iE "deciphered\|solved\|translat\|proof"` | Only hits are the explicit disclaimers "NOT glyph identity proof" / "not glyph proof" (claim.yaml limitation 1, README Limits). No decipherment/solved/translation language. |
| (h) Novelty | Cross-sign-list correspondence tables exist editorially (Mahadevan 1977 concordance sign list; Parpola CISI; Wells; mayig's own P/W/M/V tables = pwm-v01). Searches (logged: "G codes Parpola indus_website yajnadevam"; "Parpola Mahadevan sign number correspondence G-codes positional alignment") found no published G↔P crosswalk derived by structural alignment of shared texts — the contribution is the method plus the tested bridge, and it is filed as provisional type-level concordance, not glyph proof. Correct class. |

## 8. Protocol checklist

- [x] Rebuilt from raw inputs in a clean context with independently written code
- [x] Same sign-coding scheme and corpus snapshot hash (mayig @ad2f1e2, corpus sha256 verified against claim.yaml)
- [x] Threshold and split fixed before the run (git prereg audit §6; my code written from the frozen threshold text)
- [x] Null models attached (permutation control; L0-level appropriate — L4 gating applies to L3 reading claims, not this L0 concordance)
- [x] Degrees of freedom counted (one orientation binary, chosen by score with both reported; thresholds preregistered; tie-break freedom logged and shown immaterial)
- [x] Novelty checked (queries logged in §7h)
- [x] Claim wording matches what was shown (grep §7g; limitations state type-level/provisional)
- [x] Checker runs green from scratch: `recompute=match gate=PASS exit 0`

## 9. Objections (non-blocking)

- **O1 — contested reason labels underdetermined by prereg.** My reason derivation (near-tie >
  reverse-conflict > low-consistency) labels 17 reverse-conflict / 2 low-consistency; shipped
  gp-v01.csv labels 15 low-consistency / 4 `reverse-conflict:<sign>` (naming the dominating
  sign). Class assignment and all evidence counts are identical; the prereg names the three
  categories without an ordering. The shipped labels are actually more informative. Cosmetic.
- **O2 — argmax tie-break unspecified in prereg.** Ties exist only among count-1 tail pairs
  (7 logged), all inside the unmapped class; no clean/contested call is tie-sensitive. Should
  be pinned in v0.2.
- **O3 — equal-length-only alignment discards 21/161 shared texts** and models no
  insertions/deletions; a sign-off-by-one text is dropped entirely rather than partially
  aligned. Conservative (cannot create false pairs), but the true clean set is likely larger;
  worth an edit-distance variant in v0.2.
- **O4 — mayig-only exclusions (18) are all unicorn seals and the 1027 unshared G M-daro rows
  are unexamined for length/motif structure**; selection into the shared set is driven by
  mayig's 179-seal scope, not by outcome, but v0.2 should tabulate the excluded G rows.
- **O5 — G-side metadata is thin** (`object_type` all `unknown`); same-object rests on
  M-number equality + motif Bull1:* × unicorn descriptions. Acceptable for L0; keep stated.
- **O6 — G-code provenance caveat:** one search hit describes the indus_website corpus as
  cross-referenced against concordance numbering; the two transcriptions are independent as
  text digitizations but their numbering traditions may not be fully independent. The
  permutation control (0/200) shows the recovered mapping is carried by the positional
  evidence, not by numbering conventions, so this does not threaten the result — it belongs in
  the limitations as a provenance note.
- **O7 — 6 of 22 clean pairs sit at exactly support 5** (G65, G503, G415, G923…) and flip out
  under support≥6; the stable core is 16 pairs (§7e). The gate (≥20) holds, but headline
  consumers should read "22 clean" as threshold-edge for ~6 of them.

## 10. Bottom line

Every filed number — 161 shared, 140/768 alignment, 741-vs-267 orientation, 22 clean bijective
/ 19 contested / 151 unmapped over 192 signs, holdout 0.980 (48/49), 15 pwm chains — reproduces
exactly from raw inputs with independently written code; the blind checker passes; the prereg
chain is clean; and the false-positive attacks that this design is most vulnerable to
(coincidental equal-length consistency, duplicate inflation, orientation artifacts) all fail
to dent it (0/200 permutation floor, dedup no-op, wrong orientation gives zero clean pairs).
Threshold sensitivity is the honest weak edge: a defensible stable core is 16 pairs, and six
clean pairs sit on the support-5 boundary. As a provisional, type-level structural concordance
— which is exactly how it is worded — this stands.
