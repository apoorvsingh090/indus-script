"""N-gram repetition helpers for L1-0003."""
from collections import Counter, defaultdict

SEED = 260417830
N_SHUFFLES = 200


def load_oriented(csv_path):
    """Corrected order (reverse L-R rows), exact-dedup after orienting."""
    import csv
    seqs, seen = [], set()
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("sign_sequence") or "").strip()
            if not s:
                continue
            toks = s.split()
            if (row.get("reading_direction") or "").strip() == "L-R":
                toks = list(reversed(toks))
            key = " ".join(toks)
            if key in seen:
                continue
            seen.add(key)
            seqs.append(toks)
    return seqs


def repeated_counts(seqs, k):
    """Distinct length-k substrings occurring in >=2 distinct inscriptions."""
    owners = defaultdict(set)
    for i, s in enumerate(seqs):
        for j in range(len(s) - k + 1):
            owners[tuple(s[j:j + k])].add(i)
    rep = {ph: sorted(v) for ph, v in owners.items() if len(v) >= 2}
    return len(rep), rep


def null_rep(seqs, k, seed=SEED, b=N_SHUFFLES):
    import random
    rng = random.Random(seed)
    lens = [len(s) for s in seqs]
    pool = [t for s in seqs for t in s]
    out = []
    for _ in range(b):
        rng.shuffle(pool)
        it = iter(pool)
        sh = [[next(it) for _ in range(n)] for n in lens]
        out.append(repeated_counts(sh, k)[0])
    return out


def successor_coverage(seqs, top_n=10):
    """Mean over top-N signs of top-3-successor share of outgoing transitions."""
    uni = Counter(t for s in seqs for t in s)
    top = [s for s, _ in uni.most_common(top_n)]
    nxt = defaultdict(Counter)
    for s in seqs:
        for a, c in zip(s, s[1:]):
            nxt[a][c] += 1
    cov = {}
    for g in top:
        tot = sum(nxt[g].values())
        cov[g] = sum(c for _, c in nxt[g].most_common(3)) / tot if tot else 0.0
    return sum(cov.values()) / len(cov), cov
