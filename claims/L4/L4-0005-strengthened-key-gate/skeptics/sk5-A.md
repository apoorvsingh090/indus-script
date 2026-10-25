verdict: reproduced

# sk5-A — skeptic report on L4-0005 (strengthened key gate, fresh cell, CONFIRMED NEGATIVE)

Skeptic id: sk5-A. Date: 2026-10-24. Repo at commit `50faf81` (main, unmodified; nothing
committed by me). Blind-audit discipline maintained per instructions (disclosure below).

## 1. Verdict

**reproduced** — the filed negative is real and reproducible *under the frozen
implementation*, the prereg chain is clean, and the shipped checker runs green blind
(exit 0, disclosed negative-exit convention). **But the headline is
implementation-conditional in an important way** (Qualification Q1): the preregistered
"positional LL" formula `ln P_ref(cls|p) = (ref_pos[p][cls]+a)/(ref_unigram[p]+3a)` is
ambiguous, and the frozen code realizes the weakest non-vacuous reading —
`P(cls | plaintext TYPE)` (begin/middle/end class-marginal, NO position conditioning;
`how-we-built-it/l40005_lib.py::ref_pos_logp`). Under that reading the term is nearly
inert (my bigram-only control reproduces the shipped table in band). Under equally
defensible **position-resolved** readings of the same formula, the dev bar is CLEARED
(alpha*=0.5, or 0.1 for a class-pooled variant) — i.e. gate condition (a) does not fail,
readings (2) "random restarts do not help" and (3) "positional augmentation did not
rescue" are falsified, and the negative would have to be carried (if at all) by the
N_ref=974 arms, which my probes suggest still fail (5–6/10 vs the 8/10 bar). The
*overall* conclusion (this cell does not clear the full strengthened gate) very likely
survives; the *filed mechanism* (failure at condition (a), "no alpha reaches 7/10") is a
property of the frozen weak reading, not of the method family.

## 2. Independence disclosure (what was opened, when)

Phase 1 (before any code was written) — allowed inputs only:
`claims/L4/L4-0005-strengthened-key-gate/claim.yaml`, `.../README.md`,
`planner.md` §8, `agents/skeptic-protocol.md`, plus input definitions
`L4-0002/claim.yaml`, `L4-0002/how-we-built-it/sumer_lib.py` (allowed import),
`L4-0003/claim.yaml`, `L4-0004/claim.yaml`.

