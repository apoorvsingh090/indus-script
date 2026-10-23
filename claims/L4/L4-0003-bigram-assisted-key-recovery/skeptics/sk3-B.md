verdict: reproduced

# Skeptic report — L4-0003 bigram-assisted hidden-key recovery (sk3-B)

Independent audit of the CONFIRMED NEGATIVE. All gated numbers below were produced by my
own code before I ran or read anything shipped (order documented below).

## Independence disclosure (what I opened, and when)

Before writing any code, I read ONLY: this claim's `claim.yaml` + `README.md`,
`planner.md` §8, `agents/skeptic-protocol.md`, and `L4-0002/claim.yaml` (input-chain
definition). Additionally, as explicitly permitted, `L4-0002/how-we-built-it/sumer_lib.py`
(the verified claim's shipped input pipeline) — used only to cross-check my own
from-prose reimplementation (outputs bit-identical; see below). I did NOT open
`L4-0002/how-we-built-it/run_sumer.py`, any `how-we-built-it/`, `object/`,
`baseline_snapshot/` of THIS claim, or `check.py` source until after my own numbers
existed (the checker was executed blind first). I have not read sk3-A's report or scratch
(`%TEMP%/sk3A` off-limits; untracked `skeptics/` dir not listed).

## Environment

- Windows (win32), Python 3.12.10; numpy 2.4.6 (sweep-delta algebra only — disclosed);
  stdlib otherwise. My scratch: `C:\Users\Apoorv\AppData\Local\Temp\sk3B\`
  (`sk3b_input.py`, `sk3b_climb.py`, `sk3b_adversarial.py`, `sk3b_alpha.py`).
- Raw input: pre-staged `C:\Users\Apoorv\AppData\Local\Temp\l4preflight\etcsri.zip`,
  sha256 `66991601df193a5cb93bccf92e9051e86a98fbb668a9dd343477d14f0c9d54d6` — verified.
- Committed key: `sha256(json.dumps(key)) = 3b6a6c1daccd40ee02ea76b03e9338924fb1b0edf47ea5c6e52403d9b263c517`
  — verified; also equals `make_key(370)` = `Random(260417835+370).shuffle(range(370))`
  procedurally. alt1/alt2 verified against `Random(+9000/+9001+370)`.

## Implementation choices (mine, from prereg prose)

- Input reconstruction written from prose (own CDL walk for `gdl_sign`, own window RNG:
  per window text-pick → length-pick → offset-pick, token-weighted choice, modular wrap).
  Result: 1456 nonempty texts, 1948 windows @ seed 260417835, wrap 7.29%, V=370 asserted,
  974/974 halves (ref = first half plaintext; cipher = second half enciphered — inferred
  from "cipher = second half", confirmed later by shipped `arm()`). Every stage
  bit-identical to `sumer_lib` output (texts/lengths/windows `==` True).
- Objective: `L[p,q] = ln((ref_bi[p,q]+0.001)/(ref_uni[p]+0.001·370))` from the reference
  half; cipher bigram count matrix C over adjacent within-window pairs; `LL(m) = Σ C[a,b]·L[m(a),m(b)]`.
- Search: full-sweep steepest ascent via matrix algebra (`A = C@L[:,m].T`, `Bc = C.T@L[m,:]`,
  explicit corner fix for pairs in `{i,j}²`); flat argmax = first row-major maximum
  (matches "first row-major max on ties"); accept iff Δ>1e-12; cap 2000.
  Validated three ways: brute-force LL on synthetic V=30 (60 random swaps), 25 random
  real-data swaps at init per key (worst |err| = 5.6e-12), and an assert that every
  accepted step satisfies `LL_direct(m') == LL + Δ`.
- Hits: `Counter` over cipher-half token stream, `most_common(10)`, exact-match vs true
  inverse encipherment; full-key accuracy over all 370 types; init = canonical rank match
  (count desc, sign asc — full rank-to-rank zip).

## Numbers: mine vs shipped

| Quantity | Shipped (object/results.json / README) | Mine | Match |
|---|---|---|---|
| committed top-10 hits | 4/10 | **4/10** | exact |
| alt1 top-10 hits | 4/10 | **4/10** | exact |
| alt2 top-10 hits | 4/10 | **4/10** | exact |
| keys_ge7 / gate | 0 / FAIL | 0 / FAIL | exact |
| rank-only init hits (L4-0002 baseline) | 5/10 | 5/10 (all three keys) | exact |
| committed swaps | 326 | 326 | exact |
| alt1 / alt2 swaps | 318 / 303 | 315 / 310 | no (float near-ties, see below) |
| committed / alt1 / alt2 full-key | .051/.051/.046 | .057/.051/.046 | committed differs (same cause) |
| LL init / LL true (committed) | −29975 / −17157 | −29974.99 / −17157.35 | exact to 5 sig digits |
| LL final (committed) | −19981 | −19995.20 | 0.07% off (same cause) |
| "~77% of init→true LL gap closed" | 77% | 77.9% | yes |
| wrap rate, V, cipher ranks 2–7 | 0.0729, 370, 174/160/160/158/156/142 | 0.0728952772073922, 370, identical | exact |

Near-tie probe (why report-only cells diverge): 84/326 of my accepted steps have a
best-vs-second-best Δ gap < 1e-9 (smallest gap exactly 0.0 — structural ties from
zero-count types). Greedy sequences are therefore deterministic per implementation but
not bit-portable across summation orders (my numpy/BLAS vs their pure-Python dicts).
All *gated* cells (hits, keys_ge7, gate) are implementation-stable; the checker compares
exactly those.

## Checker (run blind, before reading its source)

```
KEY committed 4/10 alt1 4/10 alt2 4/10 (ge7: 0) recompute=match gate=FAIL
FAIL   (exit 1)
```

Negative-by-design exit-1 convention per L4-0002. Having then read `check.py`: it is a
genuine full recompute (rebuilds windows from the zip, re-enciphers, reruns the whole
climb for all three keys) but compares only `top10_hits` and `keys_ge7` — the two
quantities my audit shows are cross-implementation stable. Sound design.

## Prereg-chain audit (git)

- `3954eb4` (2026-10-23 22:14:50 +0530, prereg, `result: "TBD — pipeline not yet run at
  preregistration commit"`) precedes `1b87505` (22:41:05 +0530, results). ~26 min gap.
- `preregistered_threshold` **byte-identical** across the two commits; `id`, `title`,
  `key_commitment_sha256`, `corpus_snapshot_sha256`, `object`, `checker`,
  `baseline_snapshot`, `generator` all unchanged. Only `result` and a status comment changed.
- Both disclosed pre-results amendments verified exact and minimal: `check.py` diff
  changes only the exit/print convention (old code would have exited 0 for a correctly
  reproduced *negative*; gate arithmetic `hits["committed"]>=7 and n_pass>=2` untouched);
  `run_l40003.py` diff is the 2-line `mkdir` fix. Working tree `claim.yaml` == `1b87505`.

## Top-10 tie probe

Cipher-half counts: 302, 174, 160, 160, 158, 156, 142, 107, 101, 92, then 85, 80.
The rank-10/11 boundary is 92 vs 85 — no tie, so top-10 **membership** is robust to
Counter insertion-order convention. The one internal tie (ranks 3/4 at 160) stays inside
the top-10 and both types are scored independently. The metric is not tie-fragile.

## Adversarial tests (committed key; bar = 7/10; all with the frozen init+search unless noted)

| Variant | Top-10 hits | Notes |
|---|---|---|
| preregistered α=0.001 | 4/10 | reproduced |
| α=0.01 / α=0.1 | 4/10 / 4/10 | still fails |
| **α=0.2** | **10/10** | full-key 0.168, 300 swaps |
| α=0.3 / α=0.5 | 10/10 / 10/10 | full-key 0.243 / 0.232 |
| **α=1.0** | **10/10 (3/3 keys)** | full-key 0.281/.260/.287 — clears BOTH gate arms; hits recounted via independent string-dict path |
| α=2.0 / α=5.0 | 10/10 / 10/10 | full-key 0.300 / 0.238 |
| first-improvement (α=0.001) | 3/10 | 1822 swaps |
| 5 random restarts (α=0.001) | 0/10 each | best-LL restart −21022 < climb −19995 |
| simulated annealing, 200k props (α=0.001) | 2/10 | best-LL −20750 — worse than steepest |
| oracle: P_ref from all 1948 plaintext windows (α=0.001) | 10/10 | full-key 0.770 — upper bound only (uses the cipher half's own plaintext as reference; illegitimate as decipherment) |

**A reasonable variant DOES clear the bar**: only the smoothing constant changes
(α ≥ 0.2, everything else frozen), and the gate passes on all three keys (10/10 at
α=1.0). Search-scheme variants do not. At α ≥ 0.3 the climb even overshoots LL(true)
while keeping all top-10 (over-fit tail; full-key never exceeds 0.30). Mechanism
confirmed: heavy smoothing suppresses sparse-bigram chasing and resolves exactly the
near-tied top ranks (174/160/160/158/156/142) that rank-init misassigns.

## Gate checklist (planner §8 / skeptic-protocol)

- [x] Rebuilt from raw inputs in a clean context with independently written code.
- [x] Same sign-coding scheme and corpus snapshot hash (zip sha verified; V=370; wrap exact).
- [x] Threshold fixed before the run (prereg audit above; 26-min window).
- [x] Null/calibration: hidden-key gate is self-nulling (random-perm recovery ≈ chance;
      init full-key 0.024–0.027 ≈ 9× chance, final 0.046–0.057); 3-key robustness arm
      serves as replication. No multiple-comparison concern for the gated cells.
- [~] Degrees of freedom: the method family has one free constant (α) that the prereg
      fixed by inheritance (0.001, from L4-0002's L2 entropy test — a different
      estimator context). See objection 1.
- [x] Novelty: claim self-describes as Jakobsen-1995-style hill-climb and files a
      calibration negative at tiny N — no method-novelty overreach.
- [x] Wording: case-insensitive grep for `deciphered|solved|translat|proof` over
      `claim.yaml`/`README.md`/`TROPHY_CASE.md` — zero hits (only a hedged
      "not a general decipherment capability claim" limitation). No L4-0003 trophy row
      exists yet (consistent with draft). Caveat on one class-level sentence in
      objection 1.
- [x] Checker runs from scratch: `recompute=match gate=FAIL` exit 1 as designed.

## Objections (non-blocking)

1. **The negative is α-fragile, and the README's class-level conclusion overreaches.**
   The claim-as-filed (preregistered α=0.001 instance fails 4/10 on 3/3 keys) is genuine
   and exactly reproduced. But the same frozen init/search with any α in [0.2, 5] clears
   both gate arms on all three keys (10/10 at α=1.0). "Substitution-key recovery now
   fails by three independent routes … bigram hill-climb (4/10, all keys)" and "keeps
   the L3 gate shut for methods of this class" hold only for the α=0.001 member of the
   class. Recommend folding in this caveat and preregistering an α-calibrated rerun
   (fresh prereg, per the README's own rule) before treating the L4 hidden-key arm as
   uncleared by hill-climbs. The claim's own mechanism ("LL-improving swaps chase sparse
   bigram counts") is precisely what my α sweep confirms — the diagnosis is right, the
   prescribed escape (restarts/annealing/EM) misses the simpler knob.
2. **Binding constraint is reference-data sparsity, not local optima per se.** With the
   oracle 2× reference (both halves' plaintext) the *frozen* method recovers 10/10 and
   77% full-key. "Stalls in a local optimum it cannot leave by pairwise swaps" is true
   only jointly with the 4.5k-token reference; conditioning on reference size would be
   the accurate phrasing. (Oracle probe is an upper bound, not a decipherment config.)
3. **Report-only numbers are not cross-implementation portable** (84/326 steps with
   best-second Δ gap < 1e-9, min exactly 0). My alt swap counts (315/310) and committed
   full-key (0.057) differ from shipped (318/303, 0.051) for this reason; LL final 0.07%
   off. Gated cells unaffected. Read swaps/full-acc/LL-final as ±noise.
4. `object/results.json` field `n_texts: 1948` is actually n_windows (texts = 1456). Cosmetic.
5. Checker exit code conflates "recompute DIFF" with "gate FAIL" (both exit 1); the
   printed line disambiguates and the convention matches L4-0002. Disclosed in README. Fine.

## Bottom line

The preregistered method genuinely fails its preregistered gate, and every gated number
in `object/results.json` reproduces exactly from raw inputs under independently written
code (as does the whole input chain, bit-exactly). Prereg chain, amendments, commitment
sha, tie-conventions, and wording all check out. **Reproduced** — with one material
qualification the authors should fold in: the negative is an instance negative (α=0.001),
not a class negative; α ≥ 0.2 clears the bar on all keys, so the hidden-key arm is not
shown uncleared against hill-climbs generally.

— sk3-B, 2026-10-23. Scratch: `%TEMP%/sk3B` (reproduce: `python sk3b_climb.py`, then
`python sk3b_alpha.py`, then the checker command in claim.yaml order).
