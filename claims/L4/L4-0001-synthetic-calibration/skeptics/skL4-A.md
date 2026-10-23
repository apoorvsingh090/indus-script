verdict: reproduced

# skL4-A — Independent skeptic audit of L4-0001 (synthetic calibration)

Fresh context, own code throughout (`C:\Users\Apoorv\AppData\Local\Temp\opencode\skL4A\sk_gen.py`,
`sk_metrics.py`, `sk_run.py`, `sk_adv.py`, `sk_l2b.py`). Read ONLY `claim.yaml` + `README.md` +
`agents/skeptic-protocol.md`. Never read `how-we-built-it/*.py`, `check.py` (ran blind, see §5),
`object/*`, `baseline_snapshot/*`, other skeptics, or any L1/baseline code. Allowed inputs only:
P&P text fetched myself + frozen-splits lengths pool.

## 1. Provenance (verified)

- P&P `pg1342.txt`: claim sha256 `7c13190c…dfec18` VERIFIES against the text-mode (LF-normalized)
  read. Caveat: raw download bytes carry CRLF and hash to `3f6bb9d6…`; the claim hash matches after
  universal-newline normalization. Same document either way.
- Tokenization `re.findall(r'[A-Za-z]+', body).lower()` reproduces the claim's fingerprints EXACTLY:
  128565 tokens / 6729 types. Case-sensitive distinct would be 7153, so the generator lowercases.
- Lengths pool from `benchmarks/splits/v1/*.jsonl` (lengths only): 2364 texts, mean 4.557, range 1–19.

## 2. Reconstruction (GEN_SEED 260417834, nested; own RNG-stream/metric choices, documented in code)

Generators: lengths resampled w/ replacement; linguistic = contiguous excerpts; emblem =
uniform opener(8) + Zipf-s1.0 core(40) + uniform closer(6), 5% fresh-singleton on core slots
(L=1 → core; L=2 → opener+closer). Metrics, my canonical forms: ENT = MM-corrected H(W2|W1)/log V
vs B=100 global-permutation nulls, pass iff obs < null-min; L2 = bigram-MLE vs unigram-mode top-1
accuracy gain, random 60/20/20 + leakage exclusion, paired bootstrap B=1000, pass iff CI-lo > 0 and
diff > 0.01 (unseen bigram context = wrong, so diff can go negative); REP = tokens in repeated
3/4-grams vs B=100 null maxima, strict > (ties fail).

Sizes/vocabs/lengths match closely: ling types 472/796/1197/1798 (claim: 426→1613 growth);
emblem@1948 types 298 (claim ~266 — supports my 5%-of-core-slots reading); mean len ≈ 4.55.

### Main recompute (nested)

| corpus | N | ENT obs<null-min | L2 diff [CI] | REP obs vs null-max |
|---|---|---|---|---|
| ling | 250 | 0.2295<0.2398 P | -0.0237 [-0.0592, 0.0059] F | [6,0]v[2,0] F (rep4 tie) |
| ling | 500 | 0.2698<0.2875 P | -0.0140 [-0.0420, 0.0168] F | [18,0]v[4,0] F (rep4 tie) |
| ling | 1000 | 0.3120<0.3425 P | 0.0387 [0.0179, 0.0610] P | [81,10]v[8,2] P |
| ling | 1948 | 0.3474<0.3878 P | 0.0488 [0.0320, 0.0641] P | [321,59]v[31,2] P |
| emb | 250 | 0.5937<0.6422 P | -0.0240 [-0.0599, 0.0120] F | [61,2]v[37,4] F |
| emb | 500 | 0.5939<0.6625 P | -0.0465 [-0.0785,-0.0174] F | [244,8]v[119,10] F |
| emb | 1000 | 0.5733<0.6358 P | -0.0207 [-0.0350,-0.0080] F | [653,51]v[334,18] P |
| emb | 1948 | 0.5403<0.6001 P | -0.0189 [-0.0283,-0.0102] F | [1700,156]v[998,51] P |

Absolute numbers differ (own metric details), but EVERY qualitative finding reproduces:
ling@1948 all-pass (the preregistered gate); ENT ≤ 250; rep4-tie fails at 250 exactly as claimed;
full panel passes at 1000; emblem ENT+REP pass while L2 is negative at every N (significantly
negative at 500+). EXCEPTION: my L2 N_min = 1000, not the claimed 500 (see objection O1).

