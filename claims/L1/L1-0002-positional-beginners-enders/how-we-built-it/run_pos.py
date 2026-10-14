#!/usr/bin/env python3
"""Generator for L1-0002. Run AFTER the preregistration commit.
Writes object/results.json + baseline_snapshot/nulls.json.
Usage: python run_pos.py <corpus.csv> <claim_dir>
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pos_lib import cramers_v, hapax_rate, load_sequences, null_n80_end, pos_stats, zipf_slope


def main() -> int:
    corpus, claim = Path(sys.argv[1]), Path(sys.argv[2])
    seqs = load_sequences(str(corpus))
    st = pos_stats(seqs)
    nulls = sorted(null_n80_end(seqs))
    top10 = [s for s, _ in Counter(t for s in seqs for t in s).most_common(10)]
    v = cramers_v(seqs, top10)
    hap, V = hapax_rate(seqs)
    st |= {
        "rigidity_mean_V": sum(v.values()) / len(v),
        "rigidity_V": v,
        "hapax_rate": hap,
        "zipf_slope": zipf_slope(seqs),
        "site_note": "cross-site V in a follow-up (needs site column join)",
    }
    (claim / "object" / "results.json").write_text(json.dumps(st, indent=2))
    (claim / "baseline_snapshot" / "nulls.json").write_text(
        json.dumps({"method": "permute tokens across fixed lengths", "B": len(nulls),
                    "seed": 260417829, "n80_end_sorted": nulls}, indent=2)
    )
    print(f"n80 all/begin/end = {st['n80_all']}/{st['n80_begin']}/{st['n80_end']}")
    print(f"null n80_end min={nulls[0]} max={nulls[-1]}")
    print(f"V={st['rigidity_mean_V']:.4f} hapax={hap:.4f} zipf={st['zipf_slope']:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
