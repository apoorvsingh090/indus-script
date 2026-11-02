# L4-0007 - rank-init on a fresh sealed key: NEGATIVE (5/10 < 7/10)

The purpose of this cell: the rank-init exact-recovery observation made
post-hoc on the 2026-10-18 lineage's L4-0003 key (8/10, explicitly *not
claimable*) had to be re-run on a fresh sealed key draw to be claimable at
all. The prereg bar is the same 7/10 exact-rank bar that L4-0002's method
missed at 5/10.

> **Provenance (ported 2026-11-02).** This claim was built and skeptic-closed
> on a divergent local branch (original ID `L4-0004`, Oct 18). The canonical
> line later advanced through L4-0006, so it is renumbered here as L4-0007.
> The object, checker, generator, and both skeptic reports are carried over
> unchanged in substance; the checker imports the audited `rank_init` from
> this claim's own `how-we-built-it/rank_lib.py` (the current repo's L4-0003
> is a different cell with a different `rank_init`) and was re-run here.

## Result

| metric | value | bar |
|---|---|---|
| exact top-10 hits | **5/10** | >= 7/10 |
| full-alphabet exact hits | 8/370 | (reported, not gated) |

**Gate FAIL on the key arm, as designed for a negative.**

## Chain

- Prereg commit shipped `claim.yaml` (result `TBD`), `check.py`, and this
  generator, with key3 absent - `3492a077...` committed as
  `key_commitment_sha256` before any number on this key existed.
- key3 = valid permutation of range(370) via `Random(260417839 + 370)`
  (seed base 260417839 unused by any prior artifact; checker re-asserts the
  seal and the recipe).
- Checker: `rank-init top10=5/10 full=8/370 key-sha=match recompute=match`,
  FAIL exit 1.

## Reading

Rank-init's score is **key-invariant by construction** (both auditors,
independently): a substitution key is a frequency-preserving relabeling, so
the exact-rank metric is a deterministic function of the window build alone.
Evidence:

- auditors' fresh-key batteries: 0/14 and 0/24 draws differ - every draw
  gives exactly 5/10 top-10, 8/370 full;
- all three keys on the Oct-18 lineage (its L4-0002/0003/0004) give the same
  5/10 on the same windows.

The draft's original interpretation ("8/10 on that lineage's L4-0003 key was
key-draw luck") is REFUTED as a narrative: that claim's `rank_init_top10`
field stored FULL-alphabet exact hits (8/370), not top-10 hits - an erratum
filed in that lineage. Its true top-10 value on that key was 5/10, identical
to this cell's.

What DOES vary is the window build (auditor skR4-A: band 1-7/10 across 20
builds, 1/20 builds >= 7). Either way the prereg bar of 7/10 is not cleared
reliably by anything rank-init produces at this data scale: exact-rank
recovery remains nowhere near claimable. A stronger method - or tolerance
ideas that themselves must pass an L4 cell first - is required.

Future-work note (auditor): commit a windows/halves digest in the prereg so
"identical windows" becomes a checkable assertion rather than a lineage
claim.

## Prereg discipline

- Fixed before any number on this key: window protocol, key recipe,
  `rank_init` definition (the audited Oct-18 lineage function, shipped
  verbatim in `how-we-built-it/rank_lib.py`), threshold text. No amendments
  made pre-results.
- Transparency note: builder is not blind (same transparent-box-adjacent
  model as L4-0002); recovery validity does not depend on builder blindness.

## Skeptics

Confirmed 2/2 (`skR4-A`, `skR4-B`):

- Chain clean; key3 seal verified three ways (sha-of-file = sha-of
  json.dumps = prereg commitment; recipe replay byte-identical).
- skR4-B rebuilt the stream EXACTLY (V=370) - replay 5/10 top-10, 8/370 full,
  checker `recompute=match`, FAIL exit 1 as designed.
- Key-invariance proven independently by both (0/24 and 0/14 fresh draws
  differ; tie-break variants max 5/10 - nothing crosses 7).
- Mechanism correction folded into claim result + this README.
