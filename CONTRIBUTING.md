# Contributing

Public, fork-and-PR workflow. No direct repo invites needed — anyone can contribute.

## Ways to contribute

- **Replicate** an existing claim or baseline from scratch (most valuable).
- **File a claim** (`claims/L<level>/<id>/`) with `claim.yaml` + `check.py` + baseline + `how-we-built-it/`.
- **Skeptic review**: rebuild a claim in a fresh context, file report in `skeptics/`.
- **Negatives/partials welcome** — they go in `TROPHY_CASE.md` too.

## Rules (from `planner.md`)

1. Read `READ_BEFORE_CITING.md` + `agents/skeptic-protocol.md` first.
2. Pin one sign scheme per experiment (`ICIT` / `M77` / `P82`); cross-scheme counts need a concordance.
3. Fix thresholds/splits BEFORE running (commit hash/timestamp as proof).
4. LLM readings are scorer inputs, never outputs.
5. No bypassing site access controls — violations are retracted.
6. Every `check.py` must be readable in one sitting and exit 0/`PASS` only on real recompute.

## PR flow

1. Fork → branch `claim/<L>-<id>-short-name`.
2. Copy `claims/_template/` to `claims/<L>/<id>/`, fill in all fields.
3. `verify-claim` CI must pass (valid `claim.yaml` keys).
4. Request review; ≥2 independent skeptic reproductions required for `verified`.
5. Archivist updates `TROPHY_CASE.md` on pass (maintainers only).

Questions? Use [GitHub Discussions](https://github.com/apoorvsingh090/indus-script/discussions) — `Q&A` for methods, `Ideas` for targets. For sealed L5 predictions, commit only the hash to `sealed-envelopes/registry.csv`.
