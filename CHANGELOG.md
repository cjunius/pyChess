# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Lazy SMP parallel search: one iterative-deepening worker per core sharing a
  lock-free shared-memory transposition table.
- Tapered PeSTO evaluation with an incremental accumulator on `EvalBoard`.
- Check-aware, depth-bounded, fail-soft quiescence search.
- Zobrist-keyed transposition table with EXACT / LOWER / UPPER bounds.
- Move ordering: TT move, MVV-LVA captures, promotions, killers, history.
- UCI time management (`movetime`, clock + increment, `infinite`).
- Polyglot opening book support, overridable via `PYCHESS_BOOK`.
- Packaging: `src/pychess/` layout, `pyproject.toml`, `pychess` console script,
  `py.typed`.
- Tooling: Ruff (lint + format), Mypy, pytest-cov (85% gate), `pre-commit`, all
  run in CI on Python 3.12 and 3.13.
- `perft` regression tests against published node counts; unit tests for every
  module.

### Changed

- Search rebuilt as composed collaborators (`Negamax` is handed an evaluator,
  move orderer, TT, and clock) instead of a cooperative-multiple-inheritance
  mixin stack.
- Engine layer no longer prints UCI protocol - `lazy_smp.search` returns a
  `SearchResult` and `__main__` does all formatting.
- License changed to Apache-2.0.

### Removed

- The single-process search path; `go` always runs Lazy SMP.
- Legacy `archive/` tree and unused evaluation mixins.
