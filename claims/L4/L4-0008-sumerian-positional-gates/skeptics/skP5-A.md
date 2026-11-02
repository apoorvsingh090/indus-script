> Ported 2026-11-02: original claim ID L4-0005 on the divergent 2026-10-18 branch (now L4-0008 here). All other IDs referenced below (L4-0002, L1-0002b) are unchanged.

verdict: reproduced

# skP5-A — independent audit of L4-0005 (Sumerian positional-gates negative)

## 1. Scope / blind-protocol compliance

- MAY-read items used before freeze: this claim's `claim.yaml` + `README.md`; L4-0002
  `claim.yaml` + `README.md` (window protocol only); L1-0002b `claim.yaml`
  (threshold context); `agents/skeptic-protocol.md`; `planner.md` (skim);
  `benchmarks/splits/v1/*` inputs; raw `etcsri.zip` contents.
- NOT read before analysis freeze (freeze point = completion of my pipeline +
  probe battery, recorded in scratch log): any claim `*.py` — including
  L1-0002b `pos_lib.py`, L4-0002 `sumer_lib.py`, L4-0005 `run_pos5.py`,
  `check.py`, and all `object/`, `baseline_snapshot/` contents. Frozen before any
  post-freeze read; only `skeptics/skP5-A.md` written in-repo. No commits made.
- Never opened skP5-B or skR4 files.
- All code written from scratch in `C:\Users\Apoorv\AppData\Local\Temp\opencode\skP5-A`
  (extract.py, gen_windows*.py, pipeline.py, probes.py, replay.py, probes_exact.py).

## 2. Environment

Windows 11 / PowerShell 5.1; Python 3.12.10 stdlib only. Raw input
`etcsri.zip` staged at 13,186,059 bytes; sha256
`214FD724FF70DC0088395CACA6A4F2B0CA2834FAB3611A2C8CCA921E25DB60C3`
(matches `214fd724…` prefix in task). Extracted into scratch; `corpusjson`
contains 1457 `Q*.json` files, one of which (`Q001066.json`) is 0 bytes
→ 1456 decodable texts with ≥1 token.

## 3. Chain (git forensics)

- prereg `e8a2fab` (11:42): adds `claim.yaml` + `check.py` + `run_pos5.py`,
  result "TBD — pipeline not yet run".
- results `0c19e69` (11:43): adds `README.md` + `object/results.json` +
  `baseline_snapshot/nulls.json`.
- `git diff e8a2fab 0c19e69 -- claim.yaml check.py run_pos5.py` is EMPTY →
  gate text, checker, and generator unchanged between prereg and results.
- Gate text: `|n80_begin - n80_end|` strictly greater than max over B=200
  paired token-shuffle (seed 260417840), windows = L4-0002's 1948 windows
  (seed 260417835), direction not preregistered. Measured exactly as
  `bool(gap > max(D))` in the (later-read) generator; prereg wording matches
  implementation (fact verified post-freeze).

## 4. Independent rebuild (BLIND parse/windower, seed 260417835)

My own extractor: ORACC `cdl` walk, `l`-nodes, `f.gdl` arrays; recursing into
`det.seq` wrappers; token = `gdl_sign`; empty/None dropped; ellipsis/x nodes
have no `gdl_sign` and drop out. Lengths pool read from
`benchmarks/splits/v1/{train,val,test}.jsonl`.

- Corpus: 1456 texts, 67,949 tokens, corpus V=568 (builder counts V=569;
  ±1-type parse wedge reconciled post-freeze, §8).
- Window realization A ("unique-1948-pool", my best-guess protocol reading):
  windowed V=381, 9135 tokens, mean len 4.689, wrap 7.1%.
- Window realization B ("raw-2364-pool"): V=379, 8957 tokens, mean 4.565,
  wrap 7.6%.
- Builder's realization (per claim + later checker replay): V=370, 8985
  tokens, mean 4.61, wrap 7.3%. My blind runs sit in the disclosed
  370–395 builder-delta band; the ΔV≈±11 is a window-realization delta, not a
  parse-content dispute (my signs/types match theirs to ±1 token).

n80 machinery implemented from the claim.yaml text only: n80 = number of top
types whose cumulative tokens cover 80% of a position class; begin = window
index 0; end = last index of windows with len>1; n80_all = whole pool.

| realization | n80_begin | n80_end | n80_all | gap |
|---|---|---|---|---|
| my A (blind) | 65 | 71 | 69 | 6 |
| my B (blind) | 69 | 68 | 70 | 1 |
| builder (checker-confirmed) | 72 | 67 | 72 | 5 |

Conclusion is realization-invariant: no n80 asymmetry at this scale. Top
begin/end sign types overlap 10/10 under my parse (AN, KI, LUGAL, MU, A, NI,
NA…), matching the README's qualitative statement.

## 5. Null battery (B=200, my implementations)

