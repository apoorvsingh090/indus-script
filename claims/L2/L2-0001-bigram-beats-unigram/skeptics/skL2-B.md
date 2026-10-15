verdict: reproduced

# skL2-B — Independent skeptic audit of L2-0001 (bigram beats unigram, Harappa held-out)

Skeptic: B (independent, fresh context). Own code only, own seed 22, B=2000.
Workdir: `C:\Users\Apoorv\AppData\Local\Temp\opencode\skL2B\` (`skl2b.py`, `llprobe.py`, `posprobe.py`).
Read allow-list respected: only `claim.yaml`, `README.md`, `agents/skeptic-protocol.md`,
frozen splits (`benchmarks/splits/v1/*.jsonl`, `split.json`, `SHA256SUMS`), raw corpus CSV.
Never opened: `benchmarks/baselines/*.py`, `how-we-built-it/*.py`, `check.py` (run blind at the end),
`object/*`, `baseline_snapshot/*`, other skeptics' notes.

Environment: Windows (win32), Python 3.12.10, numpy 2.4.6. Checker run with `PYTHONHASHSEED=99`.

## 1. Independent reimplementation (seed 22, B=2000, paired bootstrap over texts, length-weighted)

- Models written from scratch: unigram argmax (train top = G740, prior 0.1092);
  bigram add-alpha argmax with sorted-vocab tie-break, position-0 and unseen-prev back off to unigram top;
  positional = per-absolute-position train marginal argmax, unseen positions back off to unigram top.
- Val selection over {0.001, 0.01, 0.1, 1.0}: all four tie at 0.1832 → smallest alpha 0.001 (matches claim).
- TEST (814 texts / 3400 tokens):
  unigram 0.1162 / bigram(a=0.001) 0.1738 / diff 0.0576 — exact match to 4dp.
  Own 95% CI [0.0455, 0.0697] vs claimed [0.0453, 0.0698] (their seed 260417833; delta fully explained by seed).
  Gate (CI lower bound > 0 AND diff > 0.01): PASS, with wide margin.

## 2. Leakage audit from RAW csv (main job) — CLEAN

- Order normalization re-derived independently: R-L raw kept as-is, L-R raw reversed.
  All 2364 split texts match normalized raw sequences exactly (0 mismatches).
- Harappa raw total = 970. Train-sequence overlap recomputed from raw: exactly 156 overlap,
  814 non-overlap. Test id-set EQUALS the non-overlapping id-set exactly (0 in either direction).
- ZERO test sequences occur in train (sequence-set intersection = 0).
- Within-test duplication: 618 unique seqs of 814 texts (290 texts in duplicate groups — expected for this corpus).
  Top-10 most frequent test seqs cover 90 texts / 13.2% of test tokens but contribute only
  38/591 = 6.4% of bigram's correct predictions. The win is NOT carried by a handful of formulaic repeats.
  (Most frequent test seq: G501 G405 G2 G240 G520 ×29.)

## 3. Adversarial: 156 excluded texts put BACK (all 970 Harappa, same trained models)

- Full Harappa: unigram 0.1221 / bigram 0.1842 / diff 0.0621, CI95 [0.0503, 0.0741] → gate still PASSES.
- Excluded-only (n=156): unigram 0.1686 / bigram 0.2656 (higher absolute accuracy = memorisable material,
  but the diff survives on the full set regardless).
- Conclusion: the exclusion is NOT load-bearing; if anything it is conservative (diff grows from 0.0576 to 0.0621).

## 4. Secondary: mean log-loss direction — NOT confirmed under matched smoothing (non-gated)

- With add-alpha smoothing applied symmetrically (unigram and bigram, gated a=0.001):
  unigram 7.4931 bits vs bigram 7.6181 bits → bigram is WORSE, direction opposite to report.
- Direction flips for larger alphas (a=0.01: 7.3643 vs 6.9623; a=0.1: 7.2365 vs 6.8787; a=1.0: 7.1344 vs 7.5734).
  So the log-loss secondary is smoothing-dependent and does not hold for the gated alpha under the natural
  implementation. Non-gated, so no verdict impact — but the reported direction needs a stated smoothing rule.

## 5. Git order + wording

- `6ffd459` (preregister: harness + frozen splits v1 + threshold, results TBD) precedes
  `f27ef24` (results + determinism fix). Order is correct; threshold pre-fixed.
- Wording check: title claims "beats unigram on site-held-out next-sign prediction" — matches what was shown
  (single held-out site, top-1 accuracy, paired bootstrap). No "solved"/generality stretch; single-site limitation
  is disclosed in claim.yaml. PASS.

## 6. Blind checker run (last, unread)

- `check.py --splits …/v1 --object …/object/results.json --baseline …/baseline_snapshot/unigram.json`
  → `unigram=0.1162 bigram(a=0.001)=0.1738 diff=0.0576 CI=[0.0453,0.0698] / PASS`. Matches claim to the digit.

## Objections / notes (none load-bearing)

1. Positional secondary not reproduced: natural absolute-position marginals give 0.1200 ( skeptics' code:
   left-aligned 0.1200, right-aligned 0.1347, relative-decile 0.1350, joint (pos,len) 0.1159) vs reported 0.1029.
   Formulation undisclosed in allowed reads; non-gated, recorded as found.
2. Log-loss direction (above): smoothing-dependent; needs a stated rule. Non-gated.
3. Val tie across all four alphas means alpha selection is vacuous for accuracy (argmax invariant) — fine,
   but the tie-break rule "smallest alpha" then interacts with the log-loss secondary (smallest alpha = worst log-loss).

Verdict rationale: the gated claim (diff 0.0576, CI clear of zero, exclusion clean and non-load-bearing,
checker green) reproduces exactly under fully independent code. Secondaries queried, gate unaffected.
