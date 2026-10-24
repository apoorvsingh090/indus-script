verdict: reproduced

# Skeptic report — L4-0004 disjoint-pool N_min key recovery (sk4-A)

Independent audit, positive-claim adversarial stance. I did NOT open
`how-we-built-it/{nmin_lib,run_l40004}.py`, `check.py`, `object/results.json`,
`baseline_snapshot/nmin.json`, or any other skeptic's work before my own numbers
existed. `check.py` was executed blind (source never read; only the prescribed
wording grep ever touched those file contents, after my numbers, and matched
nothing).

## Independence disclosure (what was opened, when)

Before my numbers existed — allowed inputs only:

- `claims/L4/L4-0004-key-recovery-nmin/claim.yaml` + `README.md` (the spec under audit)
- `planner.md` §8, `agents/skeptic-protocol.md`
- `claims/L4/L4-0002-sumerian-hidden-key/claim.yaml` +
  `how-we-built-it/sumer_lib.py` (input pipeline: `sign_texts`/`indus_lengths`/
  `windows`/`make_key` — imported, not rewritten, per protocol allowance)
- `claims/L4/L4-0003-bigram-assisted-key-recovery/claim.yaml` (method lineage text only;
  its `recover_lib` was NOT imported — rank-init and hill-climb reimplemented from
  the L4-0004 threshold prose)
- `claims/L1/L1-0001-rao-entropy-replication/skeptics/skeptic-task-01.md` (FORMAT only)
- repo `git log` subject lines (which quote the filed results — unavoidable; my
  comparisons below are against my own computation, then the object)

After my numbers existed: blind checker run; then `object/results.json`,
`baseline_snapshot/nmin.json`, wording grep over the whole claim dir, TROPHY_CASE.md.

## Environment

- OS: Windows (win32 10.0.26200), Python 3.12.10, numpy 2.4.6 (vectorized climb — see below)
- Raw input: pre-staged `C:\Users\Apoorv\AppData\Local\Temp\l4preflight\etcsri.zip`,
  sha256 `66991601df193a5cb93bccf92e9051e86a98fbb668a9dd343477d14f0c9d54d6` — matches claim
- My code: `C:\Users\Apoorv\AppData\Local\Temp\sk4A\{audit,adversarial,adversarial2}.py`
  (+ `my_results.json`); CC0/attribute; nothing vendored into the repo

## Implementation (my own, from the preregistered_threshold prose)

- Texts shuffled `Random(260417835+5555)`; pool A = first 728 (reference), pool B = 728
  (cipher). Seed-assignment ambiguity in the spec ("seeds +6100/+6000") resolved by the
  prereg assert itself: ref=`+6100`, cyp=`+6000` yields V_U=368 (the flip does not;
  wrap rates below then matched the object to 15 digits, confirming the choice).
- 974 windows per pool (token-weighted text choice, modular wrap, lengths from
  `benchmarks/splits/v1`), V_U=368 union types asserted; four keys via
  `sumer_lib.make_key(368, seed)`; all four sha256(json.dumps(key)) verified against
  claim.yaml — exact match.
- Rank init: count desc, sign asc, full 368 permutation (zero-count types sort last).
- Objective: `sum_{cipher bigrams} F[u,v] · ln((RB[m_u,m_v]+α)/(RU[m_u]+α·368))`.
- Climb: **my own numpy-vectorized full-sweep steepest ascent** — I derived closed-form
  row/col delta matrices for all 368·367/2 pairs per sweep (first row-major max via
  masked argmax; accept iff Δ>1e-12; cap 2000). The delta algebra was self-tested
  against brute-force score recomputation on a random 11-type instance (worst |err|
  7.4e-14) before any real run. Deviation from shipped pure-Python (permitted, noted):
  different float summation order → report-only fields drift (see below); gated cells
  exact. Each climb 2–7 s; full grid ~90 s.
- Top-10 bar: `Counter.most_common(10)` of the 974 enciphered pool-B windows; hit iff
  mapped to the true plaintext type. Gate exactly as preregistered.

## Numbers: mine vs shipped (blind checker, then object)

Cell: texts 1456, pools 728/728, V_U=368, wrap_ref 0.0575 / wrap_cyp 0.0862 —
all identical to `object/results.json:cell` (wrap rates to 15 dp).

Dev rule (dev key, N_ref=500):

| α | 0.001 | 0.01 | 0.1 | 0.2 | 0.5 | 1.0 |
|---|---|---|---|---|---|---|
| shipped hits | 4 | 4 | 4 | 7 | 7 | 7 |
| **mine hits** | 4 | 4 | 4 | 7 | 7 | 7 |
| swaps (theirs/mine) | 248/258 | 247/248 | 230/232 | 240/243 | 252/243 | 240/240 |

α\* = **0.2** by the smallest-sufficient rule — identical. Rank-init-only (no climb)
dev cell: 3/10.

Gated grid at α\*=0.2 (top-10 hits — the gated metric):

