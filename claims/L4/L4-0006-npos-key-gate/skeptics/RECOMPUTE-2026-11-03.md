# L4-0006 recompute log — 2026-11-03

Status: **draft remains draft.** This file records two recomputes of the
frozen grid. Neither is a fresh-context skeptic report; the required
≥2 fresh-context skeptic gate has **not** been met.

## Why this is not the skeptic gate

The daily loop requires ≥2 fresh-context skeptics to rebuild the claim
independently. On 2026-11-03 the subagent backend was unreachable from
this session:

```
general (sk6-A): Cannot connect to API: Was there a typo in the url or port?
general (sk6-B): Cannot connect to API: Unable to connect...
qwen-max probe:  Cannot connect to API: Unable to connect...
```

Two further skeptic launches were aborted. No fresh context could be
created, so no `sk6-*.md` reports exist. `claim.yaml` keeps
`skeptics: []` and `status: draft`.

Disclosure: both recomputes below were run by the archivist in the same
session that produced the claim. The independent arm did not import the
claim's method code, but it is **not blind** (the archivist had already
read the implementation) and shares the frozen input pipeline. It raises
confidence in the numbers; it does not substitute for fresh skeptics.

## Arm 1 — shipped checker

```
python claims/L4/L4-0006-npos-key-gate/check.py \
  --splits benchmarks/splits/v1 --scratch <cached etcsri.zip> \
  --object object/results.json --baseline baseline_snapshot/gate6.json
```

Output (exit 0):

```
alpha*=0.5 committed=2/10 full=0.07526881720430108 null_max=0.03763440860215054 recompute=match gate=FAIL
PASS
```

`recompute=match` covers the dev table, all three gate keys, both cipher
halves, the 12 nulls, and the gate verdict. Checker wallclock ≈ 1.6 h
(single process).

## Arm 2 — independent rebuild

Script: scratch-only (`repro_independent.py`), not committed. It imports
only `sumer_lib` (`sign_texts`, `indus_lengths`, `windows`, `encipher`,
`make_key` — the frozen input pipeline) and reimplements the rest from the
prereg prose: reference bigram/unigram stats, position-resolved stats,
rank-init and restart starts, full-sweep steepest-ascent swap search,
total objective, top-10 metric, permuted-reference nulls, and the gate.
The swap-delta algebra was unit-tested against full rescoring on a
synthetic instance (max error 5.1e-13) before the grid ran.

Reproduced values (identical to `object/results.json` in every field,
including start indices and swap counts):

| Arm | Claim | Independent |
|---|---|---|
| dev α = 0.001 / 0.01 / 0.1 / 0.2 / 0.5 / 1.0 | 4 / 4 / 4 / 3 / 9 / 7 | same |
| α* | 0.5 | 0.5 |
| committed @974 | 2/10, full 0.075269, 265 swaps | same |
| alt1 @974 | 3/10, full 0.051075, 265 swaps | same |
| alt2 @974 | 5/10, full 0.059140, 311 swaps | same |
| cipher halves A / B | 6/10, 3/10 | same |
| null_max (K=12) | 0.037634 | same |
| null multistart spot checks | 0.029570, 0.013441 | same |
| gate | FAIL (keys_ge8=0) | FAIL |

Independent wallclock 2540 s with 7 worker processes, run concurrently
with Arm 1 (contention included). `FULL_MATCH` on a field-by-field
comparison.

## Consequence

The object is reproducible by two code paths. L4-0006 remains **draft**
until two fresh-context skeptics can be spawned; the scientific result
(CONFIRMED NEGATIVE; full-key separation is the informative metric) is
unchanged. The named follow-up — a gate built on full-key separation —
can be preregistered without waiting, because it is a new claim with its
own frozen thresholds.
