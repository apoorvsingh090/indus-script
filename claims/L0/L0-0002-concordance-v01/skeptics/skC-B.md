verdict: reproduced

# skC-B — independent skeptic-B semantic spot-audit of L0-0002

## Environment
- Python 3.12.10, win32, PowerShell 5.1
- Claim repo: indus-script @ bea3396 (worktree clean at audit time)
- Source clone: mayig-corpus @ ad2f1e218a34b8c33c57de0d6cb8d99272765bbb (matches
  `corpus_snapshot_sha256` in claim.yaml)
- Workdir (own code only): `C:\Users\Apoorv\AppData\Local\Temp\opencode\skC-B\`
  (`rebuild_skCB.py`; written without opening `check.py`, `object/*`,
  `baseline_snapshot/*`, `skeptics/*.md`, or `build_concordance.py`)
- Inputs read: `claim.yaml`, `README.md`, `agents/skeptic-protocol.md`,
  claim artifact `data/concordance/pwm-v01.csv`, raw `features/P*.json` (396 files).

## 1. Independent rebuild — sha + counts
- Wrote own builder: sorted `features/P*.json` → `|`-join raw
  `wells/mahadevan/parpola_graphemes` in source order →
  status rule `{1W&1M: clean-1:1; 0W&0M: unmapped-WM; 0W: unmapped-W;
  0M: unmapped-M; else: multi}`.
- Object sha256: `5c487299eb9d1af7869925c8b50ca555a7febc10ae3f752b228439d25b885cc8`
  — matches `object_sha256` in claim.yaml.
- First rebuild (LF) was content-identical but sha-mismatched; diff showed the
  committed object uses CRLF terminators. Re-emitting with CRLF gives a
  **byte-identical** file (same sha). Content is fully reproduced; the only
  delta was the line-terminator convention (Windows default csv writer).
- Status counts from raw inputs:
  `clean-1:1=227, multi=80, unmapped-WM=38, unmapped-W=27, unmapped-M=24`
  (total 396) — exact match to preregistered threshold.
- Contested-M (M-codes claimed by >1 P): **13** (threshold ≥10):
  M002[P015,P016], M050[P043,P044], M064[P054,P055], M076[P066,P071],
  M099[P119,P122], M103[P123,P139], M161[P085,P086] (README example checks out),
  M167[P086,P101], M168[P086,P100], M199[P292,P293], M216[P230,P234],
  M264[P260,P359], M409[P346,P348] → 24 P-rows involved.
  Note P086 appears under three contested codes (M161/M167/M168): genuine
  multi-way split, correctly forced into explicit handling by the `multi` status.
- CSV row order is sorted P000..P396 with exactly one gap: **P220 has no
  `features/P220.json`** in the mayig source (mayig-side numbering gap, not a
  dropped row — all 396 existing P-files are covered, 396/396 rows, no extras).

## 2. Semantic audit (main job) — 34/34 faithful
- Sample: 10 random `clean-1:1` rows (own seed 5):
  P276, P103, P335, P160, P351, P307, P378, P284, P235, P014.
- Plus all 24 P-rows touching the 13 contested M-codes (superset of "all 13
  contested-M rows": every P-row on both sides of each contested code).
- For each: compared CSV `w_list/m_list/v_list` against the raw
  `features/P*.json` lists element-by-element (order-sensitive string compare
  of the `|`-join plus list equality on the split).
- Result: **34/34 faithful — no truncation, no reordering, no dropped codes.**
  Full per-row table in workdir `audit_table.csv` (all rows marked `faithful`).
- Delimiter safety: scanned all 1519 distinct sign IDs across W/M/V — **none
  contains `|` or `,`**; all match `^[WMV]\d+$`. No collision/quoting hazard.
- V-list column: populated for **396/396 rows** (zero empties); total V tokens
  **662**, distinct V codes **662** (each V-code attested under exactly one P —
  confirms the "≈662" expectation exactly; V-side needs no contested handling).

## 3. Git order + wording checks
- Prereg commit `53f406b` (2026-10-15 20:18) fixed the threshold text
  (227/80/38/27/24 + ≥10 contested); results commit `0ae13f4` (20:21) changes
  only `result`/`status` (+README/+object/results.json) — **threshold text
  byte-unchanged between prereg and results**. Ordering requirement satisfied.
- Observation (not an objection): the object CSV was already committed at the
  prereg commit rather than built after it; the checker's byte-rebuild-from-clone
  gate makes backdating moot, and the sha genuinely rebuilds from the pinned
  mayig source, so I do not count this against the claim.
- Wording: title/README stay inside what was shown — "type-level P→W/M/V
  concordance … reconciles with mayig source (contested splits listed)"; the
  13 contested codes are listed, scope limits (type-level only, G-scheme
  unbridged, mayig judgments provisional) are stated in claim.yaml. No "solved"
  stretch. `M161 by P085/P086` example verified verbatim.

## 4. Their checker (run last, never read)
- `python check.py --mayig <clone> --object <csv> --baseline <counts.json>
  --builder <build_concordance.py>` → 
  `sha match=True counts={…matches…} contested-M=13` → **PASS**.

## Objections
- None blocking. Minor notes: (a) CRLF-vs-LF sensitivity — byte-rebuild only
  passes with the platform-default CRLF writer, worth pinning explicitly in the
  builder for cross-platform skeptics; (b) object committed at prereg time
  (see §3); (c) P220 numbering gap is mayig-source-inherited, correctly
  propagated, but a one-line note in the README would pre-empt confusion.

## Verdict rationale
sha + counts + 13-contested all rebuilt from raw inputs with independently
written code; 34-row semantic spot-audit (10 random clean-1:1 + all contested
rows) is 100% faithful with no delimiter hazards; V-column fully populated
(662 distinct); prereg ordering clean; their checker PASSes from scratch.