| N_ref | committed | alt1 | alt2 |
|---|---|---|---|
| 100 | 2/2 | 2/2 | 2/2 |
| 250 | 4/4 | 8/8 | 4/4 |
| 500 | 6/6 | 5/5 | 4/4 |
| 974 | **7/7** | **7/7** | **7/7** |

(shipped = mine in all 12 cells; my rank-init-only baseline: 1/3/3/5 per key.)

Report-only fields: full-key accuracy mine vs theirs — committed 0.033/0.033,
0.052/0.049, 0.098/0.098, **0.106/0.114**; alt1 0.016/0.016, 0.092/0.092,
0.101/0.103, 0.117/0.120; alt2 0.011/0.011, 0.043/0.043, 0.109/0.109, 0.095/0.098
(≤3/368 apart, both directions — exactly the cross-implementation float tie-noise
L4-0003 already documented; gated cells unaffected). Swap counts within ±14
(theirs 112–295, mine 110–304), same phenomenon.

Gate: α\*=0.2 exists; committed@974=7/10; keys_ge7@974=3/3; N_min=974 → **PASS** in
my implementation, identical to shipped.

## Checker (blind)

Executed without reading source; ~40 min wall:

```
alpha*=0.2 N_min=974 committed@974=7/10 keys_ge7=3 recompute=match gate=PASS
PASS
EXIT=0
```

`baseline_snapshot/nmin.json` pins the four key shas (match my recomputation), V_U=368,
N_ref grid, α\*=0.2 — consistent.

## Prereg-chain audit (git)

