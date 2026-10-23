"""Corrected-order positional helpers for L1-0002b. Loader convention applied."""
import math
from collections import Counter

SEED = 260417832
N_SHUFFLES = 200


def load_sequences(csv_path):
    """Orient per reading_direction flag, THEN exact-dedup. Returns (seqs, n_raw, n_flag_lr)."""
    import csv
    seqs, seen = [], set()
    n_raw = n_lr = 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("sign_sequence") or "").strip()
            if not s:
                continue
            n_raw += 1
            toks = s.split()
            if (row.get("reading_direction") or "").strip() == "L-R":
                toks = list(reversed(toks))
                n_lr += 1
            key = " ".join(toks)
            if key in seen:
                continue
            seen.add(key)
            seqs.append(toks)
    return seqs, n_raw, n_lr


def positions(seqs):
    for s in seqs:
        for i, t in enumerate(s):
            if i == 0:
                yield t, "begin"
            elif i == len(s) - 1 and len(s) > 1:
                yield t, "end"
            else:
                yield t, "middle"


def n80(counter):
    tot = sum(counter.values())
    acc, k = 0, 0
    for _, c in counter.most_common():
        acc += c
        k += 1
        if acc >= 0.8 * tot:
            return k
    return k


def pos_stats(seqs):
    uni = Counter(t for s in seqs for t in s)
    beg = Counter(t for t, p in positions(seqs) if p == "begin")
    end = Counter(t for t, p in positions(seqs) if p == "end")
    return {
        "n_texts": len(seqs),
        "vocab": len(uni),
        "n80_all": n80(uni),
        "n80_begin": n80(beg),
        "n80_end": n80(end),
        "top_begin": beg.most_common(5),
        "top_end": end.most_common(5),
    }


def null_n80_end(seqs, seed=SEED, b=N_SHUFFLES):
    import random
    rng = random.Random(seed)
    lens = [len(s) for s in seqs]
    pool = [t for s in seqs for t in s]
    out = []
    for _ in range(b):
        rng.shuffle(pool)
        it = iter(pool)
        sh = [[next(it) for _ in range(k)] for k in lens]
        end = Counter(s[-1] for s in sh if len(s) > 1)
        out.append(n80(end))
    return out


def cramers_v(seqs, signs):
    import collections
    slot_tot = collections.Counter(p for _, p in positions(seqs))
    n = sum(slot_tot.values())
    vs = {}
    for g in signs:
        tab = {(g, p): 0 for p in ("begin", "middle", "end")}
        notab = dict.fromkeys(("begin", "middle", "end"), 0)
        for t, p in positions(seqs):
            if t == g:
                tab[(g, p)] += 1
            else:
                notab[p] += 1
        chi2 = 0.0
        row_g = sum(tab.values())
        for p in ("begin", "middle", "end"):
            for obs, row in ((tab[(g, p)], row_g), (notab[p], n - row_g)):
                exp = row * slot_tot[p] / n
                if exp > 0:
                    chi2 += (obs - exp) ** 2 / exp
        vs[g] = math.sqrt(chi2 / n)
    return vs


def hapax_rate(seqs):
    uni = Counter(t for s in seqs for t in s)
    return sum(1 for c in uni.values() if c == 1) / len(uni), len(uni)


def zipf_slope(seqs):
    import statistics
    freqs = sorted(Counter(t for s in seqs for t in s).values(), reverse=True)
    xs = [math.log(i + 1) for i in range(len(freqs))]
    ys = [math.log(f) for f in freqs]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
