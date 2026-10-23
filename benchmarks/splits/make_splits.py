#!/usr/bin/env python3
"""Frozen site-disjoint splits v1 for L2 next-sign prediction.

Design (fixed before any accuracy was computed):
- CORRECTED reading order (reverse L-R rows), per dataset-card loader convention.
- TEST  = all Harappa texts (major site, unseen in training).
- VAL   = Lothal + Dholavira + Kalibangan (mid-size sites, for smoothing choice).
- TRAIN = Mohenjo-daro + every other site.
- LEAKAGE RULE: drop test/val texts whose exact sequence occurs in TRAIN
  (65/1948 distinct seqs are multi-site; report excluded counts).
- WITHIN-split duplicates kept (train frequencies stay natural).
- object_type is uniformly "unknown" in this corpus, so the split is by site
  (documented deviation from "site and object" — object split vacuous here).

Writes train.jsonl / val.jsonl / test.jsonl (one record per line:
{"id","site","signs"}) + split.json (design + counts + sha) — then the caller
runs sha256sum into SHA256SUMS. Re-run is deterministic.
Usage: python make_splits.py <corpus.csv> <out_dir> [--test A,B] [--val C,D]
Defaults reproduce splits v1 (test Harappa; val Lothal,Dholavira,Kalibangan).
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

TEST_SITES = {"Harappa"}
VAL_SITES = {"Lothal", "Dholavira", "Kalibangan"}


def main() -> int:
    corpus, out = Path(sys.argv[1]), Path(sys.argv[2])
    test_sites, val_sites = set(TEST_SITES), set(VAL_SITES)
    args = sys.argv[3:]
    if "--test" in args:
        test_sites = set(args[args.index("--test") + 1].split(","))
    if "--val" in args:
        val_sites = set(args[args.index("--val") + 1].split(","))
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    with open(corpus, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s = (r.get("sign_sequence") or "").strip()
            if not s:
                continue
            toks = s.split()
            if (r.get("reading_direction") or "").strip() == "L-R":
                toks = list(reversed(toks))
            rows.append({"id": r.get("inscription_id") or "?", "site": r.get("site") or "unknown",
                         "signs": toks})
    buckets = {"train": [], "val": [], "test": []}
    for r in rows:
        buckets["test" if r["site"] in test_sites
                else "val" if r["site"] in val_sites else "train"].append(r)
    train_seqs = {" ".join(r["signs"]) for r in buckets["train"]}
    excluded = {}
    for name in ("val", "test"):
        keep, drop = [], 0
        for r in buckets[name]:
            if " ".join(r["signs"]) in train_seqs:
                drop += 1
            else:
                keep.append(r)
        excluded[name] = drop
        buckets[name] = keep
    info = {"design": "site-disjoint", "test_sites": sorted(test_sites),
            "val_sites": sorted(val_sites),
            "train": "all other sites",
            "order": "corrected (L-R reversed)", "leakage_rule": "drop test/val seqs seen in train",
            "excluded": excluded,
            "counts": {k: {"texts": len(v), "tokens": sum(len(r["signs"]) for r in v)}
                       for k, v in buckets.items()}}
    for name, recs in buckets.items():
        with open(out / f"{name}.jsonl", "w", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (out / "split.json").write_text(json.dumps(info, indent=2))
    blob = "".join(sorted(json.dumps(r, sort_keys=True) for v in buckets.values() for r in v))
    print(json.dumps(info, indent=2))
    print("splits-sha256:", hashlib.sha256(blob.encode()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