Main paired pool-shuffle null (fixed window lengths; all tokens of all
windows pooled, Fisher–Yates shuffled, redealt in sequence, begin/end
counters per draw):

- Blind realization A, seed 260417840: D_max=9, median 2, 13/200 draws
  exceed observed gap 6 (6.5%). Realization B: D_max=10, 149/200 exceed 1.
  Both observed gaps far inside the band.
- Exact windows (post-freeze replay, §7), disclosed seed 260417840:
  **D_max=12 (exact match to claim/baseline)**, D_p95=7, median 2, 12.0% of
  draws exceed gap 5. Band [D_min 0, D_max 12] envelopes 5.

Own-seed stability (exact windows; 3 additional own seeds):

| null seed | D_max | D_p95 | frac draws > 5 |
|---|---|---|---|
| 260417840 (disclosed) | 12 | 7 | 0.120 |
| 260417841 (own) | 14 | 8 | 0.125 |
| 777 (own) | 11 | 7 | 0.155 |
| 2026 (own) | 12 | 7 | 0.110 |

Range of null maxima 11–14 — no own seed produces a band that the observed
gap would exceed; the negative gate verdict is seed-robust (5 > 14 is false
like 5 > 12 is false). The perceived-conservatism worry ("null max is one
lucky draw") is structurally the opposite: using max-of-200 as the bar is the
hardest bar for a positive claim to clear, and the observed gap doesn't clear
even the soft P95 bar (5 < 7) nor a conventional p<0.05 exceedance (only
~11–15% of draws exceed 5).

### 5a. Adversarial probe: within-window local shuffle null

Per draw: permute tokens inside each window (lengths and per-window unigram
composition preserved), recompute begin/end classes. This is the *fairer*
null for testing whether the cross-window pool shuffle is artificially
conservative/lenient.

- Blind realization A: local D_max=9, 4.0% of draws > observed gap 6.
- Blind realization B: local D_max=9, 68% of draws > observed gap 1.
- Exact windows: local D_max=11 (vs pool 12), 8.5% of draws > 5.

Local-shuffle band ≈ pool-shuffle band (max 11 vs 12): the pool shuffle is
not hiding composition noise; the negative stands under both constructions.

### 5b. max-vs-min semantics sanity

Gate reads "gap strictly greater than null MAX over 200 draws" ≈ a
99.5%-exceedance demand. Distribution of null gap D (exact windows): min 0,
median 2–3, P95 7, max 11–14 by seed. Observed gap 5 sits ≈ 85th–89th
percentile of the null — i.e., "inside the band" is the correct reading, and
even the builder's own far weaker claim ("both figures inside their null
ranges", begin 72 ∈ [64,77], end 67 ∈ [62,76]) checks out exactly against
`baseline_snapshot/nulls.json` sorted arrays.

### 5c. Direction probe (NON-GATED context, no threshold change)

- Position-class entropies on exact windows: begin 4.6192, end 4.5837;
  both within their per-draw null ranges (P(null>obs) = 0.28 / 0.73).
- Top-10 type overlap between begin and end classes: 8/10 (top-5: 4/5).
  README's "overlap almost entirely" is fair.
- Per-sign and-slot residuals (uncorrected z over >100 signs): max |z| ≈
  2.2 (GA, end-lean), LUGAL +2.0 (begin-lean), KID/BA begin-lean, AN/RA
  end-lean — mixed directions, exactly multiple-comparison noise.
- Crucially the blind realizations A/B flip direction (A: end 71 > begin 65;
  B: 69≈68) while the builder realization leans begin 72 > end 67. No
  consistent lean exists in any statistic; Sumerian begin/end asymmetry is
  genuinely ~0 under this machinery. NON-GATED: nothing above alters the
  prereg gate or threshold.

## 6. Checker run (script UNREAD, after freeze)

`python check.py --splits benchmarks/splits/v1 --scratch <skP5-A> --object
object/results.json --baseline baseline_snapshot/nulls.json` →

```
n80 begin=72 end=67 all=72 gap=5 null_D_max=12 recompute=match
FAIL
```

exit code 1. `recompute=match`: checker rebuilt windows from the same zip +
splits and reproduced every object number; `FAIL` on exit 1 is the DESIGNED
outcome for a negative cell (observed gap ≤ null max ⇒ pass=false stored, no
gate to clear). Both arms behave exactly as the claim states.

## 7. Post-freeze exact replay (own new code)

After freezing, I read `run_pos5.py` + `sumer_lib.py` and rewrote (not
copied) the now-visible window protocol: texts in zip namelist order,
`rng.randrange(total)` integer-weighted text choice, length from raw-2364
pool, offset `rng.randrange(len(t))`, modular wrap. My fresh reimplementation
reproduces the ENTIRE object from scratch: 1456 texts; corpus V=569;
windowed V=370; n_tokens 8985; wrap 7.29%; mean 4.612; n80 72/67/72; gap 5;
top_begin/top_end lists exact; null seed 260417840 → D_max=12, D_min=0,
begin [64,77], end [62,76], gate False. Exact-replay agreement is therefore
independently double-confirmed (checker + my own code).

## 8. Diff vs pos_lib (definitions) — post-freeze

- n80: my implementation = `pos_lib.n80` semantics (Counter.most_common
  cumulative ≥ 0.8·total; count of types; tie-order cannot change the count).
  My control loop (`cum >= need: break` before add) vs theirs (add then
  `if acc >= 0.8*tot: return k`) differ only when a class is empty — both
  return 0/0 cases equivalently at class totals used here. Same numbers.
- null: their `null_n80_end` = shuffle global pool, deal by `lens`, Counter
  of end tokens (len>1), n80. L4-0005 pairs it with begin counters per draw —
  my battery implements exactly this, including matching the disclosed seed's
  D_max=12 and both n80 ranges to the digit on exact windows.
- Parse wedge found: builder top-level token rule takes `gdl_sign` if it is a
  str (so one empty-string `gdl_sign` becomes a token), and inside `det.seq`
  uses `gdl_sign or v`; nested `seq` inside `seq` is dropped by theirs,
  counted by my blind parser. Net: my blind corpus V=568/67,949 tokens vs
  builder 569/67,948 — ±1 type/token at the corpus fringe; windowed V
  identical (370) under the identical window protocol.
- (naming nit) `results.json` "n_texts": 1948 is the number of windows;
  texts = 1456. Cosmetic; `vocab` 370 is asserted by checker. No effect.

## 9. Wording honesty

- README "gap 5 is inside the null range (max 12…)": true, in fact the gap is
  inside the band under every null seed and both shuffle constructions tried.
- "Both figures sit inside their own null ranges": true (checker + my nulls).
- "Top begin/end signs overlap almost entirely": 4/5 on top-5, 8/10 on
  top-10 — fair phrasing.
- "Indus beginner/ender phenomenon does not generalize": the crucial L1-0002b
  signature was end << null-min (32 < 67). Here end=67 sits mid-range
  [62,76] — nothing remotely end-concentrated or begin-concentrated. The
  negative generalization statement is supported.
- Title "direction not preregistered" and two-sided |gap| gate are both
  honest (two-sided machinery implemented and used).

## 10. Objections / notes

1. Prereg-to-results latency is 93 seconds. The full pipeline is genuinely
   fast (~seconds for 8985 tokens / 200 shuffles), and the file-level
   sequencing (gate text + checker committed with results TBD, then objects)
   is verified by diff; no surviving objection, but conventional Gaming-adjacent
   attention on such tight timing is noted for the record.
2. The max-of-B gate is a harsh positive bar; a hypothetical true effect
   wouldn't be missed by much only because 11–15% of null draws already
   exceed the observed gap — i.e., the observed gap is ~p≈0.1–0.15 noise, and
   the direction of the tiny deviation flips across window realizations
   (see §5c). No objection to the negative; the honest reading is "no
   asymmetry detectable at this scale/protocol", which is what the claim says.
3. Pool-shuffle bar vs local-shuffle bar: pool max 12 vs local max 11 —
   conservatism of the preregistered null is bounded and immaterial here.
4. One 0-byte corpusjson in the ETCSRI zip (Q001066) — builder skips it; my
   parser too; consistent 1456 texts. Worth a DATA_NOTICE if the upstream
   zip is ever re-fetched with a different content.

## 11. Log

- env verified (py 3.12.10; zip hash ok); scratch created.
- zipped 13,186,059 B extracted; 1457 json, 1 empty, 1456 texts.
- own extractor + profiler (extract.py) → 67,949 tok, V=568.
- lengths pool from v1 splits: 2364 raw / exactly 1948 unique (mean 4.661;
  1948 = N windows; used in blind variants A/B).
- blind window grid gen_windows*.py: V 375–387 across 10 protocol variants
  (no exact 370 hit blind; delta band disclosed by claim).
- frozen independent numbers: A 65/71/69 gap 6; B 69/68/70 gap 1; null max
  9–10; extra seeds 8/9/10/11; local null max 9/9; probes (entropy,
  overlap, residuals) no directional lean.
- FREEZE. Then read object/results.json + baseline_snapshot/nulls.json
  (values as claim text), ran check.py unread → match + FAIL(1).
- Post-freeze: read pos_lib.py, run_pos5.py, sumer_lib.py; wrote replay.py
  from the read spec → full exact reproduction (V=370, 72/67/72, gap 5,
  D_max=12, ranges match to the digit); probes_exact.py on exact windows
  (seeds 260417841/777/2026: D_max 14/11/12; local D_max=11; direction
  probes as §5c). git diff e8a2fab→0c19e69 over claim/check/generator: empty.
- Wrote this file; no other repo changes; no commits.
