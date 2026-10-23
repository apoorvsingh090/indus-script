#!/usr/bin/env python3
"""Generator for L1-0003. Run AFTER the preregistration commit.
Usage: python run_ng.py <corpus.csv> <claim_dir>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ng_lib import load_oriented, null_rep, repeated_counts, successor_coverage


def main() -> int:
    corpus, claim = Path(sys.argv[1]), Path(sys.argv[2])
    seqs = load_oriented(str(corpus))
    rep3, phrases3 = repeated_counts(seqs, 3)
    rep4, phrases4 = repeated_counts(seqs, 4)
    n3 = sorted(null_rep(seqs, 3))
    n4 = sorted(null_rep(seqs, 4))
    cov, cov_by = successor_coverage(seqs)
    top3 = sorted(phrases3, key=lambda p: len(phrases3[p]), reverse=True)[:10]
    (claim / "object" / "results.json").write_text(json.dumps({
        "n_texts": len(seqs), "rep3": rep3, "rep4": rep4,
        "top_rep3": [" ".join(p) + f" x{len(phrases3[p])}" for p in top3],
        "successor_cov_top10": cov}, indent=2))
    (claim / "baseline_snapshot" / "nulls.json").write_text(json.dumps({
        "method": "permute tokens across fixed lengths (corrected order)",
        "B": len(n3), "seed": 260417830,
        "rep3_sorted": n3, "rep4_sorted": n4}, indent=2))
    print(f"texts={len(seqs)} rep3={rep3} (null max {n3[-1]}) rep4={rep4} (null max {n4[-1]}) succ_cov={cov:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
