verdict: reproduced

# Skeptic report — L4-0004 smoothing-calibrated bigram hill-climb, N_min on the disjoint-pool cell (sk4-B)

## Independence disclosure

- Opened BEFORE any numbers of mine existed, and nothing else from the claim tree:
  `claims/L4/L4-0004-key-recovery-nmin/claim.yaml`, `README.md`, `planner.md` §8,
  `agents/skeptic-protocol.md`; input definitions `claims/L4/L4-0002-sumerian-hidden-key/claim.yaml`,
  `claims/L4/L4-0002-sumerian-hidden-key/how-we-built-it/sumer_lib.py`,
  `claims/L4/L4-0003-bigram-assisted-key-recovery/claim.yaml`.
- NOT opened before my numbers existed: L4-0004 `how-we-built-it/*` (nmin_lib.py,
  run_l40004.py — still unread at time of writing), `check.py` (executed blind, source never
  read), `object/results.json`, `baseline_snapshot/nmin.json`, `skeptics/*`.
  Git history of `claim.yaml` (prereg-chain audit) uses `git show` of that file only.
- Did NOT read the sk4-A report or `%TEMP%/sk4A`; scratch is `%TEMP%/sk4B`
  (`C:\Users\Apoorv\AppData\Local\Temp\sk4B\{sk4b_lib,step1_build,step2_validate,step3_dev,step4_gated,step5_adversarial,step6_control}.py`).
- `claims/L1/L1-0001-rao-entropy-replication/skeptics/skeptic-task-01.md` read for FORMAT
  only, after my numbers were complete, before writing this report.

## Environment

- Windows (win32) 10.0.26200, Git Bash; Python 3.12.10; numpy 2.4.6 (vectorized climb — noted).
- Raw input: pre-staged `C:/Users/Apoorv/AppData/Local/Temp/l4preflight/etcsri.zip`,
  sha256 `66991601df193a5cb93bccf92e9051e86a98fbb668a9dd343477d14f0c9d54d6` — verified
  byte-identical to `claim.yaml` before anything else ran.
- Repo at commit `main` (worktree HEAD), splits at `benchmarks/splits/v1` (2364 lengths).

## Implementation (mine, from the preregistered text only)

- Imported from the ALLOWED `sumer_lib.py`: `sign_texts`, `indus_lengths`, `windows`,
  `make_key`, `encipher`. Everything else reimplemented: pools (`Random(260417835+5555)`
  shuffle, first 728 / rest), union vocab (asserted |V_U| = 368), key commitments
  (`sha256(json.dumps(key))` asserted equal to all four `key_commitment_sha256` values —
  committed/+9000/+9001/+9002, all PASS), unigram-rank init (count desc, sign asc),
  ref stats, and the climb.
- Climb: objective `sum ln P_ref(m(c_i)->m(c_{i+1}))` over within-window adjacent cipher
  pairs with `P_ref(q|p) = (ref_bigram+alpha)/(ref_unigram+alpha*368)`; steepest-ascent
  pairwise swaps, full sweep per step, first row-major maximum on ties, accept iff
  delta > 1e-12, cap 2000. I vectorized the full pair sweep with numpy (matrix form of
  the classic Jakobsen row/col-sum delta); determinism-equivalent to the spec since
  `np.argmax` over row-major upper-triangle indices = first row-major max.
- Self-test BEFORE trusting any number: vectorized total LL == non-vectorized double
  loop (diff 3.6e-11); matrix LL == direct window-sum LL (diff 6.0e-10); vectorized
  best-swap delta == O(V^2) brute-force best delta (value and argmax pair identical on
  3 random sub-problems; full-size spot checks identical).
- One bug of mine, caught and fixed BEFORE any comparison to shipped numbers: I first
  built the encipher map in the decipher direction (all dev cells gave a nonsensical
  0/10); re-derived from `sumer_lib.encipher` (plain -> cipher) and reran everything.
- Seed assignment: `claim.yaml` lists pools "A … (reference), B … (cipher); 974 windows
  each (seeds +6100/+6000)"; I took A=+6100, B=+6000. My dev table matching the claim
  cell-exactly (below) confirms the assignment; I did not need to try the swap.
- Runtime: my climbs ~2-5 s each (vectorized); 6 dev + 12 gated + ~105 control/extra
  climbs total.

