verdict: reproduced
# skS-A independent audit — L4-0002 partial negative confirmed

- claim: `claims/L4/L4-0002-sumerian-hidden-key` (read `claim.yaml` + `README.md` + `agents/skeptic-protocol.md` only at start)
- mode: fresh context, own code in `C:\Users\Apoorv\AppData\Local\Temp\opencode\skS-A\`
- forbidden respected: did NOT open `how-we-built-it/*.py`, `check.py`, `object/results.json`, `object/key.json` (until step 4), `baseline_snapshot/*`, `skeptics/*.md` before step 4. Only listed directory names. `check.py` executed blind at end (`--help` + run, never read).
- allowed inputs only: `C:\Users\Apoorv\AppData\Local\Temp\opencode\etcsri.zip` + `benchmarks/splits/v1/*.jsonl` lengths.

## env
- OS: Windows (win32, PowerShell 5.1)
- python3: 3.12.10
- git: 2.51.0.windows.1
- own seeds: windowing 20261015, ENT nulls 6000-6099 (B=100), REP nulls 7000-7099 (B=100), L2 bootstrap 8000 (B=1000)
- scripts: `skS-A/audit_gates.py`, `audit_chain.py`, `audit_open.py`, `audit_perm.py` (independent implementations)

## 1. extraction (own `gdl_sign` recursive walk)
- zip `corpusjson` files: 1457
- empty files: `['etcsri/corpusjson/Q001066.json']` (0 bytes) — matches task expectation
- nonempty texts: 1456, zero-sign nonempty: 0
- total Sumerian tokens (my extraction): 69416, mean text len 47.68
- V corpus-wide (my raw `gdl_sign`, no filtering): 630 (claim says 569)
  - OBJECTION/NOTE: +61 types vs builder. Likely builder filters/normalizes (damage markers, determinative handling, or variant folding) not documented in `claim.yaml`. I did no filtering. Difference does not affect verdict; see windowing below.
- Indus pool (train+val+test `*.jsonl`): n=2364, mean 4.5571, min 1 max 19

## windowing (own contiguous-excerpt + token-weighted + modular wrap, N=1948)
- procedure: sample 1948 lengths with replacement from Indus pool; per window choose text with prob proportional to token length; uniform start in `[0,Tl)`; take `L` tokens with modulo wrap; flag wrap if `start+L>Tl`.
- sampled lengths mean 4.5652 (claim 4.61), min 1 max 19
- windowed tokens 8893, V_win 395 (claim 370), mean_len 4.5652, wraps 136, rate 0.0698 (claim 7.3% / 0.0729, mean 4.6124)
- assessment: 1456 + Q001066 empty CONFIRMED exactly; mean/wrap within 1%/0.3pp; V_win 395 vs 370 (+6.8%) consistent with my larger raw V (630 vs 569). Order and separation confirmed; exact match not expected with independent RNG/extraction.

## 2. three gates (own estimators, own null seeds) — all PASS
- ENT (own: bigram conditional entropy `H(w_i|w_{i-1})` MLE bits, within-window only):
  - real 3.4587, null B=100 min 4.9084 max 4.9953 mean 4.9621 → `real < min` PASS (wide, ~1.45 bits margin)
  - claim: `C 0.447 < null-min 0.627` PASS — different normalization, same conclusion.
- L2 (own: unigram-top vs bigram-MAP next-sign accuracy, train A=first 974 windows, test B=last 974):
  - A→B uni 0.0687 bi 0.2757 diff 0.2070 n=3449; B→A uni 0.0707 bi 0.2820 diff 0.2114 n=3496
  - paired bootstrap B=1000 on B test windows, alpha 0.001 two-sided 99.9% CI [0.1755,0.2359]; CI-lo>0 and diff>0.01 PASS (wide)
  - claim: `d=0.1540 [0.1405,0.1687]` PASS — my diff larger (independent windows/estimator) but same verdict.
- REP (own: distinct repeated trigram-type count rep3 + 4-gram-type count rep4, within-window n-grams):
  - real rep3 549 rep4 306; null B=100 rep3 max 80 mean 63.1, rep4 max 3 mean 0.72 → both > maxima PASS (wide)
  - claim: `612/317 vs 83/4` PASS — magnitudes match closely (549≈612, 306≈317, null 80≈83, 3≈4), confirming my interpretation of rep definition is correct.
- conclusion: sensitivity on real Sumerian at Indus scale CONFIRMED with fully independent code/seeds.

## 3. key chain (no content read beyond hashing)
- (a) sha256(bytes of `object/key.json`) = `3b6a6c1daccd40ee02ea76b03e9338924fb1b0edf47ea5c6e52403d9b263c517` — matches prereg `key_commitment_sha256` in `claim.yaml` exactly. Hashed via `hashlib.sha256(open(...,'rb').read())`, did not print/parse.
- (b) git history (`git -C indus-script`):
  - `1da3312 L4-0002 preregister` : `claim.yaml` has `key_commitment_sha256 3b6a6c1d…` + `result: TBD — pipeline not yet run`; `ls-tree` shows NO `object/key.json`, NO `object/results.json`, NO `README.md`, NO `baseline_snapshot/`; files: `check.py`, `claim.yaml`, `how-we-built-it/run_sumer.py`, `sumer_lib.py`.
  - `3ef214d L4-0002 results` : adds `object/key.json`, `object/results.json`, `README.md`, `baseline_snapshot/sumer.json`; `diff --name-status 1da3312..3ef214d` = `A README.md, A baseline_snapshot/sumer.json, M check.py, M claim.yaml, A object/key.json, A object/results.json`.
  - `claim.yaml` diff prereg→results: `preregistered_threshold` UNCHANGED; only `result` TBD→PARTIAL NEGATIVE and `status` draft→draft+comment changed.
  - order: `1da3312` precedes `3ef214d` (`git log --oneline -- <claim>` shows `3ef214d` on top of `1da3312`). Commitment precedes reveal. PASS.
  - per README disclosure: prereg amended twice pre-results (parents path fixes; key resized 569→370 as design input before any gate number) — consistent with `M check.py` in diff and threshold text stability.

## 4. sealed files opened only after chain (confirm 5/10 + permutation)
- `object/key.json`: JSON list len 370, `set==set(range(370))` True, min 0 max 369 unique — valid permutation of 370. No other fields.
- `object/results.json`:
  ```json
  {"n_texts":1948,"vocab":370,"wrap_rate":0.0729,"mean_len":4.6124,
   "ent":{"C":0.4467,"null_min":0.6272,"pass":true},
   "l2":{"acc_u":0.0675,"acc_b":0.2215,"diff":0.1540,"ci":[0.1405,0.1686],"pass":true},
   "rep":{"rep3":612,"rep4":317,"null3_max":83,"null4_max":4,"pass":true},
   "hidden_key":{"top10_hits":5,"pass":false}}
  ```
  - `top10_hits 5 < 7` FAIL as claimed; gates all `pass:true`, key `pass:false` → partial negative exactly as stated.

## 5. wording honesty
- `claim.yaml result`: `PARTIAL NEGATIVE — ENT+L2+REP pass … hidden-key exact-rank 5/10 <7 … checker FAIL on key arm as designed` — honest, does not claim solved/cleared.
- `README.md`: table shows KEY `5/10` vs `≥7/10` FAIL bold; mechanism section (9/10 membership stable but mid-rank shuffling LUGAL 3→5 etc.) presented as post-hoc probe, future work L4-0003 candidate, not as excuse to move bar. Prereg amendments + alpha-no-val-split deviation explicitly disclosed.
- caveats present: (i) one-family/genre: `contiguous excerpt windows (token-weighted, modular wrap); royal-inscription genre only, not running prose`; (ii) transparent-box: `builder generated the key (procedural commitment, disclosed); recovery validity does not depend on builder blindness`; (iii) license: `CC0 per-file-header; eme-gir CC BY-SA caution — attribute+link, never vendor`. All in `claim.yaml limitations` + README. PASS.
- title still says `recovered 7+/10 by rank mapping` — this is the prereg *prediction*, while `result` clearly states 5/10 FAIL; slightly confusing in isolation but standard prereg format (threshold vs outcome) and README/claim result disambiguate. Not a stretch of “solved”.

## 6. builder checker run last (never read)
- cmd: `python check.py --splits benchmarks/splits/v1 --scratch skS-A/check_scratch (with etcsri.zip pre-staged) --object object/results.json --baseline baseline_snapshot/sumer.json --key object/key.json`
- output: `ENT 0.447<0.627 L2 d=0.1540 [0.1405,0.1687] REP 612/317 vs 83/4 KEY 5/10 recompute=match`
- exit: `FAIL` (code 1) — expected FAIL on key arm. Matches `results.json` and README exactly.

## objections / notes
- Minor: corpus-wide V 630 (mine, raw) vs 569 (builder) and windowed 395 vs 370 — needs one-line builder note on filtering/normalization to make exact reproduction possible. Not load-bearing: gates pass widely either way; key V=370 matches windowed claim, so key sizing is consistent with builder’s filtered vocab.
- Minor: `corpus_snapshot_sha256` field stores fetch description, not a hex hash; acceptable as fetch-at-build pointer but not a verifiable pin. Mitigated by my re-fetch from local zip (13,186,059 bytes) reproducing stats.
- No objection to negative framing; mechanism (exact-rank too strict for flat mid-rank) plausible and disclosed as post-hoc. Did not independently re-run cipher rank-recovery (per task, commitment verified instead); validity of 5/10 rests on builder `check.py recompute=match` which I observed.
- Independent rank-recovery not attempted (would require key, forbidden until step 4, and task explicitly says verify chain instead). No evidence of peeking: threshold text frozen, sha matches, key absent at prereg.

## log
- `audit_gates.py` output: ENT 3.4587 vs null-min 4.9084 PASS; L2 diff 0.2070 CI [0.1755,0.2359] PASS; REP 549/306 vs 80/3 PASS; windows 1948/8893/395/6.98%.
- `audit_chain.py`: sha match True; prereg TBD/no-key → results adds key/results.
- `audit_open.py`/`audit_perm.py`: key 370 perm 0-369 True; results 5/10 pass False.
- checker: FAIL as designed.
