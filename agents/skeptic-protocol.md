# Skeptic protocol (gate checklist)

Skeptics start from a **fresh context**, write their **own code**, rebuild from **raw inputs**.
If they cannot reproduce it, confirm novelty, or accept the definition of "solved", it does not count.

- [ ] Rebuilt from raw inputs in a clean context with independently written code
- [ ] Same sign-coding scheme and corpus snapshot hash (`claim.yaml` matches `SHA256SUMS`)
- [ ] Threshold and split fixed before the run (check timestamps/hashes)
- [ ] Null models and calibration results attached (L1+; L3 requires L4-gated method)
- [ ] Degrees of freedom counted; multiple-comparison correction applied
- [ ] Novelty checked against prior literature (log what was searched)
- [ ] Claim wording matches what was actually shown (no stretch of "solved")
- [ ] Checker runs green from scratch: `python check.py --corpus … --object … --baseline …`

Record each run as `claims/<L>/<id>/skeptics/<skeptic-id>.md` with: verdict
(`reproduced | failed-reproduction | withdrawn`), log, and environment.
≥2 `reproduced` required for `verified`.
