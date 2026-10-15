verdict: reproduced

# skL4-B — Independent skeptic audit of L4-0001 (fresh context, own code)

Claim: linguistic@1948 passes ENT+L2+REP; N_min ENT<=250 / L2=500 / panel=1000; emblem L2-negative at all N.
Scope: read only `claim.yaml` + `README.md` + `agents/skeptic-protocol.md`. Did NOT read `how-we-built-it/*.py`, `check.py` (executed only, last), `object/*`, `baseline_snapshot/*`, `skeptics/*.md`, `benchmarks/baselines/*.py`, any L1 code. Allowed raw inputs only: P&P text (fetched + sha-verified below) + splits-v1 lengths pool (2364 lengths, 10773 tokens).

## 1. Provenance / raw inputs (verified myself)

- P&P: `https://www.gutenberg.org/cache/epub/1342/pg1342.txt`, LF-normalized sha256 = `7c13190c04773de0a919e38450ecaac1673fbd572a60bad784ff8421acdfec18` — MATCHES `claim.yaml`. Body words (`[A-Za-z']+` on body between `*** START`/`*** END`): 128565 — MATCHES. Lowercased types: 6729 — MATCHES `~6729 types`.
- Lengths pool: `benchmarks/splits/v1/{train,val,test}.jsonl` signs-lengths (allowed as lengths source). N=2364 texts, 10773 tokens, length histogram 1:19, 2:366, 3:422, 4:479, 5:439, 6:254, 7:194, 8:80, 9:52, 10:24, 11:21, 12:7, 13:3, 14:3, 19:1; mean 4.557. Resampled with replacement.
- GEN_SEED 260417834 used for exact headline cells. Own seeds (9001+ / 777 / 9100s / 9200s) for variants. Eval seeds fixed: ENT-null 1001, REP-null 2001, L2-split 3001, L2-boot 3002 (exact cells); variants use 9xxx seeds (documented in log).

## 2. Own implementation (assumptions documented; exact formula was underspecified)

