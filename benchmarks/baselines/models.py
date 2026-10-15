"""L2 baselines v1: unigram, bigram (add-alpha), positional. Train-only fitting.

Conventions (fixed with splits v1): CORRECTED reading order in split files;
slot(pos, length): 0 -> begin; pos == length-1 and length > 1 -> end; else middle.
"""
import math
from collections import Counter, defaultdict

ALPHAS = (0.001, 0.01, 0.1, 1.0)


def load_split(path):
    import json
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def slot(pos, length):
    if pos == 0:
        return "begin"
    if pos == length - 1 and length > 1:
        return "end"
    return "middle"


class Unigram:
    name = "unigram"

    def fit(self, recs):
        self.c = Counter(t for r in recs for t in r["signs"])
        self.n = sum(self.c.values())
        self.vocab = set(self.c)
        self.top = self.c.most_common(1)[0][0]

    def predict(self, prefix, pos, length):
        return self.top

    def logprob(self, prefix, pos, length, sign, alpha=1.0):
        return math.log2((self.c.get(sign, 0) + alpha) / (self.n + alpha * max(len(self.vocab), 1)))


class Bigram:
    name = "bigram"

    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, recs):
        self.uni = Counter(t for r in recs for t in r["signs"])
        self.bi = defaultdict(Counter)
        for r in recs:
            for a, b in zip(r["signs"], r["signs"][1:]):
                self.bi[a][b] += 1
        self.vocab = set(self.uni)
        self.top = self.uni.most_common(1)[0][0]
        self.V = len(self.vocab)

    def predict(self, prefix, pos, length):
        if not prefix:
            return self.top
        prev = prefix[-1]
        if prev not in self.bi:
            return self.top
        tot = sum(self.bi[prev].values())
        best, bk = None, -1.0
        for cand in sorted(self.vocab):  # sorted: deterministic tie-break (never set order)
            p = (self.bi[prev].get(cand, 0) + self.alpha) / (tot + self.alpha * self.V)
            if p > bk:
                best, bk = cand, p
        return best

    def logprob(self, prefix, pos, length, sign, alpha=None):
        a = self.alpha if alpha is None else alpha
        if not prefix or prefix[-1] not in self.bi:
            tot = sum(self.uni.values())
            return math.log2((self.uni.get(sign, 0) + a) / (tot + a * max(len(self.vocab), 1)))
        tot = sum(self.bi[prefix[-1]].values())
        return math.log2((self.bi[prefix[-1]].get(sign, 0) + a) / (tot + a * self.V))


class Positional:
    name = "positional"

    def fit(self, recs):
        self.c = defaultdict(Counter)
        for r in recs:
            L = len(r["signs"])
            for i, t in enumerate(r["signs"]):
                self.c[slot(i, L)][t] += 1
        self.top = {s: c.most_common(1)[0][0] for s, c in self.c.items()}

    def predict(self, prefix, pos, length):
        return self.top[slot(pos, length)]

    def logprob(self, prefix, pos, length, sign, alpha=1.0):
        s = slot(pos, length)
        tot = sum(self.c[s].values())
        V = len({t for c in self.c.values() for t in c})
        return math.log2((self.c[s].get(sign, 0) + alpha) / (tot + alpha * max(V, 1)))


def accuracy(model, recs):
    """Top-1 next-sign accuracy over ALL positions (0..len-1). Returns (acc, per-text accs)."""
    per_text, tot, hit = [], 0, 0
    for r in recs:
        s = r["signs"]
        h = sum(1 for i in range(len(s)) if model.predict(s[:i], i, len(s)) == s[i])
        per_text.append(h / len(s))
        tot += len(s)
        hit += h
    return hit / tot, per_text


def mean_logloss(model, recs):
    tot, ll = 0, 0.0
    for r in recs:
        s = r["signs"]
        for i in range(len(s)):
            ll += model.logprob(s[:i], i, len(s), s[i])
            tot += 1
    return -ll / tot


def paired_bootstrap_ci(per_a, per_b, weights, seed=260417833, b=2000):
    """95% CI for mean(A-B) with texts weighted by length. Returns (lo, hi, diff)."""
    import random
    rng = random.Random(seed)
    n = len(per_a)
    diffs = [a - c for a, c in zip(per_a, per_b)]
    tot_w = sum(weights)
    base = sum(d * w for d, w in zip(diffs, weights)) / tot_w
    boots = []
    for _ in range(b):
        idx = [rng.randrange(n) for _ in range(n)]
        boots.append(sum(diffs[i] * weights[i] for i in idx) / sum(weights[i] for i in idx))
    boots.sort()
    return boots[int(0.025 * b)], boots[int(0.975 * b)], base
