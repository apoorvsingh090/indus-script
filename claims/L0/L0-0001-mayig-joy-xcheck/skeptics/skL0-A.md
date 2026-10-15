verdict: reproduced

# skL0-A — independent skeptic audit of L0-0001 (mayig→joy derivation fidelity)

## Scope / freshness
- Read only: `claims/L0/L0-0001-mayig-joy-xcheck/claim.yaml`, `README.md`, `agents/skeptic-protocol.md`.
- Did NOT read: `check.py`, `object/*`, `baseline_snapshot/*`, `skeptics/*.md` (prior to writing this file).
- Wrote own code from scratch: `C:\Users\Apoorv\AppData\Local\Temp\opencode\skL0A\repro_L0A.py` (stdlib only: csv/json/glob/re/hashlib).
- Rebuilt from raw frozen inputs (read freely):
  - mayig clone `C:\Users\Apoorv\AppData\Local\Temp\opencode\mayig-corpus` (179 JSONs under `corpus/` recursively)
  - joy CSV `C:\Users\Apoorv\AppData\Local\Temp\opencode\hf-indus\cisi_real_corpus.csv`
- Ran claimants' `check.py` only at the end as conformance, without reading it (via `--help` + one PASS run).

## Environment
- OS: Windows-11-10.0.26200-SP0 (win32, PowerShell 5.1)
- Python: 3.12.10 (tags/v3.12.10:0cc8128, MSC v.1943 AMD64)
- indus-script HEAD: `6c01719` (L0-0001 results commit)
- Date of audit: 2026-10-15 UTC
- mayig rev: `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb` via `git -C <clone> rev-parse HEAD` — MATCHES claim.yaml mayig_pin
- mayig date/msg: `2025-04-16 m184` via `git log --format="%H %ad %s"` — MATCHES claim date
- mayig LICENSE: present at `<clone>/LICENSE`, first line `MIT License`, `Copyright (c) 2024 Michael Carlson` — MIT confirmed

## Normalization rule (explicit)
- Gate uses EXACT string equality on P-codes: joy `sign_sequence.split()` list == mayig side's `[g["id"] for g in graphemes]` list, in order.
- Allograph rule decided and stated: strip trailing `_<digits>` suffix (`P121_1` → `P121`) for a SECONDARY normalized comparison; exact match is the pass/fail gate, normalized rate reported for robustness.
- Finding: underscore IDs are ABSENT in this 179-file subset — 0/182 distinct mayig grapheme IDs contain `_`; 0/182 distinct joy CSV tokens contain `_`; 0 non-`P\d+` tokens on either side. So exact == normalized here; rule is moot but documented.

## Independent result (own script output)
- mayig JSON files found (recursive `corpus/**/*.json`): 179
- distinct mayig side IDs: 179; multi-side files: 0 (all files are single-element lists, so "some side's ... sides tried in file order" is vacuous for this subset)
- distinct grapheme IDs (mayig): 182; distinct sign tokens (joy): 182
- CSV data rows: 179 (plus header = 180 lines); distinct inscription_ids: 179, duplicates: 0
- sequence length range: 1..13
- filename-stem sanity (`m001.json` ↔ `M-1A`): 0 mismatches
- coverage: 0 CSV IDs missing in mayig; 0 mayig sides missing in CSV (perfect 1:1 join on `inscription_id == side.id`)
- exact matches: 179/179, RATE_EXACT=1.000000
- normalized matches: 179/179, RATE_NORM=1.000000
- mismatches: none (empty list)
- CSV sha256 (local file, computed): `431b42a4b89ce0c06f3f52f6fc224a27f717ac6527b94d4f15a9d24d817429df`
- GATE (own): PASS (179/179 exact)

## Git order — prereg before results: PASS
- `5ce8fc0` (2026-10-15 12:48:13 +0530): "L0-0001 preregister (results TBD)" — added `check.py` + `claim.yaml` with `result: "TBD — checker not yet run..."`, `status: draft`, threshold text already present.
- `6c01719` (2026-10-15 12:51:01 +0530): "L0-0001 results ..." — added `README.md`, `object/results.json`, `baseline_snapshot/counts.json`; `claim.yaml` diff only `result: TBD → "179/179 ... PASS"`, `status: draft → under-skeptic-review`.
- `preregistered_threshold` text identical in both commits: "Exact side-sequence agreement on all 179 inscriptions (match rate == 1.0). Match rule: joy sign_sequence equals some side's grapheme-id list in the corresponding mayig JSON (sides tried in file order)."
- Conclusion: threshold + match rule fixed before checker run committed. No post-hoc gate movement.

## Wording check: PASS (no stretch of "solved")
- Claim title/result: "derivation fidelity", "exact side-sequence matches — gate PASS". README: "public derivation chain (mayig MIT → joyboseroy conversion) is faithful at sequence level."
- Limitations in claim.yaml explicitly state: sequence identity only (says nothing about transcription correctness vs CISI plates); covers 179-seal cisi subset, not the 2543-row indus_website corpus.
- No sign-meaning, decipherment, or correctness-vs-plates claim. Matches what was shown.

## Conformance (claimants' checker, run last, not read)
- `python check.py --help` shows args `--mayig --cisi --object --baseline`.
- Trial 1 with `--mayig .../mayig-corpus/corpus` → `matched 0/0 (mayig files 0, joy rows 179) / FAIL` (checker globs non-recursively; needs clone root).
- Final with `--mayig .../mayig-corpus` (clone root) `--cisi .../cisi_real_corpus.csv` `--object .../object/results.json` `--baseline .../baseline_snapshot/counts.json` → `matched 179/179 (mayig files 179, joy rows 179) / PASS`, exit 0.
- Conformance: PASS, agrees with independent 179/179.

## Objections / notes (non-blocking)
1. `corpus_snapshot_sha256` in claim.yaml (`72580755...` + note "joy cisi file is part of the same HF dataset revision") does NOT equal sha256 of the local `cisi_real_corpus.csv` (`431b42a4...`). `data/processed/SHA256SUMS` says "no frozen snapshots yet". Hash lineage needs clarification (dataset-revision hash vs file hash?), but it does not affect the sequence-identity comparison, which I recomputed from the actual files.
2. `mayig_pin` says "(179 JSONs under corpus/)": true only recursively — actual layout is `corpus/m001_m099/*.json`, `corpus/m100_m199/*.json`. Minor doc imprecision.
3. "Some side's ... (sides tried in file order)" overstates generality for this subset: all 179 files are single-side, so there is no multi-side disambiguation exercised. Rule is still correctly implemented (trivially satisfied).
4. Allograph suffixes (`P121_1`-style): none present in either source here, so the stated normalization choice is untested by this data. If future subsets introduce them, the gate must declare strip-vs-exact up front (I used exact-as-gate).
5. Checker UX: `--mayig` expects the clone root, not the `corpus/` subdir; worth documenting to avoid 0/0 FAIL confusion.

## Log
- `C:\Users\Apoorv\AppData\Local\Temp\opencode\skL0A\repro_L0A.py` run → 179/179 exact, 0 mismatches (full stdout captured in session).
- `git -C mayig-corpus rev-parse HEAD` → `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`.
- Claimants' checker final run → PASS 179/179.
- Touched nothing else; this file is the sole deliverable.
