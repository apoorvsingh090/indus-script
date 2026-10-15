verdict: reproduced

# skR-B — independent audit of L2-0003 (delegation integrity + leakage angles)

## Environment
- OS: Windows (win32, PowerShell 5.1); Python 3.12.10, numpy 2.4.6
- Repo HEAD at audit time: `bea3396`; working tree clean (one unrelated untracked dir only)
- Own code: `C:\Users\Apoorv\AppData\Local\Temp\opencode\skR-B\audit.py` (written from scratch, no claim/benchmark code read)
- Own seed: 32, B=2000 paired bootstrap (requirement was B>=1000)
- Inputs used: `benchmarks/splits/v2/*.jsonl` + raw corpus `hf-indus/indus_website_real_corpus.csv` only. Never read: `benchmarks/baselines/*.py`, any L2-0001/L2-0003 code (`how-we-built-it/*`, `check.py` source), `object/*`, `baseline_snapshot/*`, `skeptics/*.md`. `check.py` executed (not read) once, at the end.
- Read for context only: claim `claim.yaml`, `README.md`, `agents/skeptic-protocol.md`.

## 1. Reimplementation (own models) — numbers confirmed exactly
- Protocol rediscovered blind from data: token-level next-sign prediction; unigram predicts train argmax (G740, n=538/4533); bigram predicts argmax P(w|prev) with lex tie-break, unseen-context/pos-0 backoff to unigram. Order normalization verified against raw CSV for all 2453 v2 rows: reverse iff `reading_direction == 'L-R'` (0 mismatches).
- v2 TEST (1126 texts / 5625 tokens), train-fitted, my seed-independent point estimates:
  - unigram 611/5625 = **0.1086** ✓ (claim 0.1086)
  - bigram(a=0.001 behavior; accuracy is alpha-invariant given tie-break) 1113/5625 = **0.1979** ✓ (claim 0.1979)
  - diff = **0.0892** ✓ (claim 0.0892)
- Paired bootstrap with MY seed 32, B=2000:
  - token-level: CI95 **[0.0796, 0.0988]** vs claimed [0.0805, 0.0978] — same center/width, lower bound comfortably > 0 ✓
  - text-cluster variant: [0.0800, 0.0981] (same conclusion; gate robust to bootstrap unit)
  - Gate (CI lower > 0 AND diff > 0.01): **PASS** under my seed too.

## 2. DELEGATION AUDIT (main job) — rotation is real, not a v1 re-run
Observable-behavior checks (IDs + site fields only, no code):
- Test purity: all **1126/1126 test rows carry `site == "Mohenjo-daro"`** ✓
- Train composition: **970 Harappa + 163 from 47 other sites = 1133**; Mohenjo-daro count in train = **0** ✓ (mirror image of v1's "Mohenjo-daro + rest" train)
- Val sites: Dholavira 70 / Kalibangan 48 / Lothal 76 — identical site set to v1 (documented val reuse; leakage-free vs new test since val sites ∩ test site = ∅) ✓
- v1-vs-v2 test ID overlap: **0 / 814 / 1126** — disjoint ✓
- Rotation proof: **all 1126 v2-test IDs are members of the v1 train set** (1126/1126) — i.e. the held-out site genuinely swapped sides; a re-run of the v1 pipeline would have reproduced the 814 Harappa test IDs, which it does not.
- Conclusion: the "thin wrapper over L2-0001's frozen pipeline" delegates modeling but the *evaluation* is observably a new rotation. No delegation fraud.

## 3. ADVERSARIAL — leakage restoration (76 excluded texts)
- Recomputed from RAW CSV independently: normalized every raw sequence (L-R reversed), built train-site sequence set (all sites except Mohenjo-daro/Dholavira/Kalibangan/Lothal) → **1202** Mohenjo-daro raw texts, of which **76** have sequences seen in train sites. Matches claim exactly (76 excluded; 1126 + 76 = 1202; 0 of the 76 appear in v2 test). Exclusion list is honest, not cherry-picked.
- Re-scored all 1202 with MY models: unigram 0.1103 / bigram 0.2020 / **diff 0.0916, CI95 [0.0824, 0.1013] → gate still PASSES** with leakage included. Leakage slightly *inflates* the gap (+0.0024), so the exclusion is conservative; the finding does not depend on it.
- Log-loss (alpha=0.001, same smoothing): unigram 5.3377 vs bigram **5.3948** — bigram is WORSE at the gated alpha (overconfident sparse model; 80% miss rate at ~7.3 nats each). Direction bigram<unigram does NOT hold at a=0.001; it holds only for heavier smoothing (a=0.01: 4.84<5.21; a=0.1: 4.70<5.09; flips back at a=1.0). Accuracy/log-loss dissociate here. The claim's gate is accuracy-only so this does not fail the claim, but any "bigram is a better probabilistic model" gloss would be unsupported at the reported alpha.

## 4. Git order + wording
- `3e7dfb5` (2026-10-15 20:30 +0530) froze v2 splits + preregistered the rotated gate ("results TBD") BEFORE `bea3396` (20:34) reported results. Correct preregistration order ✓
- Wording check: "bigram beats unigram with sites rotated (test Mohenjo-daro, train Harappa+rest)" — accurate. "Wider margin than v1's +5.8pp" — my diff 0.0892 ✓. "Positional ≈ unigram (0.1088 vs 0.1086)" — see objection O2. "Single rotation only" limitation is disclosed ✓. No "solved" stretch ✓
- Their checker run last (unread, executed only): `check.py --splits v2 --object object/results.json --baseline baseline_snapshot/unigram.json` → `unigram=0.1086 bigram(a=0.001)=0.1979 diff=0.0892 CI=[0.0805,0.0978] PASS` ✓

## Objections (none gate-failing)
- O1 (minor, informational): log-loss at gated alpha favors unigram (5.3377 < 5.3948). Suggests future claims separate accuracy-alpha from probability-quality claims.
- O2 (minor, auxiliary-number mismatch): the reported positional 0.1088 (612/5625) is NOT reproduced by plain train slot-argmax under either lex (564 → 0.1003) or unigram-frequency (584 → 0.1038) tie-breaks; 612 is exactly what slot-argmax + backoff-to-unigram on low-support slots (7+) yields. Since the implementation is frozen/opaque to me by design, I flag that the positional figure depends on an undocumented backoff choice. It does not affect the gate (bigram−unigram), and qualitatively "positional ≈ unigram" still holds (0.100–0.109 in all variants).
- O3 (design note, already disclosed): val sites reused from v1 — accepted as documented; val is leakage-free vs the new test site.

## Bottom line
Gated numbers reproduced exactly under an independent seed; rotation verified as genuine via disjoint test sets and full v2-test⊂v1-train containment; the 76-text exclusion recomputed exactly from raw and shown to be conservative (gate passes with or without it). `verdict: reproduced` with two minor non-gate objections above.
