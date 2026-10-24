verdict: reproduced

# skL0-C independent audit — L0-0003 G<->P type-level concordance v0.1

## Independence disclosure (what was opened, and when)

Phase 1, before any code was written — only these repo files: `claim.yaml`,
`README.md`, `planner.md` §8 (lines 120–159), `agents/skeptic-protocol.md`,
plus input definitions `claims/L0/L0-0001-mayig-joy-xcheck/claim.yaml`,
`claims/L0/L0-0002-concordance-v01/claim.yaml`, and the header/first rows of
`data/concordance/pwm-v01.csv`. Raw inputs inspected for structure only: the
G corpus CSV (columns, one sample row, site counts) and the mayig clone
(directory listing, `m001.json` as one sample, per-directory file counts).
Input pins verified before anything else (below).

Phase 2: wrote my own implementation (`%TEMP%/skL0C/my_build.py`,
`probes.py`) purely from the `preregistered_threshold` text. Own numbers
existed at this point.

Phase 3, only after own numbers existed: executed the shipped `check.py`
BLIND (output only — its source was never read), then read
`object/results.json`, `baseline_snapshot/counts.json`,
`data/concordance/gp-v01.csv`, and ran the git prereg audit
(log/diff/ls-tree). `how-we-built-it/build_gp.py` source was never opened.
No other skeptic's report was read; the concurrent skeptic's work was not
touched. `claims/L1/L1-0001-rao-entropy-replication/skeptics/` was opened
for FORMAT only, after all analysis was complete.

Honesty note: this session was interrupted twice by transient infrastructure
errors ("model concurrency limit exceeded" at launch, before any file
access; "Start Plan is busy" mid-run, right after the git ancestry check).
No work was lost; I resumed each time from the persisted scratch state and
no step was re-ordered relative to the fresh-context rules above.

## Environment

- Windows 10.0.26200 x64, Git Bash; Python 3.12.10, stdlib only
  (`csv, json, re, os, collections`)
- mayig clone @ `C:/Users/Apoorv/AppData/Local/Temp/gbridge/mayig` —
  `git rev-parse HEAD` = `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb` (matches pin)
- G corpus `.../gbridge/indus_website_real_corpus.csv` — sha256 recomputed
  `7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8` (matches)
- Scratch: `%TEMP%/skL0C` (`my_build.py`, `probes.py`, `my_results.json`)

## Implementation (own, from the preregistered text)

Join G rows (site==Mohenjo-daro, `cisi_number` full-match `^M-?\d+[A-Z]?$`)
to mayig entry ids (`^M-?(\d+)`) on the integer M-number; G tokens reversed
where `reading_direction=='L-R'`; both global P variants (as-stored /
reversed) scored by sum over G-signs of max_p C[g][p], higher wins; every
equal-length (G-row, P-side) pair aligned positionally; per G-sign
classification: clean iff n_g>=5 AND support>=5 texts AND C[g][p1]>=0.9*n_g
AND g is p1's top source AND C[g][p1]>=0.9*n_p1 (I additionally required no
near-tie flag; moot here); contested iff n_g>=5 with reason(s); unmapped iff
n_g<5. Holdout: every 5th of the sorted shared M-numbers held out, mapping
inferred on the rest, scored at clean-mapped held-out positions.

## My numbers vs shipped

| Item | Claimed/shipped | Mine |
|---|---|---|
| shared M-numbers | 161 | 161 |
| mayig sides / G M-daro rows with M-number | 179 / 1188 | 179 / 1188 |
| orientation top-sums (reversed / as-stored) | 741 / 267 → reversed | 741 / 267 → reversed |
| equal-length (G-row, P-side) pairs | 140 | 140 |
| aligned positions | 768 | 768 |
| G / P signs observed at aligned positions | 192 / 164 | 192 / 164 |
| clean / contested / unmapped | 22 / 19 / 151 | 22 / 19 / 151, per-sign membership identical (0 disagreements over all 192 rows) |
| bijective over clean | yes | yes |
| top supports | G2→P122 60/63, G740→P324 75/76, G220→P050 27/29 | same triples exactly |
| holdout (33 texts) | 48/49 = 0.980 | 48/49 = 0.9796 (miss: M-127 G220, actual P060, predicted P050) |
| composition with pwm-v01 | 22/22 P codes present, 15 clean-1:1 chains | 22/22, 15 (incl. G220→P050→M059, G233→P058→M072, G235→P060→M065) |
| baseline counts.json | 161/192/22/19/151 | all match |

