> Ported 2026-11-02: original claim ID L4-0005 on the divergent 2026-10-18 branch (now L4-0008 here). All other IDs referenced below (L4-0002, L1-0002b) are unchanged.

verdict: reproduced

skeptic: skP5-B (mechanism-focused audit of the NULL and the METRIC for the draft negative)
claim: L4-0005 (Sumerian positional gates on the L4-0002 window set)
date: 2026-10-18
repo: C:\Users\Apoorv\indus-script (no commits made; only this file written)

## 1. Scope / blind protocol

READ (allowed, pre-freeze):
- claims/L4/L4-0005-sumerian-positional-gates/claim.yaml + README.md
- claims/L4/L4-0002-sumerian-hidden-key/claim.yaml + README.md (window protocol provenance)
- claims/L1/L1-0002b-positional-corrected-order/claim.yaml (metric provenance)
- agents/skeptic-protocol.md; planner.md; TROPHY_CASE.md; README.md
- benchmarks/splits/v1/*.jsonl (disclosed lengths pool); git forensics (prereg e8a2fab, results 0c19e69)
- raw corpus: staged etcsri.zip (13,186,059 bytes; sha256 214fd724ff70dc0088395caca6a4f2b0ca2834fab3611a2c8cca921e25db60c3 — matches the disclosed prefix and size before unzipping)

NOT read before freeze (honored): any claim *.py (incl. this claim's check.py, run_pos5.py, and
L1-0002b pos_lib.py), object/*, baseline_snapshot/*, other claims' object content, other skeptics' files.
All computations done from my own stdlib-only code written before freeze, from the prereg text
extracted from claim.yaml. After freeze I read run_pos5.py/check.py for a definitions diff only,
and ran check.py UNREAD beforehand (single execution, stdout+exit code captured).

Posters: prereg commit e8a2fab (2026-10-18 11:42:00 +0530) committed claim.yaml + check.py +
run_pos5.py, results commit 0c19e69 (11:43:33) added README/object/baseline only. 93 s prereg→results
is short but consistent with a deterministic pipeline run on an already-staged zip.

## 2. Environment

Windows 11 / PowerShell 5.1; Python 3.12.2800.0 (WindowsApps store build), stdlib ONLY
(json, glob, random, collections, math). All work + outputs in
C:\Users\Apoorv\AppData\Local\Temp\opencode\skP5-B\*. PYTHONUTF8=1 set (cp1252 console otherwise
crashes on cuneiform tokens).

## 3. Prereg spec extracted from claim.yaml

- Data: ETCSRI bulk zip (oracc.museum.upenn.edu/json/etcsri.zip), gdl_sign stream, line document
  order. Windows identical to L4-0002: N=1948, window seed 260417835 (KEY_SEED), lengths resampled
  from the Indus corrected-order pool (benchmarks/splits/v1/*.jsonl), token-weighted text choice,
  contiguous excerpts with modular wrap; both halves pooled, no key.
- Metric (imported from L1-0002b pos_lib): begin = index 0 of every window; end = last index of
  windows with len>1; n80 = number of top types whose cumulative tokens cover 80% of that position
  class; n80_all over all window tokens.
- PRIMARY GATE: |n80_begin - n80_end| strictly greater than max over B=200 paired token-shuffle
  draws (fixed window lengths, pool-shuffle after null_n80_end, begin+end counters per draw),
  null seed 260417840. Direction NOT preregistered. Fixed before any Sumerian positional number.

## 4. Rebuild (own code; scratch: common.py, null_sweeps.py, metrics.py, power.py)

Extractor (own, no claim code consulted): walk cdl; at each `l` node collect every `f.gdl` element's
`gdl_sign` in document order, descending into `seq` containers (det groups contribute children).
- 1457 files in corpusjson, 1 empty (Q001066.json) → 1456 texts with ≥1 sign (expected "~1456"):
  MATCH. 68,308 tokens, corpus-wide V=622 (builder documented cross-implementation drift 569–630:
  in band).
- Per-text streams cached to texts_gdl.json.

Windower (own): draw order ambiguity is legitimate pre-freeze; I ran BOTH plausible orders
(len→text→offset and text→len→offset) with random.Random(260417835), lengths pooled from
train+val+test jsonl (2364 lengths, pool mean 4.557), text ∝ token count, offset uniform 0..T-1,
tokens [(s+i) mod T]. Parse deltas recorded; n80 does not require V==370:

| variant | N | V | mean len | wrap% | n80 b/e/all | gap | tokens |
|---|---|---|---|---|---|---|---|
| len,text,off | 1948 | 396 | 4.60 | 7.9 | 68/69/71 | 1 | 8958 |
| text,len,off | 1948 | 389 | 4.58 | 8.2 | 70/75/73 | 5 | 8865 |
| builder (object) | 1948 | 370 | 4.61 | 7.3 | 72/67/72 | 5 | 8985 |

Window-seed sweep (own extra seeds; same build, draw order len,text,off): gap 1–3 across
window seeds 260417835/7/424242/123456789 (V 381–396, tokens 8.8–9.0k). The negative does not
depend on the particular window set. Top-10 begin/end types overlap almost entirely
(begin: AN NA KI A LUGAL MU NI KA BA E2; end: AN KI MU NI NA A LUGAL KA GA DA) as the README says.

## 5. Null sweeps (own; claim null numbers in brackets)

Paired pool-shuffle (fixed lengths; flatten windows, shuffle, deal) — my implementation of the
mirrored null_n80_end construction:

| null seed | real gap | gap max | min | median | builder gapmax |
|---|---|---|---|---|---|
| 260417840 (disclosed) | 1 / 5 | 10 / 9 | 0 | 2/3 | [12]* |
| 9900011 | 1 / 5 | 9 / 9 | 0 | 3 | — |
| 9900012 | 1 / 5 | 10 / 10 | 0 | 2 | — |
| 9900013 | 1 / 5 | 10 / 11 | 0 | 3 | — |

*builder's 12 comes from its exact window stream (V=370) + exact RNG consumption order; my
stream differs by the documented window-drift (V 396/389). 9–12 null max over B=200 is the
same band; the real gap (1–5) is an order below it in every construction.

WITHIN-WINDOW shuffle null (composition-preserving; the stress variant the prereg did NOT use):
gap max 11/9/10/9 at disclosed seed 260417840 and extras 9900011/12/13 — indistinguishable from
the pool-shuffle band. The negative is robust to BOTH null styles: under either, real gap 5 (or 1)
sits inside the null range. If window-composition had been secretly driving the gap metric, the two
null styles would separate; they do not.

## 6. Metric alternatives (all NON-GATED calibration commentary) + power

Ref histograms from the Indus split pool itself (corrected order as stored in the jsonl):
n80 begin/end = 99/27 (gap 72; L1-0002b reported 107/32 on its own 1948-dedup set — same effect size
class). Metrics on my primary window set (len,text,off), real vs null bands (min/max over B=200,
both styles × 2 seeds):

| alternative metric | real | null band(s) | inside? |
|---|---|---|---|
| JS^1/2(begin hist, end hist) | 0.2635 | [0.239, 0.293] | yes, all 4 sweeps |
| JS^1/2(begin, global) | 0.1820 | [0.168, 0.201] | yes, all 4 |
| JS^1/2(end, global) | 0.1834 | [0.170, 0.199] | yes, all 4 |
| fractional n80 gap (len-1 windows 0.5/0.5) | −2 | [−11, +12] | yes, all 4 |
| symmetric first2/last2 n80 gap | −1 | [−8, +8] | yes, all 4 |

(+ parallel runs of the second window variant: everything inside; JS^1/2 begin-end there 0.2590 in
[0.238, 0.293].) NO reasonable variant shows a positional specialization that beats its null. The
earlier-in-flight bug scare (all-JS-zero) was my own JS implementation error, fixed before any
reading was taken; nothing in this table predates the fix.

POWER (would the design detect an Indus-style effect on this same Sumerian skeleton?):
Pour Indus-style position behaviour onto my 1948-window skeleton (token[0] ~ P_begin(indus),
interior ~ global, token[-1] ~ P_end(indus), synthetic draws):
- c = 1 (full Indus effect): n80 b/e = 89/26 (@260417840) and 92/25 (@9900011); gap 63–67 vs
  SAME-construction null max 12–14 → detected 20/20. So YES, with numbers: an Indus-magnitude
  positional asymmetry (gap ~72–75, cf. 99/27 from the split pool) clears this design's null
  trivially, by ~5–6×.
- MDE sweep (end token drawn from c·P_end + (1−c)·P_global; 20 reps, B=60 null each):
  detect-rate 13/20 at c=0.05 (gap med 16), 17/20 at c=0.15–0.2 (gap med 19–20), 20/20 from
  c=0.3 up (gap med 23). Smallest reliably-detected effect ≈ gap ~20 at this scale, i.e. roughly
  a quarter of Indus's own gap. The prereg metric was therefore NOT under-powered at
  Indus-effect strength; only a weak (≤~25%-of-Indus) positional effect could hide from it, and
  the honest reading is "no effect even remotely this strong exists in Sumerian windows here".

## 7. Checker run (UNREAD before execution)

cd claims/L4/L4-0005-sumerian-positional-gates
python check.py --splits benchmarks/splits/v1 --scratch C:\Users\Apoorv\AppData\Local\Temp\opencode --object object/results.json --baseline baseline_snapshot/nulls.json

First invocation failed (FileNotFoundError sumer_lib path — my relative --splits resolved against
the claim dir, not repo root; not a checker defect, exit 1 before any recomputation). Rerun with
absolute --splits:

  n80 begin=72 end=67 all=72 gap=5 null_D_max=12 recompute=match
  FAIL
  EXITCODE=1

recompute=match (independent code path via sumer_lib/pos_lib rebuilds the windows and
regenerates the null from raw inputs; V=370 asserted before gating) and FAIL exit 1 is the
designed outcome for a negative (gate `gap > null max` cannot hold). object/results.json carries
"pass": false explicitly; numbers equal the README table and nulls.json (D range 0–12,
begin null range [64,77], end null range [62,76]).

## 8. Wording honesty

- The README scopes the negative correctly: "at Indus scale", specific position classes, this
  window protocol, against shuffle noise; reading 2 attributes the Indus effect to
  corpus/genre/loader conventions rather than universal claims. No "no positional structure ever"
  language. Title/claim disclose "direction not preregistered" (two-sided calibration cell).
- My fuller battery says the claim could even say slightly more: no signal in ANY tested variant
  (counts, fractional, 2-granularity, distribution-distance), not just in the prereg metric.
  The "well under detectable effect size" statement is quantitatively supported by §6.
- claim.yaml `result:` still reads "TBD — pipeline not yet run" and `status: draft` even though
  results commit 0c19e69 wrote README/object/baseline. The gate numbers live in object+checker
  and are mutually consistent, but the yaml is stale relative to its own commit pair; update
  result/status/skeptics at archivist time (see §9).

## 9. Objections / notes

1. STALE claim.yaml (§8): result/status must be synced before verification stamp. Blocking nothing
   in the numbers; process hygiene only.
2. Builder (run_pos5.py) + checker present in the PREREG commit (e8a2fab). Unusual order for
   "results-only-after-prereg" discipline, but transparent: the .py contain no numbers, the
   results commit is disjoint (README/object/baseline only), and the checker recomputes from raw
   inputs independently. No peeking channel identified.
3. results.json key `n_texts: 1948` is actually the window count (vocab/n_tokens are windowed
   quantities); mislabel, cosmetic, does not enter the gate.
4. Exact-reproduction nuance: true bit-exactness is delegated to the builder's own window stream
   (V=370; checker asserts it). My independent implementation drifted within the disclosed band
   (windowed V 396/389 vs 370; wrap 7.9/8.2% vs 7.3%; mean len 4.58–4.60 vs 4.61) and every
   conclusion is invariant (gap 1–5 real vs 9–14 null maxima). Verdict-level agreement throughout,
   matching the builder's own Sumerian drift disclosure (V 370 vs 395).
5. Null maxima vary 9–12 across implementations/streams at B=200 seeds; the claim's gate (single
   max vs gap) is sensitive to that scale in principle, but no legitimate variant brings null
   max under the observed gap 5, and the PREREG direction was two-sided. No pass/gap inversion
   found under any of: 2 window draw orders, 4 window seeds, 5 null seeds, 2 shuffle styles,
   5 metric variants.
6. Genre: royal-inscription excerpts with modular wrap, deterministic sign order — the
   "no asymmetry" reading is about these excerpts, not running prose; claim limitation already
   says so.

## 10. Log (ordered)

1. sha256 + size of staged etcsri.zip verified (214fd724…, 13,186,059 bytes). Unpacked to scratch.
2. Read claim.yaml/README (L4-0005), claim.yaml/README (L4-0002), L1-0002b claim.yaml,
   skeptic protocol, planner/TROPHY skim; benchmarks/splits/v1 listing+format; git show e8a2fab/0c19e69.
3. Wrote custom.py-equivalent common.py (extractor, lens pool, windower, n80); inspected corpusjson
   structure (Q000844/Q000835/Q000376 etc.).
4. Extract: 1456 texts, V=622, 68,308 tokens (texts_gdl.json).
5. Windower seed 260417835, two draw orders: V 396/389, n80 68/69/71 and 70/75/73.
6. Null seed 260417840 paired pool-shuffle B=200: gapmax 10/9; extras 9900011/12/13: 9/10/10/11
   (mean over variants). Within-window B=200 ×4 seeds: 10–11. Real gaps 1/5 inside all.
7. metrics.py: JS^1/2 + fractional n80 + first2/last2, B=200 bands × (pool, within) × 2 seeds:
   all real values inside; (fixed JS expression bug mid-way; rerun is authoritative).
8. power.py: Indus ref histograms 99/27; synthetic c=1 gap 63/67 vs nullmax 12/14 (20/20);
   MDE curve c=0.05→1.0 (detect 13/20 → 20/20; gap med 16 → 62).
9. Window-seed sweep 7/424242/123456789: gaps 3/1/3, V 384/391/381.
10. FREEZE → read object/results.json + baseline_snapshot/nulls.json (match README).
11. Ran check.py UNREAD (2nd attempt with absolute --splits path): recompute=match, FAIL, exit 1.
12. Post-freeze read of run_pos5.py + check.py for definitions diff (§7/§9 consistency).
13. Wrote this file; no repo modifications besides it.

skP5-B — 2026-10-18
