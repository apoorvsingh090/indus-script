# Changelog

All notable changes to this repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
There are no versioned releases yet; everything lives under `[Unreleased]`
until the first tag is cut.

## [Unreleased]

### Added

- GitHub Actions `ci` workflow: Python syntax check across all checkers plus
  repo-wide `claim.yaml` validation on every push/PR
  (`verify-claim` remains the path-filtered claim gate)
- `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1) and `SECURITY.md`
- Bug-report issue template and issue-template chooser (`config.yml` with
  Discussions links)
- `CHANGELOG.md`
- Labels `claim` and `skeptic-review` (referenced by the claim/skeptic
  templates but previously missing)
- README badges (CI, license)

### Fixed

- README had two `## Contributing` sections; merged into one that links
  `CONTRIBUTING.md`

### Verified results (see `TROPHY_CASE.md` for full table)

- 2026-10-14: L1-0001, L1-0002 (negative), L1-0002b, L1-0003, L1-0004
  skeptic-confirmed (2/2 each)
- 2026-10-15: L0-0001, L0-0002, L2-0001, L4-0001, L2-0003, L4-0002
  (partial negative) skeptic-confirmed (2/2 each)
- 2026-10-15: splits v2 frozen (test = Mohenjo-daro); audit scorecard
  extended to L0/L2/L4 (all checkers recomputed green)

### Known gaps

- No corpus files vendored yet (`data/raw/` provenance + license TODOs open)
- First tagged release not cut