- `909d6c0` (prereg, 2026-10-24 12:04:56 +0530) is the direct parent of `b0e50d2`
  (results, 12:48:20 +0530) — prereg strictly precedes results, ~43 min gap (much
  saner than L1-0001's 67 s).
- At prereg: `result: "TBD — pipeline not yet run at preregistration commit"`,
  `skeptics: []`. `README.md`, `object/`, `baseline_snapshot/` first appear in
  `b0e50d2`; `check.py`, `nmin_lib.py`, `run_l40004.py` are byte-unchanged between
  the two commits.
- `preregistered_threshold` line byte-identical across `909d6c0`, `b0e50d2`, and the
  worktree (sha256 `efb6b5e0…ea93`); `sign_scheme`, `key_commitment_sha256`,
  `corpus_snapshot_sha256` also identical. No other commits touch the claim.
- Same caveat as prior skeptic reports: generator/checker code existed at prereg time,
  so this verifies threshold-before-*results*, not threshold-before-*code*.

## Adversarial battery (trying to break a positive)

| # | Attack | Result | Verdict |
|---|---|---|---|
| a | Pool disjointness | pools are an index partition of one shuffled list (id-disjoint, 728/728); windows draw only from their own pool. BUT 6 content-identical texts straddle the boundary (119 tokens = 0.39%/0.41% of pool token mass; lengths 4–39); within-pool duplicate excess 9/6. Substring spot-check: 31/101 pool-A windows occur verbatim inside some pool-B text (46/108 reverse) — 4–5-token royal-formula windows are simply not pool-discriminative | disjoint at object level ✓; "share no underlying texts" is ~0.4%-mass false at content level (wording nit) |
| b | Shuffled-bigram reference (within-window permutation, N_ref=974, α\*=0.2; unigram marginals preserved exactly — asserted) | committed: 10 seeds → hits [7,5,4,5,7,3,8,5,4,3], mean 5.1, ≥7 in 3/10; alt1: 5,5 (0/2); alt2: 8 seeds → mean 4.5, ≥7 in 1/8; global token-shuffle ref: 5/10. Full-key accuracy under shuffled refs: mean 0.031 vs 0.095–0.117 real (3× separation). Per-shuffle co-occurrence of ≥7 across keys: max 1/3 — the prereg ≥2/3-keys conjunction passes on **0 of 10** structureless-reference draws | bigram structure IS load-bearing (not a pure unigram-marginal artifact), but the 7/10 bar alone is noisy: a single 7/10 reading is weak evidence — see objection 1 |
| c | α-grid peek-inheritance (sk3-B informed) | reasoned, not rerun — see objection 3 | disclosed; partially mitigated |
| d | alt1@250 = 8/10 stability | tie-break reversed (last row-major): 8/10; α ∈ {0.2−1e-9, 0.2, 0.2+1e-9, 0.19, 0.21}: 8/10 in all five. The non-monotonic dip (8@250 → 5@500) also reproduces at 5/10 under every perturbation | 8/10 is real per-key/N_ref variance, not fp tie-noise |
| d′ | Gate-cell stability | **all 12 gated cells identical** under reversed tie-break; committed@974, alt1@974, alt2@974, committed@500 all identical under α ±1e-9 and ±0.01 | gate cells rock solid |
| e | Top-10 boundary | cipher counts ranks 8–12: [97, 83, 82, 79, 78] — rank10 vs rank11 gap = **1 token** (1.2%), no tie at rank 10 (set deterministic; identical multiset across keys) | set is fixed by the prereg corpus, but the metric boundary is knife-edge — see objection 2 |
| f | Wording | `grep -rniE "deciphered|solved|translat|proof"` over the whole claim dir + TROPHY_CASE.md: **zero hits**. TROPHY_CASE.md has no L4-0004 entry (correct — awaits skeptics). README explicitly denies any Indus-reading implication | clean |
| g | Novelty | Jakobsen 1995 (Cryptologia, "A Fast Method for Cryptanalysis of Substitution Ciphers") is exactly this method family (frequency init + pairwise-swap hill-climb on bigram scores; searched 2026-10-24; practicalcryptography.com walkthrough; Bulatović et al. 2019 lineage) | calibration result, not method novelty — and the claim never says otherwise ("Jakobsen-style", "L4-0003's frozen hill-climb, α parameterized") |

## Gate checklist (planner §8 / skeptic-protocol)

- [x] Rebuilt from raw inputs, own code (numpy climb self-tested vs brute force, 7e-14)
- [x] Same sign scheme + snapshot hash (zip sha verified; V_U=368; key shas verified;
      wrap rates match object to 15 dp)
- [x] Threshold fixed before run (prereg parent-of-results, TBD at prereg, threshold
      byte-identical across commits; code-before-prereg caveat noted)
- [x] Null/calibration models attached (shuffled-bigram controls, dev-key rule, my own seeds)
- [x] DoF/multiplicity: α grid selected on dev key only; 3-key conjunction tested
      directly against structureless references (0/10 pass) rather than corrected
- [x] Novelty checked (Jakobsen 1995 lineage; logged above)
- [x] Wording matches what was shown (no overclaim; no trophy entry)
- [x] Checker green from scratch, run blind: `recompute=match gate=PASS`, exit 0

## Objections (non-blocking)

1. **The top-10 bar is only weakly separated from unigram-marginal signal.** Rank-init
   alone already scores 5/10 at N_ref=974, and structureless (shuffled-bigram)
   references reach 7/10 in 3/10 (committed) and 1/8 (alt2) of my control runs. The
   claim's evidential weight rests on the conjunctive structure — 3/3 keys at exactly
   7/10 with real bigrams vs 0/10 shuffles getting ≥2 keys — plus the collapse at
   N_ref≤250 and the 3× full-key separation. A single "7/10 recovered" reading at this
   scale should not be treated as strong evidence on its own; future gates at Indus
   scale should use full-key accuracy or a bar >7.
2. **Zero slack at the gate.** All three keys land at exactly 7/10 at 974 (never 8+),
   and the top-10 set boundary is one token (83 vs 82). N_min=974 means "reaches the
   bar at 974", not "clears it"; one boundary-type flip on a different corpus draw
   could push a key to 6. Stable to tie-order and α perturbation, but the pass has no
   margin to lose.
3. **α-grid peek-inheritance is real but partially self-neutralizing.** The grid
   {…,0.2,0.5,1.0} was chosen knowing sk3-B found α≥0.2 sufficient on the *old* cell,
   so α\*=0.2 is not a novel prediction (claim discloses this). Mitigation is genuine
   — dev/gated key separation, never-measured disjoint cell, smallest-sufficient rule —
   and the gate outcome is α-insensitive within the grid (dev 7/10 at 0.2, 0.5, and
   1.0), so the specific α\* value is not load-bearing for PASS. Residual: a grid blind
   to sk3-B might not have included 0.2 at all; the honest reading is "some α in
   [0.2,1.0] suffices", which the data supports.
4. **Content-level duplication across pools.** 6 texts (0.4% token mass) are
   byte-identical across the "disjoint" pools (royal-inscription duplicates), plus
   in-pool duplicates. "No shared texts" holds at the object/index level; wording
   should say so. Mass is too small to matter numerically.
5. **Genre leakage is disclosed but structural.** The substring spot-check shows short
   formulaic windows recur verbatim across pools; the cell measures same-genre
   disjoint recovery, not cross-genre. The shuffled-bigram control (objection 1) shows
   the pass is not *purely* marginal leakage, but genre redundancy is part of what
   makes 974 windows sufficient — the limitation list already says this.
6. Report-only fields (full-key accuracy ±3/368, swap counts ±14) are not
   cross-implementation portable — same float tie-noise L4-0003 documented; my numpy
   summation order differs from their pure Python. Gated cells: exact everywhere.
7. Method/checker code existed at the prereg commit (threshold-before-results, not
   before code) — repo-wide precedent, disclosed in earlier skeptic reports; unchanged
   here.

## Bottom line

Every gated number reproduces exactly from raw inputs under my own implementation
(dev 4/4/4/7/7/7 → α\*=0.2; committed 2/4/6/7, alt1 2/8/5/7, alt2 2/4/4/7; N_min=974;
3/3 keys at 974; PASS), the shipped checker runs green blind from the same zip, the
prereg chain is intact and byte-identical, and the adversarial battery breaks nothing
the gate depends on — the controls show the result needs real bigram structure and
would not pass the 3-key conjunction on structureless references. The honest
qualifications are thin margins (all keys at exactly 7/10) and a top-10 bar that is
noisy against unigram-marginal baselines by itself. **Reproduced.**
