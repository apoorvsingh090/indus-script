# Agent loop config (daily run)

## Roles
- **Scout**: maintains hit list; picks a few targets per run (from L1→L3 sub-problems).
- **Builder**: attempts a target; produces claim artifacts (`claim.yaml` + `check.py` + baseline + generator).
- **Skeptics (≥2)**: fresh context each, rebuild from scratch, try to break it.
- **Archivist**: files claim + checker + baseline; updates `TROPHY_CASE.md` on pass.

## Rules
- LLM hypotheses (Sanskrit, Dravidian, anything) are scorer inputs, never report outputs.
- Fixed budget per run; stop conditions defined up front (fill in):
  - `max_tool_calls:` _TBD_
  - `max_wallclock_min:` _TBD_
  - `stop_when:` _TBD_
- Network access only where permitted by site rules; no evasion. Violations → retraction.
- Every run logs what was tried, including failures (`claims/<L>/<id>/how-we-built-it/` + run log).
- Notify only on skeptic-confirmed results.

## Hit list (seed; Scout owns this)
- [x] L1: replicate Rao et al. 2009 conditional entropy + rebuttals → L1-0001 (verified), L1-0004 (verified)
- [x] L1: positional / n-gram analyses from Adhikari repo → L1-0002 (confirmed negative: loader spec error), L1-0002b (verified), L1-0003 (verified)
- [x] L1: synthetic-baseline scorecard (arXiv 2604.17828) → metrics compared (Nair 2026), generators cannot-rerun (code upon-request); see `benchmarks/phase2-scorecard.md`
- [x] L2: fixed site/object splits + unigram/n-gram/positional baselines + power analysis → splits v1 frozen; L2-0001 bigram-beats-unigram (verified)
- [x] L4: synthetic + hidden-key calibration harness → L4-0001 (verified): sensitivity floors + emblem profile; hidden-key on real scripts still open
- [x] L4: bigram-assisted hidden-key recovery (L4-0003 candidate from L4-0002 review) → L4-0003 verified-negative 2/2 @α=0.001; CONFIG-SCOPED: α-calibrated rerun (fresh prereg) is the open follow-up
- [x] L4: α-calibrated rerun on disjoint pools + N_ref grid (L4-0004) → verified-pass 2/2 (bounded): reaches bar at 974, collapses ≤250; top-10 bar weakly separated — any L3 attempt needs a STRENGTHENED key gate (structureless-null arm / full-key bar / higher bar) as its L4 prerequisite
- [x] L0: G-scheme bridge (Phase-1 scheme debt) → L0-0003 verified 2/2: gp-v01.csv (22 clean G→P, stable core 16; 15 G→P→M chains via pwm-v01); open: tail signs need more shared texts (ICIT/M77 index blocked); v0.2 edit-distance alignment candidate
- [x] L4: strengthened key gate on a fresh cell (sk4 spec, L4-0005) → verified-negative 2/2: dev bar missed at every α (frozen reading); gate fails under every reading tried; L4-0004 pass = boundary draw; L3 SHUT — named follow-up: preregistered normalized-position positional term (dev bar near-reachable 6/10)
- [x] Candidate (ported 2026-11-02 from the Oct-18 branch): rank-init on a fresh sealed key → L4-0007 verified NEGATIVE 2/2: 5/10 top-10, key-invariant by construction
- [x] Candidate (ported 2026-11-02 from the Oct-18 branch): positional-gate extension (L1-0002b machinery on Sumerian windows) → L4-0008 verified NEGATIVE 2/2: gap 5 inside null band; Indus beginner/ender effect is corpus-specific
- [x] L4-0006 verified NEGATIVE 2/2 (sk6-C, sk6-D): top-10 gate fails on fresh cell #3 (2/3/5, keys_ge8=0) despite dev 9/10; full-key ~2x null but unweighted-only (token-weighted 1.27x) and bucket-edge-sensitive; dev-rule calibration unreliable
- [ ] L4-0009 (preregistered 2026-11-03): full-key-separation gate on fresh cell #4 (V_U9=371; seeds +10000/+11000), alpha frozen at 0.5; thresholds 1.5x / 1.25x / 0.060 frozen before any recovery — RESULT: gate FAILS at half-replication (B = 1.00x null_max) despite committed 0.1725 vs null_max 0.0674 (2.56x) and all 3 keys replicating; next question is the A/B half asymmetry

## Open decisions (planner §10)
- [ ] Compute + token budget per daily run
- [ ] Which external epigrapher/linguist reviewer(s)
- [ ] Include seal iconography / find context now or later
