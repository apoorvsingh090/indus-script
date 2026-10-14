# claims/ — one folder per claim

```
claims/
  _template/     # copy this to L<level>/<id>/
  L0/ L1/ L2/ L3/ L4/ L5/
```

Each claim folder MUST contain:
- `claim.yaml` (copy of `_template/claim.yaml`, filled in)
- `check.py` (readable in one sitting; exits 0 on pass, non-zero + message on fail)
- `baseline_snapshot/` or `baseline_snapshot.md` (table/split it beats)
- `how-we-built-it/` (code + notes to regenerate `object`)
- `object` (the artifact: json/csv/model/etc.)

Statuses: `draft | under-skeptic-review | verified | failed-reproduction | withdrawn`.
Only `verified` (≥2 independent skeptics) lands in `TROPHY_CASE.md`.
