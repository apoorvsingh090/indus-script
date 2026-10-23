# L0-0001 — mayig → joyboseroy derivation fidelity: GATE PASS (179/179)

Every `cisi_real_corpus.csv` sequence equals some side's grapheme-id list in the
corresponding mayig source JSON (sides tried in file order). The public
derivation chain (mayig MIT → joyboseroy conversion) is faithful at sequence level.

## Note for Phase-1 concordance work

mayig JSONs also carry Wells feature vectors per grapheme — the raw material
for a future G↔Wells mapping. The authoritative ICIT↔M77 / ICIT↔Parpola
concordances live in Fuls 2023 Catalog Ch. 2.4/2.5 (©, extraction needs
permission) — that remains the blocked path, not this one.

## Information lost in the mayig → joy derivation (skeptic-B inventory)

Bijection holds (179↔179, no orphans/drops; all single-side files, so the
sides-order rule is vacuous here), but the CSV drops: Wells feature tails
(782/1003 glyphs), damage *location* (bool kept), line *assignment* (counts
kept), uncertainty *distribution* (mean kept), and any M77 crosswalk (joy has
no M77 column; mayig `features/` keeps only type-level `mahadevan_graphemes`,
e.g. P086→M161 — a sign-level bridge seed, unverified). Checker takes the
clone ROOT (`corpus/*/*.json` glob); pointing it at `corpus/` gives 0/0 FAIL
by construction — documented, not a bug.
