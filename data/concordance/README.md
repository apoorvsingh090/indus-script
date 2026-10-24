# data/concordance — sign-code mappings

Pin one scheme per experiment. Never compare counts across ICIT / M77 / P82
without going through the concordance (planner §4 hygiene).

Files:
- `m77-p82-icit.csv` — placeholder for the authoritative map (Fuls 2023 Ch.2.4/2.5, © blocked).
- `pwm-v01.csv` — PROVISIONAL type-level P→W/M/V from mayig features/ (MIT), built by
  `build_concordance.py` (sha `5c487299…`); 396 P-signs: 227 clean-1:1, 80 multi,
  38 unmapped-WM, 27 unmapped-W, 24 unmapped-M; 13 M-codes shared by >1 P
  (contested). G-scheme NOT bridged in v0.1. Covered by claim L0-0002.
- `gp-v01.csv` — PROVISIONAL type-level G→P from structural alignment of 161
  shared M-numbered Mohenjo-daro unicorn texts (mayig @ad2f1e2 × indus_website
  @47e8616d); 192 G-signs observed: 22 clean bijective, 19 contested (reasons
  listed), 151 unmapped (n_g<5). P orientation reversed vs G corrected order.
  Covered by claim L0-0003; composes with pwm-v01 → 15 clean G→P→M chains.
- Contested splits listed explicitly; L0 checker fails if a contested code is used silently.
