# Agent loop config (daily run)

## Roles
- **Scout**: maintains hit list; picks a few targets per run (from L1â†’L3 sub-problems).
- **Builder**: attempts a target; produces claim artifacts (`claim.yaml` + `check.py` + baseline + generator).
- **Skeptics (â‰¥2)**: fresh context each, rebuild from scratch, try to break it.
- **Archivist**: files claim + checker + baseline; updates `TROPHY_CASE.md` on pass.

## Rules
- LLM hypotheses (Sanskrit, Dravidian, anything) are scorer inputs, never report outputs.
- Fixed budget per run; stop conditions defined up front (fill in):
  - `max_tool_calls:` _TBD_
  - `max_wallclock_min:` _TBD_
  - `stop_when:` _TBD_
- Network access only where permitted by site rules; no evasion. Violations â†’ retraction.
- Every run logs what was tried, including failures (`claims/<L>/<id>/how-we-built-it/` + run log).
- Notify only on skeptic-confirmed results.

## Hit list (seed; Scout owns this)
- [x] L1: replicate Rao et al. 2009 conditional entropy + rebuttals â†’ L1-0001 (verified), L1-0004 (verified)
- [x] L1: positional / n-gram analyses from Adhikari repo â†’ L1-0002 (confirmed negative: loader spec error), L1-0002b (verified), L1-0003 (verified)
- [x] L1: synthetic-baseline scorecard (arXiv 2604.17828) â†’ metrics compared (Nair 2026), generators cannot-rerun (code upon-request); see `benchmarks/phase2-scorecard.md`
- [x] L2: fixed site/object splits + unigram/n-gram/positional baselines + power analysis â†’ splits v1 frozen; L2-0001 bigram-beats-unigram (verified)
- [x] L4: synthetic + hidden-key calibration harness â†’ L4-0001 (verified): sensitivity floors + emblem profile; hidden-key on real scripts still open
- [x] L4: bigram-assisted hidden-key recovery (L4-0003 candidate from L4-0002 review) â†’ L4-0003 verified-negative 2/2 @Î±=0.001; CONFIG-SCOPED: Î±-calibrated rerun (fresh prereg) is the open follow-up
- [x] L4: Î±-calibrated rerun on disjoint pools + N_ref grid (L4-0004) â†’ verified-pass 2/2 (bounded): reaches bar at 974, collapses â‰¤250; top-10 bar weakly separated â€” any L3 attempt needs a STRENGTHENED key gate (structureless-null arm / full-key bar / higher bar) as its L4 prerequisite
- [x] L0: G-scheme bridge (Phase-1 scheme debt) â†’ L0-0003 verified 2/2: gp-v01.csv (22 clean Gâ†’P, stable core 16; 15 Gâ†’Pâ†’M chains via pwm-v01); open: tail signs need more shared texts (ICIT/M77 index blocked); v0.2 edit-distance alignment candidate
- [x] L4: strengthened key gate on a fresh cell (sk4 spec, L4-0005) â†’ verified-negative 2/2: dev bar missed at every Î± (frozen reading); gate fails under every reading tried; L4-0004 pass = boundary draw; L3 SHUT â€” named follow-up: preregistered normalized-position positional term (dev bar near-reachable 6/10)
- [x] Candidate (ported 2026-11-02 from the Oct-18 branch): rank-init on a fresh sealed key â†’ L4-0007 verified NEGATIVE 2/2: 5/10 top-10, key-invariant by construction
- [x] Candidate (ported 2026-11-02 from the Oct-18 branch): positional-gate extension (L1-0002b machinery on Sumerian windows) â†’ L4-0008 verified NEGATIVE 2/2: gap 5 inside null band; Indus beginner/ender effect is corpus-specific
- [x] L4-0006 verified NEGATIVE 2/2 (sk6-C, sk6-D): top-10 gate fails on fresh cell #3 (2/3/5, keys_ge8=0) despite dev 9/10; full-key ~2x null but unweighted-only (token-weighted 1.27x) and bucket-edge-sensitive; dev-rule calibration unreliable
- [x] L4-0009 verified NEGATIVE 2/2 (sk9-A, sk9-B): full-key-separation gate on fresh cell #4 (alpha frozen 0.5) - committed 0.1725 vs null 0.0674 (2.56x), all 3 keys replicate, top-10 would clear the old bar, but half B = 1.00x null_max; (c) is calibration-sensitive (half-scale null 19/371 -> B 1.32x); successor half-split gates must preregister half-scale nulls; next question: half-B   composition (ref-bigram coherence)
- [ ] L4-0010 (preregistered 2026-11-05): full-key-separation gate v2 on fresh cell #5 (V_U10=353; pools +12000, windows +12100/+12200, keys +13000..+13003), alpha frozen 0.5. Gate v2 = L4-0009 conditions PLUS matched-scale half nulls (974-permuted-ref + 487-cyp half, K=12) as (c1)/(c2), the original full-scale half reading kept as (c3), and a token-weighted guard (d) committed TW >= 1.25x max null TW. Design answers the two skeptic findings: half-scale null calibration (sk9-B) and token-weighted specificity (sk6-D/sk9-B). Band policy: margins < 3/353 flagged. Runtime ~1h45. [RESULTS 2026-11-05] gate FAILS only at (c3) legacy full-scale half reading (half A 0.625x full-null) while v2 matched-scale conditions pass on both halves (A at exact equality 10/353 vs 1.25x8; B 39/353 decisively); (a) 1.88x, (b) 3/3 keys, (d) TW guard 1.65x pass; committed 30/353 (0.0850), alt1 28, alt2 64; composition diag corrected post-run (plaintext-arm bug, report-only only). NEXT: checker confirm, then 2 skeptics, then fold.

## Open decisions (planner Â§10)
- [ ] Compute + token budget per daily run
- [ ] Which external epigrapher/linguist reviewer(s)
- [ ] Include seal iconography / find context now or later
