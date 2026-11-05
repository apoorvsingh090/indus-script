# sk9-B — Fresh-context skeptic report on L4-0009 (full-key-separation gate)

**Skeptic id:** sk9-B · **Date:** 2026-11-04 · **Environment:** Python 3.12, Windows, stdlib only.
**Verdict: REPRODUCED** — the gate verdict (FAIL at condition (c), half-B non-replication) reproduces
with my own method code written from the preregistration text, all gate-bearing numbers landing
equal to the shipped object (three gate arms and null_max bit-exact; the two 487-window halves and
dev within ±3/371), and — after the grid completed and the builder code became readable — a
float-faithful re-run reproducing **every** shipped field exactly (accuracies to the last printed
digit, accepted-swap counts, winning start indices, top-10 counts).

## 1. What I did

Fresh-context blind protocol followed. Before any computation I read only `claim.yaml`/`README.md`
of L4-0009, claim.yaml/README.md of L4-0002..0006, `benchmarks/splits/v1/*`, `agents/skeptic-protocol.md`,
and the raw `etcsri.zip`. L4-0009 `check.py`, `how-we-built-it/*`, `object/*.json`,
`baseline_snapshot/*.json` and all other claims' method code were **not** opened until my
gate-bearing grid had completed; they were read afterwards only for the reconciliation section.
The allowed shared pipeline `L4-0002/how-we-built-it/sumer_lib.py` was used and disclosed rather
than reimplemented (`sign_texts`, `indus_lengths`, `windows`, `encipher`, `make_key`).

