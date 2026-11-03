# Changelog

All notable changes to this repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
There are no versioned releases yet; everything lives under `[Unreleased]`
until the first tag is cut.

## [Unreleased]

### Added

- GitHub Actions `ci` workflow: Python syntax check across all checkers plus
  repo-wide `claim.yaml` validation on every push/PR
  (`verify-claim` remains the path-filtered claim gate)
- `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1) and `SECURITY.md`
- Bug-report issue template and issue-template chooser (`config.yml` with
  Discussions links)
- `CHANGELOG.md`
- Labels `claim` and `skeptic-review` (referenced by the claim/skeptic
  templates but previously missing)
- README badges (CI, license)

### Fixed

- README had two `## Contributing` sections; merged into one that links
  `CONTRIBUTING.md`

### Verified results (see `TROPHY_CASE.md` for full table)

- 2026-10-14: L1-0001, L1-0002 (negative), L1-0002b, L1-0003, L1-0004
  skeptic-confirmed (2/2 each)
- 2026-10-23: L1-0001 third independent reproduction (skeptic-task-03,
  stdlib-only reimplementation, own seeds; C bit-identical to shipped object) —
  now 3/3 skeptics (PR #1)
- 2026-10-15: L0-0001, L0-0002, L2-0001, L4-0001, L2-0003, L4-0002
  (partial negative) skeptic-confirmed (2/2 each)
- 2026-10-15: splits v2 frozen (test = Mohenjo-daro); audit scorecard
  extended to L0/L2/L4 (all checkers recomputed green)
- 2026-10-23: L4-0003 (new claim) — bigram-assisted hidden-key recovery
  CONFIRMED NEGATIVE 2/2 skeptics (4/10 vs bar 7 on 3/3 keys, under
  rank-only 5/10); qualifications folded: negative is config-scoped
  (α≥0.2 clears 10/10; full-corpus reference recovers 10/10)
- 2026-10-24: L4-0004 (new claim) — α-calibrated recovery on a disjoint-pool
  cell GATE PASS 2/2 skeptics: α*=0.2 by dev rule, reaches the bar at
  N_ref=974 (7/7/7, zero slack), collapses below ~250; qualifications
  folded: top-10 bar passes 17% of structureless controls (joint pattern
  carries the claim), 3-key conjunct = relabeling robustness, L3 gated
  behind a strengthened key-recovery design
- 2026-10-24: agents/outreach-template.md — external-reviewer outreach
  draft (planner Phase 0)
- 2026-10-24: L0-0003 (new claim) — G↔P concordance v0.1 via structural
  alignment on 161 shared M-numbered Mohenjo-daro unicorn texts, verified
  2/2 skeptics: 22 clean bijective pairs (stable core 16), 19 contested,
  151 unmapped; holdout 0.980, permutation floor 0/200; P stored reversed
  vs G corrected order; composes with pwm-v01 → 15 clean G→P→M chains;
  gp-v01.csv ships (scheme-debt: G now bridged for high-frequency signs)
- 2026-10-25: L4-0005 (new claim) — strengthened key gate (sk4-A/sk4-B
  spec) on a fresh cell, verified-negative 2/2: frozen reading misses the
  7/10 dev bar at every α; gate fails under every reading tried (best
  6/10 @974); S_true>S_best everywhere (search/data-size failure);
  L4-0004 pass bracketed as a boundary draw; L3 stays shut; two filed
  readings withdrawn as over-strong per review

- 2026-11-02: L4-0007 (ported; original ID L4-0004) - rank-init on a fresh
  sealed key CONFIRMED NEGATIVE 2/2 skeptics: 5/10 top-10 (8/370 full)
  < 7; metric key-invariant by construction (0/24 fresh draws differ).
- 2026-11-02: L4-0008 (ported; original ID L4-0005) - positional
  token-concentration asymmetry on Sumerian windows CONFIRMED NEGATIVE
  2/2: n80 begin 72 / end 67, gap 5 inside B=200 null band (max 12);
  the Indus L1-0002b effect is corpus-specific, not generic.
- 2026-11-03: L4-0006 (draft) — two recomputes of the frozen grid match the
  object field-for-field: the shipped checker (`recompute=match`, gate FAIL)
  and a from-prose independent rebuild. NOT the skeptic gate: subagent
  backends were unreachable, so status stays draft; named follow-up
  (full-key-separation gate) queued for prereg.
- 2026-11-03: L4-0006 (new claim) — CONFIRMED NEGATIVE 2/2 skeptics
  (sk6-C, sk6-D): dev 9/10 @α*=0.5 but gate keys 2/3/5 (keys_ge8=0),
  halves 6/3; full-key 0.075 vs null_max 0.038. Qualifications folded:
  the ~2x separation is unweighted-only (token-weighted 1.27x), bucket-edge
  choice moves it 18-30/372, and the prereg's "8.9% of tokens" is 8.9% of
  windows; top-10 negative robust to tie/bucket variants.
- 2026-11-03: L4-0009 (new claim, prereg `a511cb0`) — full-key-separation
  gate on fresh cell #4, alpha frozen 0.5: committed full 0.1725 (64/371)
  vs null_max 0.0674 (2.56x), all 3 keys replicate, top-10 10/10/10/7 —
  but cipher half B falls to 1.00x null_max, so the gate FAILS at the
  half-replication condition; a large multi-key separation that is not
  uniform across halves. Checker recompute=match; L3 stays shut.

### Known gaps

- No corpus files vendored yet (`data/raw/` provenance + license TODOs open)
- First tagged release not cut
