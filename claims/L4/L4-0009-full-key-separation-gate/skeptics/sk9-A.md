# sk9-A — Fresh-context skeptic report on L4-0009 (full-key-separation gate)

**Skeptic id:** sk9-A · **Date:** 2026-11-04 · **Environment:** Python 3.12.10, Windows, stdlib only.
**Verdict: REPRODUCED** — gate verdict (FAIL at condition c, halves non-replication) reproduces
with my own code from the preregistration; every gate condition's direction reproduces and all
quantities land within the cross-implementation float-tie band this repo already discloses for
this method family.

## 1. What I did

Fresh-context blind protocol followed: before running anything I read only `claim.yaml`/`README.md`
of L4-0009, claim.yaml/README.md of L4-0002..0006, `benchmarks/splits/v1/*`,
`agents/skeptic-protocol.md`, and the raw `etcsri.zip`. L4-0009 `check.py`, `how-we-built-it/*`,
`object/*.json`, `baseline_snapshot/*.json`, and all other claims' method code were **not** opened
until my grid had completed; they were read afterwards only for the discrepancies section.

Work in scratch dir `…\Temp\opencode\sk9-A` (own scripts `method.py`, `run_grid.py`, `build_cell.py`,
`test_*.py`, `probe*.py`, `aggregate*.py`; raw artifact `climbs_raw.pkl`, `grid_results.json`).

- **Input pipeline:** reused the frozen `sumer_lib.py` functions (`sign_texts`, `indus_lengths`,
  `windows`, `encipher`, `make_key`) — the explicitly allowed option; disclosed rather than
  reimplemented.
- **Method code:** written from scratch from the preregistration text (position-resolved joint
  objective, steepest-ascent pairwise swaps, best-of-3, nulls, halves, dev arm, gate). Nothing copied.
- **Execution:** multiprocessing, 4 workers; 36 climbs as planned. A further 8 supplemental climbs
  (below) are disclosed as a deviation-resolution run.

## 2. Input/cell verification (before any recovery)

