"""Zipfian-control helpers for L1-0004."""
import math
from collections import Counter

SEED = 260417831


def load_oriented(csv_path):
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
    vocab = {t for s in seqs for t in s}
    return seqs, len(vocab)


def mm_point(seqs, vocab_size):
    """MM-corrected (H1_norm, C) with base-vocab logs."""
    uni = Counter(t for s in seqs for t in s)
    n1 = sum(uni.values())
    bi = Counter((a, b) for s in seqs for a, b in zip(s, s[1:]))
    n2 = sum(bi.values())

    def mm(counts, n):
        h = -sum((c / n) * math.log2(c / n) for c in counts if c > 0)
        return h + (len(counts) - 1) / (2 * n * math.log(2))

    h1, h2 = mm(list(uni.values()), n1), mm(list(bi.values()), n2)
    logL = math.log2(vocab_size)
    return h1 / logL, (h2 - h1) / logL


def zipf_s_ols(seqs):
    import statistics
    freqs = sorted(Counter(t for s in seqs for t in s).values(), reverse=True)
    xs = [math.log(i + 1) for i in range(len(freqs))]
    ys = [math.log(f) for f in freqs]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    return -sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def synth_zipf(lens, vocab_size, s, seed=SEED):
    """iid draws with p(k) proportional to k^-s over vocab_size types."""
    import random
    rng = random.Random(seed)
    weights = [(k + 1) ** (-s) for k in range(vocab_size)]
    types = [f"Z{i}" for i in range(vocab_size)]
    return [[rng.choices(types, weights)[0] for _ in range(n)] for n in lens]