## 3. Adversarials

(a) NON-NESTED (fresh draws per N, own seeds 201–204): ladder survives in kind —
ling ENT passes all N; ling L2 fails 250/500 (500: +0.0204, CI crosses 0), passes 1000/1948;
ling REP passes 500+ (one rung earlier than nested); emb L2 negative-significant at all N;
emb REP fails 500 (rep4 tie 10v10), passes elsewhere. So under resampling, L2 N_min = 1000 and the
500-rung flips with seed. Panel = 1000 is the robust joint floor.
(b) EMBLEM SWEEP (16 openers, core Zipf s=1.5, 10 closers, GEN_SEED stream): L2 STILL fails at all
N, significantly negative at 500+ (-0.0286/-0.0190/-0.0124). ENT passes (obs ≈ 0.44–0.46, lower as
expected under steeper Zipf); REP passes at all N (steeper Zipf → more repeats, incl. 250).
L2 non-discrimination on emblem-like is NOT a one-parameter-point artifact.
(Zig-zag check: add-one-smoothed logprob-gain L2 variant fails everywhere incl. ling@1948 —
over-smoothing with V≈1800 drowns all signal; discarded as uninformative, accuracy-gain stands.)

## 4. Git order + wording

- Order clean: `f25ea2c` prereg (threshold + checker + generator, result "TBD — pipeline not yet
  run", status draft) at 12:18:58 precedes `6e484bd` results (README/gates/results.json) at
  12:21:12. Threshold was fixed before any synthetic number existed.
- Wording: one-family scope IS disclosed — limitation "one Nair-style family, not the full
  non-linguistic space", README "One family only: no general non-linguistic exclusion claimed",
  result hedged as "discriminates in this setup". No "solved" stretch. Title matches content.

## 5. Checker conformance (blind run, `--help` for CLI only, never read source)

`python check.py --splits benchmarks/splits/v1 --scratch <my-own-tmpdir> --object object/results.json
--baseline baseline_snapshot/gates.json` → PASS. Per-N lines agree with my pattern on the gate
(ling@1948 ENT/L2/REP True) and emblem L2 False everywhere; checker adds that their L2 passes
ling@500 and their emblem REP passes @500 — i.e. all checker-vs-mine disagreements sit at N=500
(see O1). (Note: scratch dir had to be pre-created; checker does not mkdir it — harness nit.)

## 6. Objections

- O1 (minor — rung fragility, acknowledged cliff): N=500 is inside the power cliff under BOTH
  implementations. Mine: ling L2 fails @500 across 8 split seeds (diffs -0.014…+0.014) and fails
  nested/non-nested; theirs: passes @500 (checker True) but their own N=250 CI "touches 0.0000".
  Claimed "L2=500" is a one-draw outcome, not seed/metric-robust; robust statement is L2 N_min ∈
  {500, 1000}, joint-panel floor 1000 (both agree). The preregistered gate itself (@1948) is
  unaffected and reproduces solidly.
- O2 (nit — provenance hashing): claim sha256 matches only the LF-normalized read, not raw CRLF
  download bytes. Recommend stating "sha256 of UTF-8 text with universal newlines". Same document,
  no integrity issue.
- O3 (accepted design limits, already disclosed): transparent-box (no hidden key), B=100/1000
  budgets, one emblem family. Nothing hidden; future-work items are real.

## 7. Env / log

Win32, Python 3.12.10, stdlib only (`random`, `re`, `json`, `hashlib`, `math`). Full recompute
≈10 s; adversarials ≈16 s. Artifacts: `skL4A/main_results.json`, `skL4A/adv_results.json`.
Repo otherwise untouched (`git status` clean apart from this file).

Verdict rationale: the preregistered gate (linguistic@1948 all three, exact budgets/seeds as
far as the claim fixes them), the N_min ladder shape, the rep4-tie mechanics, and the emblem
discriminator profile (ENT+REP pass, L2 negative — robust to resampling AND parameter sweep) all
reproduce from raw inputs with independently written code. O1 qualifies one rung, not the claim.
