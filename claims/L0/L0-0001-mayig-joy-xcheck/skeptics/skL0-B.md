verdict: reproduced

# skL0-B — L0-0001 identifier-chain audit (independent angle)

Claim: joy `cisi_real_corpus.csv` sequences reproduce mayig source JSONs 179/179 (derivation fidelity, sequence identity only).
Scope read: `claim.yaml` + `README.md` + `agents/skeptic-protocol.md` only. Never read `check.py`, `object/*`, `baseline_snapshot/*`, `skeptics/*.md` (listed `skeptics/` dir only to pick a non-colliding filename). Ran claim `check.py` last via `--help` + execution only.

## Environment
- Python 3.12.10 (MSC v.1943 64-bit AMD64), win32, PowerShell 5.1
- Date: 2026-10-15 (UTC+0530 local commits same day)
- mayig clone: `C:\Users\Apoorv\AppData\Local\Temp\opencode\mayig-corpus` @ `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb` (matches `claim.yaml` mayig_pin; `git rev-parse HEAD` verified)
- joy CSV: `C:\Users\Apoorv\AppData\Local\Temp\opencode\hf-indus\cisi_real_corpus.csv`, sha256 `431b42a4b89ce0c06f3f52f6fc224a27f717ac6527b94d4f15a9d24d817429df`, 14521 bytes, 180 lines (header + 179 rows)
- indus-script HEAD: `6c01719` ("L0-0001 results: 179/179 mayig-joy agreement (checker PASS)")
- Own code: `C:\Users\Apoorv\AppData\Local\Temp\opencode\skL0B\verify_L0B.py` (fresh parser, no reuse of claim code) → `skL0B_results.json` (full JSON dump of numbers below)

## Independent sequence check (own parser, stated normalization)
- Normalization: `sign_sequence.strip().split()` (whitespace-split) vs mayig `[g["id"] for g in side["graphemes"]]` exact list equality, keyed by `inscription_id == side["id"]`.
- Result: **179/179 exact matches, match_rate 1.0, 0 mismatches.**
- Vocab: joy 182 distinct signs, mayig 182 distinct signs, `joy-only []`, `may-only []`, non-`P\d+` tokens `[]` on both sides, whitespace/suffix anomalies `[]`, empty sequences `[]`.
- Claim `check.py` run LAST (args discovered via `--help`, not reading): `--mayig <clone-root> --cisi cisi_real_corpus.csv --object object/results.json --baseline baseline_snapshot/counts.json` → `matched 179/179 (mayig files 179, joy rows 179) / PASS`. (Note: `--mayig` must point at clone root, not `corpus/` subdir — first probe with `corpus/` gave `matched 0/0 FAIL`, root gives PASS.)

## 1. Identifier audit (main job) — bijection holds, with one vacuous clause
- mayig: 179 `*.json` files under `corpus/` (recursive glob), 179 sides total, **0 multi-side files**, 0 duplicate side ids.
- joy: 179 rows, 179 unique `inscription_id`, duplicates `[]`, all match `^M-\d+[A-Z]$`, suffix counter `{A: 179}`.
- Join: `joy-only orphans []`, `mayig-only drops []`, intersection 179 → **bijection OK (179↔179, no orphans/dups/silent drops).**
- Filename↔id: numeric part of filename (`m001.json`) equals numeric part of side id (`M-1A`) for all 179 — mismatches `[]`. Gaps exist in numbering (e.g. no M-2) but they are identical on both sides, so not a drop.
- Caveat: claim's match rule "joy equals *some side's* list (sides tried in file order)" is **vacuous on this snapshot** — every file has exactly 1 side, so file-order tie-breaking is untested. A future multi-side case could exercise that logic; this data does not.

## 2. CISI↔M77 bridge — text-level crosswalk is ABSENT in this chain
- joy columns (9): `inscription_id,sign_sequence,site,object_type,line_count,damaged,reading_direction,motif,mean_uncertainty` — **no M77 / Mahadevan / ICIT column** (`joy_has_m77_col: false`, `joy_preserves_features: []`).
- mayig `corpus/**/*.json` fields per side: only `{id, description, graphemes:[{id, features}]}`. Regex scan for `M77|Mahadevan|ICIT` over all 179 JSONs: **0 hits** (excluding the false-positive filename `m077.json`, which is artefact M-77 / side `M-77A`, not a sign-list ref).
- Only M77 mentions in mayig repo: `indus_corpus/src/lib.rs` struct comment (`mahadevan_graphemes: "correspondence list … from Mahadevan's 1977 sign list"`) and `features/P*.json` type-level concordance, e.g. `P086 → mahadevan_graphemes [M161,M162,M167,M168,M169]` alongside `parpola_graphemes`/`wells_graphemes` (396 feature files). This is a **sign-list-level P→M(sign) mapping, NOT the text-number-level CISI↔M77 index** (Fuls 2023 Catalog Ch. 2.4/2.5) the planner references — and **joy drops even that** (sequences are bare P-codes).
- Net: what survives in this chain = CISI text ids (`M-*A`) + P-code token sequences. What is LOST/absent = any M77 text-number crosswalk. README's "blocked path … remains blocked" is accurate; do not mistake `features/` type-level sign mapping for a text-level concordance.

