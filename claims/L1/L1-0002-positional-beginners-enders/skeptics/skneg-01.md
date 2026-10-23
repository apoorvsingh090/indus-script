verdict: reproduced

# skneg-01 — independent skeptic recomputation of L1-0002 (negative claim)

Independent skeptic. Fresh context, own code only
(`C:\Users\Apoorv\AppData\Local\Temp\opencode\skneg\skneg_recompute.py`),
own seed 7, B=150 global-permutation shuffles. Did NOT read
`how-we-built-it/*.py`, `check.py` (until final conformance run),
`object/results.json`, or `baseline_snapshot/nulls.json` before recomputing.
Inputs read: `claim.yaml`, `README.md`, `agents/skeptic-protocol.md`,
raw CSV `hf-indus/indus_website_real_corpus.csv`, dataset card `ds-readme.md`.

## 1. Corpus identity + dedup

- SHA256 of raw CSV: `7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8`
  — matches `claim.yaml:corpus_snapshot_sha256` exactly.
- Raw rows: 2543. Exact-dedup on `sign_sequence` as-stored (stripped string):
  **1918** unique — matches claimed 1918.
- Deduped lengths: min 1, max 19, mean 4.693; 11 len-1 texts (begin-only),
  0 empty. N_begin = 1918, N_end = 1907 (len>1 only), per prereg convention
  (begin = index 0; end = index len-1 with len>1).
- Token pool (deduped): 9001 tokens, 592 distinct signs (matches G-scheme size).

## 2. n80 recomputation (as-stored order)

Definition used: n80(slot) = smallest k such that the top-k sign types cover
>=80% of slot tokens. Slot counters from as-stored, deduped texts.

- n80_begin = **27** (223 distinct begin types; top: G740 669, G400 178, G520 138)
- n80_end = **103** (370 distinct end types; top: G820 116, G861 110, G817 103)
- Matches claimed 27/103 exactly.

## 3. Own shuffle null for n80_end

Method: global permutation of the 9001-token pool, re-chunked into the 1918
fixed text lengths, n80 recomputed on end slot; RNG `random.Random(7)`, B=150.
(Builder used B=200, seed 260417829; mine is intentionally independent.)

- Null n80_end: min **68**, max **88**, mean 77.39.
- Claimed null: min 69, max 87. Mine is 1 wider on each side — ordinary
  sampling variation from different seed/B, and immaterial: real n80_end=103
  exceeds BOTH null maxima by ~15, so the gate outcome is insensitive to it.
- Prereg gate: need `n80_end < n80_begin (27)` AND `n80_end < null_min`.
  Observed: `103 < 27` False; `103 < 68` False. **Gate NOT met — confirmed.**

## 4. Cause confirmation (loader convention)

Dataset card (`ds-readme.md`) quotes:

- L105: `` `sign_sequence` | string | Space-separated sign IDs, left-to-right as stored (see `reading_direction`) ``
- L110: `` `reading_direction` | string | `"R-L"` means use `sign_sequence` as stored; `"L-R"` means reverse it before use. A loader-convention flag, not a claim about the script's actual reading direction. `indus_website` has a genuine mix of both values (per-inscription, source-provided) ``
- L136-139 (conversion notes): "**Reading direction (`indus_website`).** The original conversion had sign order backwards. Caught by a diagnostic checking for a published fingerprint (final sign position should show lower entropy than initial position); confirmed correct after reversal."

My count from raw CSV: L-R = **2440**, R-L = 103, other = 0 (2440/2543 = 95.95%).
Matches claimed "2440/2543 rows are L-R". As-stored analysis therefore swaps
begin/end for ~96% of texts — cause statement confirmed. (I did not verify the
L1-0002b corrected-orientation result; out of scope for this negative claim.)

## 5. Git order (prereg before results)

`git -C C:\Users\Apoorv\indus-script log --oneline` (top, dates 2026-10-14):

- `e41920f L1-0002 preregister: positional asymmetry gate (threshold fixed, results TBD)`
- `c2e006f L1-0002 negative recorded (as-stored gate not met; loader-convention cause)`

Prereg `e41920f` is the parent-older commit; negative record `c2e006f` comes
after it. `claim.yaml`-scoped log shows exactly these two commits in that order.
Prereg-before-results confirmed. (Same-day commits, so ordering rests on git
topology, which is unambiguous here.)

## 6. Checker conformance (run last, not read first)

After the above recomputation, ran (from claim dir):

`python3 check.py --corpus <raw CSV> --object object/results.json --baseline baseline_snapshot/nulls.json`

- Output: `n80 begin/end = 27/103 null_min = 69` / `FAIL: gate not met`
- Exit code: **1 (non-zero)** — expected FAIL for a negative claim. Checker
  numbers agree with my independent recomputation (null_min 69 vs my 68 is the
  seed/B difference noted above).

## 7. Objections / caveats

- NO load-bearing objection. The negative finding reproduces: gate-not-met is
  confirmed by a wide margin under my own seed/B.
- Minor notes: (a) null min/max differ by 1 from the builder's (68/88 vs 69/87)
  — expected with independent seed/B, does not affect the verdict; (b) all four
  L1-0002 commits share date 2026-10-14, so temporal preregistration relies on
  commit topology rather than wall-clock separation — topology here is clean;
  (c) n80 definition (top-k covering >=80%) was inferred from the name/values
  rather than a spec sentence, but exact numeric match (27/103) validates the
  inference; (d) novelty/literature check (Adhikari, Nair values) not re-audited
  beyond noting the claim's own limitations section — not needed for a
  gate-not-met confirmation.

## Environment / log

- Windows PowerShell 5.1, Python 3.12.10, git 2.51.0.windows.1
- Script: `C:\Users\Apoorv\AppData\Local\Temp\opencode\skneg\skneg_recompute.py` (seed 7, B=150)
- Full stdout saved in run log (numbers above copied verbatim).

## Protocol checklist

- [x] Rebuilt from raw inputs with independently written code
- [x] Same corpus snapshot hash (SHA256 match)
- [x] Threshold/split fixed before run (git prereg e41920f precedes c2e006f)
- [x] Null model attached (own B=150 shuffle null, seed 7)
- [x] Claim wording matches what was shown (negative: gate NOT met)
- [x] Checker runs as designed (FAIL, exit 1) from scratch paths
