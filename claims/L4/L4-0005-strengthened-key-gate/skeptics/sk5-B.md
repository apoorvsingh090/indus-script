verdict: reproduced

# sk5-B — L4-0005 audit (resumed-instance angle: adoption + spot-verification of interrupted scratch)

## HONESTY NOTE (read first)

This audit was **started by a prior instance of sk5-B** (same role, full
fresh-context rules) which wrote its own independent implementation
(`%TEMP%\sk5B\sk5b_build.py`, `sk5b_lib.py`, `sk5b_dev.py`), rebuilt the cell
from raw inputs, ran the full 18-climb dev sweep
(`dev_run.log`, `my_dev_results.json`), read the claim/protocol documents
(its `c_prereg.yaml`/`c_results.yaml` snapshots are byte-identical to the
`git show` versions of `claim.yaml` at 4cc930c / 50faf81 — verified by me),
and was then **killed by an infrastructure error before finishing**. I am the
resumed instance. I **adopted that scratch and spot-verified it** rather than
redoing all 18 climbs: reran 2 full dev cells (α=0.2 and α=1.0, all 3 starts,
6 climbs) with the scratch code — **all 12 start-level values matched to
1e-6 in S** (plus swaps, hits, init-hits, full372, full_present) **and both
S_true values matched** — and independently re-verified the cell identity
(zip sha256; all four committed key SHAs under `json.dumps` serialization,
each a valid permutation of 0..371; V=372; wrap rates to 1e-6). Everything
else in this report I performed myself in full: spot-check (6 climbs),
report-only probes (15 climbs), blind checker run, git prereg audit, wording
grep, object comparison.

Independence disclosure: the prior instance's build imports `sumer_lib` from
**L4-0002's** how-we-built-it (the input-pipeline definition the prereg
references), disclosed in its docstring; all *method* code (objective,
climb, starts, scoring) is independent of this claim's implementation. Read
set across both instances: L4-0005 `claim.yaml` + `README.md`,
`planner.md` §8, `agents/skeptic-protocol.md`, L4-0002 `claim.yaml` +
`sumer_lib.py` (input pipeline only), L4-0003/L4-0004 `claim.yaml` +
`README.md` (grep-level), L4-0002's `skeptics/skS-B.md` (style calibration
only, after my analysis was complete), `object/*` and
`baseline_snapshot/*` (opened only after the blind checker finished).
**Never opened:** this claim's `how-we-built-it/*`, `check.py` source
(executed unread), `skeptics/sk5-A.md`, `%TEMP%\sk5A`.

## Environment

- Windows 10 (26200), Python 3.12.10, numpy (vectorized deltas), 8 cores.
- Raw input: `etcsri.zip` (13,197,377 B) staged at
  `%TEMP%\l4preflight\etcsri.zip`, sha256
  `66991601df193a5cb93bccf92e9051e86a98fbb668a9dd343477d14f0c9d54d6` —
  verified twice (prior instance at build; byte-hash re-verified by me).
