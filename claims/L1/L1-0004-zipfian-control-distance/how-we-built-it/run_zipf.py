#!/usr/bin/env python3
"""Generator for L1-0004. Run AFTER the preregistration commit.
Usage: python run_zipf.py <corpus.csv> <claim_dir>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from zipf_lib import load_oriented, mm_point, synth_zipf, zipf_s_ols


def main() -> int:
    corpus, claim = Path(sys.argv[1]), Path(sys.argv[2])
    seqs, vocab = load_oriented(str(corpus))
    h1r, cr = mm_point(seqs, vocab)
    s = zipf_s_ols(seqs)
    syn = synth_zipf([len(x) for x in seqs], vocab, s)
    h1z, cz = mm_point(syn, vocab)
    d = max(abs(h1z - h1r), abs(cz - cr))
    (claim / "object" / "results.json").write_text(json.dumps({
        "zipf_s_ols": s, "synth": {"H1n": h1z, "C": cz},
        "d": d, "verdict": "distinguishable-supports-Rao-reply" if d >= 0.05 else "indistinguishable-supports-Sproat"}, indent=2))
    (claim / "baseline_snapshot" / "real_point.json").write_text(json.dumps({
        "real": {"H1n": h1r, "C": cr}, "n_texts": len(seqs), "vocab": vocab}, indent=2))
    print(f"s={s:.4f} real=({h1r:.4f},{cr:.4f}) synth=({h1z:.4f},{cz:.4f}) d={d:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
