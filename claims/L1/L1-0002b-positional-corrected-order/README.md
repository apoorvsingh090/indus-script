# L1-0002b — Positional asymmetry, loader-corrected order: GATE PASS

Corrected order = reverse rows with `reading_direction == "L-R"` (2440/2543),
keep `"R-L"` as stored, per dataset-card loader convention; exact-dedup after
orienting → 1948 texts (vs 1918 as-stored; orientation changes dup identity).

## Gated result

| Metric | Real (corrected) | Shuffled null (B=200, seed 260417832) | Gate |
|---|---|---|---|
| n80_begin | 107 | — | — |
| n80_end | **32** | min 67, max 85 | **PASS** (32 < 107 and < 67) |

Literature mirror: Adhikari et al. (M77-EBUDS) report 82 beginners vs 23 enders
for 80% coverage; we find **107 vs 32** — same direction, same magnitude ratio.

## Reported (not gated) vs Nair 2026 (ICIT 1916/584/11110)

| Metric | Ours (G-592) | Nair ICIT | Note |
|---|---|---|---|
| Rigidity mean-V (top-10) | 0.1560 | 0.15 | near-exact |
| Site V Mohenjo-daro / Harappa | 0.168 / 0.132 (n=970/660) | 0.160 / 0.153 | same direction ("same positional grammar") |
| Hapax rate | 0.3632 | 0.33 | same ballpark |
| Zipf slope (log-log OLS) | −1.4236 | −1.49 | same ballpark |
| Mean length | 4.66 (9080/1948) | 4.42 | same ballpark; revision/dedup drift |

Top beginners/enders (G-codes, scheme-specific — no M77 concordance yet):
see `object/results.json` (`top_begin`, `top_end`).

## Evidentiary note

An earlier run executed before the prereg commit due to a workdir error; the chain
was repaired (`git reset` to `e41920f`, pure-prereg `cac214e`, fresh re-run —
deterministic seeds give identical numbers). Threshold text unchanged throughout.
