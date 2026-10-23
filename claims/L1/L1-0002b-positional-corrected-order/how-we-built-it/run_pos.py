#!/usr/bin/env python3
"""Generator for L1-0002b. Run AFTER the preregistration commit.
Writes object/results.json + baseline_snapshot/nulls.json.
Usage: python run_pos.py <corpus.csv> <claim_dir>
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pos_lib import cramers_v, hapax_rate, load_sequences, null_n80_end, pos_stats, zipf_slope


def site_groups(csv_path):
    """Oriented sequences grouped by site (global dedup keeps first occurrence's site)."""
    groups, seen = {}, set()
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
            groups.setdefault(row.get("site") or "unknown", []).append(toks)
    return groups


def main() -> int:
    corpus, claim = Path(sys.argv[1]), Path(sys.argv[2])
    seqs, n_raw, n_lr = load_sequences(str(corpus))
    st = pos_stats(seqs)
    nulls = sorted(null_n80_end(seqs))
    top10 = [s for s, _ in Counter(t for s in seqs for t in s).most_common(10)]
    v = cramers_v(seqs, top10)
    hap, _ = hapax_rate(seqs)
    st |= {
        "n_raw_rows": n_raw,
        "n_reversed_LR": n_lr,
        "rigidity_mean_V": sum(v.values()) / len(v),
        "rigidity_V": v,
        "hapax_rate": hap,
        "zipf_slope": zipf_slope(seqs),
    }
    groups = site_groups(str(corpus))
    site_v = {}
    for site in ("Mohenjo-daro", "Harappa"):
        g = groups.get(site, [])
        if len(g) >= 50:
            gv = cramers_v(g, [s for s, _ in Counter(t for x in g for t in x).most_common(10)])
            site_v[site] = {"n": len(g), "mean_V": sum(gv.values()) / len(gv)}
    st["site_V"] = site_v
    (claim / "object" / "results.json").write_text(json.dumps(st, indent=2))
    (claim / "baseline_snapshot" / "nulls.json").write_text(
        json.dumps({"method": "permute tokens across fixed lengths (corrected order)",
                    "B": len(nulls), "seed": 260417832, "n80_end_sorted": nulls}, indent=2)
    )
    print(f"raw={n_raw} reversed={n_lr} texts={st['n_texts']} vocab={st['vocab']}")
    print(f"n80 all/begin/end = {st['n80_all']}/{st['n80_begin']}/{st['n80_end']}")
    print(f"null n80_end min={nulls[0]} max={nulls[-1]}")
    print(f"V={st['rigidity_mean_V']:.4f} hapax={hap:.4f} zipf={st['zipf_slope']:.4f} sites={site_v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
