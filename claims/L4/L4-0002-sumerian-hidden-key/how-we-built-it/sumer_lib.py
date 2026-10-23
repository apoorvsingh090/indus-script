"""Sumerian windows + hidden-key test for L4-0002."""
import json
import random
import zipfile
from pathlib import Path

KEY_SEED = 260417835
KEY_SHA256 = "3b6a6c1daccd40ee02ea76b03e9338924fb1b0edf47ea5c6e52403d9b263c517"
KEY_V = 370  # windowed vocab size (design input); key = perm(range(370)) via Random(KEY_SEED + 370)
ETCSRI_URL = "http://oracc.museum.upenn.edu/json/etcsri.zip"
N_WINDOWS = 1948


def make_key(vocab_size, seed_base=KEY_SEED):
    rng = random.Random(seed_base + vocab_size)
    k = list(range(vocab_size))
    rng.shuffle(k)
    return k


def fetch_zip(scratch):
    import urllib.request

    p = Path(scratch) / "etcsri.zip"
    if not p.exists():
        urllib.request.urlretrieve(ETCSRI_URL, p)
    return p


def sign_texts(zip_path):
    """Ordered gdl_sign streams per text; skips undecodable/empty files."""
    z = zipfile.ZipFile(zip_path)
    texts = []

    def walk(nodes, out):
        for nd in nodes:
            if nd.get("node") == "l":
                f = nd.get("f") or {}
                for g in f.get("gdl", []) or []:
                    seq = g.get("seq")
                    if isinstance(seq, list):
                        for s in seq:
                            v = s.get("gdl_sign") or s.get("v")
                            if v:
                                out.append(str(v))
                    elif isinstance(g.get("gdl_sign"), str):
                        out.append(g["gdl_sign"])
            elif nd.get("node") == "c":
                walk(nd.get("cdl", []) or [], out)

    for n in z.namelist():
        if not (n.endswith(".json") and "corpusjson/Q" in n):
            continue
        try:
            raw = z.read(n).decode("utf-8-sig")
            if not raw.strip():
                raise ValueError("empty")
            out = []
            walk(json.loads(raw).get("cdl", []) or [], out)
            if out:
                texts.append(out)
        except Exception:
            continue
    return texts


def indus_lengths(splits_dir):
    lens = []
    for n in ("train", "val", "test"):
        for line in open(Path(splits_dir) / f"{n}.jsonl", encoding="utf-8"):
            lens.append(len(json.loads(line)["signs"]))
    return lens


def windows(texts, lens_pool, n, seed):
    """Token-weighted text choice, random offset, modular wrap; report wrap rate."""
    rng = random.Random(seed)
    weights = [len(t) for t in texts]
    total = sum(weights)
    seqs, wraps = [], 0
    for _ in range(n):
        x = rng.randrange(total)
        acc, ti = 0, 0
        for i, w in enumerate(weights):
            acc += w
            if x < acc:
                ti = i
                break
        t = texts[ti]
        L = lens_pool[rng.randrange(len(lens_pool))]
        off = rng.randrange(len(t))
        seqs.append([t[(off + k) % len(t)] for k in range(L)])
        if off + L > len(t):
            wraps += 1
    return seqs, wraps / n


def load_key(path):
    return json.load(open(path))


def encipher(seqs, vocab_sorted, key):
    mp = {s: vocab_sorted[key[i]] for i, s in enumerate(vocab_sorted)}
    return [[mp[t] for t in s] for s in seqs], mp


def recover_topk(ref_seqs, cipher_seqs, k=10):
    """Rank-order mapping from reference plaintext freqs; score top-k cipher types."""
    from collections import Counter
    ref_rank = [t for t, _ in Counter(t for s in ref_seqs for t in s).most_common()]
    cyp_rank = [t for t, _ in Counter(t for s in cipher_seqs for t in s).most_common()]
    guess = {c: ref_rank[i] for i, c in enumerate(cyp_rank) if i < len(ref_rank)}
    return guess
