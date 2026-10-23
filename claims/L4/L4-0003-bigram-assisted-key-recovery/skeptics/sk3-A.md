verdict: reproduced

# Skeptic-A (sk3-A) independent audit — L4-0003 bigram-assisted key recovery

Independent reimplementation of the preregistered recovery from the raw ETCSRI
zip. No L4-0003 method code (`how-we-built-it/recover_lib.py`,
`how-we-built-it/run_l40003.py`) was ever opened — including after my numbers
existed; the only bytes of the generator I have seen are the two disclosed
`mkdir` lines in the `git diff 3954eb4..1b87505` (prereg-chain audit). The
shipped `check.py` was EXECUTED BLIND before its source was read.

## Independence disclosure (order of what was opened)

1. `claims/L4/L4-0003-bigram-assisted-key-recovery/claim.yaml` (prereg text)
2. `claims/L4/L4-0003-bigram-assisted-key-recovery/README.md`
3. `planner.md` §8, `agents/skeptic-protocol.md`
4. `claims/L4/L4-0002-sumerian-hidden-key/claim.yaml` (input-chain definition)
5. `claims/L4/L4-0002-sumerian-hidden-key/how-we-built-it/sumer_lib.py` —
   read/imported as the PRIOR VERIFIED CLAIM's frozen input pipeline
   (fetch-pinned zip → gdl_sign texts → 1948 windows @ seed 260417835 on
   splits/v1 lengths), as explicitly permitted; it is an input definition,
   not L4-0003 method code. `sumer_lib.make_key(370)` was verified to
   reproduce `object/key.json` bit-exactly.