- Linguistic-like: 1948 lengths via `random.Random(GEN_SEED).randrange` over 2364-pool, then contiguous excerpts: uniform start in lowercased P&P stream, nested prefixes 250/500/1000/1948.
- Emblem-like: same-length resample (independent draw, same seed mechanism); vocab OP 8 uniform / CORE 40 Zipf s=1.0 / CL 6 uniform; L==1: 1xCORE; L==2: OP+CL; L>=3: OP+(L-2)xCORE+CL; 5% per-token replacement by unique `SINGn` (literal reading of "5pct singletons").
- ENT (MM-C): within-text bigram conditional `H(Y|X)` with Miller-Madow `(M-1)/2N` on `H1`/`H12` (nats), normalized by `log V` (base-V, alphabet-agnostic). Null: B=100 global token permutation re-chunked to same lengths; gate `C < null-min`.
- REP: distinct repeated trigram/4-gram types (`count>=2`, overlapping, within-text only). Null B=100 same shuffles; gate `rep3>null-max AND rep4>null-max`.
- L2: random 60/20/20 text split + leakage rule (drop val/test seqs seen in train, as spec); unigram = train mode (pos0 backs off to mode); bigram = MLE `argmax c(prev,nxt)` (add-α does not change top-1 argmax, so VAL selection over {0.001,0.01,0.1,1.0} ties → smallest α=0.001, per spec); test top-1 accuracy all positions; diff=`bi-uni`; paired bootstrap B=1000 over test positions, 95% percentile CI; gate `CI-lo>0 AND diff>0.01`.
- Code lives in `C:\Users\Apoorv\AppData\Local\Temp\opencode\skL4B\` (`gen.py`, `gates.py`, `run_head.py`, `run_adv.py`, `mech.py`); this report is the only file touched inside the repo.

## 3. Headline cells (own code, GEN_SEED exact)

| cell | ENT C vs null-min | L2 diff [CI] (uni/bi) | REP rep3/rep4 vs null-max | gate |
|---|---|---|---|---|
| ling@250 | 0.2295 < 0.2389 PASS | 0.0359 [0.0090,0.0628] PASS (0.0359/0.0717) | 3/0 vs 1/0 FAIL (rep4 tie) | ENT-only |
| ling@500 | 0.2698 < 0.2865 PASS | 0.0200 [0.0067,0.0356] PASS (0.0245/0.0445) | 9/0 vs 3/0 FAIL (rep4 tie) | ENT+L2 |
| ling@1000 | 0.3120 < 0.3425 PASS | 0.0344 [0.0195,0.0494] PASS (0.0344/0.0689) | 39/5 vs 6/1 PASS | ALL-PASS |
| ling@1948 | 0.3474 < 0.3873 PASS | 0.0382 [0.0281,0.0495] PASS (0.0337/0.0720) | 150/29 vs 14/1 PASS | ALL-PASS |
| emb@250 | 0.5146 < 0.5691 PASS | -0.0365 [-0.0777,0.0046] FAIL | 27/2 vs 20/2 FAIL (rep4 tie) | ENT-only |
| emb@500 | 0.5363 < 0.6005 PASS | -0.0047 [-0.0187,0.0093] FAIL | 102/7 vs 55/5 PASS | ENT+REP |
| emb@1000 | 0.5185 < 0.5806 PASS | -0.0088 [-0.0164,-0.0025] FAIL (neg) | 239/30 vs 143/9 PASS | ENT+REP |
| emb@1948 | 0.4889 < 0.5500 PASS | -0.0086 [-0.0141,-0.0025] FAIL (neg) | 576/79 vs 398/23 PASS | ENT+REP, L2-neg |

Comparison to claimed: ling@1948 claimed `0.362<0.407 / 0.0490 [0.0376,0.0603] / 110/7 vs 13/1` — mine `0.347<0.387 / 0.0382 [0.0281,0.0495] / 150/29 vs 14/1`: same PASS pattern, same order of magnitude; rep4 higher in mine (vocab 1798 vs claimed 1613 — see §6). Emblem@1948 claimed `0.615<0.705 / -0.0230 [-0.0317,-0.0148] / 668/98 vs 487/27` — mine `0.489<0.550 / -0.0086 [-0.0141,-0.0025] / 576/79 vs 398/23`: absolute ENT differs (normalization detail) but PASS holds; L2 significantly negative in both (CI excludes 0 on the negative side); REP magnitudes strikingly close. Exclusions (leakage rule): mine emb@1948 val-drop 81 / test-drop 68; claimed "83 at 1948" — same order (theirs likely test-only or total-val; either way template collisions grow with N as described). Ling exclusions ~0-2 (expected for diverse English).

N=250 linguistic L2 borderline — CONFIRMED with seed-sensitivity nuance: my fixed split (3001) PASSES, but 4/8 neighboring split seeds FAIL with CI lower exactly `0.0000` (splits 2,3,42: diffs 0.0190/0.0183/0.0198, CIs `[0.0000,0.0427]` etc.), matching the claimed `0.0289 [0.0000,0.0586] FAIL`. N=500 fixed-split PASSES but 2/8 splits FAIL — so the power cliff is real; N_min L2=500 is the first passing grid size on the fixed split, not a split-robust threshold. N_min ENT<=250 holds (PASS at 250); full-panel 1000 holds (REP rep4-tie fails at 250 and 500, passes at 1000).

## 4. Adversarials (both, own seeds)

(a) WORD-SHUFFLED linguistic@1948 — global permutation (shuffle seed 9001, eval seeds 9002/9003/9004/9005, same Zipf marginals, syntax destroyed): ENT `0.3881 vs min 0.3872` FAIL; REP `8/0 vs 13/1` FAIL; L2 `diff -0.0063 CI [-0.0148,0.0028]` FAIL (uni 0.0369/bi 0.0307). All three FAIL — no gate passes on shuffled words, no flag. Methods detect order, not Zipf. Note shuffled ENT (0.3881) sits just above null-min (0.3872), as expected for a null-draw.

(b) BELOW-GRID N=100 linguistic — GEN_SEED nested prefix with own eval seeds (9101-9104): ENT `0.1861 vs 0.1922` PASS (marginal); REP `2/0 vs 1/0` FAIL; L2 `0.0000 [0.0000,0.0000]` FAIL. Own-seed regeneration (gen seed 777, eval 9201-9204): ENT `0.1600 vs 0.1593` FAIL (marginal the other way); REP `0/0 vs 1/0` FAIL; L2 `0.0099 [-0.0396,0.0495]` FAIL. Full panel FAILS at N=100 in both (2-3/3 gates fail); ENT at N=100 is borderline (pass/fail flips with sample), consistent with `ENT<=250` and confirming the floor is real — N=250 ENT-pass is not vacuous for the panel (panel still fails below grid), though ENT alone is sensitive down to ~100.

## 5. Mechanism probe (emblem@1948, reported, no gate)

Unigram does not win because OP/CL masses dominate as individual types: the overall mode is CORE1 at 13.05% (1156/8857 tokens), while each OP is ~2.6% and each CL is ~3.5% (group masses OP 20.7% / CL 20.7% / CORE 53.8% / SING 4.7%). The train-mode baseline (CORE1) scores 12.85% overall but 0.0% on position-0 (323/323 miss, since 94.3% of first tokens are OP) and 16.0% on later positions; the bigram scores 12.0% overall with 15.0% on later positions — i.e. it loses even where OP/CL position effects are removed. This is expected under the template: CORE draws are iid Zipf independent of the preceding OP/CORE and CL draws are uniform independent of the preceding CORE, so `P(next|prev)` carries no signal and the memorized prev→next map only overfits train noise, ending significantly below the marginal mode. First-is-OP 94.3% / last-is-CL 94.4% (remainder = 5% singleton replacements) confirms the template fired as designed.

## 6. Git order + wording checks

- Order: `f25ea2c` (2026-10-15 12:18:58 +0530) preregisters gate + N_min sweep (`check.py`, `claim.yaml` with `result: TBD`, generators); `6e484bd` (2026-10-15 12:21:12) adds `README.md`, `baseline_snapshot/gates.json`, `object/results.json`, fills `result`. `git diff` on `claim.yaml` shows `preregistered_threshold` byte-identical across the two commits; only `result`/`status` changed. Threshold+splits fixed before numbers — PASS.
- Wording: title/claim says sensitivity "on linguistic-like synthetic (N_min reported); emblem-like profile characterized", "L2 bar discriminates in this setup", "One family only: no general non-linguistic exclusion claimed", transparent-box + reduced-budget limitations stated. Matches what was shown; no "solved/deciphered" stretch — PASS.
- Checker: `python check.py --splits benchmarks/splits/v1 --scratch <tmp>/scratch --object .../object/results.json --baseline .../baseline_snapshot/gates.json` → prints per-N ENT/L2/REP lines and `PASS` (exit 0). Executed last, file never opened for reading. Note it fetched P&P over network into scratch (as designed).

## 7. Objections / limitations (do not overturn verdict)

1. Generator underspecified: "5pct singletons" mechanism ambiguous. Literal 5%-of-tokens (mine) gives emblem vocab 471 (54 base + 417 singletons) vs claimed ~266; 5%-of-CORE-only would give ~292 (closer); 5%-of-texts would give ~151. Ling vocab 1798 (250:472) vs claimed 1613 (250:426) — 11% high, likely lengths-RNG or excerpt-sampling detail. Lengths-RNG stream, excerpt start-sampling (overlapping vs sequential), case handling (lowercased assumed — matches 6729), and random-split seed are not pinned in `claim.yaml`. Absolute ENT numbers therefore differ (mine ling 0.347 vs 0.362; emb 0.489 vs 0.615) though pass/fail and magnitudes for REP/L2 match closely.
2. Split-seed fragility: N=250 L2 flips 4/8 splits; N=500 flips 2/8. `N_min L2=500` should be read as fixed-split grid minimum with the power-cliff caveat (already hinted by "touches 0.0000"), not a seed-robust floor. Pin the split seed or report split-seed distribution in future work.
3. Budgets B=100/1000 vs production 200/2000 and single emblem family / transparent-box (not hidden-key) are disclosed limitations — accepted, and the claim explicitly disavows general non-linguistic exclusion.

## 8. Env + repro

- Windows 10/11, Python 3.12.10, numpy 2.4.6, git 2.51.0. No forbidden files read. Rebuild code: `C:\Users\Apoorv\AppData\Local\Temp\opencode\skL4B\` (`gen.py`, `gates.py`, `run_head.py`, `run_adv.py`, `mech.py`, `diag_*.py`, `pp` texts, `lengths_pool.json`). Only repo file created: `claims/L4/L4-0001-synthetic-calibration/skeptics/skL4-B.md` (this file).

Novelty/DoF: not a literature-novelty claim (calibration of frozen L1/L2 methods); no multiple-comparison correction needed beyond the pre-fixed per-gate minima/maxima rule (B=100 nulls, B=1000 bootstrap, 95% CI); thresholds pre-fixed per git history above.
