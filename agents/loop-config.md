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
- [ ] L4: synthetic + hidden-key calibration harness

## Open decisions (planner §10)
- [ ] Compute + token budget per daily run
- [ ] Which external epigrapher/linguist reviewer(s)
- [ ] Include seal iconography / find context now or later
