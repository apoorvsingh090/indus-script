#!/usr/bin/env python3
"""Checker for L2-0003 — readable in one sitting.

Runs the FROZEN L2-0001 checker against splits v2 (same gate, rotated site).
Usage: python check.py --splits <v2 dir> --object <results.json> --baseline <unigram.json>
"""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    frozen = (Path(__file__).resolve().parent.parent
              / "L2-0001-bigram-beats-unigram" / "check.py")
    sys.exit(subprocess.run([sys.executable, str(frozen)] + sys.argv[1:]).returncode)
