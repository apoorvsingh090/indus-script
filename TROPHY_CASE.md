# Trophy Case — Verified Results (including negatives)

> Only skeptic-confirmed results land here. Everything else stays in `claims/<L>/` with its own status.
> Format: one row per claim. Negatives and partials are first-class.

| Claim | Level | Result | Corpus | Scheme | Skeptics | Date |
|---|---|---|---|---|---|---|
| [L1-0001](claims/L1/L1-0001-rao-entropy-replication/claim.yaml) | L1 | C=0.4098 < null-min 0.5593 (97σ) and < uniform 0.4642 — Rao-2009 structural pattern replicates (partial: pattern-level, not numeric) | indus_website @47e8616d (`72580755…`) | G-592 | skeptic-task-01, skeptic-task-02 | 2026-10-14 |
| [L1-0002](claims/L1/L1-0002-positional-beginners-enders/claim.yaml) | L1 | NEGATIVE: as-stored n80 27/103 fails gate — cause confirmed as loader-convention spec error (corrected follow-up: L1-0002b) | indus_website @47e8616d | G-592 | skneg-01, skneg-02 | 2026-10-14 |
| [L1-0002b](claims/L1/L1-0002b-positional-corrected-order/claim.yaml) | L1 | n80 107/32 beats null (min 67) — mirrors Adhikari 82/23; V 0.156, site-V, hapax, Zipf all match Nair-2026 neighborhood | indus_website @47e8616d | G-592 | sk2b-A, sk2b-B | 2026-10-14 |
| [L1-0003](claims/L1/L1-0003-formulaic-ngrams/claim.yaml) | L1 | rep3 576 / rep4 189 beat nulls (111/4); match Nair 565/187 | indus_website @47e8616d | G-592 | sk3-A, sk3-B | 2026-10-14 |
| [L1-0004](claims/L1/L1-0004-zipfian-control-distance/claim.yaml) | L1 | iid-Zipf distinguishable d=0.27 (C-alone matches; H1n separates — Rao's reply point, measured independently) | indus_website @47e8616d | G-592 | sk4-A, sk4-B | 2026-10-14 |
| [L2-0001](claims/L2/L2-0001-bigram-beats-unigram/claim.yaml) | L2 | bigram 0.1738 beats unigram 0.1162 on Harappa held-out (diff 0.0576, CI95 [0.0453, 0.0698]); positional 0.1029 < unigram as found | splits v1 (`0398a16b…`) | G-592 | skL2-A, skL2-B | 2026-10-15 |
| [L4-0001](claims/L4/L4-0001-synthetic-calibration/claim.yaml) | L4 | linguistic-like@1948 passes ENT+L2+REP; N_min ENT≤250 / L2=500 fixed-split (robust 1000) / panel=1000; emblem L2-negative at all N | synthetic (P&P + templates) | SYNTH | skL4-A, skL4-B | 2026-10-15 |
| [L0-0001](claims/L0/L0-0001-mayig-joy-xcheck/claim.yaml) | L0 | mayig→joy cisi derivation faithful 179/179 exact (bijection, no drops); info-loss inventoried | joy cisi (`431b42a4…`) + mayig @ad2f1e2 | P-codes | skL0-A, skL0-B | 2026-10-15 |

## How entries get added

Via the Archivist role only, after the skeptic gate passes (`agents/skeptic-protocol.md`).
Each entry links to `claims/<L>/<id>/claim.yaml` + checker output log.
