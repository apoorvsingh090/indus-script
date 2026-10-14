#!/usr/bin/env python3
"""Fetch the pinned public corpus (NOT vendored — license hygiene, planner §4).

Downloads indus_website_real_corpus.csv from joyboseroy/indus_decipher at the
pinned HF revision and verifies SHA256. Underlying transcription: yajnadevam
terms (GPL-3.0-family); conversion work MIT. Provenance only — verify before reuse.
Usage: python fetch_corpus.py [out_dir]
"""
import hashlib
import sys
from pathlib import Path

REPO = "joyboseroy/indus_decipher"
REVISION = "47e8616dff4d1ff62343bd74f3eeefc4afbfd4d8"
FILE = "indus_website_real_corpus.csv"
SHA256 = "7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8"


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else ".") / FILE
    from huggingface_hub import hf_hub_download

    p = hf_hub_download(REPO, FILE, repo_type="dataset", revision=REVISION, local_dir=str(out.parent))
    h = hashlib.sha256(Path(p).read_bytes()).hexdigest()
    if h != SHA256:
        print(f"FAIL: sha mismatch {h} != {SHA256}")
        return 1
    print(f"OK: {p} sha={h[:16]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
