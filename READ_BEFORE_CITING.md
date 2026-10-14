# READ BEFORE CITING

This repo is **verification-first**. Most content here is unverified by design.

## Rules

1. **Nothing in `claims/` counts unless** its `claim.yaml` has `status: verified` with ≥2 independent skeptic IDs listed, and the checker passes on the pinned `corpus_snapshot_sha256`.
2. **LLM-produced readings are hypotheses, never evidence.** Do not cite them as results, even if they look fluent. See `planner.md` §1.
3. **Check the sign scheme.** Counts under `ICIT` vs `M77` vs `P82` are not comparable without `data/concordance/`. The scheme is pinned in every `claim.yaml`.
4. **Check the snapshot hash.** If `data/processed/SHA256SUMS` does not contain the claimed hash, the claim is stale.
5. **Synthetic / model-generated sequences are never real data.** `hellosindh/indus-script-models` and any `synthetic/` outputs must not be cited as Indus attestations.
6. **Translations in third-party repos are outputs of unverified methods, not labels.** We strip them on ingest.
7. **Sealed envelopes (`sealed-envelopes/`) are commitments, not results.** Only cite after the reveal + confirmation.
8. **Negatives count.** `TROPHY_CASE.md` lists failed replications too — check it before claiming novelty.

## How to cite a verified claim

```
<author>, indus-script <claim-id> (<short hash>), <sign-scheme>,
corpus <snapshot-sha256-short>, checker <path>, skeptics [<ids>]
```

If any of those fields are missing, do not cite it as verified.
