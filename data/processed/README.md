# data/processed — frozen snapshots

Canonical parses live here, frozen + checksummed. `SHA256SUMS` is the source of truth
for every `claim.yaml: corpus_snapshot_sha256`.

No snapshot yet (Phase 1 pending). When created:
1. Write `corpus-<scheme>-<date>.jsonl` (one `schema.json` record per line).
2. Run `sha256sum * > SHA256SUMS` and commit both together.
3. Never edit a frozen file — mint a new date-stamped one.
