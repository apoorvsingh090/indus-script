verdict: reproduced

# SK4-A — Independent skeptic audit of L1-0004 (rebuttal-side control)

Role: INDEPENDENT SKEPTIC A. Fresh context, own code, own seed.
Read only: `claim.yaml`, `README.md`, `agents/skeptic-protocol.md` + raw CSV.
Did NOT read: `how-we-built-it/*.py`, `check.py` (executed only, `--help` + full run), `object/results.json`, `baseline_snapshot/real_point.json`, `skeptics/*.md`.

## Environment
- OS: Windows (win32), PowerShell 5.1
- Python 3.12.10 (MSC v.1943 64-bit AMD64), numpy 2.4.6 (only for version report; repro uses stdlib `random`, `math`, `csv`, `hashlib`)
- Own code: `C:\Users\Apoorv\AppData\Local\Temp\opencode\sk4A\repro_sk4A.py`, seed 31337
- Raw corpus: `C:\Users\Apoorv\AppData\Local\Temp\opencode\hf-indus\indus_website_real_corpus.csv`
- Claim dir: `C:\Users\Apoorv\indus-script\claims\L1\L1-0004-zipfian-control-distance\`

## 1. SHA256 / orient + dedup / Zipf fit / real MM
- SHA256(CSV) = `7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8` — matches `claim.yaml:corpus_snapshot_sha256` (case-insensitive). PASS.
- Raw rows: 2543 (header + 2543? 2544 lines incl header → 2543 data). Raw distinct strings: 1918.
- Orient rule applied independently: reverse tokens iff `reading_direction == 'R-L'` (103 R-L, 2440 L-R). Post-orient dedup: **1948 texts** — matches claim's "same 1948 lengths". Total tokens 9080, mean len 4.6612. Vocab observed 592 (V=592 confirmed).
- Own log-log OLS Zipf fit (x=log rank, y=log freq, slope=-s): **s = 1.423604** — matches claim s=1.4236 to 4dp. PASS.
- Own MM base-592 implementation (re-derived to match numbers, not copied):
  - H1n = (H1_ML + (m1-1)/(2N)) / ln(592), N=9080
  - C = (H2_ML_joint + (m2-1)/(2Nb) − H1_MM) / ln(592), Nb=7132 bigrams (no cross-boundary), m2=observed bigram types
  - Real: **(H1n,C) = (0.756139, 0.416650)** — matches claim (0.7561,0.4167) to 4dp. PASS.

## 2. Own iid-Zipf synthetic (self-fit s, same lengths, seed 31337)
- Method: p(k) ∝ k^-s, k=1..592, V=592, per-text iid draws at the 1948 deduped lengths, `random.Random(31337)`, inversion via cumulative table, integer tokens 0..591 (label-permutation invariant for (H1n,C)). Same MM code as real.
- Result self-fit s=1.4236: **(H1n,C) = (0.485871, 0.419872)**
- Claim's synth (seed 260417831): (0.4816,0.4189). Difference ~0.004 in each coordinate — expected sampling variation across seeds. No contradiction.
- Distance: ΔH1n=0.270268, ΔC=0.003222, **d=maxΔ=0.270268 ≥ 0.05 → PASS (distinguishable)**. Matches claim d=0.2746 within seed noise.
- Nuance confirmed: **C-alone matches** (0.4199 vs 0.4167, Δ=0.003), **H1n separates** (Δ=0.27). Exactly Rao's-reply structure reported in README. PASS.

## 3. Adversarial tests
### 3a. BORROWED slope s=1.46 (Nair, not self-fit), same seed 31337, same lengths
- Synth s=1.46: **(H1n,C) = (0.464347, 0.406614)**
- ΔH=0.291792, ΔC=0.010037, **d=0.291792 ≥ 0.05 → verdict SURVIVES** (indeed larger d than self-fit 0.2703).
- Table:
  - self-fit s=1.4236 → d=0.2703
  - borrowed s=1.46 → d=0.2918
- Borrowing Nair's constant does not flip the gate; if anything it strengthens separation (lower s-entropy → lower H1n). Objection "self-fit was cherry-picked to inflate d" fails.

### 3b. HALF-SPLIT stability (hash-of-sequence halves)
- Split sorted-dedup set by SHA256(sequence string) rank: half1=974, half2=974.
- half1 real: (0.755434, 0.382397); half2 real: (0.749654, 0.382704).
- Stability: H1n within 0.0007/0.0065 of full (0.7561); C both ~0.382, ~0.034 below full 0.4167 (smaller-N bias, symmetric across halves). Half–half maxΔ ≈ 0.034.
- d(synth_self-fit vs half1-real)=0.2696, d(vs half2-real)=0.2638 — both ≥0.05 with ~8× margin over half–half jitter (0.27 vs 0.034). **Not a small-sample artifact.** PASS.
- Note: full-corpus C > half C is expected direction for this MM-difference estimator under smaller Nb; does not threaten the comparison since synth and real use identical N/Nb and estimator.

## 4. Git order + wording check
- `git log --oneline -- claims/L1/L1-0004-zipfian-control-distance`: `d7c6b4c preregister (2026-10-14 18:17:25)` before `bf4b49d results (2026-10-14 18:17:57)`. PASS (prereg before results).
- Prereg stat: `check.py + claim.yaml + how-we-built-it/run_zipf.py + zipf_lib.py`, no `object/results.json` / `baseline_snapshot/` — threshold fixed before synthetic numbers. Gate in claim.yaml is directional (d≥0.05 = distinguishable = PASS; d<0.05 = counterexample succeeds, equally publishable). No HARKing structure.
- Wording: `claim.yaml:limitations` + `README.md` both state "One counterexample family (iid Zipf) ... does not close the broader rebuttal, only this instance" and "MM estimator ... DISTANCE comparison uses same estimator". **One-family-doesn't-close-rebuttal caveat PRESENT.** No "solved"/"deciphered" stretch. PASS.

## 5. Their checker (run last, not read)
- `python check.py --corpus <hf csv> --object object/results.json --baseline baseline_snapshot/real_point.json`
- Output: `s=1.4236 real=(0.7561,0.4167) synth=(0.4816,0.4189) d=0.2746 / PASS: distinguishable`
- Expectation met: PASS. Green from scratch against raw corpus. (Only `--help` + this invocation executed; file contents never opened.)

## Objections considered and disposition
1. C-alone match could be quoted to claim indistinguishability — rejected as gate is joint maxΔ preregistered; README explicitly reports C-match nuance, no hiding.
2. Borrowed-sensitivity — tested s=1.46, gate survives (d=0.29).
3. Small-N artifact — half-split shows real point stable (jitter 0.034 << d 0.27).
4. Estimator dependence (MM vs NSB) — acknowledged in claim limitations; distance uses same estimator both sides, so comparison is fair even if absolutes shift. No objection to L1 gate.
5. Single family — explicitly caveated; not counted as closing Sproat's broader casebook.

## Verdict rationale
All core numbers reproduced from raw inputs with independent code/seed within sampling noise; adversarial variations preserve d≥0.05; prereg order, hash, wording, and checker all green.

verdict: reproduced
