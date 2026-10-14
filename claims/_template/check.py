#!/usr/bin/env python3
"""Claim checker template — readable in one sitting.

Contract: exit 0 + print PASS on success; exit non-zero + print FAIL + reason.
Must rebuild the headline number from raw inputs (corpus snapshot + object +
baseline), not just re-print a cached value. Keep under ~150 lines.
Usage: python check.py --corpus <path> --object <path> --baseline <path>
"""
import argparse
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--object", required=True)
    ap.add_argument("--baseline", required=True)
    args = ap.parse_args()

    # TODO: load corpus snapshot, verify sha256 matches claim.yaml,
    # recompute metric, compare vs preregistered threshold + baseline.
    print(f"FAIL: checker not implemented (corpus={args.corpus})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
