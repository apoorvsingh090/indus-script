# Indus Script Project: Planner

*Last updated: 2026-10-14. Modeled on the discipline of elder-plinius/V3R1T4S and the "Daily Oracle" thread, not on its targets.*

## 1. Goal and non-goals

**Goal.** Build a verification-first repo of falsifiable claims about the Indus script, worked by autonomous agents, where nothing counts until independent skeptics reproduce it.

**Non-goals.**
- Declaring the script "deciphered". There is no oracle (no bilingual text, unknown language, very short inscriptions), so a fluent reading proves nothing.
- Treating LLM-produced readings as evidence. They are hypotheses to be scored, never results.

## 2. Principles (carried over from V3R1T4S)

1. Every claim ships four things: the object itself, a checker readable in one sitting, a snapshot of the baseline or table it beats, and the code that generated it.
2. Skeptic agents start from a fresh context, write their own code, and rebuild the result from scratch. If they cannot reproduce it, confirm it is new, or accept the definition of "solved", it does not count.
3. Pre-register: hash predictions before the test data or new finds are visible (sealed envelopes).
4. Negative and partial results are first-class and get published.
5. Data access follows the rules. Anything that depended on bypassing a site's controls is retracted.

## 3. Claim ladder

| Level | Claim type | Checker | Pass condition |
|---|---|---|---|
| L0 | Corpus and sign list | Reproducible parse, dedup report, sign-code concordance | Counts reconcile with source; contested splits listed |
| L1 | Structural (direction, positional regularities, entropy-style stats) | Script plus null models (shuffled, non-linguistic systems, known scripts) | Beats nulls at a threshold fixed *before* running |
| L2 | Prediction (masked-sign / next-sign on held-out inscriptions) | Fixed split, scoring script | Beats the structural baseline on held-out data |
| L3 | Reading claims (machine-readable sign to value mapping) | Scored by compression/MDL, cross-site consistency, predictive gain, with a free-parameter penalty | Beats L2 baseline; survives skeptics |
| L4 | Calibration | Same method run on scripts with hidden keys and on synthetic Indus-sized corpora | Method recovers known answers at this data size |
| L5 | Future-facing predictions | Sealed hash of predictions about unpublished inscriptions or finds | Confirmed after the data is released |

Rule: no L3 claim is accepted from a method that has not passed L4.

## 4. Data plan

| Source | What | Status | Action |
|---|---|---|---|
| ICIT (Wells / Fuls, TU Berlin) | Most complete corpus with site and object metadata | Access by emailing the administrator | Request access; ask about license and redistribution |
| Fuls, *Corpus of Indus Inscriptions* (2022) and sign catalogue | Printed corpus and sign list | On Academia (may need login) | Use for cross-checking the parse |
| Mahadevan 1977 and Parpola CISI | Classic corpora; different sign numbering (M-codes, P-codes) | Papers on RMRL; photo scans partly available | Build a concordance table |
| Adhikari GitHub (`ronojoy/indus`) | Replication code and papers | Public | Use as replication targets |
| Hugging Face `hellosindh/indus-script-models` | Tokenizer and models on 3,310 inscriptions, CC-BY-4.0 | Public | Prototype only; contains model-generated sequences |
| Comparison corpora (Linear B, Ugaritic, proto-Elamite via CDLI) | Calibration and null models | Not yet checked | Verify availability and licenses |

**Hygiene rules**
- Record provenance and license per file. Verify license terms before reuse (not yet verified for any source).
- Dedup exact duplicates and report the count (about 24% in one raw corpus).
- Pin one sign-coding scheme per experiment; never compare counts across schemes without a concordance.
- Never mix synthetic or model-generated sequences into training or evaluation as if real.
- Strip "translations" from third-party repos; they are outputs of unverified methods, not labels.
- Expect only a few thousand short texts (about 11k sign tokens in one deduplicated set). Every benchmark needs a power or null-distribution check.

## 5. Phases and milestones

**Phase 0: Decisions and access**
- [ ] Decide public repo vs private workflow (see section 10)
- [ ] Email ICIT administrator for access; ask about license
- [ ] Pick a repo name, license for code and for data
- [ ] Line up at least one epigrapher or linguist as an external reviewer

**Phase 1: Corpus layer (L0)**
- [ ] Define the inscription schema (id, signs, site, object type, side, completeness, source refs)
- [ ] Parser, dedup, and completeness filters, each with a checker
- [ ] Sign-code concordance (Mahadevan / Parpola / ICIT)
- [ ] Frozen corpus snapshot with SHA256SUMS