Clean list (mine, = shipped): G740→P324, G2→P122, G220→P050, G60→P120,
G240→P062, G520→P217, G820→P378, G235→P060, G233→P058, G368→P202, G3→P123,
G33→P147, G140→P011, G90→P013, G255→P073, G31→P144, G176→P194, G16→P126,
G923→P175, G65→P201, G503→P210, G415→P092.

## Checker (blind run, after own numbers)

```
shared=161 pairs=140 p_reverse=True clean=22 contested=19 unmapped=151
bij_viol=False recompute=match gate=PASS
PASS
EXIT=0
```

As expected: recompute=match, gate=PASS, exit 0.

## Prereg audit (git)

- `7e0025d` (2026-10-24 15:23:33 +0530, "preregister ... no mapping computed
  yet") is an ancestor of `7861f78` (2026-10-24 20:15:45 +0530, results).
- `preregistered_threshold` byte-identical across the two commits: the full
  claim.yaml diff touches only `result:` ("TBD — pipeline not yet run at
  preregistration commit" → the GATE PASS text) and a `status:` comment.
- At `7e0025d` the claim tree contains only `claim.yaml`, `check.py`,
  `build_gp.py` — no README, no `object/`, no `baseline_snapshot/`, no
  `gp-v01.csv`. All result artifacts first appear at `7861f78`.

## Adversarial battery (positive claim — attacked toward false positive)

| Probe | Result |
|---|---|
| (a) Join-object validity | Shared G rows 161/161 motif `Bull1:*` (W65/J52/S27/I6/U3/T2/V2/X2/plain1/L1); mayig shared ids 161/161 `unicorn N seal` (IV88/III39/II16/I9/V9). Both sides independently classify every shared object as the unicorn motif, with disjoint vocabularies. mayig-only = 18 M-numbers (19,22,27,39,55,60,61,62,66,105,106,110,125,137,141,167,169,175); G-only = 1027; 14 M-daro rows have no M-form cisi_number at all. No mismatched-object evidence found. |
| (b) Leakage into G csv | 9 fixed columns; every `sign_sequence` token matches `^G\d+$` (0 offenders, 592 distinct codes = the G-592 scheme); 0 rows contain a `P###` token; 0 rows contain "unicorn"; motif vocabulary (`Bull1/Gaur/Elep/Bult/Othr`) disjoint from mayig's. No P-coded or mayig-derived data detected in the G corpus. |
| (c) Orientation | Both variants reproduce (741 reversed vs 267 as-stored). Sensitivity: mismatched relative orientation collapses evidence — G-corrected + P-as-stored = 267, clean 0; G-RAW + P-reversed = 267, clean 0. Matched relative orientation (G-RAW + P-as-stored) gives 741 and the identical 22 clean pairs. So the finding is a *relative*-convention fact (the two sources store sequences in opposite orders); the preregistered both-variants rule decides it decisively and cannot silently pick wrong. |
| (d) Threshold sensitivity | clean count over min_support {4,5,6} × consistency {0.85,0.90,0.95}: 28/22/19, 28/22/19, 25/19/16. Flips: cons 0.85 gains G1→P121, G32→P145, G692→P256, G390→P086, G840→P349, G760→P332; cons 0.95 loses G235→P060, G820→P378, G220→P050; support 6 loses G65→P201, G503→P210, G415→P092. 16/22 pairs invariant across the entire grid; gate bar (>=20) fails only at the grid edges (cons 0.95, or support 6 at cons>=0.90). |
| (e) Own holdout split | Every-3rd (54 held texts, train-clean=15): 101/102 = 0.9902 at clean-mapped positions. Every-5th offset variant (32 held): 63/64 = 0.984. Single miss in both: G220 (actual P060 / P056 vs predicted P050). Accuracy robust to split rule. |
| (f) Contested clusters | G861/G817→P385 (13 vs 12 texts), G803/G806→P364 (9 vs 5), G900/G920→P154 (6 vs 3): the two G signs of each cluster never co-occur in any shared text (0 overlap). G550/G798→P230 (9 vs 7): co-occur in exactly 1 text. Complementary distributions support the split-variant reading for all four clusters (3 strictly). |
| (g) Wording grep | `grep -riE "deciphered|solved|translat|proof"` over claim.yaml/README.md hits only "NOT glyph identity proof" / "identity proof" — negations. No overclaim. |
| (h) Novelty | Cross-referencing sign numbers across the canonical lists is long-established (Mahadevan 1977 concordance, 417 signs; Parpola 386; Wells ~700+; comparison tables exist in the literature). New here: a G-592 (yajnadevam web chain) ↔ Parpola P-code bridge derived by preregistered positional alignment with evidence counts, plus the orientation-convention finding. The claim self-describes as a type-level provisional bridge — no novelty overclaim. Searched (2026-10-24): "Indus script sign number concordance Parpola Wells Mahadevan cross-reference sign lists". |

## Protocol checklist

- [x] Rebuilt from raw inputs in a clean context with independently written code
- [x] Same sign-coding scheme and corpus snapshot hash (mayig pin + CSV sha256 recomputed)
- [x] Threshold and split fixed before the run (prereg audit: ancestry, byte-identical threshold, result TBD at prereg, no result artifacts at 7e0025d)
- [x] Null models/calibration — N/A at L0 (structural concordance, no statistical gate)
- [x] Degrees of freedom — 1 orientation bit (2 variants), disclosed and decisive (741 vs 267; 22 vs 0 clean)
- [x] Novelty checked against prior literature (logged above)
- [x] Claim wording matches what was shown
- [x] Checker runs green from scratch (blind run: recompute=match, gate=PASS, exit 0)

## Objections (non-blocking)

1. **gp-v01.csv zeroes the tail's evidence.** All 151 unmapped rows ship
   `p=''` and `c_g_p=n_g=support=0`, but every one of those signs DOES have
   aligned evidence (true n_g in [1,4]; e.g. G4→P124 4/4, G190→P076 4/4,
   G100→P009 3/3 — my numbers). The preregistered gate text promised "every
   sign listed ... with evidence counts". Class assignment is unaffected
   (all n_g<5), and the checker reproduces the same zeroing — consistent,
   but self-referential on this point. Recommend shipping true tail counts.
2. **README wording on exclusions:** "1027 G M-daro rows without an
   M-number join" — in fact 1188 rows carry M-form numbers, of which 1027
   have no mayig counterpart; 14 rows have no M-form cisi_number at all. The
   count 1027 verifies; the phrasing conflates "no M-number" with "no
   mayig counterpart".
3. **Reason vocabulary vs narrative:** shipped contested reasons are
   `low-consistency` for the cluster members (they fail the two-way
   `C[g][p1]>=0.9*n_p1` precisely because both G signs feed the same P),
   while the README narrates "split-convention clusters" — an interpretation
   outside the preregistered reason taxonomy. My complementarity probe (f)
   supports it, but it is an interpretation, not a computed reason code.
4. **Orientation is selected on the same data it gates** (1 bit, disclosed
   in limitations; margin 741-vs-267 and 22-vs-0-clean makes it benign).
   Relatedly, the data cannot distinguish "reverse P" from "don't reverse
   G" — the claim's wording ("stored opposite to the G corrected order") is
   already the correct relative statement.
5. **Holdout residual is structural:** the single error in every split is
   G220 (predicted P050, actual P060/P056), adjacent to clean G235→P060.
   0.980 is honest, but the miss is a sign-split artifact, not random noise.
6. **Gate margin at edges:** 19 clean at min_support=6 or consistency=0.95
   (bar fails there). The preregistered cell is central and the 16
   grid-invariant pairs carry the result; worth remembering when composing
   downstream claims.

## Bottom line

Every gated number reproduces exactly from raw inputs with independent
code — 161 shared M-numbers, 741/267 orientation scores, 140 pairs, 768
positions, 22/19/151 classes with identical per-sign membership, bijective
clean set, holdout 48/49 — the blind checker returns recompute=match /
gate=PASS / exit 0, the prereg chain is clean (ancestry, byte-identical
threshold, result TBD before results commit), and all eight adversarial
probes support rather than undercut the claim: the join is same-object on
both sides' own vocabularies, no P/mayig data leaks into the G corpus,
wrong relative orientation collapses the clean set to zero, thresholds
move the count by at most ±6 with a stable core, my own split gives
0.990, and the contested clusters show textbook complementary
distributions. The claim is honestly worded as a provisional type-level
bridge. Reproduced.
