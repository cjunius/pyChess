# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-30

Initial release.

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
  run in CI, with Codecov coverage + test-analytics uploads.
- `perft` regression tests against published node counts; unit tests for every
  module.

### Changed

- Require Python 3.14 (`requires-python = ">=3.14"`); CI runs on 3.14 only.
- Search rebuilt as composed collaborators (`Negamax` is handed an evaluator,
  move orderer, TT, and clock) instead of a cooperative-multiple-inheritance
  mixin stack.
- Engine layer no longer prints UCI protocol - `lazy_smp.search` returns a
  `SearchResult` and `__main__` does all formatting.
- License changed to Apache-2.0.

### Fixed

- `go nodes N` now enforces the node limit in Lazy SMP workers; previously the
  limit was parsed but never passed to `Clock`.

### Removed

- The single-process search path; `go` always runs Lazy SMP.
- Legacy `archive/` tree and unused evaluation mixins.

[Unreleased]: https://github.com/cjunius/pyChess/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/cjunius/pyChess/releases/tag/v0.1.0
