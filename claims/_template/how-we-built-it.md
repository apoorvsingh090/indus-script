# how-we-built-it/

Document exactly how `object` was generated so a skeptic can rebuild from scratch:

- Environment (python version, `pip freeze` or lockfile)
- Commands run, in order, with seeds
- Threshold/split commitment (hash + timestamp, fixed BEFORE the run)
- Null models / calibration attached (L1+)
- What failed (negatives are first-class — log them)
