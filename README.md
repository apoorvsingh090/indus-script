# Indus Script — Verification-First Repo

[![ci](https://img.shields.io/github/actions/workflow/status/apoorvsingh090/indus-script/ci.yml?branch=main)](https://github.com/apoorvsingh090/indus-script/actions/workflows/ci.yml)
[![verify-claim](https://img.shields.io/github/actions/workflow/status/apoorvsingh090/indus-script/verify-claim.yml?branch=main)](https://github.com/apoorvsingh090/indus-script/actions/workflows/verify-claim.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Nothing counts until independent skeptics reproduce it.
> Modeled on the discipline of elder-plinius/V3R1T4S and the "Daily Oracle" thread, not on its targets.

See `planner.md` for the full plan. See `READ_BEFORE_CITING.md` before citing or reusing anything here.

## Goal / non-goals

**Goal:** build a repo of falsifiable claims about the Indus script, worked by autonomous agents, where nothing counts until reproduced.

**Non-goals:**
- Declaring the script "deciphered". No bilingual, unknown language, very short inscriptions — a fluent reading proves nothing.
- Treating LLM-produced readings as evidence. They are hypotheses to be scored, never results.

## Claim ladder

| Level | Claim type | Pass condition |
|---|---|---|
| L0 | Corpus and sign list | Counts reconcile; contested splits listed |
| L1 | Structural (direction, positional, entropy stats) | Beats nulls at pre-fixed threshold |
| L2 | Prediction (masked/next-sign, held-out) | Beats structural baseline |
| L3 | Reading claims (sign→value map) | Beats L2 + survives skeptics; requires L4-gated method |
| L4 | Calibration (hidden-key + synthetic) | Recovers known answers at Indus data size |
| L5 | Future-facing sealed predictions | Confirmed after release |

Rule: **no L3 accepted from a method that has not passed L4.**

## Repo layout

```
indus-script/
  README.md  planner.md  READ_BEFORE_CITING.md
  data/
    raw/            # untouched + provenance + license per file
    processed/      # frozen snapshots + SHA256SUMS
    concordance/    # M77 / P82 / ICIT mappings
    schema.json     # inscription record schema (Phase 1)
  claims/
    L0/ ... L5/     # one folder per claim: object, checker, baseline, how-we-built-it
    _template/      # claim.yaml + check.py template
  benchmarks/
    splits/  baselines/  calibration/
  agents/
    prompts/  skeptic-protocol.md  loop-config.md
  sealed-envelopes/ # hashes only
  TROPHY_CASE.md    # verified results, incl. negatives
```

## Every claim ships four things

1. `object` — the artifact itself
2. `checker` (`check.py`) — readable in one sitting
3. `baseline_snapshot` — table/split it beats
4. `generator` (`how-we-built-it/`) — code that generated it

Plus `claim.yaml` (see `claims/_template/claim.yaml`). Skeptics rebuild from raw inputs in a clean context with independently written code.

## Status

Phase 0 in progress. See `planner.md` §5 for milestones, `TROPHY_CASE.md` for verified results (currently none).

## Data access

No corpus files are vendored yet. See `data/raw/README.md` + `data/raw/provenance.csv` for sources, status, and license TODOs. Anything that depended on bypassing a site's controls is retracted per planner §2.5.

## Contributing

Open to all via fork + PR — see [`CONTRIBUTING.md`](CONTRIBUTING.md) for the
full rules (read `READ_BEFORE_CITING.md` and `agents/skeptic-protocol.md`
first; pin one sign scheme per experiment; fix thresholds/splits *before*
running with timestamp/hash proof; file negatives and partials — they go in
`TROPHY_CASE.md` too). No invite needed.

Use [Discussions](https://github.com/apoorvsingh090/indus-script/discussions)
for Q&A and target ideas, and the `claim` / `skeptic` issue templates for
reviews. Epigraphers and linguists especially welcome as external reviewers
(planner Phase 0). By participating you agree to the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Security

Report vulnerabilities (checker short-circuits, sealed-envelope leaks, CI
bypass) privately via
[GitHub Security Advisories](https://github.com/apoorvsingh090/indus-script/security/advisories);
see [SECURITY.md](SECURITY.md).

## License

Code: MIT (`LICENSE`). Data: per-file terms in `data/raw/provenance.csv` — see `DATA_NOTICE.md`; verify before reuse, do not assume redistribution is allowed.