## 3. Information-loss inventory (mayig → joy derivation)
| mayig source | joy derivation | Fidelity in this subset |
|---|---|---|
| grapheme `id` list (plain `P\d+`, 182 types; no `_`-suffixes like `P121_1` on either side) | `sign_sequence` space-joined P-codes | **Lossless** (179/179 + vocab identical) |
| per-grapheme Wells/allograph tail features (indices ≥3; e.g. P205 `[…,3,4,0,2,0]`) — 782/1003 graphemes have `len(features)>3` | dropped entirely | **LOST** (raw material for future G↔Wells mapping, per README, does not survive in joy) |
| per-grapheme `damage` int (low-2-digits % + high digits location, e.g. 1410/80/20/10) | boolean `damaged` | **Count-exact, detail lost**: `damaged == any(damage!=0)` holds 179/179 (75 True / 104 False), but % + location codes lost |
| per-grapheme `line` int | `line_count` | **Count-exact, assignment lost**: `line_count ∈ {distinct-lines, max-line}` holds 179/179 (172×1, 7×2; the 7 are M-23/66/67/68/79/154/165A); which glyph on which line lost |
| per-grapheme `uncertainty` 0–100 | `mean_uncertainty` (round to 2dp) | **Mean-preserved, distribution lost**: `round(may_mean,2)==joy` 179/179, max abs diff 0.0046; per-glyph variance lost |
| `description` free text (e.g. `unicorn IV seal`, 5 variants) | `motif` (`unicorn_IV`) + `object_type` (`seal`) | **Deterministic here, lossy in general**: `desc.replace(" seal","").replace(" ","_")==motif` 179/179; free-text nuance lost |
| filename prefix / CISI series | `site=Mohenjo-daro` (179/179), `reading_direction=L-R` (179/179), `object_type=seal` (179/179) | **Zero-variance constants** — derivation of these columns untested by this subset (all M-series unicorn seals; mayig README notes script reads R-T-L but graphemes stored L-to-R — joy `L-R` = storage order, not an epigraphic direction claim) |

## 4. Git order + wording checks
- Order: `5ce8fc0` (prereg: `check.py` + `claim.yaml` with `result: TBD`, threshold text fixed) → `6c01719` (results: `README/object/baseline`, `result: 179/179 … PASS`, `status: under-skeptic-review`). Timestamps 12:48:13 → 12:51:01 +0530 same day. `git diff 5ce8fc0..6c01719 -- check.py` is **empty (checker frozen)**; `claim.yaml` diff changes only `result`/`status`, threshold paragraph **byte-identical**. mayig pin matches clone HEAD. → prereg-before-results holds.
- Wording: title + `result` claim "sequence identity / derivation faithful at sequence level"; both `claim.yaml` limitations (sequence-only, not transcription-vs-plates; 179-seal cisi subset, not 2543-row website corpus) and README Phase-1 note are appropriately scoped. No "solved/deciphered" stretch. → wording PASS.

## Objections / reservations (do not overturn L0 as scoped)
1. **Snapshot-hash ambiguity (main objection):** `claim.yaml:corpus_snapshot_sha256: 72580755…` ≠ actual `cisi_real_corpus.csv` sha256 `431b42a4…`. Parenthetical says "part of the same HF dataset revision", i.e. it is a *revision* hash, not a file hash, and there is **no `SHA256SUMS` file at repo root** to resolve per skeptic-protocol item 2. Recommend adding file-level sha256 to the claim. Independent reproduction used the file hash above.
2. **Multi-side logic untested** (§1 caveat) — accept L0 but note the "sides in file order" rule has zero coverage here.
3. **Zero-variance joy columns** (`site/object_type/reading_direction`, single motif family) — joy's enrichment logic beyond sequences is unvalidated by this gate.
4. `mean_uncertainty` 2dp rounding (≤0.005) — negligible for L0, recorded for downstream users needing per-glyph uncertainty.
5. No novelty/lit-search or null-model obligation at L0 beyond the above; transcription correctness vs CISI plates explicitly out of scope (copyrighted scans).

Verdict rationale: the L0 claim as written — exact P-code sequence agreement 179/179 on the stated snapshot/pin with the stated match rule — reproduces under an independently written parser, the join keys are bijective, the checker passes, prereg order and wording are clean. Information loss and the missing M77 text-level bridge are real but *outside* what L0 asserts (and the README discloses the blocked path).
