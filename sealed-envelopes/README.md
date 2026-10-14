# sealed-envelopes — hashes only

Pre-register predictions about unpublished inscriptions/finds (L5) by committing
**only the hash** here. Reveal later; confirmation requires the pre-image to match.

## Format (`registry.csv`)

`id,level,description,sha256,created_utc,reveal_status`

Hash = `sha256(prediction-file-bytes)`. Keep the file private until reveal.
No prediction counts without a pre-dating commit hash visible on GitHub.