6. My own implementation run (committed + alt1 arms completed) — **the
   harness timed me out mid-run on 2026-10-23** (alt2 was in flight, no
   results file had been written; only the tee'd stdout log existed). On
   resume, alt2 was completed standalone BEFORE any forbidden file was
   opened, then steps 7–10 below.
7. Shipped `check.py` executed blind (output below); source read only after
   execution, and only the prereg→results diff.
8. `object/results.json`, `baseline_snapshot/l40003.json` (read only after my
   own numbers existed).
9. git history: `3954eb4`, `1b87505` (claim.yaml byte-diff, check.py and
   run_l40003.py amendment diffs).
10. `claims/L1/L1-0001-rao-entropy-replication/skeptics/skeptic-task-02.md`
    — FORMAT reference only (different claim, per assignment).

Self-disclosed dead end: a first debugging run (`probe.py`) of mine had
enciphered the wrong half (cipher tokens=4511 = plaintext side) and produced
meaningless 10/10 numbers; discarded before any shipped L4-0003 file was
read. It is retained in the scratch dir for the record.

## Environment

- OS: Windows 11 (10.0.26200), Git Bash; Python 3.12.10 (MSC v.1943 64-bit)
- numpy 2.4.6 for matrix deltas (repo builder is stdlib-only; mine is an
  independent implementation, see fp caveat O1); stdlib otherwise
- Scratch: `C:\Users\Apoorv\AppData\Local\Temp\sk3A\` (sk3a_primary.py,
  sk3a_adversarial.py, sk3a_refscope.py + logs/results)
- Corpus: pre-staged `etcsri.zip`, sha256 recomputed
  `66991601df193a5cb93bccf92e9051e86a98fbb668a9dd343477d14f0c9d54d6`
  (13197377 bytes) — matches `claim.yaml:corpus_snapshot_sha256`
- Key: `claims/L4/L4-0002-sumerian-hidden-key/object/key.json` (public since
  reveal); `sha256(json.dumps(key))` recomputed =
  `3b6a6c1daccd40ee02ea76b03e9338924fb1b0edf47ea5c6e52403d9b263c517` — matches
  `key_commitment_sha256`

## My implementation (from claim.yaml:preregistered_threshold prose)

- Inputs via imported `sumer_lib`: 1456 nonempty gdl_sign texts; splits/v1
  length pool n=2364 mean 4.5571; 1948 windows, wrap 7.29%, mean len 4.6124;
  V=370 asserted; plaintext half = first 974 windows (4511 tokens), cipher
  half = other 974 (4474 tokens) enciphered position-wise as cipher=key[plain]
  (set-level halves per L4-0002's "reference = plaintext half, cipher = other
  half"; confirmed by output agreement).
- Alt keys: `random.Random(seed).shuffle(range(370))` with
  alt1=260417835+9000+370, alt2=260417835+9001+370 (not sha-committed, per
  claim.yaml).
- Reference model from plaintext half: P_ref(p→q) = (ref_bigram+0.001)/
  (ref_unigram+0.001·370) as a dense 370×370 log-matrix (316 unigram types,
  1760 distinct bigrams, 3537 bigram tokens).
- Init: unigram rank match with canonical sort (count desc, sign asc on the
  vocab-sorted type names) — reproduces the L4-0002 rank-only 5/10 baseline on
  all three keys.
- Objective: Σ ln P_ref(m(c_i)→m(c_{i+1})) over adjacent within-window pairs
  of the cipher half (3500 pairs). Swap deltas via sparse cipher adjacency
  (row/col/corner decomposition), SELF-TESTED against full LL recompute on 8
  random swaps per key: PASS (max rel err < 1e-7). The adversarial script
  additionally uses a vectorized full-sweep delta matrix, validated against
  the sparse reference on 300 random pairs (max|diff| = 5.8e-13; an initial
  transcription bug — column vs row of C — was caught by exactly this
  validation and fixed before any variant number was accepted).
- Search: deterministic steepest ascent, full sweep per step, first
  row-major max on ties, accept iff Δ>1e-12, cap 2000 accepted swaps.
- Hits: of `Counter.most_common(10)` cipher-half types, count m[c] ==
  true_inverse(key)[c]. Gate: committed ≥7/10 AND ≥2 of 3 keys ≥7/10.

## Numbers — mine vs shipped (preregistered method)

| Arm | init hits (mine) | final hits (mine/shipped) | full-key (mine/shipped) | swaps (mine/shipped) | LL init→final (mine) |
|---|---|---|---|---|---|
| committed | 5/10 | **4/10** / 4 | 20/370=0.054 / 0.051 | 328 / 326 | −29974.99 → −19966.03 (true −17157.35, 78.1% gap closed) |
| alt1 | 5/10 | **4/10** / 4 | 19/370=0.051 / 0.051 | 315 / 318 | −30516.69 → −20077.48 (78.1%) |
| alt2 | 5/10 | **4/10** / 4 | 17/370=0.046 / 0.046 | 309 / 303 | −30179.65 → −20343.29 (75.5%) |

- GATE (mine): committed 4 < 7 AND keys≥7 = 0/3 → **FAIL** — matches shipped
  `keys_ge7: 0`, `gate.pass: false`, README table 4/4/4, and the 5→4
  degradation vs the L4-0002 rank-only baseline.
- Cipher-half top-10 counts (mine): 302, 174, 160, 160, 158, 156, 142, 107,
  101, 92 — byte-matches README's near-tie diagnosis (ranks 2–7 within 18
  tokens); the top-10 SET is stable (gap 142→107) but ranks 2–7 are
  fp-fragile in order, consistent with the claimed mechanism.
- Divergences (LL −19966.03 vs shipped −19981; swaps 328 vs 326; committed
  full 20 vs 19): my optimum is marginally BETTER in LL, same 4/10. Two of my
  own implementations of the same deterministic rule (sparse-delta primary:
  −19966.03/328 swaps; vectorized sweep sanity: −19995.20/326 swaps/21 full)
  also differ from each other by ~30 nats. Cause: the objective is massively
  degenerate near convergence — swap deltas tie to ~1e-12, so fp summation
  order decides which of several near-equal maxima "first row-major" picks.
  The preregistered algorithm is deterministic only relative to an fp
  summation order; the OUTCOME (4/10 < 7 on every key, LL ≈ −19.9k to
  −20.4k, ~76–78% gap closed, 5→4 top-10 degradation) is invariant across
  three independent code paths (mine ×2, shipped). This strengthens, not
  weakens, the negative: 4/10 is a property of the basin, not of a lucky
  path. Verdict-level agreement is the bar and is met.

## Shipped checker (executed BLIND, before reading its source)

```
$ python claims/L4/L4-0003-bigram-assisted-key-recovery/check.py \
    --splits benchmarks/splits/v1 --scratch <l4preflight> \
    --object .../object/results.json --baseline .../baseline_snapshot/l40003.json \
    --key claims/L4/L4-0002-sumerian-hidden-key/object/key.json
KEY committed 4/10 alt1 4/10 alt2 4/10 (ge7: 0) recompute=match gate=FAIL
FAIL
(exit code 1)
```

Exactly the expected negative-by-design convention (L4-0002-style):
`recompute=match` (checker's own regeneration from the raw zip matches the
shipped object) with gate FAIL and exit 1.

## Prereg-chain audit (git)

- `3954eb4` (L4-0003 preregister, **2026-10-23T22:14:50+05:30**) IS an
  ancestor of `1b87505` (results, **22:41:05+05:30**) —
  `git merge-base --is-ancestor` true.
- `claim.yaml` diff between the commits: ONLY line 12 (`result:`: "TBD —
  pipeline not yet run at preregistration commit" → the negative text) and
  line 14 (`status:` comment). The `preregistered_threshold` line (1045
  bytes) is **byte-identical** at both commits (sha256
  `35a5f57cac74d202c63a0b72bc7f39d49b2cb0b6823fae4e4109f14226a1b692` each).
- Disclosed amendments verified in the diff: `check.py` changes only the
  exit/print convention (old: PASS iff recompute-match AND gate equals the
  object's stored gate; new: PASS iff recompute-match AND gate passes — the
  gate computation line itself is untouched); `run_l40003.py` adds only two
  `mkdir(exist_ok=True)` lines before the writes. Both are reporting/
  plumbing changes, no method or threshold change. Benign, and honestly
  disclosed in README's evidentiary notes.

## Adversarial variants (all on committed key; goal: break the 4/10 negative)

Vectorized-sweep steepest climb unless noted; all use the frozen inputs and
the same rank init unless noted; hits = top-10 exact.

| Variant | Result | Notes |
|---|---|---|
| S sanity, α=0.001 steepest | 4/10, 21/370 full, 326 swaps, LL −19995.20 | reproduces primary/shipped outcome |
| A α=0.01 | 4/10, 19/370, 310 swaps, LL −17830.31 | smoothing does not rescue top-10 |
| A α=0.1 | 4/10, 17/370, 285 swaps, LL −17092.49 | LL nearly reaches true (−17157) yet still 4/10 |
| B first-improvement (row-major) | 3/10, 10/370, 1822 swaps, LL −20112.25 | worse, near cap |
| C best of 10 random restarts | 0/10, best LL −20922.90 | random inits are far worse — rank init is load-bearing |
| D1 anneal, rank init, T0=2 ratio .995, 200k props | 2/10 best | schedule freezes fast (greedy tail) |
| D2 anneal, rank init, T 2→0.02, 200k props | 3/10 best | no rescue |
| D3 anneal, random init, T 2→0.02 | 0/10 | — |
| E ref = all 1948 windows | **10/10**, 285/370=0.77 full, LL −9813 | TASK REDEFINITION (see O2) |
| F best of 6 targeted restarts (top-30 perturbations) | 5/10, 22/370, LL −19684 | ties rank-init baseline, no better |

**No preregistered-task variant reaches 7/10.** The only 10/10 is E, which
changes the attacker's information (see below).

### E decomposition (reference-scope probe, sk3a_refscope.py)

| Reference | tokens | final top-10 | full-key | LL true (under that ref) |
|---|---|---|---|---|
| R1 disjoint plaintext half (PREREG) | 4511 | 4/10 | 21/370 | −17157 |
| R2 cipher-half's own windows (circular, same size) | 4474 | 5/10 | 91/370 | −8673 |
| R3 all 1948 windows (overlap AND 2× data) | 8985 | **10/10** | 285/370 | −9481 |

Overlapping the attacked text AT THE SAME DATA SIZE (R2) still fails top-10
(only full-key improves 21→91). The flip needs roughly doubled reference
statistics (R3). So the negative is a statement about REFERENCE SIZE at Indus
scale, not about overlap per se — see O2.

## Gate checklist (agents/skeptic-protocol.md)

- [x] Rebuilt from raw inputs in a clean context with independently written
  code (only the L4-0002 input pipeline reused, as permitted; L4-0003 method
  code never opened)
- [x] Same sign-coding scheme and corpus snapshot hash (zip sha match, V=370,
  1948 windows @ 260417835, key sha match; L4-0002 checker re-run green on
  this zip is asserted in claim.yaml and consistent with my rebuild)
- [x] Threshold and split fixed before the run (git chain above; result=TBD
  at prereg; threshold byte-identical prereg→results)
- [x] Null/calibration: this claim IS a calibration negative at the
  preregistered bar; L1/L2/ENT legs belong to verified L4-0002 and are out of
  scope here (not re-run)
- [x] Degrees of freedom: one preregistered gate (committed ≥7 AND ≥2/3
  keys), no multiplicity issue; adversarial variants are exploratory
  robustness bounds, reported uncorrected and none clears the bar
- [x] Novelty checked: Jakobsen 1995 ("A Fast Method for the Cryptanalysis of
  Substitution Ciphers", Cryptologia 19(3):265–274) is the acknowledged prior
  art and the claim styles itself "Jakobsen-1995-style"; this is a
  calibration-negative at tiny N, not a method-novelty claim — correct
  framing (web search logged 2026-10-23)
- [x] Claim wording matches what was shown: `grep -riE
  "deciphered|solved|translat|proof"` over claim.yaml, README.md,
  TROPHY_CASE.md → zero hits; README says "fails"/"does not clear", reports
  mechanism post-hoc as such
- [x] Checker runs from scratch per the negative-claim convention:
  recompute=match, gate=FAIL, exit 1 (by design, matching L4-0002)

## Objections / notes (non-blocking, fold into the record)

- **O1 (fp-path non-determinism across implementations):** "deterministic
  steepest-ascent, first row-major max" is deterministic only up to
  floating-point summation order; three implementations (mine sparse, mine
  vectorized, shipped) land on LL −19966/−19995/−19981 with 315–328 swaps.
  Reported swap counts and LL finals should be quoted with this ±-band; the
  gated outcome (4/10, FAIL) is invariant. Anyone re-running should expect
  small numeric drift, not bit-identity, in the non-gated report-only fields.
- **O2 (reference-scope condition on the negative — the important one):** the
  negative holds for the preregistered attacker (equal-size disjoint
  reference) and even for an equal-size overlapping (circular) reference
  (R2: 5/10), but the same hill-climb with the full ~9k-token corpus as
  reference recovers 10/10 top-10 and 77% of the full key (R3). The filed
  claim is honest about its frozen inputs, but ladder-level wording ("the L4
  hidden-key arm remains uncleared", "substitution-key recovery fails at
  Indus scale") should carry the condition: fails given an equal-size
  reference sample; succeeds with ~2× corpus-scale reference. At Indus scale
  there may be no 2× corpus to draw on, but the condition should ride with
  any L3-gate citation.
- **O3 (committed full-key 20/370 vs shipped 19/370):** same verdict class,
  my path marginally better LL; covered by O1.
- **O4 (alt keys not sha-committed):** alt1/alt2 are deterministic from the
  committed KEY_SEED (disclosed in claim.yaml); I reproduced them exactly.
  Acceptable, but they are post-hoc-selectable in principle — the 3/3
  consistency (and my independent 3/3) is the real evidence.
- **O5 (checker exit-convention amendment post-prereg):** verified benign by
  diff (reporting only, gate untouched); the prereg version would have
  printed PASS/exit 0 for a *matching* negative, the amended one correctly
  FAILs it per the L4-0002 convention. Keep the amendment note visible.
- **O6 (session transparency):** the audit harness timed out mid-run on
  2026-10-23; committed/alt1 numbers come from the pre-timeout tee'd log
  (verbatim quoted into the consolidated results JSON), alt2 from the resume
  run. No shipped L4-0003 artifact was read between timeout and resume
  completion of my own numbers. An early buggy probe of mine (wrong half
  enciphered) was discarded; numbers above are from the corrected pipeline
  only.
- **O7 (license):** ORACC/ETCSRI treated per repo convention — zip fetched/
  staged externally, attributed, never vendored into the repo by me; scratch
  copy lives only in %TEMP% and is deleted with it.

## Bottom line

The preregistered bigram-assisted recovery was reimplemented independently
from the raw zip and the frozen L4-0002 inputs: it fails its gate exactly as
filed (committed 4/10, alt1 4/10, alt2 4/10; keys_ge7=0; and it underperforms
the 5/10 rank-only init on every key). The objective is not at fault (LL_true
−17157 ≫ LL_init ≈ −30k) — the greedy climb stalls at ~77% of the gap and
trades top-sign mapping for sparse bigram cells, as the README's mechanism
story states; my near-tie count profile (174/160/160/158/156/142) matches
byte-for-byte. Ten adversarial variants (smoothing, first-improvement, 10
random restarts, 3 annealings, targeted restarts) all stay ≤5/10 under the
preregistered task; the negative flips only when the attacker's reference is
doubled to the full corpus (O2), which is outside the preregistered threat
model and must be stated as a scope condition wherever the L3-gate
consequence is cited. Checker runs blind to `recompute=match gate=FAIL`
exit 1; prereg chain and disclosed amendments verified in git. Verdict:
**reproduced** (with objections O1/O2 folded in).
