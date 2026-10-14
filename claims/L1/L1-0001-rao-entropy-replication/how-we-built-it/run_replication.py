#!/usr/bin/env python3
"""Generator for L1-0001: Rao-2009-style entropy replication.

Writes object/results.json (real corpus stats) and baseline_snapshot/nulls.json
(shuffled null distribution + uniform control). Run AFTER the preregistration
commit; threshold was fixed before this ever executed.
Usage: python run_replication.py <corpus.csv> <claim_dir>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from entropy_lib import corpus_stats, load_sequences, shuffled_C, uniform_C


def main() -> int:
    corpus, claim = Path(sys.argv[1]), Path(sys.argv[2])
    seqs, vocab = load_sequences(str(corpus))
    real = corpus_stats(seqs, vocab)
    nulls = shuffled_C(seqs, vocab)
    nulls_sorted = sorted(nulls)
    uni = uniform_C(seqs, vocab)
    (claim / "object" / "results.json").write_text(json.dumps({"real": real}, indent=2))
    (claim / "baseline_snapshot" / "nulls.json").write_text(
        json.dumps(
            {
                "method": "permute tokens across fixed lengths",
                "B": len(nulls_sorted),
                "seed": 260417828,
                "C_sorted": nulls_sorted,
                "C_uniform": uni,
            },
            indent=2,
        )
    )
    print(f"texts={real['n_texts']} tokens={real['n_tokens']} vocab={real['vocab']}")
    print(f"C_real={real['C_cond_norm']:.4f} null_p0.5={nulls_sorted[0]:.4f} C_uniform={uni:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
