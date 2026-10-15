# L4-0002 — Sumerian calibration: GATES PASS, hidden-key arm FAILS (partial negative)

N=1948 Sumerian sign windows (ETCSRI, CC0-per-file, fetch-at-build; V=370;
mean len 4.61, wrap 7.3%). Key sealed by sha at prereg, revealed in
`object/key.json` (verified `3b6a6c1d…`, valid permutation).

## Gated result

| Arm | Real | Bar | Verdict |
|---|---|---|---|
| ENT | C 0.447 < null-min 0.627 | < min (B=100) | PASS |
| L2 (974/974 halves, α=0.001) | d=0.1540 [0.1405, 0.1687] | CI-lo > 0, diff > 0.01 | PASS (wide) |
| REP | 612/317 vs 83/4 | > maxima (B=100) | PASS |
| Hidden-key rank recovery | **5/10** | ≥ 7/10 | **FAIL** |

Frozen methods pass on a real non-Indus language at Indus scale (sensitivity
confirmed beyond English). But naive exact-rank substitution recovery manages
only 5/10 — the key bar as specified is NOT cleared.

## Why (mechanism, probed post-hoc)

9/10 of half-A's top signs appear in half-B's top-10 — membership is stable,
but mid-rank COUNTS are near-tied (MU 140 vs KA 91) and shuffle positions
(LUGAL 3→5, MU 6→3, GA 7→9, KID drops out). Exact rank-position mapping is too
strict for flat mid-rank distributions. A tolerance/bigram-assisted recovery is
future work (L4-0003 candidate); this claim stands as a partial negative.

## Evidentiary notes

- Prereg amended twice pre-results (run/check `parents[]` path fixes; key
  resized 569→370 after measuring windowed V — design input, zero gate numbers
  seen; threshold text otherwise unchanged). Full disclosure, no peeking.
- Alpha fixed at production 0.001 (no val split on this cell — stated deviation).
- License caution kept: CC0 per file header; attribution + link; never vendored.
