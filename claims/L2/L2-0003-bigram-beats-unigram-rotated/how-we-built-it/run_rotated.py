#!/usr/bin/env python3
"""Rotated-run driver for L2-0003: the FROZEN L2-0001 pipeline on splits v2.
No new modeling code — rotation tests generality, not implementation.
Usage: python run_rotated.py (paths fixed below)
"""
import sys
from pathlib import Path

CLAIM = Path(__file__).resolve().parent.parent
L20001 = CLAIM.parent / "L2-0001-bigram-beats-unigram"
sys.path.insert(0, str(L20001 / "how-we-built-it"))
import run_l2  # noqa: E402  (frozen, committed; threshold logic unchanged)

ROOT = CLAIM.parents[2]
sys.argv = ["run_l2.py", str(ROOT / "benchmarks" / "splits" / "v2"), str(CLAIM)]
sys.exit(run_l2.main())
