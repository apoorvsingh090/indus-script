"""Shared entropy helpers for L1-0001. Imported by run_replication.py and check.py."""
import math
from collections import Counter

SEED = 260417828
N_SHUFFLES = 200


def load_sequences(csv_path):
    """Return (seqs, vocab_size): exact-deduped token lists, as-stored order."""
    import csv
    seen, seqs = set(), []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("sign_sequence") or "").strip()
            if not s or s in seen:
                continue
            seen.add(s)
            seqs.append(s.split())
    vocab = {t for s in seqs for t in s}
    return seqs, len(vocab)


def mm_entropy(counts, n_total):
    """Miller-Madow-corrected ML entropy in bits."""
    h = -sum((c / n_total) * math.log2(c / n_total) for c in counts if c > 0)
    return h + (len(counts) - 1) / (2 * n_total * math.log(2))


def corpus_stats(seqs, vocab_size):
    """Return dict with H1, H2, C=(H2-H1)/log2(L) (MM-corrected, bits)."""
    uni = Counter(t for s in seqs for t in s)
    n1 = sum(uni.values())
    bi = Counter((a, b) for s in seqs for a, b in zip(s, s[1:]))
    n2 = sum(bi.values())
    h1 = mm_entropy(list(uni.values()), n1)
    h2 = mm_entropy(list(bi.values()), n2)
    logL = math.log2(vocab_size)
    return {
        "n_texts": len(seqs),
        "n_tokens": n1,
        "n_transitions": n2,
        "vocab": vocab_size,
        "H1_bits": h1,
        "H2_bits": h2,
        "H1_norm": h1 / logL,
        "C_cond_norm": (h2 - h1) / logL,
    }


def shuffled_C(seqs, vocab_size, seed=SEED, b=N_SHUFFLES):
    """Null: permute all tokens across fixed lengths; return list of C values."""
    import random
    rng = random.Random(seed)
    lens = [len(s) for s in seqs]
    pool = [t for s in seqs for t in s]
    out = []
    for _ in range(b):
        rng.shuffle(pool)
        it = iter(pool)
        sh = [[next(it) for _ in range(k)] for k in lens]
        out.append(corpus_stats(sh, vocab_size)["C_cond_norm"])
    return out


def uniform_C(seqs, vocab_size, seed=SEED + 1):
    """Control: iid uniform draws over vocab at same lengths."""
    import random
    rng = random.Random(seed)
    vocab = [f"S{i}" for i in range(vocab_size)]
    syn = [[rng.choice(vocab) for _ in range(len(s))] for s in seqs]
    return corpus_stats(syn, vocab_size)["C_cond_norm"]
