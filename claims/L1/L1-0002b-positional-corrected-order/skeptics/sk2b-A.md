verdict: reproduced

# sk2b-A — Independent skeptic audit of L1-0002b (corrected order)

Independent code: `C:\Users\Apoorv\AppData\Local\Temp\opencode\sk2bA\recompute_sk2bA.py`
(own seed 101, own B=100 token-shuffle null, fixed lengths; written without
reading `how-we-built-it/*.py`, `check.py`, `object/results.json`,
`baseline_snapshot/nulls.json`, or any `skeptics/*.md`).
Only inputs: `claim.yaml`, `README.md`, `agents/skeptic-protocol.md`,
dataset card `ds-readme.md` (loader convention), raw CSV.

## Environment

- Windows-11-10.0.26200-SP0, Python 3.12.10 (MSC v.1943 64-bit AMD64)
- No third-party deps: csv, hashlib, collections, math, random only
- Raw corpus: `C:\Users\Apoorv\AppData\Local\Temp\opencode\hf-indus\indus_website_real_corpus.csv`

## 1. SHA256 + orientation + dedup

- SHA256 computed: `7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8` — MATCHES `claim.yaml` (case-insensitive).
- Rows: 2543 (2544 lines incl. header). `reading_direction == "L-R"`: 2440 (reversed); `"R-L"`: 103 (kept as stored). Matches claim 2440/2543.
- Exact dedup AFTER orienting: 1948 texts. Matches claim.
- Vocab: 592 distinct signs. Matches claim.
- Total tokens 9080, mean length 4.6612 (9080/1948 ≈ 4.66). Matches claim.
- len<=1 texts: 11 (excluded from end counts under prereg convention).

## 2. n80 begin/end + own shuffle null

Convention (prereg): begin = index 0; end = index len-1 with len>1; middle = rest.
n80 = # distinct signs covering ≥80% of position tokens.

| Metric | Claim | Mine (seed 101, B=100) | Match |
|---|---|---|---|
| n80_begin | 107 | 107 | exact |
| n80_end | 32 | 32 | exact |
| null n80_end range | 67–85 (B=200, seed 260417832) | 69–84, mean 76.35 (B=100, seed 101) | band overlaps; gate unaffected |
| gate: end < begin AND end < null-min | PASS (32<107, 32<67) | PASS (32<107, 32<69) | reproduced |

Null detail (mine, sorted): min 69, max 84; full list in run log.
Margin is large (~37 below null-min), so seed/B differences cannot flip the gate.

## 3. Rigidity / site-V / hapax / Zipf (reported, not gated)

| Metric | Claim | Mine | Match |
|---|---|---|---|
| mean Cramer's V, top-10 (2×3: sign/other × begin/middle/end) | 0.1560 | 0.1560 (0.156) | exact to 3dp |
| Site V Mohenjo-daro (n=970) | 0.168 | 0.1683 with **per-site top-10**; 0.1641 with global top-10 | matches under per-site-top-10 reading |
| Site V Harappa (n=660) | 0.132 | 0.1320 with **per-site top-10**; 0.1426 with global top-10 | matches under per-site-top-10 reading |
| Hapax rate (type-based: hapax signs / vocab) | 0.3632 | 0.3632 (215/592) | exact |
| Zipf slope (log-log OLS, rank vs freq) | −1.4236 | −1.4236 | exact to 4dp |
| Mean length | 4.66 | 4.6612 | match |

Top-10 global signs (mine): G740, G2, G220, G32, G400, G240, G390, G520, G60, G861.
Per-sign V e.g. G740 0.391, G400 0.223, G520 0.198, G2 0.191 — mean 0.156.
Site text counts confirmed: Mohenjo-daro 970, Harappa 660 (post-dedup).
Cramer's V uses chi2/N with min(r,c)−1=1; verified by hand formula in code.

Note (minor ambiguity, not a failure): the claim does not state whether
site-V uses global or per-site top-10. I computed both; only the per-site
top-10 variant reproduces 0.168/0.132. Recommend the authors pin this
definition in words (one sentence). Direction ("same positional grammar",
M ≥ H) holds under either variant.

## 4. Adversarials (all run, gate survives each)

A. **len-1 texts counted as BOTH begin and end** (instead of excluded from end):
n80 107/33; own null (same convention, seed 101, B=100) min 69 max 85 →
PASS (33<107, 33<69). Survives (end shifts 32→33 only).

B. **Drop all len-1 texts entirely** (n=1937 kept):
n80 105/32; own null min 69 max 85 → PASS (32<105, 32<69). Survives.

C. **Per-site n80, Mohenjo-daro alone** (n=970, own null on that subset):
n80 96/23; own null min 60 max 82 → PASS (23<96, 23<60). Survives.
(Harappa alone for context: n=660, n80 82/25 — same direction.)

## 5. Git order + wording

- `git log --oneline`: `cac214e L1-0002b preregister` (2026-10-14 18:15:09 +0530)
  precedes `f991376 L1-0002b results` (2026-10-14 18:17:56 +0530). Order OK.
- Prereg `claim.yaml` at `cac214e` shows `result: TBD — pipeline not yet run`,
  with the full threshold text (corrected-order reversal rule, dedup-after-
  orienting, position convention, B=200/seed gate) already fixed; threshold
  text at HEAD is byte-identical in the `preregistered_threshold` field.
  (README's repair note about an early workdir run + `git reset` to `e41920f`
  is consistent with this history; deterministic seeds make the re-run
  identical, and my independent seed/B confirms the numbers are not
  seed-fragile.)
- Wording check: claim + README hedge correctly — "Sign IDs not comparable
  to M77 lists without a concordance — direction/count pattern only",
  "`"Corrected"` = loader convention only, not a claim about the script's
  true reading direction", "Literature mirror … same direction, same
  magnitude ratio" (not "same signs" / not "deciphered"). No overstatement
  found. Gated vs reported (not gated) metrics are explicitly separated.

## 6. Conformance (check.py run LAST, never read)

`python check.py --corpus <raw csv> --object object/results.json --baseline baseline_snapshot/nulls.json`
→ stdout: `corrected order: n80 begin/end = 107/32 null_min = 67` + `PASS`.
Exit 0. Conformance green from scratch.

## Objections / reservations (none blocking)

1. Site-V definition (global vs per-site top-10) should be stated explicitly;
   both variants agree on direction, only per-site reproduces the numbers.
2. Hapax "rate" is type-based (215/592); token-based would be 0.0237. The
   Nair comparison (0.33) is clearly the type-based one — fine, but worth
   one clarifying word ("type-based").
3. Null band moves slightly with seed/B (mine 69–84 vs theirs 67–85), as
   expected; the ~35-point margin makes the gate robust, confirmed by three
   adversarial variants above.

## Verdict rationale

Every load-bearing number (1948 / 2440 / 592 / 107 / 32 / 0.156 / 0.168 /
0.132 / 0.3632 / −1.4236 / 4.66) reproduced with independently written code
and an independent seed/null. Gate passes independently and survives all
adversarial position/site conventions. Prereg precedes results; wording is
appropriately hedged; checker passes. → `reproduced`.
