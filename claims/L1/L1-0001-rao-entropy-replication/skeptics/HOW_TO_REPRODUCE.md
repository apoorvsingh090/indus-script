# How to reproduce L1-0001 yourself (skeptic walkthrough)

Takes ~10 min. You need: git, Python 3.11+ (stdlib only — no pip packages required
for the check; `huggingface_hub` only if you use the fetch script).

## 1. Clone the repo

```powershell
git clone https://github.com/apoorvsingh090/indus-script.git
cd indus-script
```

## 2. Get the corpus (NOT in the repo — license hygiene)

Option A — fetch script (pinned revision + SHA check):
```powershell
pip install huggingface_hub
python claims\L1\L1-0001-rao-entropy-replication\how-we-built-it\fetch_corpus.py $env:TEMP
```

Option B — manual: download `indus_website_real_corpus.csv` from
https://huggingface.co/datasets/joyboseroy/indus_decipher and verify:
```powershell
Get-FileHash .\indus_website_real_corpus.csv -Algorithm SHA256
# must equal 7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8
```

## 3. Write YOUR OWN script (do not open `how-we-built-it/*.py` yet)

Recipe (any language):
1. Parse CSV, take `sign_sequence`, split on whitespace. Drop empty rows.
2. Exact-dedup on the raw sequence string. Expect **1918 texts, 9001 tokens, vocab 592**.
3. Unigram counts → `H1 = -Σ (c/N)·log2(c/N)`; add Miller-Madow `+ (K−1)/(2·N·ln2)`.
4. Ordered bigram counts within each inscription → same formula → `H2`.
5. `C = (H2 − H1) / log2(592)`. Expect **≈ 0.41**.
6. Null with YOUR OWN seed: pool all 9001 tokens, shuffle, re-chunk to the original
   1918 lengths, compute C; repeat B ≥ 50. Expect null ≈ **0.56 ± 0.002** — real must
   sit below the whole null range.
7. Uniform control: iid draws over 592 signs at the same lengths. Expect ≈ **0.46** —
   real must sit below it (note: margin is thinner here by construction).

## 4. Cross-check with the repo checker (after your numbers exist)

```powershell
python claims\L1\L1-0001-rao-entropy-replication\check.py --corpus <your csv> --object claims\L1\L1-0001-rao-entropy-replication\object\results.json --baseline claims\L1\L1-0001-rao-entropy-replication\baseline_snapshot\nulls.json
# expect PASS
```

## 5. Try to break it (pick at least one)

- Different seed / B for the null. Different estimator (plain ML, Chao-Shen).
- Drop length-1 texts; or keep duplicates (C should drop further — dedup is conservative).
- Per-site split (e.g. Mohenjo-daro only): effect should persist, else it is a mixing artifact.
- Confirm prereg order: `git log --oneline` — `L1-0001 preregister` (result TBD) must
  predate `L1-0001 results`.

## 6. File your report

Write `claims\L1\L1-0001-rao-entropy-replication\skeptics\<your-id>.md` starting with
`verdict: reproduced` or `verdict: failed-reproduction`, with env + numbers +
gate checklist + objections. Submit via PR (see `CONTRIBUTING.md`).