**Phase 2: Baselines and replication (L1)**
- [ ] Replicate Rao et al. (2009) conditional entropy and the published rebuttals
- [ ] Replicate positional and n-gram analyses from the Adhikari repo
- [ ] Replicate the recent synthetic-baseline scorecard (arXiv 2604.17828)
- [ ] Publish a table of what replicates, what does not, and under which sign scheme

**Phase 3: Benchmark harness (L2)**
- [ ] Fixed train / validation / held-out splits (split by site and by object, not by random line, to limit leakage)
- [ ] Baselines: unigram, n-gram, positional model
- [ ] Power analysis for each metric

**Phase 4: Calibration (L4)**
- [ ] Synthetic scripts generated from known languages, matched to Indus corpus size and inscription length
- [ ] Hidden-key runs on known scripts
- [ ] Publish the minimum data size at which each method recovers the key

**Phase 5: Agent loop**
- [ ] Implement the daily run (section 7)
- [ ] Hit list of sub-problems drawn from L1 to L3
- [ ] Skeptic review gate wired to the claim schema

**Phase 6: Intake and sealed envelopes (L3, L5)**
- [ ] Reading-claim submission format and scorer
- [ ] Hash-registry for pre-registered predictions

## 6. Repo layout

```
indus-script/
  README.md
  planner.md
  READ_BEFORE_CITING.md
  data/
    raw/            # untouched, with provenance + license per file
    processed/      # frozen snapshots + SHA256SUMS
    concordance/    # sign-code mappings
  claims/
    L0/ ... L5/     # one folder per claim: object, checker, baseline, how-we-built-it
  benchmarks/
    splits/  baselines/  calibration/
  agents/
    prompts/  skeptic-protocol.md  loop-config.md
  sealed-envelopes/ # hashes only
  TROPHY_CASE.md    # verified results, including negative ones
```

## 7. Agent loop (daily-run design)

**Roles**
- *Scout*: maintains the hit list; picks a few targets per run.
- *Builder*: attempts a target and produces claim artifacts.
- *Skeptics (several)*: fresh context each, rebuild from scratch, try to break the claim.
- *Archivist*: files the claim, checker, and baseline; updates the trophy case.

**Rules**
- Hypotheses from language models (Sanskrit, Dravidian, anything) are inputs to a scorer, never outputs to a report.
- Fixed budget per run; stop conditions defined up front.
- Network access only where permitted by site rules; no evasion.
- Every run logs what was tried, including failures.
- Notify only on skeptic-confirmed results.

## 8. Skeptic protocol (checklist)

- [ ] Rebuilt from raw inputs in a clean context with independently written code
- [ ] Same sign-coding scheme and corpus snapshot hash
- [ ] Threshold and split fixed before the run (check timestamps/hashes)
- [ ] Null models and calibration results attached
- [ ] Degrees of freedom counted; multiple-comparison correction applied
- [ ] Novelty checked against prior literature
- [ ] Claim wording matches what was actually shown (no stretch of "solved")

## 9. Claim record (template)

```yaml
id: L2-0007
title: <one line>
level: L2
corpus_snapshot_sha256: <hash>
sign_scheme: ICIT   # or M77 / P82
object: path/to/object
checker: path/to/check.py   # readable in one sitting
baseline_snapshot: path/to/baseline
generator: path/to/how-we-built-it/
preregistered_threshold: <fixed before run>
result: <metric + interval>
skeptics: [id1, id2, id3]   # each reproduced independently
status: verified | failed-reproduction | withdrawn
```

## 10. Risks and open decisions

**Risks**
- *Confabulated readings* that sound convincing: mitigated by the ladder, L4 gate, and skeptics.
- *Data leakage and tiny samples*: mitigated by site-level splits and power checks.
- *Sign-scheme drift*: mitigated by pinned schemes and the concordance.
- *License or access problems*: mitigated by asking maintainers first and recording terms.
- *Domain blind spots*: mitigated by an external epigraphist reviewer.

**Open decisions**
- [ ] Public repo with community submissions, or private research workflow?
- [ ] Compute and token budget per daily run
- [ ] Which external reviewer(s) to approach
- [ ] Whether to include non-text context (seal iconography, find context) from the start or as a later phase
