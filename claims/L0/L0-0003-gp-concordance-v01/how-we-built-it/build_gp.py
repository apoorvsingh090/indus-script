#!/usr/bin/env python3
"""Builder for L0-0003 — G<->P type-level concordance v0.1 (preregistered).

Run AFTER the preregistration commit. Deterministic, stdlib only.

Frozen method (see ../claim.yaml:preregistered_threshold):
- Inputs: mayig corpus @ad2f1e2 (179 side-sequences, P-codes, M-number ids)
  and indus_website_real_corpus.csv @47e8616d (G-codes, cisi_number, site).
- Join on M-number (G rows: site == Mohenjo-daro and cisi_number matches
  ^M-?\\d+[A-Z]?$; mayig ids ^M-?(\\d+)([A-Z]?)).
- G orientation: reverse tokens where reading_direction == 'L-R' (the
  corrected order used repo-wide since L1-0002b). P orientation: BOTH
  global variants scored; selection rule = higher sum of top-pair counts
  over G-signs with n_g >= 5; both totals reported.
- Alignment: every (G-row, P-side) pair with equal token length under the
  selected orientation; position-level co-occurrence C[g][p]; per-text
  support.
- Classification per G-sign g (n_g = aligned occurrences):
    clean     n_g>=5 AND support(g,p1)>=5 AND C[g][p1]>=0.9*n_g AND
              g is p1's top source AND C[g][p1]>=0.9*occurrences(p1)
    contested not clean AND n_g>=5 (reason: near-tie if C[g][p2]>=0.8*C[g][p1],
              reverse-conflict if some other g' tops p1, else low-consistency)
    unmapped  n_g<5
- Gate: >=20 clean bijective pairs; clean+contested+unmapped reconciles to
  the number of distinct G-signs observed at aligned positions; every sign
  ships with class+evidence; join counts reproduce 161 shared / 140
  same-length candidates.
- Report-only: holdout (every 5th sorted shared M-number) — infer mapping
  from the rest, measure positional accuracy at clean-mapped positions.

Outputs: claim object/results.json + baseline_snapshot/counts.json and
data/concordance/gp-v01.csv (g,p,clean_evidence_texts,c_g,n_g,n_p,class,reason).
Usage: python build_gp.py <mayig_repo_dir> <corpus.csv> <claim_dir> <repo_root>
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

CLEAN_MIN_OCC = 5
CLEAN_MIN_SUPPORT = 5
CLEAN_CONSISTENCY = 0.9
NEAR_TIE_RATIO = 0.8


def load_mayig(repo):
    sides = defaultdict(list)
    for sub in sorted(p for p in (repo / "corpus").iterdir() if p.is_dir()):
        for f in sorted(sub.glob("*.json")):
            for side in json.loads(f.read_text(encoding="utf-8")):
                m = re.match(r"^M-?(\d+)", side["id"])
                if m:
                    sides[int(m.group(1))].append(
                        {"id": side["id"], "seq": [g["id"] for g in side["graphemes"]]})
    return sides


def load_g(corpus_csv):
    rows = []
    for r in csv.DictReader(open(corpus_csv, encoding="utf-8")):
        if r["site"] != "Mohenjo-daro":
            continue
        m = re.match(r"^M-?(\d+)[A-Z]?$", r["cisi_number"] or "")
        if not m:
            continue
        toks = (r["sign_sequence"] or "").split()
        if (r.get("reading_direction") or "").strip() == "L-R":
            toks = list(reversed(toks))
        rows.append({"m": int(m.group(1)), "seq": toks})
    return rows


def evidence(gsides, psides, p_reverse):
    """Position-level C[g][p], per-(g,p) text support, aligned totals."""
    C = defaultdict(Counter)
    support = defaultdict(set)
    ng = Counter()
    np_ = Counter()
    pairs = 0
    for m, gs in gsides.items():
        ps = psides.get(m, [])
        for g in gs:
            for p in ps:
                pseq = list(reversed(p["seq"])) if p_reverse else p["seq"]
                if len(g["seq"]) != len(pseq):
                    continue
                pairs += 1
                for a, b in zip(g["seq"], pseq):
                    C[a][b] += 1
                    support[(a, b)].add(m)
                    ng[a] += 1
                    np_[b] += 1
    return C, support, ng, np_, pairs


def classify(C, support, ng, np_):
    top_of_g = {g: sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
                for g, c in C.items() if c}
    counts_of_g = {g: dict(c) for g, c in C.items()}
    out = {}
    for g in sorted(ng):
        n_g = ng[g]
        if n_g < CLEAN_MIN_OCC:
            out[g] = ("unmapped", "", 0, 0, 0)
            continue
        ranked = sorted(counts_of_g.get(g, {}).items(), key=lambda kv: (-kv[1], kv[0]))
        p1, c1 = ranked[0]
        p2, c2 = (ranked[1] if len(ranked) > 1 else ("", 0))
        sup1 = len(support.get((g, p1), ()))
        top_src_of_p1 = sorted(((C[gg].get(p1, 0), gg) for gg in C if C[gg].get(p1)), reverse=True)
        top_src = top_src_of_p1[0][1] if top_src_of_p1 else None
        if (sup1 >= CLEAN_MIN_SUPPORT and c1 >= CLEAN_CONSISTENCY * n_g
                and top_src == g and c1 >= CLEAN_CONSISTENCY * np_[p1]):
            out[g] = ("clean", p1, c1, n_g, sup1)
        elif c2 >= NEAR_TIE_RATIO * c1:
            out[g] = ("contested", p1, c1, n_g, sup1, "near-tie:" + p2)
        elif top_src != g:
            out[g] = ("contested", p1, c1, n_g, sup1, "reverse-conflict:" + str(top_src))
        else:
            out[g] = ("contested", p1, c1, n_g, sup1, "low-consistency")
    return out


def main() -> int:
    mayig_dir, corpus_csv, claim_dir, repo_root = (Path(a) for a in sys.argv[1:5])
    psides = load_mayig(mayig_dir)
    grows = load_g(corpus_csv)
    gsides = defaultdict(list)
    for r in grows:
        gsides[r["m"]].append(r)
    shared = sorted(set(gsides) & set(psides))

    # orientation selection rule: higher sum of per-sign top-pair counts
    variants = {}
    for p_reverse in (False, True):
        C, support, ng, np_, pairs = evidence(gsides, psides, p_reverse)
        top_sum = sum(max(c.values()) for c in C.values() if c)
        variants[p_reverse] = (C, support, ng, np_, pairs, top_sum)
    p_reverse = max(variants, key=lambda k: (variants[k][5], k))
    C, support, ng, np_, pairs, top_sum = variants[p_reverse]

    cls = classify(C, support, ng, np_)
    clean = {g: v[1] for g, v in cls.items() if v[0] == "clean"}
    bijection_violations = [p for p, n in Counter(clean.values()).items() if n > 1]

    # holdout: every 5th shared M-number; infer on the rest, score clean-mapped
    hold = set(shared[::5])
    C2, sup2, ng2, np2, _ = evidence({m: v for m, v in gsides.items() if m not in hold},
                                     {m: v for m, v in psides.items() if m not in hold}, p_reverse)
    cls2 = classify(C2, sup2, ng2, np2)
    clean2 = {g: v[1] for g, v in cls2.items() if v[0] == "clean"}
    hit = tot = 0
    for m in sorted(hold):
        for g in gsides[m]:
            for p in psides.get(m, []):
                pseq = list(reversed(p["seq"])) if p_reverse else p["seq"]
                if len(g["seq"]) != len(pseq):
                    continue
                for a, b in zip(g["seq"], pseq):
                    if a in clean2:
                        tot += 1
                        hit += (clean2[a] == b)
    holdout_acc = hit / tot if tot else None

    n_clean = len(clean)
    n_contested = sum(1 for v in cls.values() if v[0] == "contested")
    n_unmapped = sum(1 for v in cls.values() if v[0] == "unmapped")
    gate_pass = (n_clean >= 20 and not bijection_violations
                 and n_clean + n_contested + n_unmapped == len(ng)
                 and len(shared) == 161 and pairs >= 1)

    out = {
        "join": {"shared_m_numbers": len(shared), "mayig_sides": sum(len(v) for v in psides.values()),
                 "g_mdaro_rows_with_mnum": len(grows)},
        "orientation": {"selected_p_reversed": p_reverse,
                        "top_sum_as_stored": variants[False][5], "top_sum_reversed": variants[True][5]},
        "alignment": {"equal_length_pairs": pairs, "aligned_positions": sum(ng.values()),
                      "g_signs_observed": len(ng), "p_signs_observed": len(np_)},
        "classes": {"clean": n_clean, "contested": n_contested, "unmapped": n_unmapped,
                    "bijection_violations": bijection_violations},
        "holdout_report_only": {"texts": len(hold), "positions_scored": tot,
                                "accuracy_at_clean_mapped": holdout_acc},
        "gate": {"bar": ">=20 clean bijective; classes reconcile to g_signs_observed; shared==161",
                 "pass": bool(gate_pass)},
    }
    obj = Path(claim_dir) / "object"
    base = Path(claim_dir) / "baseline_snapshot"
    obj.mkdir(exist_ok=True)
    base.mkdir(exist_ok=True)
    (obj / "results.json").write_text(json.dumps(out, indent=2))
    (base / "counts.json").write_text(json.dumps(
        {"shared_m_numbers": len(shared), "g_signs_observed": len(ng),
         "clean": n_clean, "contested": n_contested, "unmapped": n_unmapped}, indent=2))

    # concordance CSV (repo-wide artifact, pwm-v01 format + evidence)
    conc = repo_root / "data" / "concordance" / "gp-v01.csv"
    with conc.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["g", "p", "class", "c_g_p", "n_g", "support_texts", "reason"])
        for g in sorted(cls):
            v = cls[g]
            w.writerow([g, v[1] if v[0] != "unmapped" else "", v[0],
                        v[2], v[3], v[4], v[5] if len(v) > 5 else ""])
    print(f"shared={len(shared)} pairs={pairs} p_reverse={p_reverse} "
          f"clean={n_clean} contested={n_contested} unmapped={n_unmapped} "
          f"bij_viol={len(bijection_violations)} holdout_acc={holdout_acc} "
          f"gate={'PASS' if gate_pass else 'FAIL'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
