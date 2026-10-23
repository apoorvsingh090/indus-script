verdict: reproduced (negative confirmed)

# L1-0002 skeptic skneg-02 — independent negative confirmation

Independent skeptic #2. Own code only; did not open `how-we-built-it/*.py`, `check.py` (executed blind at end), `object/results.json`, `baseline_snapshot/nulls.json`, or `skeptics/*.md` (skneg-01 exists, not opened). Allowed inputs only: `claim.yaml`, `README.md`, `agents/skeptic-protocol.md`, raw CSV, dataset card `ds-readme.md`.

## Environment / provenance
- OS: Windows 11 Pro 10.0.26200; Python 3.12.10
- Raw: `C:\Users\Apoorv\AppData\Local\Temp\opencode\hf-indus\indus_website_real_corpus.csv`
- Own code: `C:\Users\Apoorv\AppData\Local\Temp\opencode\skneg2\recompute.py`, seed 99, B=120
- SHA256: `7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8` — matches `claim.yaml:corpus_snapshot_sha256` (lowercase compare).

## Recomputation (as-stored, exact-dedup)
- Raw rows: 2543; directions raw: L-R 2440 / R-L 103 (matches README 2440/2543).
- Exact-dedup on stripped `sign_sequence`: 1918 unique (625 removed) — matches expected 1918.
- Length-1 texts: 11; empty: 0 — matches claim.yaml parenthetical "11 len-1 texts count as begin only".
- Position rule used: begin=index 0 (N=1918); end=index len-1 iff len>1 (N=1907).
- n80 (min types covering >=80% tokens at slot), own implementation:
  - n80_begin = 27, n80_end = 103 — exact match to published 27/103.
  - distinct types: begin 223, end 370.
- Own shuffle null for n80_end (flat token shuffle over 9001 tokens / 592 types, fixed lengths, re-chunk, seed 99, B=120):
  - min 69, max 87, mean 77.16; full sorted list in run log.
  - Builder B=200 reported min 69 / max 87 — my B=120 reproduces both endpoints exactly.
- Gate (preregistered: need n80_end < n80_begin AND n80_end < null-min):
  - 103 < 27 = False; 103 < 69 = False → GATE NOT MET. Negative confirmed.

## Causal flip test (different check than quote-matching)
- Corrected order built myself per card convention (`reading_direction=="L-R"` → reverse tokens, else as-stored; card `ds-readme.md:110` confirms this convention): same 1918 texts, reversed where indicated.
- Corrected n80_begin = 107, n80_end = 32 (distinct begin 379 / end 224).
- Mirror vs as-stored: begin 27↔end 32, end 103↔begin 107; distinct counts also mirror (223/370 → 379/224).
- Robustness: dedup-after-correction N=1917 (one reversal collision), n80 107/31 — same conclusion.
- This confirms the diagnosed cause actually explains the failure: the error direction matters, and fixing orientation flips the asymmetry to the literature direction. True causal check passed.

## Git order + wording
- `e41920f6bcfdff4fd6a7570d9429b172a279f4f2 2026-10-14 18:12:56 +0530 preregister` precedes `c2e006f54ae8ec21448e814a8fe00336952d722b 2026-10-14 18:15:08 +0530 negative recorded`. Prereg before record confirmed.
- Wording: `claim.yaml:result` and `README.md` state GATE NOT MET, "specification error, NOT evidence against the literature asymmetry", disposition as published negative with follow-up L1-0002b. No "solved"/decipherment overstatement. Pass.

## Checker (run last, blind)
- `python claims\L1\L1-0002-positional-beginners-enders\check.py --corpus <raw csv> --object <object/results.json> --baseline <baseline_snapshot/nulls.json>` (args from `--help` only, file never read) → stdout `n80 begin/end = 27/103 null_min = 69 / FAIL: gate not met`, exit 1. Expected FAIL confirmed; agrees with my recomputation.

## Objections / limits
- None overturning. Minor notes: my null B=120 vs builder B=200 (endpoints identical); corrected rededup 1917 vs 1918 (n80 shift 32→31, immaterial); n80 tie-handling not specified but exact integer match makes it moot.