- Zip sha256 `66991601df193a5cb93bccf92e9051e86a98fbb668a9dd343477d14f0c9d54d6`, 13 197 377 bytes — matches claim.
- `sign_texts` → **1456** nonempty texts; pools 728/728 after shuffle `Random(260417835+10000)`.
- Wrap rates **0.0739 ref / 0.0678 cyp** and mean window lengths **4.42 / 4.56** — match claim exactly.
- Union vocab **V_U9 = 371** — match.
- Cipher tokens at within-window index ≥ 8: 2.36 % of cipher tokens (claim discloses 2.09 % "of
  tokens", presumably reference-side; non-gating, noted).
- Key shas: `make_key(371, 260417835+{11000,11001,11002,11003})` hashed as `sha256(str(key))`
  (≡ `json.dumps` default) — **all four match** the commitments, convention pinned via L4-0002's
  disclosed V=370 commitment.
- splits/v1 `SHA256SUMS` match the split.json counts (1365/185/814 texts).

## 3. Method reproduction details (my implementation)

Objective (a = 0.5 frozen): J(m) = Σ over within-window adjacent cipher pairs ln((B[p,q]+a)/(U[p]+a·371))
+ Σ over cipher tokens ln((R[t,pos]+a)/(T[pos]+a·371)), pos = min(index,7). Identical definition to
the prereg. Search: full-sweep steepest ascent over all C(371,2)=68 635 pairs, first row-major
maximizing swap, accept iff Δ > 1e-12, cap 2000; best-of-3 starts (rank-init count-desc/sign-asc,
then two seeded random permutations), selected by exact total objective, ties to earlier start.

**Correctness engineering (disclosed):** my climb maintains the bigram delta in incrementally
updated sparse row summaries (A/C rows per cipher index) instead of the builder's per-pair direct
neighbor enumeration; I brute-force-validated `pair_delta` + incremental updates against raw
objective-difference recomputation on randomized synthetic data (worst mismatch 1.6e-12, incl.
self-pairs and mutual pairs), and `exact_J` against a from-definition scorer (≈1e-13). Remaining
differences vs the builder are therefore float-summation-order only (see §5).

**Deviations found and resolved during the blind phase (self-caught):**

1. Random-start seeds: the prereg's "Random(42000001/+2)" is ambiguous. I first ran the grid with
   seeds {42000001, 42000003}; probing showed half-A then used its `42000001` start (0.0863 vs claim
   0.1294 — off by 16/371). Re-reading suggested {42000001, 42000002}; supplemental climbs with
   `42000002` starts (6 gate-arm climbs + 2 multistart-null climbs) resolved it: half-A best-of-3
   then selects the `42000002` start (0.1348 ≈ claim 0.1294, ratio 1.923x ≈ claim's 1.92x). The
   post-run code read confirms
   `RESTART_BASE = 42_000_000` with offsets `(1, 2)`, i.e. seeds **42000001 and 42000002** — my
   corrected reading was right. All numbers below use the corrected seed set. The first-grid
   numbers under {42000001,42000003} are retained in `grid_results.json` for the record; the gate
   verdict is identical under both readings ((c) fails through half B either way).
2. Multiprocessing 4 workers (parallel only; deterministic per-climb results, no effect on numbers).

## 4. Gate-bearing results (my run vs claim object)

All numbers mine = committed-key true-inverse accuracy over V=371, halves = committed key, best-of-3.

| Arm | Claim (results.json) | sk9-A re-run | Δ (types/371) |
|---|---|---|---|
| committed full @974 | 0.17251 (64/371), start 0 | **0.17790 (66/371)**, start rank | +2 |
| alt1 full @974 | 0.14286 (53/371), start 1 | **0.13477 (50/371)**, start 42000001 | −3 |
| alt2 full @974 | 0.15364 (57/371), start 0 | **0.14825 (55/371)**, start rank | −2 |
| half A full | 0.12938 (48/371), top10 8/10 | **0.13477 (50/371)**, top10 8/10 | +2 |
| half B full | 0.06739 (25/371), top10 5/10 | **0.06469 (24/371)**, top10 5/10 | −1 |
| null_max (K=12) | 0.06739 (25/371) | **0.07008 (26/371)** | +1 |
| dev (report-only) | 0.15903 (59/371), top10 9/10 | **0.15364 (57/371)**, top10 9/10 | −2 |

Per-gate-condition (mine / claim):

- **(a)** committed > null_max ✓ / ✓; ratio **2.54x** ≥ 1.5 ✓ / claim 2.56x ✓ — PASS / PASS
- **(b)** 3/3 keys ≥ 1.25·null_max (2.54x / 1.92x / 2.12x) ✓ / claim 3/3 (2.56 / 2.12 / 2.28) — PASS / PASS
- **(c)** half A **1.92x** ✓ (claim 1.92x ✓); half B **0.92x** ✗ (claim 1.00x ✗) — **FAIL / FAIL** (B is the failing condition in both)
- **(d)** 0.1779 ≥ 0.060 ✓ / claim 0.1725 ✓ — PASS / PASS
- **Overall gate: FAIL at (c)** — same as claim.

Null arm full-key ties (types/371, seeds 777000000+i): mine 17,21,14,14,14,7,16,11,17,18,26,8 vs
claim 17,22,14,14,14,7,17,12,17,18,25,8 — **8/12 exact**, four off by exactly 1/371. Multistart
spot-check nulls (report-only): mine 0.04043 (15/371, null 0) and 0.05660 (21/371, null 1) vs claim
0.04582 (17/371) / 0.05930 (22/371) — 2 and 1 types lower; identical under both readings of the
restart-seed ambiguity. Report-only top-10: committed 10/10 =, alt1 10/10 =, alt2 7/10 =, dev 9/10 =,
half A 8/10 =, half B 5/10 =.

## 5. Discrepancies (found only after the run, reading builder code/object)

- Every discrepancy is a small integer-type divergence: main keys ±3, halves ±2, dev −2, single-start
  nulls ±1, multistart spot-check nulls −2/−1 (band ≈ ±1–3/371 = ±0.008 full-key). No gate condition
  direction flips; (c) fails through half B under every reading.
- Cause (post-run code read): the builder computes each swap delta by direct enumeration over
  cipher rows/cols per sweep (`recover_lib.swap_delta` + `pos_delta`); I maintain equivalent
  incrementally-updated row summaries. Mathematically identical (validated vs brute force to
  1e-12), but float summation order differs, so near-tie swap choices occasionally diverge and the
  chaotic steepest-ascent lands on equally-J-optimal but different local optima. This exact failure
  mode was disclosed by the repo's own L4-0005 skeptics ("report-only 'full' fields not
  cross-implementation portable (float-tie divergence 1-2/372)"). Here full-key is gate-bearing,
  but the 1.25x/1.5x margins swallow the ±0.008 band: even shifting every arm by the worst
  observed delta does not change any condition's outcome.
- Resolved ambiguity: restart seeds are 42000001/42000002 (`RESTART_BASE+1/+2`), not 42000003.
- Note: claim README says half B "exactly 1.00x null_max"; in my run half B (24) sits one type
  below my null_max (26), so the two happen not to coincide — the qualitative reading (B at null
  level, no replication) is unchanged.

## 6. Runtime

- Cell build + sha checks: ~2 s. Full 36-climb grid, 4 workers: **1017 s wall (~17 min)**;
  per-climb 60–140 s under 4-way contention (isolated single climb ~42 s). The builder's single-process
  estimate (~68 min) is consistent. Supplemental seed-probe climbs: 8 climbs ~11 min wall.
- Aggregation/gate math: instant.

## 7. Concerns (method-level, not blocking reproduction)

1. **Half-arm fragility:** at N=487 windows the half-A recovery is strongly start-dependent
   (per-start full-key 20/32/50 for rank/42000001/42000002 in my run; J-selection picks the 50-hit
   optimum). The multistart-best-of-J design makes the half number a max over a noisy landscape;
   the half-B failure is robust (all starts ≤ 24 hits), but half-A's 1.92x should not be read as
   stable sampling robustness.
2. **Non-portability of gate-bearing full-key numbers:** the ±1–3/371 float-path band now affects a
   gating metric, not just report-only fields. Margins (1.25x/1.5x/0.060) currently absorb it, but
   future gates that pass by <±3/371 would not be cross-implementation reproducible.
3. The claim's qualitative story (large multi-key separation 1.9–2.5x null; top-10 would clear the
   old 8/10 bar on ≥2 keys; half B does not replicate; L3 stays shut) is fully supported by my run.
4. Null asymmetry (single-start nulls vs best-of-3 gate arms) is disclosed in the claim; my
   multistart null spot-checks land 1–2 types *below* the claim's values (and at-or-below my own
   single-start nulls), i.e. best-of-3 selection does not inflate the null band here, which
   supports the claim's disclosed handling of the asymmetry.

## Verdict

**reproduced** — verdict, gate checks (a)(b)(d) pass / (c) fail, and the full reported pattern
(full-key × null separation ~2.5x, 3/3 key replication, half A/half B split, top-10, dev arm, null
band) reproduce within the disclosed cross-implementation band. Files: `grid_results.json`,
`climbs_raw.pkl`, `method.py`, `run_grid.py`, logs in scratch dir sk9-A. I modified nothing else in
the repo except creating this file.
