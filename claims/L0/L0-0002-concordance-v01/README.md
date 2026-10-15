# L0-0002 — Concordance v0.1 reconciles: GATE PASS

`data/concordance/pwm-v01.csv` rebuilt byte-identical from mayig @ad2f1e2
(sha `5c487299…`): 396 P-signs → 227 clean-1:1, 80 multi, 38 unmapped-WM,
27 unmapped-W, 24 unmapped-M; 13 M-codes claimed by >1 P (e.g. M161 by
P085/P086) — the contested list the ladder requires.

Scope honesty: type-level grapheme sets only; G-scheme (our working corpus)
unbridged; mayig judgments provisional vs Fuls authority. This table lets
future claims convert P-side counts to M-side approximately — with the
multi/unmapped rows forcing explicit contested-code handling.

Status glossary: `clean-1:1` = exactly one W and one M per P; `multi` = split
or merge on either side (contested); `unmapped-W` = has M but no W;
`unmapped-M` = has W but no M; `unmapped-WM` = neither. Schema = CSV header
`p,w_list,m_list,v_list,status` (pipe-joined, source order).
