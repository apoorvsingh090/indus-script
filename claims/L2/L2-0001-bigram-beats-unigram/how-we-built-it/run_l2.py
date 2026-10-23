#!/usr/bin/env python3
"""Generator for L2-0001. Run AFTER the preregistration commit.
Fits on TRAIN only, selects bigram alpha on VAL, evaluates once on TEST.
Writes object/results.json + baseline_snapshot/unigram.json.
Usage: python run_l2.py <splits_dir> <claim_dir>
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "benchmarks" / "baselines"))
from models import ALPHAS, Bigram, Positional, Unigram, accuracy, mean_logloss, paired_bootstrap_ci


def main() -> int:
    splits, claim = Path(sys.argv[1]), Path(sys.argv[2])
    from models import load_split
    train, val, test = (load_split(splits / f"{n}.jsonl") for n in ("train", "val", "test"))

    uni = Unigram()
    uni.fit(train)
    pos = Positional()
    pos.fit(train)
    scored = []
    for a in ALPHAS:
        bg = Bigram(alpha=a)
        bg.fit(train)
        acc, _ = accuracy(bg, val)
        scored.append((acc, a))
    best = min([s for s in scored if s[0] == max(x[0] for x in scored)], key=lambda s: s[1])
    bg = Bigram(alpha=best[1])
    bg.fit(train)

    out, weights = {}, []
    for name, model in (("unigram", uni), (f"bigram_a{best[1]}", bg), ("positional", pos)):
        acc, per_text = accuracy(model, test)
        out[name] = {"acc": acc, "logloss_bits": mean_logloss(model, test),
                     "n_predictions": sum(len(r["signs"]) for r in test)}
        if name == "unigram":
            pu = per_text
        if name.startswith("bigram"):
            pb = per_text
    weights = [len(r["signs"]) for r in test]
    lo, hi, diff = paired_bootstrap_ci(pb, pu, weights)
    out["comparison"] = {"diff_bigram_minus_unigram": diff, "ci95": [lo, hi],
                         "alpha_grid": list(ALPHAS), "alpha_selected": best[1],
                         "val_accs": {str(a): acc for acc, a in scored}}
    (claim / "object" / "results.json").write_text(json.dumps(out, indent=2))
    (claim / "baseline_snapshot" / "unigram.json").write_text(json.dumps(
        {"model": "unigram", "test_acc": out["unigram"]["acc"],
         "test_logloss_bits": out["unigram"]["logloss_bits"]}, indent=2))
    print(f"unigram={out['unigram']['acc']:.4f} bigram={out[f'bigram_a{best[1]}']['acc']:.4f} "
          f"pos={out['positional']['acc']:.4f} diff={diff:.4f} CI=[{lo:.4f},{hi:.4f}] alpha={best[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