## Numbers: mine vs shipped

Cell construction (mine): n_texts=1456, pools 728/728 object-disjoint, 974+974 windows,
|V_U|=368 asserted, 4/4 key shas asserted. wrap rates 0.0575 (A) / 0.0862 (B), mean
window length 4.504 / 4.615 — all identical to `object/results.json` `cell`.

Dev rule (dev key, N_ref=500, top-10 hits / accepted swaps):

| alpha | claim+object | mine |
|---|---|---|
| 0.001 | 4 / 248 | 4 / 259 |
| 0.01  | 4 / 247 | 4 / 245 |
| 0.1   | 4 / 230 | 4 / 231 |
| 0.2   | 7 / 240 | 7 / 246 |
| 0.5   | 7 / 252 | 7 / 243 |
| 1.0   | 7 / 240 | 7 / 240 |

alpha* = 0.2 by the smallest-sufficient rule — reproduced.

Gated grid at alpha* = 0.2 (top-10 hits; full-key accuracy; swaps, shipped|mine):

| cell | claim/object | mine |
|---|---|---|
| committed@100 | 2 (0.0326; 112) | 2 (0.0326; 109) |
| committed@250 | 4 (0.0489; 174) | 4 (0.0543; 176) |
| committed@500 | 6 (0.0978; 239) | 6 (0.0978; 239) |
| committed@974 | **7** (0.1141; 295) | **7** (0.1087; 288) |
| alt1@100 | 2 (0.0163; 121) | 2 (0.0163; 121) |
| alt1@250 | 8 (0.0924; 193) | 8 (0.0924; 197) |
| alt1@500 | 5 (0.1033; 278) | 5 (0.1005; 271) |
| alt1@974 | **7** (0.1196; 285) | **7** (0.1196; 276) |
| alt2@100 | 2 (0.0109; 113) | 2 (0.0109; 116) |
| alt2@250 | 4 (0.0435; 172) | 4 (0.0435; 176) |
| alt2@500 | 4 (0.1087; 242) | 4 (0.1087; 246) |
| alt2@974 | **7** (0.0978; 273) | **7** (0.0951; 284) |

- All 12 gated top-10 cells EXACT. N_min = 974, keys_ge7@974 = 3/3, GATE PASS — reproduced.
- Full-key accuracy identical in 8/12 cells, differs by 1-2/368 (<=0.005) in 4
  (committed@250/974, alt1@500, alt2@974); accepted swaps differ by <=10. This is the
  L4-0003-documented cross-implementation float tie-noise on report-only fields (my
  vectorized delta sums in a different order); gated cells are stable, as claimed there.
- Context (mine): rank-init alone scores 1/3/3/5 of 10 at N_ref 100/250/500/974 on every
  key, so the climb adds +2 at 974 (5 -> 7); committed@974 climb closes 80.6% of the
  init-to-true LL gap (LL -19942.7 -> -16033.0 vs true -15093.1), 288 swaps, under the cap.

## Checker (run blind, executed only)

```
python claims/L4/L4-0004-key-recovery-nmin/check.py --splits benchmarks/splits/v1 \
  --scratch C:/Users/Apoorv/AppData/Local/Temp/l4preflight \
  --object claims/L4/L4-0004-key-recovery-nmin/object/results.json \
  --baseline claims/L4/L4-0004-key-recovery-nmin/baseline_snapshot/nmin.json
-> alpha*=0.2 N_min=974 committed@974=7/10 keys_ge7=3 recompute=match gate=PASS
   PASS   EXIT=0                                     (~19 min)
```

`check.py` source still unread; expectations met exactly.

## Prereg-chain audit (git)

- `909d6c0` (2026-10-24 12:04:56 +0530, "preregister … results TBD") is the direct parent
  of `b0e50d2` (12:48:20, "results"). Preceding commit `cdda6cb` is the L4-0003 closure.
- `preregistered_threshold` byte-identical across `909d6c0`, `b0e50d2`, `HEAD`
  (sha256 prefix `82c889cd8709993e`, length 1323).