Work dir `…\Temp\opencode\sk9-B\` (zip cached, sha256 `66991601df…c9d54d6` verified; `work/` holds
my code and results: `sk9_lib.py` [method lib], `sk9_test.py` [selftest], `sk9_stage1.py` →
`cell4.json` [inputs + verification], `sk9_stage2.py`, `sk9_stage3.py`–`3f.py`, `sk9_diag_i/ii.py` →
`results_grid.jsonl`, `results_ri.jsonl`, `results_probe.jsonl`, `results_pd.jsonl`,
`results_resid.jsonl`, `results_halfnulls.jsonl`, `results_splits.jsonl`, `diag_ii_stats.json`,
`results_faithful.jsonl`). Multiprocessing, 4 workers (determinism preserved per climb).

## 2. Input/cell verification (before any recovery)

- Zip sha256 `66991601df193a5cb93bccf92e9051e86a98fbb668a9dd343477d14f0c9d54d6` — matches claim.
- `sign_texts` → **1456** nonempty texts; pools **728/728** after `Random(260417835+10000)`.
- Windows 974/974 from `Random(+10100)`/`Random(+10200)`, splits/v1 lengths; wrap rates
  **0.0739 / 0.0678** and mean window lengths **4.42 / 4.56** — match claim.
- Union vocab **V_U9 = 371** (`assert` in my builder).
- Key shas: `make_key(371, 260417835+{11000,11001,11002,11003})`, serialization `sha256(str(key))`
  (≡ `json.dumps` default) — **all four match** the commitments (convention pinned via L4-0002's
  disclosed committed-key sha).
- Positional cross-check in my pipeline: within-window index ≥8 tokens = 2.23 % of combined
  pool tokens (8747 core; claim discloses 2.09 %, per-side reference figure; non-gating, noted).
- splits/v1 `SHA256SUMS` match split.json counts (1365/185/814).

## 3. Method reproduction details (my implementation)

Objective (alpha FROZEN 0.5, L4-0006 position-resolved joint form):

    J(m) = Σ within-window adjacent cipher pairs ln((B[p,q]+0.5)/(U[p]+0.5·371))
         + Σ cipher tokens ln((R[t,pos]+0.5)/(T[pos]+0.5·371)),  pos = min(index,7)

Search: full-sweep steepest ascent over all C(371,2)=68 635 pairs, first row-major maximizer,
accept iff Δ > 1e-12, cap 2000 accepted swaps; best-of-3 starts (rank-init count-desc/sign-asc,
then two seeded random-bijection starts), winner = max exact total J, ties → earlier start.
Nulls: K=12 within-window-shuffled references, seeds 777000000+i, single-start. Halves =
committed key on cipher windows 0:487 / 487:974. Dev = committed-key-style arm with dev key
(+11003) at ref_prefix 500 (report-only). Top-10 (report-only): cipher-side
`Counter(...).most_common(10)` exact-map check.

**Correctness engineering:** my climb keeps table-ized delta increments (`G`/`H` per-assignment
tables + sparse row/col summaries) instead of the builder's per-pair enumeration;
`sk9_lib.selftest()` brute-force-validates pair deltas and incremental updates against
from-definition objective differences on randomized synthetic data (worst |Δ| 5.1e-13; climb
drift ~3e-13 vs exact re-score).

**Spec ambiguities resolved during the blind phase (self-caught, disclosed):**

1. `ref_unigram` denominator: **token counts**, not reference-bigram-row sums. Row-sum reading
   gives committed 66/371 ≠ shipped 64/371; token reading matches.
2. Random-restart construction: prereg says "random starts, seeds Random(42000001/+2)". I ran
   rand-standalone and probe grids over several constructions; only
   **start = shuffled `range(V)` (a random bijection), seeds 42000001 and 42000002** reproduces
   alt1 (53/371, winner = start index 1). Alternative constructions tried and rejected:
   `perm_values` / `perm_domain` (+ both inverse variants), rank-init-permuted (`rri_*`) variants
   on both/ref/cyp sides, `sample()`-based reading, seeds {42000002,42000003}.
3. Tie-break detail: "absent×absent" pairs have Δ=0 and are skipped; identical outcomes vs
   full-scan-with-init-1e-12 (both terminate identically under the >1e-12 accept rule).
4. My half-arm **top-10 sets** were initially computed against the full-cipher top-10 rather than
   each half's own top-10 (my slip, non-gating; corrected in the post-run faithful pass —
   per-half values 8/10 and 5/10 then match the claim).

## 4. Gate-bearing results — blinded run (my code) vs shipped object

All numbers = committed-key true-inverse exact count over V=371 (best-of-3, J-selected).

| Arm | Claim (results.json) | sk9-B blind re-run | Δ (types/371) |
|---|---|---|---|
| committed full @974 | 0.1725067385444744 (64/371), start 0 | **0.1725067385444744 (64/371)**, start 0 | 0 (exact, incl. digits) |
| alt1 full @974 | 0.14285714285714285 (53/371), start 1 | **0.14285714285714285 (53/371)**, start 1 | 0 (exact) |
| alt2 full @974 | 0.15363881401617252 (57/371), start 0 | **0.15363881401617252 (57/371)**, start 0 | 0 (exact) |
| half A full | 0.1293800539083558 (48/371) | **0.12668463611859837 (47/371)** | −1 |
| half B full | 0.0673854447439353 (25/371) | **0.05929919137466307 (22/371)** | −3 |
| null_max (K=12) | 0.0673854447439353 (25/371) | **0.0673854447439353 (25/371)** | 0 (exact) |
| dev (report-only) | 0.15902964959568733 (59/371) | **0.15633423180592992 (58/371)** | −1 |

- Single-start null ties (types/371, seeds 777000000+i): mine **17,23,14,14,14,7,18,11,17,18,25,9**
  vs claim 17,22,14,14,14,7,17,12,17,18,25,8 — 9/12 bit-exact, three off by exactly ±1.
  Multistart spot-check nulls (report-only): I ran seeds {12,13} (my reading of the URI); claim's
  shipped ones are seeds {0,1} — see §6 (both agree with their single-start values).
- My accepted-swap counts: committed 271, alt1 340, alt2 259 vs shipped 268/337/258 (same starts,
  adjacent optima — see §6).
- Report-only top-10 (half arms under my corrected per-half convention): committed 10/10 =,
  alt1 10/10 =, alt2 7/10 =, dev 9/10 =, halves 8/10 and 5/10 (= per-half; corrected post-run).

**Gate conditions (mine / claim), ratios vs my null_max (25/371):**

- (a) committed 2.56× > 1 ✓, ≥1.5× ✓ / claim 2.56× ✓ — PASS / PASS
- (b) keys ≥1.25× : committed 2.56×, alt1 2.12×, alt2 2.28× → 3/3 ✓ / claim 3/3 (identical numbers) — PASS / PASS
- (c) half A 47/25 = **1.88×** ✓ (claim 1.92× ✓); half B 22/25 = **0.88×** ✗ (claim 1.00× ✗)
  — **FAIL / FAIL**, failing through half B in both.
- (d) committed 0.1725 ≥ 0.060 ✓ / claim 0.1725 ✓ — PASS / PASS
- **Overall gate: FAIL at (c)** — same as shipped object (`pass: false`, `keys_replicated: 3`).

## 5. Diagnostics (run after the blind grid, before unblinding)

**(i) Half-scale null calibration.** With nulls regenerated **per half** (487-window reference
halves → committed-key cipher half, K=12 seeds 777000000+i, single-start): halfA ties
[6,8,14,15,19,14,19,17,6,19,11,8] (max 19/371 = 0.0512); halfB ties
[8,6,19,5,5,5,6,4,6,4,9,4] (max 19/371 = 0.0512). The full-scale null_max (25/371) that
condition (c) uses is ~30 % higher than either half-specific null_max — a data-scale artifact of
comparing 487-window halves against a 974-window null. Under half-scale calibration the claim's
half-B = 25/371 = **1.32×** its own half-null max would **pass** the 1.25× margin; my 22/371 =
**1.16×** sits borderline. So condition (c)'s outcome is a function of the preregistered
comparison to the full-scale null_max (and hence fails there), but it is *calibration-sensitive*:
half B performs at exactly null level (full-scale) or marginally above the half-scale band.

**(ii) Composition symmetry of the halves.** Diag stats: halfA 487 w / 2213 tok / 244 types, 195
in ref (80.0 % coverage), cipher-ref bigram coherence 57.2 %, positions-with-visible-pair 87.1 %,
mean length 4.544, tail ≥8 tokens 2.30 %; halfB 487 / 2229 / 249 types, 203 in ref (81.5 %),
54.9 %, 86.6 %, 4.577, 2.42 %. Lengths, coverage and positional tails are essentially identical;
the only asymmetric lever is ~2.3 pp of ref-bigram coherence. **Alternate 487-window splits**
(own probe, bo3, committed key): random split #1 (`Random(99001)` shuffle) **46/371** (2.42× its
own recovered band), complement **47/371** (1.88×), even-indexed windows **52/371** (10/10
top-10), odd-indexed **58/371** (10/10). Half A behaves like other random samples; half B is the
specific outlier, not a generic small-sample effect.

**(iii) Token-weighted accuracy.** Token-weighted hit rate (cipher-token mass recovered): final
blinded arm values — committed **0.6452**, alt1 0.3982, alt2 0.5434, dev 0.6335, halfA **0.5739**
(its 47/371 winner; an adjacent same-band optimum scores 0.5432 at 45/371), halfB **0.2934**,
nulls (single) 0.309/0.357/0.284/0.192/0.277/0.138/0.282/0.220/0.353/0.313/**0.445**
(null10)/0.152, splits: rand #1 0.4890, even 0.6121, odd 0.6704, complement 0.5780. Half B's
token-weighted recovery (0.2934) is below the largest null's (0.445) — its residual plaintext
mass sits in low-frequency types; B does not replicate the core-tissue recovery that A exhibits.

**(iv) Construction/robustness probes.** (a) eps 1e-15 vs 1e-12 → identical accepted-swap
sequences on tested arms; (b) `perm_values`/`perm_domain` (both straight and inverse readings) as
start constructions under seeds {42000001,42000002} and {42000002,42000003} → gate verdict
unchanged (committed/alt2 unchanged-ish, alt1 falls to ~0.097 → (b) still 2/3 ≥ 1.25×, (c) still
fails at B); (c) `rank_counts` alternatives (counts from full cipher, etc.) and eps variants
(stage3f) → no reproduction of alt1 53 and no verdict flip; (d) `rri_*` rank-permuted starts → no
(see §3 item 2). The claim's negative verdict at (c) is robust to every probe tried.

## 6. Post-run reconciliation (reads permitted only after my grid completed)

Reading the shipped object, `check.py`, and the builder stack
(`l40009_lib.py`, `L4-0003/recover_lib.py`, `L4-0004/nmin_lib.py` — imports used by the L4-0009
runner) explained **every** residual of my blinded run, as two mechanisms:

1. **Halves vocabulary.** The runner computes `vocab` **once** over the full ref+cipher union
   (371) and reuses it for *every* arm, including the 487-window halves and dev. My blinded run
   built per-arm unions (shorter for halves), which changes rank-init zero-count tie ordering on
   halves.
2. **Float summation path.** The builder stores `logp[p][q] = log((B[p][q]+a)/(U[p]+a·V))` as a
   dense direct-ratio matrix and iterates dict **insertion order** with an exact per-pair term
   order (`rowA → rowB → colA → colB → corner terms → positional delta` — pos delta added
   *after* the bigram delta per pair). My table form (`log(B+a)−log(U+aV)` and grouped
   accumulations) is mathematically identical (brute-force-validated to 5e-13) but differs in the
   last ulp, occasionally flipping a near-tie argmax; the chaotic steepest-ascent then lands on an
   adjacent optimum (±1–3/371, ±1–4 swaps, same top-10 counts).

**Float-faithful confirmation run** (`sk9_stage4.py`, 36 climbs, transcription of the disclosed
arithmetic path only — my own input/metric layer kept): **every shipped field reproduced
exactly** — committed 0.1725067385444744 / start 0 / **268 swaps**; alt1 0.14285714285714285 /
start 1 / **337 swaps**; alt2 0.15363881401617252 / start 0 / **258 swaps**; halfA
0.1293800539083558 / start 2 / 300 swaps; halfB 0.0673854447439353 / start 0 / 211 swaps; dev
0.15902964959568733 (top10 9/10); all 12 single-start nulls and the 2 multistart nulls to full
printed precision (e.g. null0 0.04582210242587601, null1 0.05929919137466307); halves top-10 8/10
and 5/10. I.e. `object/results.json` is seamlessly regenerable, and my independent blinded
implementation sat inside the disclosed cross-implementation band around it on every arm.

Also confirmed from the runner: the multistart null spot-checks are seeds {0,1} (my blind-phase
{12,13} guess was a report-only reading error, disclosed in §4); null multistart never beats
single-start rank-init on those seeds (values equal), consistent with the claim's disclosed
asymmetry handling. `check.py` re-derives the whole gate the same way and compares with 1e-12
tolerance; my faithful pass would satisfy it. `baseline_snapshot/gate9.json` matches my sha set.

## 7. Runtime

- Cell build + input verification: ~2 min (incl. sha checks and union asserts).
- Stage 2 disambiguation (4 combos × 3 climbs): 895.9 s @ 4 workers.
- Main grid (36 climbs; §4): 2058.6 s @ 4 workers (343.1 s/arm).
- Probe grids (3b 566 s; 3c ~1398.8 s incl. 10+ constructions; 3d ri re-verify 1046.8 s; 3e/3f
  residual probes 814.7 + 321.9 s).
- Diagnostics: half-nulls (2×12 climbs) 649.4 s; composition + 4 alternate splits 365.6 s + stats.
- Float-faithful 36 climbs: 1576.5 s @ 4 workers (~110 s/climb isolated, matching the builder's
  ~68 min single-process estimate).

## 8. Concerns

1. **Condition (c) is calibration-sensitive (§5-i):** the preregistered comparison against the
   full-scale null_max stacks the halves against a null band generated from 2× their reference
   data. At half-scale calibration the claimed half-B number would clear the 1.25× margin; at
   full-scale it sits at exactly 1.00×. The preregistered reading (and hence the claim's negative
   verdict) is correct as written, but a future half-split gate should pre-register half-scale
   nulls (or require both) to be interpretable.
2. **Float-path portability now touches a gating surface:** ±1–3/371 cross-implementation bands
   shift from report-only (as disclosed in L4-0005 skeptics) to gate-bearing numbers. Margins
   (1.25×/1.5×/0.060) comfortably absorb it here; a future gate passing by <3/371 would be
   non-reproducible across independent implementations. Mitigation I used: exact-arithmetic
   canonicalization or disclosed float-path transcription (§6) makes results bit-stable.
3. **Half B is a specific anomaly, not a small-sample generic effect** (§5-ii): other 487-window
   splits at equal size replicate at 2.4–2.5× commit-level accuracy; B's unique failure is
   compositional (2–3 pp lower ref-bigram coherence), not length/coverage-related.
4. **My blind-phase reading slips (corrected, disclosed):** bo3-null seed set ({12,13} vs the
   runner's {0,1}), halves' per-arm vocab (mechanism of my ±1–3 residuals, §6), halves' top-10
   convention. None affect the gate outcome; all were resolved before the verdict.
5. The alpha-freeze design (a=0.5 carried from L4-0006 rather than re-dev-loaded on cell #4) is a
   disclosed, preregistered methodological weakness — the dev arm is accordingly report-only and
   my numbers agree with the claim's (58±1/371, top-10 9/10).

## Verdict

**reproduced.** My independent blinded implementation reproduces the gate verdict (FAIL at
condition (c) through half B; (a),(b),(d) pass) with committed/alt1/alt2 and null_max
**bit-exact**, halves within −1/−3 types and dev −1 (all inside the cross-implementation band the
repo already discloses), and the follow-up float-faithful re-run reproduces every shipped field
(including accepted-swap counts and start indices) exactly. Diagnostics (i)–(iv) show the half-B
non-replication is composition-specific and survives start-construction, eps-tolerance and
construction-reading probes, while flagging that condition (c)'s calibration scale is a fragile
design choice worth re-registering in any successor gate. Files: `cell4.json`,
`results_grid.jsonl`, `results_halfnulls.jsonl`, `results_splits.jsonl`, `results_faithful.jsonl`,
`results_*.jsonl`, `diag_ii_stats.json`, all scripts `sk9_*.py` in the sk9-B scratch dir. I
modified nothing else in the repo except creating this file.
