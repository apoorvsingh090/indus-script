verdict: reproduced

# skC-A (INDEPENDENT SKEPTIC A, redo) — L0-0002 concordance v0.1 audit

## Environment
- OS: win32 (PowerShell 5.1); Python 3.12.10
- Source clone: C:\Users\Apoorv\AppData\Local\Temp\opencode\mayig-corpus @
  ad2f1e218a34b8c33c57de0d6cb8d99272765bbb (matches claim.yaml corpus pin;
  `git status` clean, branch main, single-commit `m184` context)
- Claim repo HEAD at audit time: bea339675ed3217f09a9299a81c14ba5cac19bf7
  (claim history: prereg 53f406b 2026-10-15 20:18:21 +0530, results 0ae13f4
  2026-10-15 20:21:55 +0530)
- Own code: C:\Users\Apoorv\AppData\Local\Temp\opencode\skC-A2\audit.py
  (freshly written for this audit; no reuse of check.py / build_concordance.py,
  which were never opened). Rebuilt artifact:
  C:\Users\Apoorv\AppData\Local\Temp\opencode\skC-A2\rebuilt-pwm-v01.csv
- Files read: claim.yaml + claims README.md + agents/skeptic-protocol.md, plus
  data/concordance/README.md (format/scope doc only, not builder logic) and raw
  source features/P*.json. NEVER opened: check.py, claim object/*,
  baseline_snapshot/*, skeptics/skC-B.md, data/concordance/build_concordance.py.
- Format discovery (stated openly): inspected ONLY the header/first-300-bytes and
  binary line-ending metadata of data/concordance/pwm-v01.csv to learn the
  schema (`p,w_list,m_list,v_list,status`, `|`-join preserving source order,
  CRLF, trailing CRLF, no BOM). No data rows were copied — all mapping rows
  were extracted from source JSONs by my own code.

## 1. Independent rebuild (own status rule, stated)
- Status rule (mine, V-count ignored): W==0&M==0 → unmapped-WM; W==0 → unmapped-W;
  M==0 → unmapped-M; W==1&M==1 → clean-1:1; else → multi.
- Serialization (mine, matching schema above): rows sorted by P id; multi-values
  `|`-joined in source array order (verified e.g. P003 W159|W160|W161 =
  JSON order); empty list → empty field; `csv.writer(lineterminator="\r\n")`,
  UTF-8 no BOM, trailing CRLF. Asserted no field contains `,`/`"`/newline.
- CRLF handling: wrote CRLF explicitly (StringIO newline="" + lineterminator
  "\r\n"); hashed the exact bytes. No LF-normalization.

## Numbers (rebuilt vs claimed)
- Rebuilt sha256: 5c487299eb9d1af7869925c8b50ca555a7febc10ae3f752b228439d25b885cc8
- Claimed sha (claim.yaml): same → SHA MATCH: True (byte-exact, first try)
- Counts rebuilt: clean-1:1=227, multi=80, unmapped-WM=38, unmapped-W=27,
  unmapped-M=24 → COUNTS MATCH claimed {227/80/38/27/24}: True
- M-codes shared by >1 P: 13 (≥10 gate: True):
  M002[P015,P016], M050[P043,P044], M064[P054,P055], M076[P066,P071],
  M099[P119,P122], M103[P123,P139], M161[P085,P086], M167[P086,P101],
  M168[P086,P100], M199[P292,P293], M216[P230,P234], M264[P260,P359],
  M409[P346,P348]

## 2/3. Adversarial checks
- Unmapped-WM sample (raw JSON wells/mahadevan): P000 W=[] M=[] V=[V599];
  P005 W=[] M=[] V=[V750]; P018 W=[] M=[] V=[V754]; P049 W=[] M=[] V=[V354];
  P072 W=[] M=[] V=[V527] → all genuinely lack both keys. PASS
- Unmapped-M sample: P030 W=[W145] M=[]; P033 W=[W143] M=[]; P090 W=[W956] M=[];
  P094 W=[W521] M=[]; P097 W=[W642] M=[] → all genuinely lack M with W present.
  (Unmapped-W spot: P002 W=[] M=[M013] likewise genuine.) PASS
- Shared-M hand-verified in raw JSONs (3): M161 ∈ P085(M=[M161]) & P086
  (M=[M161,M162,M167,M168,M169]); M002 ∈ P015 & P016 (both M=[M002]);
  M409 ∈ P346 & P348 (both M=[M409]). PASS
- Completeness: 396 features/P*.json files; 396 unique ids; every
  filename==id; zero duplicates, zero drops; id range P000–P396 minus P220
  (397−1=396). Sort order verified ascending. PASS

## 4. Git order + wording
- Order: prereg 53f406b (threshold + sha + counts + ≥10 contested fixed,
  result "TBD", status draft) precedes results 0ae13f4 (PASS) by ~3.5 min.
  Prereg-before-results: PASS
- Wording: claim.yaml limitations + README scope honesty both state type-level
  grapheme sets only, G-scheme unbridged, mayig judgments provisional vs Fuls —
  no "solved" stretch. PASS

## Conformance (their checker, run LAST, never read)
- `check.py --mayig <clone> --object data/concordance/pwm-v01.csv
  --baseline baseline_snapshot/counts.json --builder
  data/concordance/build_concordance.py` → `sha match=True
  counts={...} contested-M=13 / PASS` (exit True). Matches my independent result.

## Objections
- None load-bearing. Minor notes: (a) CSV schema is documented nowhere except
  the header itself — future versions should pin header/join/line-ending spec in
  the prereg text, not just the builder; (b) "unmapped-W" naming is easy to
  misread (means W-side empty, M present) — suggest a glossary line. Neither
  affects reproducibility: byte-exact rebuild succeeded.