- Prereg commit contains claim.yaml with `result: "TBD — pipeline not yet run"` +
  check.py + how-we-built-it, and NO `object/` or `baseline_snapshot/` (those first
  appear in `b0e50d2`). 43-minute prereg-to-results gap, consistent with 18 pure-Python
  climbs at the stated 2-4 min each.

## Adversarial battery (positive claim — attacked toward false-positive)

| # | Attack | Result |
|---|---|---|
| a | Pool disjointness | Pools are object-disjoint (no shared text objects; verified). Content-level duplicates DO straddle: 9+6 within-pool duplicate groups, 6 content groups appear in BOTH pools — 128/38679 = 0.33% of pool-A tokens, 99/29269 = 0.34% of pool-B. Replaying the window RNG (token-exact vs cached windows for both pools) shows 336/728 and 407/728 distinct source texts actually sampled, sharing 2 content tuples. "No shared texts" holds at object level; content leakage exists but is ~0.3% — quantitatively negligible, should have been disclosed numerically. |
| b | Structureless control (permute tokens within each ref window at N_ref=974, alpha*=0.2 — unigram marginals intact, bigram structure destroyed) | Per-key, 10 seeds each: committed [5,8,4,4,3,4,7,4,7,5] (3/10 >= 7), alt1 [5,7,7,5,7,7,7,4,7,7] (7/10 >= 7!), alt2 [4,8,5,5,1,6,5,5,7,8] (3/10 >= 7). Full-gate control (one shuffled ref per seed, all 3 keys, 30 seeds): **gate would PASS 5/30 = 17%** of the time with a structure-destroyed reference; all-three->=7 in 4/30 (13%). Control mean hits 4.8/5.2/4.9 vs real 7/7/7; control full-key max 0.071, mean 0.032-0.036 vs real 0.095-0.120; control committed@500 (10 seeds) 1-4 vs real 6. Verdict: the top-10 bar ALONE is weakly separated from marginal+search noise (~30% per-key false-clear), but the observed joint pattern (7/7/7 + full-key ~3x every control draw + committed 6@500 above the entire control band) is unlikely under the control; the real cell does exploit true bigram structure. The gate as an isolated statistic has a ~1/6 false-pass rate against THIS null — future gates should include a structureless-null arm or gate on full-key accuracy. |
| c | Boundary fragility | No ties anywhere near the 10/11 boundary (ranks 8-14 counts 99,97,83,82,79,78,76 — distinct on every key), so the top-10 SET is stable; but every key sits at EXACTLY 7/10 (zero slack) with an IDENTICAL hit pattern (cipher ranks 1-7 hit, 8-10 miss) and IDENTICAL top-10 counts [361,194,160,159,147,143,139,99,97,83] — the three keys relabel one plaintext frequency multiset, so 3/3 keys is closer to one observation ("top-7-by-frequency recovered") than three independent replicates. committed's 2->4->6->7 walk crosses the bar on its final step, inside the control noise band. |
| d | alpha peek-inheritance (sk3-B, disclosed) | Mitigation verified: my dev sweep independently reproduces 4/10 at alpha<=0.1 and 7/10 at 0.2/0.5/1.0 on the dev key at N_ref=500 (a key never used in gating, on a never-measured cell); gated re-run at alpha 0.5 and 1.0 gives 7/10 on all three keys — the gate outcome is invariant across [0.2, 1.0], so the peek could only have mattered by excluding alpha<=0.1, which the dev rule re-derives honestly. Residual force: alpha* as a VALUE is not a novel prediction (claim discloses exactly this). |
| e | Wording | grep -iE "decipher\|solv\|translat\|proof\|crack" over claim.yaml + README.md + TROPHY_CASE.md: 0 hits; no TROPHY_CASE entry yet. README explicitly withholds reading claims and licenses only this configuration for L3 consideration. Clean. |
| f | Novelty | Method is Jakobsen-1995 lineage ("A Fast Method for the Cryptanalysis of Substitution Ciphers", Cryptologia 19(3):265-274, 1995 — bigram log-likelihood + hill-climbing from a frequency-rank init), cited by the claim as such; contribution is calibration (dev-rule alpha*, disjoint-pool N_min measurement at Indus scale), not method novelty. Search logged (Jakobsen 1995 Cryptologia bigram hill-climbing; metaheuristics survey). Framing honest. |

## Gate checklist (planner §8 / skeptic-protocol)

