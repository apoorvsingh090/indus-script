# L0-0003 — G↔P concordance v0.1: 22 clean bijective pairs from 161 shared texts (2/2 skeptics)

Closes the biggest piece of the Phase-1 scheme debt: the G-592 scheme
(indus_website, all L1/L2 claims) had **no bridge at all** to the
P/W/M/V world (L0-0002's pwm-v01). This claim derives one structurally:
mayig's 179 P-coded Mohenjo-daro unicorn seals joined to the G corpus by
M-number (161 shared), aligned positionally on equal-length texts.
Reproduced by skL0-C and skL0-D (own code, blind checker runs
`recompute=match gate=PASS`).

## How (preregistered, deterministic)

- Join: `cisi_number` M-form on Mohenjo-daro G rows ↔ mayig `M-###X` ids →
  161 shared texts (design input, disclosed at prereg).
- G side in corrected order (`reading_direction == "L-R"` reversed — the
  repo-wide convention since L1-0002b). P orientation chosen by rule:
  aggregate top-pair count **741 reversed vs 267 as-stored** → reversed.
  This is itself a convention finding: mayig side sequences are stored
  opposite to the G corrected order.
- 140 equal-length (G-row, P-side) pairs → 768 aligned positions over 192
  G-signs / 164 P-signs.
- clean = support ≥ 5 texts, two-way consistency ≥ 0.9, top-source both
  directions; contested carries a reason; unmapped = tail (n_g < 5).

## Result — GATE PASS

| Class | Count | Notes |
|---|---|---|
| clean | 22 | bijective; top supports G2→P122 60/63, G740→P324 75/76, G220→P050 27/29 |
| contested | 19 | split-convention clusters: G861/G817→P385, G803/G806→P364, G900/G920→P154, G550/G798→P230; rest low-consistency |
| unmapped | 151 | n_g < 5 in the shared unicorns — evidence ceiling by design |

Reconciles 22+19+151 = 192 G-signs observed; no silent drops. **Holdout
(report-only):** mapping inferred without every 5th shared text predicts
held-out positions at clean-mapped signs with **0.980 accuracy (48/49)**.

## Composition with pwm-v01 (report-only)

All 22 clean P codes appear in pwm-v01; **15 chain clean-1:1 through to
M-codes** (e.g., G220→P050→M059, G233→P058→M072, G235→P060→M065). The
G→P→W/M/V bridge now exists for the most frequent signs; the scorecard's
scheme-debt list shrinks from "G unbridged" to "G bridged for 15-22 clean
+ 19 contested high-frequency signs, tail open."

## Limits

- Type-level and provisional — frequency/position evidence, not glyph
  identity proof; the contested clusters are where the two transcriptions
  split signs differently (complementary text distributions per skL0-D).
- Evidence base is 161 unicorn seals (~768 positions): only frequent signs
  can clear support ≥ 5. Extending the bridge needs more shared texts
  (ICIT/M77 index remains the blocked path).
- Same-object guarantee rests on M-number equality across two independent
  digitizations; exclusions: 18 mayig-only M-numbers, 1027 M-daro G rows
  whose M-numbers have no mayig counterpart, and 14 M-daro G rows with no
  M-form cisi_number at all.

## Skeptic qualifications (2/2 reproduced; folded in, gate unaffected)

- **Threshold-stable core is 16 pairs** (skL0-C, skL0-D): 6 of the 22
  clean pairs sit exactly at support 5 and drop under support ≥ 6 or
  consistency ≥ 0.95. Compose downstream claims on the stable core or
  re-justify thresholds.
- **Coincidental floor ≈ 0** (skL0-D): random equal-length pairing yields
  0/200 clean pairs (max top-pair count 11 vs the real 75) — the mapping
  is positional evidence, not a numbering artifact.
- **No duplicate inflation** (skL0-D): 161/161 shared G sequences are
  distinct; dedup rerun is a no-op despite the formulaic genre.
- Contested *reason labels* are underdetermined by the prereg (skL0-D's
  ordering: 17 reverse-conflict / 2 low-consistency vs shipped 15/4) —
  classes and evidence counts are identical.
- Equal-length-only alignment discards 21 shared texts (no indel
  modeling) — conservative; edit-distance variant is v0.2 future work.
- Provenance caveat: indus_website `cisi_number` values may derive from
  concordance cross-referencing; the permutation control shows the bridge
  does not depend on it.
- CSV amendment post-review: unmapped rows now ship top-pair + true
  evidence counts (skL0-C objection; classification unchanged).

## Reproduce

```
python how-we-built-it/build_gp.py <mayig_repo@ad2f1e2> <indus_website_real_corpus.csv@47e8616d> <claim_dir> <repo_root>
python check.py --mayig <dir> --corpus <csv> --object object/results.json \
  --baseline baseline_snapshot/counts.json --concordance ../../../../data/concordance/gp-v01.csv
```
