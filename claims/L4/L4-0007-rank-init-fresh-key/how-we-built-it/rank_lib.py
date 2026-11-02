"""Exact-rank (rank_init) baseline shipped with L4-0007.

Imported VERBATIM from the audited 2026-10-18 lineage's L4-0003
`keyrec_lib.rank_init` (the definition both skR4-A and skR4-B audited).
Kept here so the claim is self-contained: the current repo's L4-0003 is a
different cell and ships a different rank_init (canonical count-desc/sign-asc
sort), which is NOT the function this claim measured.
"""
from collections import Counter


def rank_init(ref_seqs, cipher_seqs, cipher_types, plain_types):
    """Frequency-rank mapping: i-th most frequent cipher type -> i-th most
    frequent plain type (same 370-type alphabet, permuted). Cipher types absent
    from the cipher half take leftover plain ranks in sorted order."""
    ref_rank = [t for t, _ in Counter(t for s in ref_seqs for t in s).most_common()]
    cyp_rank = [t for t, _ in Counter(t for s in cipher_seqs for t in s).most_common()]
    cyp_pos = {t: i for i, t in enumerate(cyp_rank)}
    plain_idx = {s: i for i, s in enumerate(plain_types)}
    m, used = [], set()
    for c in cipher_types:
        if c in cyp_pos and cyp_pos[c] < len(ref_rank):
            p = plain_idx[ref_rank[cyp_pos[c]]]
        else:
            p = None
        m.append(p)
        if p is not None:
            used.add(p)
    leftover = iter([i for i in range(len(plain_types)) if i not in used])
    return [x if x is not None else next(leftover) for x in m]