Phase 2 (my own numbers computed FIRST; nothing forbidden opened before them):
my implementation + all my runs (18-climb dev sweep, adversarial battery, follow-ups)
completed in `C:\Users\Apoorv\AppData\Local\Temp\sk5A\` — logs `step2_devsweep.log`,
`step3_adversarial.log`, `step4_followups.log`.

Phase 3 (only after my numbers existed): ran the shipped checker BLIND
(`checker_blind.log`, ~48 min), then opened `check.py` source,
`object/results.json`, `baseline_snapshot/gate5.json`,
`how-we-built-it/l40005_lib.py`, and — to complete the implementation comparison —
`L4-0003/how-we-built-it/recover_lib.py` (imported by the shipped lib; opened
post-numbers, disclosed). `how-we-built-it/run_l40005.py` not needed (checker exercises
the same frozen functions). Other skeptics' work not read; `skeptics/` did not exist
when I started writing.

## 3. Environment

Windows 10 (10.0.26200), Git Bash, Python 3.12.10, **numpy 2.4.6 (disclosed — dense
372x372 float64 swap-delta matrices; the spec allows numpy with note)**. ETCSRI zip
pre-staged at `%TEMP%\l4preflight\etcsri.zip`, sha256
`66991601df193a5cb93bccf92e9051e86a98fbb668a9dd343477d14f0c9d54d6` — matches
claim.yaml. Scratch: `%TEMP%\sk5A`. ORACC/ETCSRI CC0-per-file; attributed, not vendored.

## 4. My implementation (from claim.yaml:preregistered_threshold only)

- Cell: `sign_texts` -> shuffle `Random(260417835+7000)` -> pool A = first 728 / pool B =
  728; 974 windows each, seeds `+7100` (A) / `+7200` (B) (assignment forced by V_U5=372,
  see §6-d), `splits/v1` lengths; union vocab **V_U5=372 asserted**; keys
  `make_key(372, 260417835{,+9000,+9001,+9002})`, sha256(json.dumps(key)) all four match
  claim.yaml.
- Objective (my reading of the ambiguous positional formula — position-resolved):
  bigram LL `ln P_ref(q|p)=(ref_bigram+a)/(ref_ctx+a*372)` over within-window adjacent
  cipher pairs + positional LL `ln P_ref(t | pos, cls) = (ref_pos[(pos,cls)][t]+a)/(ref_tok[pos]+3a)`,
  cls per the L1-0002b convention (pos 0 begin; last pos end when L>1; L==1 begin-only).
  Variants run: positional OFF (bigram-only); class-pooled positional
  `ln P(t|pos)` with the same `(tot+3a)` denominator.
- Search: steepest-ascent pairwise swaps, full sweep, **first row-major max**
  (np.argmax over the upper triangle in C-order = first max), accept iff delta>1e-12,
  cap 2000; swap delta via maintained OUT/IN/POS matrices with an internal-pair
  correction term Gamma — **validated against brute-force objective recomputation on 30
  random swaps (worst |err| 8.1e-12)**; every climb additionally verified a true local
  optimum by fresh rebuild (max residual delta <= 5.7e-14).
- Multi-start: rank-init (count desc, sign asc both sides) + `Random(42000001/42000002)`
  shuffles of identity; best exact total objective, ties to earlier start. (Convention
  later confirmed identical to shipped `l40005_lib.starts`.)
- Dev rule: smallest alpha in grid with >=7/10 top-10 (`Counter.most_common(10)`) on the
  dev key, cipher = all 974 pool-B windows, reference = FIRST 500 pool-A windows.

## 5. My numbers vs shipped (dev cell, N_ref=500, dev key, best-of-3)

| alpha | shipped hits (start) [full] | mine: position-resolved joint (per-start -> best) [full] | mine: class-pooled positional | mine: bigram-only [full] |
|---|---|---|---|---|
| 0.001 | 2 (s0) [0.032] | 3/1/1 -> 3 (s0) [0.046] | 3 [0.054] | 2 [0.030] |
| 0.01  | 3 (s0) [0.040] | 5/1/1 -> 5 (s0) [0.046] | 4 [0.081] | 3 [0.054] |
| 0.1   | 4 (s0) [0.094] | 6/1/2 -> 6 (s0) [0.108] | **8** [0.143] | 5 [0.097] |
| 0.2   | 4 (s0) [0.099] | 6/1/2 -> 6 (s0) [0.105] | **8** [0.145] | 4 [0.089] |
| 0.5   | 4 (s0) [0.083] | **8**/2/1 -> **8 (s0)** [0.145] | 6 [0.108] | 4 [0.094] |
| 1.0   | 4 (s0) [0.108] | 4/2/**10** -> **10 (s2)** [0.153] | 4 [0.118] | 4 [0.094] |
| alpha\* | **None** | **0.5** | **0.1** | **None** |

- Shipped row 2/3/4/4/4/4, alpha\*=None: reproduced in band by my bigram-only control
  (2/3/5/4/4/4; the 0.1-cell off by one — see Q5 on the bigram-denominator convention,
  plus the known fp tie-noise band from L4-0003/0004 precedents). My full-keys land in
  the shipped band at every alpha under the bigram-only and class-marginal-equivalent
  readings. This is consistent with the shipped positional term being nearly inert.
- Under position-resolved readings the table is materially higher and CLEARS the 7/10
  dev bar at alpha 0.1–0.5; at alpha=1.0 the **random restart (start 2) wins with the
  strictly best exact objective** (-36944.5 vs rank-init -37280.6) and 10/10 top-10,
  full-key 0.153 — contradicting shipped reading (2) under the stronger objective.

## 6. Adversarial battery (attack toward false negative)

| # | Probe | Result |
|---|---|---|
| a | Positional term OFF (bigram-only), full grid at N_ref=500 | 2/3/5/4/4/4, alpha\*=None; shuffles 0/10 everywhere; matches shipped table in band -> the shipped "joint" objective behaves like bigram-only; **inverse of the usual failure direction**: here the positional term (properly resolved) is what rescues, so the negative is conditional on the weak reading (Q1) |
| b | True-key vs recovered objective | a=0.2: true beats recovered under both objectives (joint -38026.1 vs -38314.6) — objective sane. **Flag**: at a=0.5 and a=1.0 (joint) the RECOVERED mapping exceeds the true key's objective (-37343.3 vs -37564.3; -36944.5 vs -37147.6) — over-smoothing moves the optimum past truth; a known hill-climb property (cf. practicalcryptography note that garbled keys can outscore true plaintext). Does not affect the a=0.2 sanity pass or the alpha\*=0.5 existence claim, but the 10/10@1.0 cell should not be read as "objective anchored on truth" |
| c | Multi-start selection audit | my best-of-3 uses exact direct recomputation of the total objective; at a=1.0 start 2 wins strictly (no tie), elsewhere start 0 wins; selection machinery verified correct on my side and shipped convention confirmed identical (same seeds, same shuffle-of-identity, same ties-to-earlier) |
| d | Cell sanity | V_U5=372 exact; all four key shas match; wrap rates 0.0903/0.0678 — byte-match object/results.json; pools disjoint as objects (8 duplicate-content text groups straddle the boundary, same disclosed phenomenon as L4-0004's 6); **seed-assignment forced**: swapping window seeds (+7200/+7100) yields V_U5=373 != 372, so my assignment is the only one consistent with the prereg |
| e | Boundary probe: dev key at FULL N_ref=974 (report-only) | joint position-resolved: a=0.2 best 5/10; a=0.5 best 6/10 (per-start 5/3/6); a=1.0 best-by-score 5/10 (start 1 had 7/10 but lower objective). No alpha reaches 8/10 at 974 -> even under the strong reading, gate arm (b) would very likely still fail; the failure is NOT reference-size-driven (500->974 does not rescue under any reading) |
| f | Wording grep `-iE "deciphered|solved|translat|proof"` | sole hit "re**solved** the question in the negative direction" (README) — no overstatement; "no reading claim" discipline maintained |
| g | Novelty | Hill-climb substitution cryptanalysis is classic (Jakobsen 1995; Knight & Yamada 1999 computational-decipherment framing); the claim asserts no method novelty — its contribution is the preregistered fresh-cell feasibility measurement, which is the repo's own design. Negative direction consistent with the Indus short-text literature (unicity-distance arguments; Yadav et al. 2009 n-gram study). Searches logged 2026-10-24 |

## 7. Checker (blind) and prereg audit

- Blind checker (my numbers already fixed): `python check.py --splits benchmarks/splits/v1
  --scratch %TEMP%/l4preflight --object object/results.json --baseline
  baseline_snapshot/gate5.json` -> `alpha*=None committed=-/10 full=- null_max=-
  recompute=match gate=FAIL` / `PASS`, **exit 0** (~48 min) — the disclosed
  negative-exit convention holds: exit 0 means the negative reproduces.
- Observation (non-blocking): at alpha\*=None the checker compares only the recomputed
  alpha\* against the shipped alpha\* (check.py short-circuits `same=True`); the 18
  individual dev cells in object/results.json are not separately asserted. My
  independent per-cell band (§5) supplies that cross-implementation layer.
- Git: `4cc930c` (prereg, 2026-10-24 21:43:29 +0530, result "TBD") precedes `50faf81`
  (results, 22:53:46 +0530); `preregistered_threshold` **byte-identical** across
  4cc930c, 50faf81, and the working tree (sha of the field: a8ee8bf9dbb151fd);
  `how-we-built-it/l40005_lib.py` and `check.py` **unchanged since the prereg commit**
  (the weak positional reading was frozen BEFORE any result — no post-hoc weakening).
  Baseline pins all four key shas + V_U5=372.

## 8. Protocol checklist

- [x] Rebuilt from raw inputs (staged zip, sha-verified) in a clean context with
      independently written code (numpy implementation, delta brute-force validated)
- [x] Same sign-coding scheme and corpus snapshot hash
- [x] Threshold and split fixed before the run (prereg chain verified; byte-identical)
- [x] Null models: N/A by the frozen rule (gate failed at (a) before nulls run); my
      974-probes and bigram-only control serve as calibration context
- [x] Degrees of freedom: 18 dev climbs, smallest-alpha rule, dev/gate key separation;
      no multiple-comparison issue beyond the preregistered grid
- [x] Novelty checked (searches logged, §6g)
- [x] Claim wording matches what was shown, EXCEPT readings (2)/(3) over-generalize
      (Q1–Q3 below)
- [x] Checker runs green from scratch (blind, exit 0 per disclosed convention)

## 9. Objections (non-blocking; recommend folding in)

- **Q1 (main): the dev-cell failure is reading-conditional.** The prereg formula
  `P_ref(cls|p)` admits (i) the literal `P(cls|position)` — mapping-independent, i.e. a
  no-op; (ii) the shipped `P(cls|plaintext type)` — class-marginal, nearly inert (my
  bigram-only reproduces the shipped table); (iii) `P(type|position,cls)` and
  `P(type|position)` — position-resolved, genuinely "positional": these CLEAR the dev
  bar (alpha\*=0.5 / 0.1, 8/10–10/10, full-key up to 0.153). "No alpha reaches the 7/10
  dev bar" is therefore a property of reading (ii), not of the preregistered method
  family. The claim text should scope the negative to the frozen class-marginal term and
  record the position-resolved counter-result.
- **Q2: reading (2) "random restarts do not help" is falsified under (iii)** — at
  alpha=1.0 the fixed restart Random(42000002) wins with strictly better exact objective
  and 10/10. Under readings (i)/(ii) I confirm restarts never beat rank-init.
- **Q3: reading (3) "positional augmentation did not rescue" is conditional on the term
  being nearly information-free.** A position-resolved term — the reading that actually
  implements the cited L1-0002b positional structure — rescues the dev cell.
- **Q4: overall gate outcome probably robust.** My 974-reference probes (dev key) give
  at most 6/10 by selection (5-7/10 across starts) under the strong reading — the 8/10
  arm would likely fail; "strengthened gate fails on this fresh cell" likely survives,
  but via arm (b), not arm (a). Not a full gated rerun — flagged as probe, not proof.
- **Q5: bigram denominator convention differs** — shipped uses full unigram count
  `ur[p]+a*V` (recover_lib/nmin_lib), I used context count `ctx[p]+a*V`; explains most
  of the 0.1-cell band gap (5 vs 4); disclosed, immaterial to any bar.
- **Q6: over-smoothing optimum** — at a>=0.5 the climb's optimum exceeds the true key's
  objective (both readings); 10/10@1.0-style cells are partly objective artifacts, not
  truth-anchored recovery. Worth carrying into any future reading of high-alpha passes.
- **Q7 (minor):** at alpha\*=None the checker asserts only alpha\*, not the 18 cells;
  8 duplicate-content texts straddle the pool boundary (0.3%-scale, same disclosure as
  L4-0004); my runtime was numpy-fast (~40 s per 18-climb sweep) vs the ~50 min pure
  Python checker — cross-implementation float ordering differs (tie-noise band, per
  L4-0003 precedent).

## 10. Bottom line

Filed negative mechanically reproduces (blind checker exit 0; my independent band
matches under the frozen reading; prereg chain byte-clean, code frozen pre-results), so
this is a **reproduction with a material qualification**: the headline "no alpha
reaches the 7/10 dev bar" hinges on the weakest non-vacuous reading of an ambiguous
positional formula; under position-resolved readings of the same preregistered term the
dev bar clears (alpha\*=0.1–0.5), random restarts do help at high alpha, and the gate
would fail later (N_ref=974 arms, 5-6/10 vs 8/10 in my probes) rather than at condition
(a). Recommend folding Q1–Q4 into the claim record; the L3-keeps-shut consequence is
unaffected, but the "boundary draw" narrative should say the strengthened gate fails at
the full-reference arms under the strong reading, not at the dev bar outright.
