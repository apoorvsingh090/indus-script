verdict: reproduced

# SK4-B independent skeptic audit — L1-0004 Zipfian-control distance

Skeptic ID: sk4-B. Fresh context, own code, own seed 987654. No imports from claim repo.
Read only: claim.yaml, README.md, agents/skeptic-protocol.md. Did not read how-we-built-it/*.py,
check.py (ran blind last), object/results.json, baseline_snapshot/real_point.json, skeptics/*.md.

## Environment
- Python 3.12.10 (MSC v.1943 64-bit AMD64), stdlib only (csv, hashlib, math, collections, random, json)
- Corpus file: C:\Users\Apoorv\AppData\Local\Temp\opencode\hf-indus\indus_website_real_corpus.csv
- Own code: C:\Users\Apoorv\AppData\Local\Temp\opencode\sk4B\sk4b_repro.py (+ sk4B_numbers.json)
- Seeds: 987654 (primary), 987655, 987656 (threshold stress); uniform + Nair cross-check reuse 987654
- Git HEAD at audit: bf4b49d

## 1. SHA256 + orient/dedup + real MM point + Zipf fit + synthetic → d
- SHA256(indus_website_real_corpus.csv) = 7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8
  matches claim.yaml corpus_snapshot_sha256 (case-insensitive). PASS.
- Raw rows: 2543. Raw distinct without orient: 1918. Oriented (reverse R-L → L-R, normalize to
  majority L-R) then dedup: 1948. Matches claim "same 1948 lengths" and README cross-check
  note (1948 vs L1-0001 1918). Orient rule inferred as reverse-R-L; verified by count.
- Estimator reconstructed independently as Miller-Madow, base-592 logs:
  H1_MM = H1_MLE + (m-1)/(2N); H2_MM = H2_MLE + (mb-1)/(2Nb); H1n = H1_MM/ln592;
  C = H2_MM/ln592 − H1_MM/ln592, with N = total tokens, Nb = total bigrams (N − ntexts).
  Real: N=9080, m=592, Nb=7132, mb=3054 → H1n=0.756139…, C=0.416650….
  Rounded (0.7561, 0.4167) exactly matches claim.yaml/README. PASS.
- Own log-log OLS Zipf fit over all 592 ranks (ln freq vs ln rank): slope −1.42360389 → s=1.4236,
  R²≈0.961, exactly matches claimed s=1.4236. No borrowed constants. PASS.
- Own synthetic (iid p(k)∝k^−s, V=592, same 1948 lengths, random.Random seed 987654):
  H1n=0.4905, C=0.4270, m=398, mb=1889 → d=max(|ΔH1n|,|ΔC|)=0.2656 ≥ 0.05. Gate PASS.
  Their-seed spot check (260417831, same method): H1n=0.4816 exact match, C=0.4216 vs
  claimed 0.4189 (Δ0.0027, sampling noise; H1n dominates d=0.2746 match). Confirms pipeline.

## 2. Adversarials (both done)
(a) UNIFORM-OVER-592 synthetic, same lengths, seed 987654 (random.Random uniform 0–591):
    H1n=1.00000338, C=0.46591979, m=592, mb=7077.
    Distance from real: max(0.2439, 0.0493)=0.2439. FAR from real, H1n≈1.0 as predicted.
    Metric space not degenerate; uniform does not collapse onto real. Sanity PASS.
(b) THRESHOLD STRESS — three independent Zipf draws, own fit s=1.4236:
    987654: (0.4905, 0.4270) d=0.2656 (ΔH1=0.2656, ΔC=0.0103)
    987655: (0.4864, 0.4191) d=0.2698 (ΔH1=0.2698, ΔC=0.0024)
    987656: (0.4841, 0.4212) d=0.2720 (ΔH1=0.2720, ΔC=0.0046)
    min d = 0.2656, margin over gate ≈0.216 (≈5× gate), std ≈0.003.
    No draw near/below 0.05. Gate NOT fragile. Separation is stably in H1n; C-alone gaps
    are 0.002–0.010 (confirming C-alone match nuance). PASS.

## 3. Nair-slope cross-check (s=1.49, one draw seed 987654)
- Synthetic s=1.49: H1n=0.4540, C=0.4033, m=364, mb=1614 → d=0.3022 ≥ 0.05.
  Verdict survives; steeper slope increases H1n gap (0.302 vs ~0.27). Plausible and
  consistent with "same ballpark" note. PASS.

## 4. Git order + wording checks
- `git log -- claims/L1/L1-0004*`: d7c6b4c preregister 2026-10-14 18:17:25 +0530
  ("preregistered_threshold d≥0.05 … result: TBD — pipeline not yet run") precedes
  bf4b49d results 2026-10-14 18:17:57 +0530. Order correct; threshold + definition
  (MM, base-592, corrected order, post-orient dedup, V=592, same lengths, seed, own-fit s,
  directional with Sproat-side negative equally publishable) fixed before numbers. PASS.
- Wording: title "…is entropically distinguishable…(supports Rao's reply)" is scoped by
  limitations ("One counterexample family…does not close the rebuttal, only this instance")
  and README nuance ("C alone matches…separation is in H1n…Both sides get something").
  No "solved/deciphered" stretch. Real-C shift vs L1-0001 (0.4167 vs 0.4098) explained by
  1948-vs-1918 dedup set; reproduced counts support it. PASS with minor note below.

## Checker (run last, blind)
- `python check.py --corpus … --object … --baseline …` → 
  `s=1.4236 real=(0.7561,0.4167) synth=(0.4816,0.4189) d=0.2746 / PASS: distinguishable`.
  Expect-PASS met. PASS.

## Objections / notes (non-blocking)
1. Sampler dependence: my random.Random vs likely numpy Generator gives C jitter ~±0.003
   (my C 0.4216–0.4270 vs claimed 0.4189) but H1n/d match to ~0.004; gate margin 0.21 dwarfs it.
   Recommend recording sampler (numpy vs stdlib) in generator for exact bit-repro.
2. C definition (H2_MM − H1_MM with mismatched N/Nb) is estimator-dependent by construction;
   claim already discloses MM-dependence. Distance comparison uses same estimator both sides,
   so objection is noted but does not break the gate.
3. Prereg→results gap 32 s same-day; order verified via git, no evidence of threshold edit
   after seeing numbers (prereg diff shows TBD). Accept.
4. Uniform C=0.4659 is only 0.049 above real C — a future single-metric-C claim would be
   fragile; the joint (H1n,C) gate as preregistered is what saves it. No change requested.

## Conclusion
All core numbers reproduced from raw inputs with independent code/seed; both adversarial
sanity checks pass; threshold stable (min d 0.2656); Nair cross-check survives; git order,
wording, and blind checker all green.
