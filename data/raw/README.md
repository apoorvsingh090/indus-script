# data/raw — untouched sources

Drop untouched downloads/exports here, one file per source. Never edit in place.
Every file MUST have a row in `provenance.csv` with license + access terms.

## Hygiene (planner §4)

- Record provenance + license per file. Nothing here is license-verified yet.
- Dedup exact duplicates on ingest; report the count (~24% dups seen in one raw corpus).
- Strip third-party "translations" — unverified outputs, not labels.
- Never mix synthetic / model-generated sequences in as real.
