"""Synthetic corpora for L4-0001. All randomness from GEN_SEED sub-streams."""
import hashlib
import random
import re
from pathlib import Path

GEN_SEED = 260417834
SIZES = (250, 500, 1000, 1948)
PANDP_URL = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
PANDP_SHA = "7c13190c04773de0a919e38450ecaac1673fbd572a60bad784ff8421acdfec18"


def fetch_words(scratch):
    """Download P&P once into scratch, verify sha, return word list."""
    import urllib.request

    p = Path(scratch) / "pg1342.txt"
    if not p.exists():
        urllib.request.urlretrieve(PANDP_URL, p)
    raw = p.read_text(encoding="utf-8")
    assert hashlib.sha256(raw.encode()).hexdigest() == PANDP_SHA, "P&P sha mismatch"
    a = raw.find("START OF TH")
    b = raw.find("END OF TH")
    body = raw[raw.index("\n", a):b]
    return re.findall(r"[a-z]+", body.lower())


def indus_lengths(splits_dir):
    """Resampling pool: corrected-order lengths from frozen splits v1."""
    import json
    lens = []
    for n in ("train", "val", "test"):
        for line in open(Path(splits_dir) / f"{n}.jsonl", encoding="utf-8"):
            lens.append(len(json.loads(line)["signs"]))
    return lens


def linguistic_corpus(words, lens_pool, n, seed):
    """Contiguous excerpts: random start, walk forward non-overlapping, wrap if needed."""
    rng = random.Random(seed)
    lens = [lens_pool[rng.randrange(len(lens_pool))] for _ in range(n)]
    start = rng.randrange(len(words))
    seqs, i = [], start
    for L in lens:
        seq = [words[(i + k) % len(words)] for k in range(L)]
        seqs.append(seq)
        i = (i + L) % len(words)
    return seqs


def emblem_corpus(lens_pool, n, seed):
    """Heraldic-style: opener + Zipfian core + closer (+5% singleton)."""
    rng = random.Random(seed)
    openers = [f"OP{i}" for i in range(8)]
    core_w = [(k + 1) ** -1.0 for k in range(40)]
    core = [f"CO{i}" for i in range(40)]
    closers = [f"CL{i}" for i in range(6)]
    singletons = [f"SG{i}" for i in range(200)]
    seqs = []
    for _ in range(n):
        L = lens_pool[rng.randrange(len(lens_pool))]
        s = [rng.choice(openers)]
        for _ in range(max(L - 2, 0)):
            s += [rng.choices(core, core_w)[0]]
        if L >= 2:
            s.append(rng.choice(closers))
        if rng.random() < 0.05:
            s.append(rng.choice(singletons))
        seqs.append(s)
    return seqs


def build_family(family, words, lens_pool, seed_base):
    """Full N=1948 corpus per family; smaller sizes are prefixes (nested)."""
    if family == "linguistic":
        full = linguistic_corpus(words, lens_pool, 1948, seed_base)
    else:
        full = emblem_corpus(lens_pool, 1948, seed_base + 1)
    return {n: full[:n] for n in SIZES}