- [x] Rebuilt from raw inputs (zip sha verified) with independently written code
      (sumer_lib imported for the input pipeline only, per protocol).
- [x] Same sign scheme and corpus snapshot hash — gdl_sign stream, zip sha match,
      |V_U|=368 and 4/4 key shas asserted.
- [x] Threshold fixed before the run — prereg 909d6c0 < results b0e50d2, threshold
      byte-identical, result TBD at prereg, no object/ before results. 43-min gap.
- [x] Null models attached — mine: structureless-reference control (30-seed full-gate
      evaluation + per-key sweeps); not part of the claim, folded in as objection 1.
- [x] Degrees of freedom — no metric search: single preregistered gate; dev alpha
      chosen on a separated dev key; DISCLOSED peek considered under (d).
- [x] Novelty checked — Jakobsen 1995 lineage; calibration contribution (above).
- [x] Claim wording matches what was shown — yes; "N_min = the whole corpus" headline
      overstates precision (objection 3), body hedges honestly.
- [x] Checker runs green from scratch — recompute=match, gate=PASS, exit 0 (blind).

## Objections (non-blocking)

1. **Top-10 bar is weakly separated from marginals+search noise.** Under a
   structureless reference the full preregistered gate still passes 17% of draws
   (all-three->=7 in 13%); alt1 alone clears 7/10 in 7/10 shuffles. The real cell's
   joint evidence (7/7/7, full-key 0.095-0.120 vs control max 0.071, committed 6@500
   above the whole control band) supports genuine structure exploitation — but as a
   STANDALONE statistic the gated bar has a ~1/6 false-pass rate against this null.
   Recommend: future key-recovery gates add a structureless-null arm, or gate on
   full-key accuracy (which separates ~3x), or raise the top-10 bar.
2. **The 3-key conjunct is not 3 independent replicates.** All keys share the same
   cipher count structure (top-10 counts identical) and produced the identical hit
   pattern (ranks 1-7). "keys_ge7 = 3/3" certifies robustness to key relabeling, not
   to sampling noise; the claim's caveat structure survives this, but readers should
   not read 3/3 as triplicate evidence.
3. **"N_min = the whole corpus" is a one-key, one-draw boundary.** alt1 hit 8/10 at
   N_ref=250 (above the bar mid-grid) and committed crossed only at the last grid
   point with zero slack (6->7), inside control noise (control spans 1-8 at fixed
   N_ref). The honest reading is "committed crosses 7 exactly at the top of the
   grid"; the README title carries more precision than the measurement supports.
   Body discloses alt1 non-monotonicity; headline should be softened or banded.
4. **Content-level pool leakage is nonzero.** 6 duplicate content groups straddle the
   pools (0.33%/0.34% of tokens; 2 realized among sampled source texts). Object-level
   disjointness claim is true; genre + duplicate leakage should be quantified in the
   limitations rather than only the genre caveat.
5. **Report-only fields are not cross-implementation portable** (full-key +/-2/368,
   swaps +/-10 — float tie-noise on near-tied swaps; same phenomenon L4-0003 recorded).
   Gated cells reproduced exactly; no action needed beyond the existing convention.
6. **LL-consistency note.** recovered LL (-16033) remains ~940 above true-key LL
   (-15093) — the climb's optimum is not the true key, consistent with the disclosed
   ~0.10 full-key accuracy; no claim is made beyond the top-10 bar.

## Bottom line

Every gated number reproduced exactly from raw inputs with independently written code
(dev table, 12/12 grid cells, alpha*=0.2, N_min=974, 3/3 keys, cell statistics, 4/4 key
sha commitments); the shipped checker re-verified blind (`recompute=match gate=PASS`,
exit 0); the prereg chain is clean (threshold byte-identical, TBD-before-results,
43-min separation). The claim is honestly scoped (top-10 bar only, no reading claim,
peek disclosed). My adversarial battery narrows the interpretation — the top-10 bar
alone has a ~17% false-pass rate against a structureless-reference null and the 3-key
conjunct is key-relabeling robustness rather than triplication, and the N_min=974
headline is one noisy 6->7 step — but none of this overturns the preregistered gate as
filed. **Reproduced**, with objections 1-3 to fold into the claim's limitations before
any L3 use.
