# Security Policy

## Reporting a vulnerability

Report **privately**, never as a public issue:

1. Preferred: GitHub Security Advisories —
   **Security tab → Report a vulnerability**
   (https://github.com/apoorvsingh090/indus-script/security/advisories/new).
2. Otherwise contact [@apoorvsingh090](https://github.com/apoorvsingh090)
   via GitHub's private contact options.

Please allow time for a fix before public disclosure.

## Scope

In scope:

- **Sealed-envelope integrity:** anything that could leak or forge a future
  prediction hash in `sealed-envelopes/` before release
- **Checker trust:** a `check.py` that can pass without real recomputation
  (short-circuits, hardcoded PASS, network lookups that change results) —
  this is a integrity-critical bug for this repo's purpose
- **CI bypass:** workflows that could mark `verify-claim` green without
  validation
- **Data provenance:** corpus files committed without `provenance.csv`
  entries or with licenses that don't allow redistribution
- Secrets accidentally committed (`.env`, API keys, cookies — already
  git-ignored; report leaks so history can be cleaned)

Out of scope:

- The scientific disagreement with any claim's conclusion (that's what
  skeptic review is for — use the `skeptic` issue template)
- Quality of LLM-produced readings (they are scorer inputs, never results)

## Design notes

- Every claim must pass its `check.py` from scratch in CI (`verify-claim`).
- Thresholds/splits are preregistered with commit/timestamp proof before runs.
- Anything that depended on bypassing a site's access controls is retracted
  per `planner.md` §2.5.

## Supported versions

Only the latest code on `main` is supported.