- Scratch outside the repo: `C:\Users\Apoorv\AppData\Local\Temp\sk5B\`.

## Implementation (own code, prior instance's + my spot-verification)

- **Cell rebuild from raw inputs**: 1456 nonempty texts via `sumer_lib`;
  pools `Random(260417835+7000)` shuffle → A=728 / B=728; 974 windows each
  (seeds +7100/+7200, splits/v1 lengths); **V_U5=372**; four keys
  `make_key(372, seed)` — all four committed SHAs in `claim.yaml` reproduce
  under the `json.dumps` convention. Tokens A=4524 / B=4400; types 285/317,
  shared 230.
- **Method per prereg text only**: objective = bigram LL
  `ln (RB+a)/(RU+a·372)` + positional LL `ln (RP[p,cls]+a)/(RU[p]+3a)`,
  cls = begin/middle/end, len-1 = begin only; steepest-ascent pairwise
  swaps, full sweep, first row-major max, accept iff Δ>1e-12, cap 2000;
  best-of-3 (rank-init count-desc/sign-asc; `Random(42000001)`;
  `Random(42000002)`), best exact recomputed total, ties→earlier start;
  hits via `Counter.most_common(10)` over the cipher token stream.
- **Self-verification**: every accepted swap's vectorized delta asserted
  against a brute-force `total_S` recomputation (+3 random pairs per sweep)
  — zero failures across all 39 climbs in this audit. My spot rerun of the
  α=0.5/start-1 cell that the prior log timed at 12,663.8 s completed in
  ~5 s — that logged outlier is a machine-sleep artifact, not compute.

## My numbers vs shipped (`object/results.json`)

| α | hits (mine) | hits (shipped) | full mine | full shipped | winner start |
|---|---|---|---|---|---|
| 0.001 | 2 | 2 | 10/372 | 12/372 | 0 = 0 |
| 0.01 | 3 | 3 | 15/372 | 15/372 | 0 = 0 |
| 0.1 | 4 | 4 | 35/372 | 35/372 | 0 = 0 |
| 0.2 | 4 | 4 | 36/372 | 37/372 | 0 = 0 |
| 0.5 | 4 | 4 | 30/372 | 31/372 | 0 = 0 |
| 1.0 | 4 | 4 | 39/372 | 40/372 | 0 = 0 |

- **Gating statistics reproduce exactly**: hits 2/3/4/4/4/4, winner =
  rank-init start 0 at every α, **α\*=None** — the filed negative.
- **Full-key (report-only) differs by ≤2/372 on 4 of 6 α** (mine lower by
  2/1/1/1; identical on 0.01, 0.1). This is the float-tie terminal-permutation
  divergence across a third implementation that L4-0003 already disclosed
  ("report-only fields not cross-implementation portable; gated cells
  stable"); no gate consumes `full` here (the gate died at condition (a)).
  The README's "best full-key 0.108 at α=1.0" = 40/372 = 0.1075 — consistent
  with the shipped object; my 39/372 = 0.105 is the same one-item gap.
- Cell identity: wrap rates 0.090349/0.067762 identical to 1e-6; V=372.

## Blind checker

Shipped `check.py` **executed unread** (args from the audit brief; source
never opened), scratch outside repo, ~50 min wall:

```
alpha*=None committed=-/10 full=- null_max=- recompute=match gate=FAIL
PASS
EXIT_CODE=0
```

Exactly the disclosed convention: exit 0 = the negative reproduces
(`recompute=match`), the `gate=FAIL` line carries the outcome. Consistent
with the shipped object (gated arms never ran, hence `-` placeholders) and
with `baseline_snapshot/gate5.json` (same four key SHAs I verified;
`v_union: 372`; `alpha_star: null`).

## Git prereg audit

- `4cc930c` (2026-10-24T21:43:29+05:30) — prereg; `result:` is
  *"TBD — pipeline not yet run at preregistration commit"*; claim dir
  contains only `claim.yaml`, `check.py`, `how-we-built-it/` (no object,
  no baseline, no README).
- `50faf81` (2026-10-24T22:53:46+05:30) — results; adds README,
  `object/results.json`, `baseline_snapshot/gate5.json`; exactly **1 commit
  later**; `4cc930c` **is an ancestor** of `50faf81`.
- `preregistered_threshold` **byte-identical** (1794 chars) across 4cc930c,
  50faf81, and the working tree; `key_commitment_sha256`,
  `corpus_snapshot_sha256`, `sign_scheme` also unchanged.
- `check.py` and `how-we-built-it/` unchanged between the two commits;
  working tree clean vs 50faf81 (only untracked `skeptics/`).

## Report-only probes (own scripts, reuse of my verified climber)

**(a) Position-resolved positional variant** — dev key, N_ref=500,
**rank-init single start only** (caveat: random starts were strictly worse
at every prereg cell, so best-of-3 would not plausibly raise these):

| conditioning | α=0.2 | α=0.5 | α=1.0 |
|---|---|---|---|
| (cls, len-band), K=15 | 4/10 (full 34) | 4/10 (full 42) | 4/10 (full 44) |
| normalized-position bins, K=8 | 3/10 (full 26) | **6/10** (full 43) | 4/10 (full 39) |

The 7/10 bar does **not** clear under either stronger reading; 6/10 at
npos/α=0.5 is the closest any reading gets. Supports the claim's reading
(3): positional structure was not the binding constraint — though 6/10
says the bar is *near*-reachable, not far (objection 3).

**(b) Full-reference boundary probe** — dev key, **N_ref=974** (all pool-A
windows), all 3 starts: winner start 0 at every α; hits **5/10** at 0.2
(full 24), 5/10 at 0.5 (full 30), 5/10 at 1.0 (full 19). Max 5/10 is far
below the 8/10 gate bar and still below the 7/10 dev bar — **doubling the
reference does not rescue this cell**. Contrast: on the *old* cell the
full-corpus reference rescued the frozen climb to 10/10 (L4-0003 skeptic
finding); on this fresh cell it does not, which *strengthens* the
boundary-draw reading (1) in the filed result.

**(c) S_true − S_best carry (over-smoothing check)** — positive at every
prereg α at N_ref=500 (+209, +1011, +279, +297, +328, +265 nats for
0.001→1.0) and at N_ref=974 (+970, +851, +760 for 0.2/0.5/1.0): the true
key always outscores every permutation the search finds. The frozen
objective never prefers the recovered solution over the truth — the
negative is a search/data-size failure, not the objective ranking truth
below a competitor. (This does not certify the truth as global optimum,
only that the climb never surpasses it.)

## Protocol checklist

- [x] Rebuilt from raw inputs, independently written method code (interruption
      + adoption + spot-verification disclosed above)
- [x] Same sign-coding scheme and snapshot hash (zip sha256; V=372; wrap 1e-6)
- [x] Threshold and split fixed before the run (git audit; result TBD at prereg)
- [x] Nulls/calibration: gate failed at (a) so no null arm ran; baseline pins
      key SHAs + α\*=null — appropriate for the filed negative
- [x] DoF/multiple comparisons: α-grid with smallest-α rule preregistered;
      dev key separate from gate keys; uniform fail needs no correction
- [x] Novelty: method family is standard and the repo says so (L4-0003
      README: "Jakobsen-1995-style"); lineage Jakobsen 1995 (*Cryptologia*
      19(3):265–274, bigram hill-climb substitution cryptanalysis) and
      Knight & Yamada 1999 ("A Computational Approach to Deciphering
      Unknown Scripts", ACL W99-0906). L4-0005 claims a calibration
      negative, not method novelty — no overreach. Searched: repo greps
      (Jakobsen/Knight/cryptanalys/hill-climb over claims/), web check of
      the two citations, wording grep over claim/README/TROPHY_CASE.
- [x] Wording: no `deciphered|solved|translat|proof` hits; the only grep
      match is "re**solved** the question in the negative direction"
      (benign); L4-0005 absent from TROPHY_CASE.md (correct for a draft
      negative awaiting skeptics)
- [x] Checker runs green from scratch (blind run above, exit 0 as disclosed)

## Objections (non-blocking)

1. **Report-only `full` is not cross-implementation portable** (−1..−2/372
   on 4/6 α in a third implementation; gated stats exact). The object
   should carry the L4-0003-style caveat label on `full`.
2. **9 duplicate-content texts straddle the pools** (index-level
   disjointness is definitional — pools split a shuffled text list; the
   royal-inscription corpus is formulaic). ~1% of texts; immaterial to the
   failure direction, but worth a line in limitations.
3. **npos@α=0.5 = 6/10** (single-start) shows the 7/10 dev bar is
   near-reachable under a normalized-position positional term; the claim's
   "positional augmentation did not rescue" is accurate for the frozen
   3-class term and for (cls,len-band), but a preregistered npos variant is
   the obvious next probe — the boundary is close, which the README's
   "at-or-beyond the feasibility boundary" phrasing already honors.
4. Checker ergonomics: ~50 min for 18 climbs a vectorized equivalent does
   in ~35 s (my whole 18-climb sweep ≈ 2 min of compute). No correctness
   objection; blind-run discipline just costs wall-clock.
5. Cosmetic: "best full-key 0.108" rounds 0.1075 up.

## Bottom line

The CONFIRMED NEGATIVE **reproduces**. An independent implementation
(prior instance's code, spot-verified by me to 1e-6 on 2 of 6 dev cells)
gives the identical gated table — hits 2/3/4/4/4/4, best-of-3 always the
rank-init start, α\*=None, strengthened gate fails at condition (a) — on a
cell whose identity (zip sha, four key SHAs, V=372, wrap rates) I verified
independently. The blind checker returns `recompute=match gate=FAIL` with
exit 0 under the disclosed convention; the prereg commit provably precedes
the results commit with a byte-identical threshold; wording is clean. My
probes strengthen the negative rather than softening it: full reference
still tops out at 5/10 (the old cell's reference-scope rescue does not
transfer), and the true key outscores every recovered permutation at every
setting (search/data-size failure, not objective misranking). Caveats are
confined to report-only fields (±2/372 float-tie portability) and the
near-reachability of the dev bar under a normalized-position variant
(6/10, single-start), both documented above.
