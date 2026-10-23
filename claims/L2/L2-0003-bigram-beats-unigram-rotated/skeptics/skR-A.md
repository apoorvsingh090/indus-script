verdict: reproduced

# skR-A — independent audit of L2-0003 (rotation: test Mohenjo-daro)

Skeptic id: skR-A. Fresh context; own code only, written from the claim text.
Work dir: `C:\Users\Apoorv\AppData\Local\Temp\opencode\skR-A\` (`audit.py`, `sweep.py`,
`sweep_pos.py`, `final.py`; stdlib only, no project code imported or read).

Inputs read: `claim.yaml`, `README.md`, `agents/skeptic-protocol.md`,
`benchmarks/splits/v2/{split.json,test.jsonl,train.jsonl,val.jsonl,SHA256SUMS}`.
Never read: `baselines/*.py`, `how-we-built-it/*`, `check.py` (source),
`object/*`, `baseline_snapshot/*`, other skeptics' notes, L2-0001 material.
`check.py` was executed black-box (`--help`, then one run) only after all
independent numbers were fixed.

Environment: Windows 10 Pro (2009), Python 3.12.10, stdlib only
(`json, hashlib, math, random, collections, pathlib, re`).

## 1. Splits verification (all pass)

- SHA256SUMS: all 4 entries match recomputed file hashes (split/test/train/val) → OK.
- Counts: train 1133 texts / 4533 tokens, val 194 / 883, test 1126 / 5625 — exact match.
- Sites: test = {Mohenjo-daro} only; val = {Dholavira, Kalibangan, Lothal};
  train has 0 Mohenjo-daro and 0 val-site texts (train top site Harappa, 970 texts).
  Train ∩ (test ∪ val) sites = ∅ → site-disjoint OK.
- Leakage rule (exact sign-sequence match vs train): 0/194 val, 0/1126 test → OK.
- Sign scheme: all signs match `G<num>`; train/val/test vocabs 388/188/469;
  190 test signs unseen in train.
- Open items (non-blocking): (a) the `splits_sha256 6996368c…` derivation is opaque —
  it is not the sha256 of SHA256SUMS, split.json, or concatenated jsonl bytes
  (candidates tested, none match); per-file SHA256SUMS integrity holds regardless.
  (b) Exclusion counts (val 14 / test 76) cannot be re-derived from frozen inputs
  alone (need pre-exclusion data); post-exclusion leakage is 0 as shown above.

## 2. Own reimplementation (stated tie-breaks)

Trained on TRAIN only, vocab = sorted train signs (V=388):
- Unigram: global train mode; ties → lexicographically smallest sign string.
  Top = G740 (n=538).
- Bigram (add-alpha argmax): score(c|prev) = c(prev,c)+alpha; for fixed prev the
  ranking is alpha-independent. Ties → lexicographically smallest sign string
  (variant with unigram-count tie-break was also tested — see below).
  Position 0 and unseen-prev contexts back off to the unigram prediction.
- Positional: per-index train mode; ties → lexicographically smallest;
  indices beyond train maxlen (13) → unigram.
- Bootstrap: paired per-token differences, own seed 31, B=2000
  (plus a second seed-7/B=5000 run).

TEST results (n=5625 tokens):
- Unigram: 611 hits = 0.1086 — EXACT match to claim.
- Bigram (lex tie-break): 1113 hits = 0.1979 — EXACT match to claim (any alpha;
  verified a=0.001 and a=1.0 give bit-identical prediction vectors).
  diff = 502/5625 = 0.0892 — exact match.
- Paired bootstrap diff CI95: seed-31/B=2000 → [0.0798, 0.0985];
  seed-7/B=5000 → [0.0796, 0.0988]; claim [0.0805, 0.0978].
  Same center; bounds agree within Monte-Carlo noise (~±0.001).
  Gate (CI-lo > 0 AND diff > 0.01): PASS under both of my runs.
- Tie-break note: pure-lexicographic tie-break reproduces 1113 exactly; the
  unigram-count-then-lex variant scores 1129 (0.2007). So the frozen pipeline's
  tie-break is evidently plain lexicographic — consistent with the claim's
  "tie-break unchanged" and immaterial to the gate either way (both pass).
- Alpha note: my val-NLL grid is minimized at alpha=0.1, not 0.001, so the
  frozen alpha-selection criterion is evidently not val-NLL as I formulated it —
  but since argmax predictions are provably alpha-invariant, the reported
  `a=0.001` cannot move any gated number. Non-issue for the gate.

## 3. Adversarials (gate survives both)

- (a) Force alpha=1.0: predictions bit-identical to a=0.001 (1129-variant also
  identical to itself); acc 0.1979, diff 0.0892, CI95 [0.0798, 0.0985] → PASS.
- (b) Positions ≥ 1 only (n=4499): uni 0.1343 / bi 0.2458 / diff 0.1116,
  CI95 [0.0994, 0.1234] → PASS with wider margin. Pos-0 backoff is not
  carrying the result.

## 4. Git order / threshold / wording

- `3e7dfb5` (2026-10-15 20:30:07 +0530): splits v2 frozen + L2-0003 preregistered
  gate, `result: "TBD — pipeline not yet run…"`, status draft.
- `bea3396` (2026-10-15 20:34:47 +0530): results + README, status
  under-skeptic-review. Prereg precedes results.
- `git diff 3e7dfb5 bea3396 -- claim.yaml`: `preregistered_threshold` text
  byte-identical; only `result`/`status` changed. The driver path fix
  (`parents[3]`→`[2]`) touches only `how-we-built-it/run_rotated.py`, one line;
  threshold untouched. (Driver source diff inspected via git only to confirm
  the one-line path fix; modeling code not read.)
- Wording: modest and matched to evidence — "beats unigram on held-out",
  "generality holds across rotation", positional "≈ unigram… recorded as found",
  limitations (single rotation; val-site reuse) stated in claim.yaml. No "solved"
  stretch. The README's "wider margin than v1's +5.8pp" is a cross-claim remark
  I did not verify (L2-0001 out of scope); not load-bearing for this gate.

## 5. Frozen checker (run last, black-box)

`python check.py --splits benchmarks\splits\v2 --object …/object/results.json
--baseline …/baseline_snapshot/unigram.json` →
`unigram=0.1086 bigram(a=0.001)=0.1979 diff=0.0892 CI=[0.0805,0.0978]` → PASS.
Checker output matches the claim numbers exactly. (Source never read.)

## Objections / residuals (none load-bearing)

1. Positional-model reconstruction gap (reported-only, ungated): my variants give
   564 hits (lex, 0.1003), 584 (unigram-tie-break, 0.1038), 767–779 for
   right-aligned / train+val variants — none reproduces the reported 612
   (0.1088). The reported value is exactly unigram+1 token and the claim's prose
   ("positional ≈ unigram… no predictive edge either way") is consistent with any
   of these, so the wording stands, but the positional recipe is not fully
   pinned down by the claim text. Does not affect the gated bigram-vs-unigram result.
2. `splits_sha256` derivation opaque (see §1); per-file hashes all verify.
3. Exclusion counts 14/76 taken on trust from `split.json` (post-exclusion
   leakage verified 0/0).

## Conclusion

Gated claim independently reproduced from frozen inputs with own code: splits
integrity/site-disjointness/leakage/counts all verify; unigram 0.1086 and bigram
0.1979 match to the token (611 and 1113/5625); diff 0.0892 with 95% CI lower
bound > 0 under two independent bootstrap seeds; both adversarials pass;
preregistration precedes results with threshold text unchanged; frozen checker
passes. `verdict: reproduced`.
