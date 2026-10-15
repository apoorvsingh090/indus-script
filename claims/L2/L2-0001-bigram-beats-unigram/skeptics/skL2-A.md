verdict: reproduced

# skL2-A — independent skeptic audit of L2-0001 (bigram beats unigram)

## Method / independence
- Fresh context; wrote own code in `C:\Users\Apoorv\AppData\Local\Temp\opencode\skL2A\`
  (`verify.py`, `diag.py`, `diag2.py`, `results.json`). Never read: `benchmarks/baselines/*.py`,
  `how-we-built-it/*.py`, `check.py` (file contents), `object/*`, `baseline_snapshot/*`,
  `skeptics/*.md`. Only read: `claim.yaml`, `README.md`, `agents/skeptic-protocol.md`,
  `benchmarks/splits/v1/{split.json,SHA256SUMS,train,val,test.jsonl}`.
- Model rules (mine, deterministic; all tie-breaks = sorted sign-string ascending):
  - Unigram: argmax train frequency (top = G740, 713/6527); same prediction at every position.
  - Bigram: add-alpha argmax; position-0 backs off to unigram top; unseen-prev contexts
    back off to unigram top (full-backoff primary). Alpha grid {0.001, 0.01, 0.1, 1.0} by
    VAL accuracy, ties -> smallest. (Argmax makes alpha provably irrelevant; verified.)
  - Positional slot: per-absolute-position train mode (pos 0,1,2,... from left);
    overlong positions -> unigram top (no test token needed it: train maxlen 19 > test maxlen 13).
  - Metric: top-1 accuracy over ALL token positions. Bootstrap: paired, text-level resampling
    (texts weighted by length implicitly), own seed 11, B=2000.
- `check.py` executed only at the end as black-box conformance (`--help` for args, then run);
  its contents were never read.

## Environment
- Windows 10 (2009), Python 3.12.10, git 2.51.0; repo `C:\Users\Apoorv\indus-script`, branch
  main (ahead 2). No extra packages (stdlib only: hashlib/json/collections/random).

## 1. Splits verification — PASS
- SHA256 recompute of all 4 files matches `SHA256SUMS` (split.json `41c9bf4b…`,
  test `1c2637e2…`, train `a3f48438…`, val `cf377d45…`).
- Counts exact: train 1365/6527, val 185/846, test 814/3400.
- Site-disjoint: test={Harappa}, val={Dholavira,Kalibangan,Lothal}, none in train's 49 sites. PASS.
- Leakage rule: 0/185 val and 0/814 test sequences occur in train. PASS
  (`split.json` excluded counts 23 val / 156 test consistent with filtering having occurred).

## 2. Reimplementation results — gate REPRODUCED exactly
| Model (test, all positions) | Mine | Claim |
|---|---|---|
| Unigram | 0.1162 (395/3400) | 0.1162 |
| Bigram (alpha=0.001, val-selected; all 4 alphas tied on val at 0.1832 = 155/846) | 0.1738 (591/3400) | 0.1738 |
| Diff | 0.0576 | 0.0576 |
| Paired-bootstrap 95% CI (mine: seed 11, B=2000, text-level) | [0.0447, 0.0691] | [0.0453, 0.0698] (seed 260417833) |
- CI lower bound > 0 AND diff > 0.01 with my own seed: gate PASS, independent of their seed.
- Note: exact bigram match (591/3400) requires full backoff (unseen-prev -> unigram top;
  134/2586 test pos>=1 contexts have unseen prev). Strict pos-0-only backoff (unseen -> smallest
  vocab sign G0) gives 0.1697 (577/3400), diff 0.0535, CI [0.0404, 0.0653] — gate still passes
  comfortably. The claim text says only "position-0 backs off", so the unseen-prev rule is
  under-specified in prose, but EITHER reading passes the gate; the full-backoff reading matches
  all claimed numbers to the token.

## 3. Adversarials — both survive
- (a) Force alpha=1.0 (skip val selection): bigram predictions are alpha-free under argmax
  (val acc identical 0.1832 for all 4 alphas); test stays 0.1738, diff 0.0576. Still beats
  unigram clearly. PASS.
- (b) Positions >= 1 only (drop pos-0 where bigram merely copies unigram):
  unigram 0.1462 (378/2586), bigram 0.2220 (574/2586), diff 0.0758,
  paired-bootstrap CI95 (seed 11, B=2000) [0.0591, 0.0914], lower > 0.
  The gate survives on genuine contextual predictions — the effect is NOT a pos-0 artifact
  (it is larger away from pos-0). PASS.

## 4. Git order (prereg before results) — PASS
- `6ffd459` "L2 harness … L2-0001 preregister (results TBD)": `claim.yaml` created with full
  `preregistered_threshold` and `result: TBD — pipeline not yet run`.
- `f27ef24` "L2-0001 results … (checker PASS); set-order determinism fix": results filled in later.
- Threshold text identical pre/post; no post-hoc gate movement.

## 5. Wording check — PASS (no stretch)
- Title/claim says "beats … on site-held-out next-sign prediction (top-1 accuracy, paired
  bootstrap)" with single-Harappa scope and limitations disclosed in-claim
  (single test site; vacuous object split). No "solved/deciphered" language. Matches what was shown.

## 6. check.py conformance (black box, run last) — PASS
- `check.py --splits …/v1 --object …/object/results.json --baseline …/baseline_snapshot/unigram.json`
  -> `unigram=0.1162 bigram(a=0.001)=0.1738 diff=0.0576 CI=[0.0453,0.0698] PASS`,
  identical under `PYTHONHASHSEED=99`. Matches my independent numbers.

## Objections / open items (non-blocking for the gate)
1. OBJECTION (minor, non-gated): positional number NOT reproduced by the standard reading.
   My absolute-position slot model gives test 0.1200 (408/3400), not the reported 0.1029
   (350/3400); train slots have zero ties, train maxlen covers all test positions, so neither
   tie-breaks nor backoff explain the gap. The 0.1029 figure is explicitly "reported (not gated)",
   so the gate is unaffected — but the claim prose should define the positional model precisely.
   Curiosity (hypothesis only, not verified against their code): a first/middle/last 3-bucket model
   scores exactly 350/3400 = 0.1029 on my run; right-aligned gives 0.1347; shifted variants give
   0.1082/0.0806. If their "slot" is a coarse bucketing, it should be stated.
   Also note: under my absolute-slot reading positional (0.1200) slightly *beats* unigram (0.1162),
   within noise, so the "positional UNDERPERFORMS" remark is definition-dependent.
2. Clarification request: state the unseen-bigram-context rule in the claim (full backoff vs
   uniform-tie); both pass the gate here, but future corpora with more unseen mass could diverge.
3. Not checked: corpus snapshot hash (`corpus_snapshot_sha256`) — raw corpus was out of scope for
   this audit; splits (the actual model inputs) verified by hash above.

## Bottom line
Splits genuine and leak-free; unigram/bigram/diff/CI reproduced to the token with independent code
and an independent bootstrap seed; both adversarials pass; prereg predates results; wording is
honest; black-box `check.py` PASSes. Non-gated positional definition needs a one-line spec fix.
