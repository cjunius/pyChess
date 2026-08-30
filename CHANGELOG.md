# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Null-move pruning in `Negamax.search`: when a null move fails high at reduced
  depth (`R = 2..3`) the node returns a `beta` cut-off without searching the
  real moves. Skipped at the root, while in check, in likely zugzwang (side to
  move has only king and pawns), below depth 3, and when it was already tried
  on the path; a verification search guards the cut-off at depth >= 10.
- Late move reductions in `Negamax.search`: past the first three moves at a
  node (depth >= 3), quiet non-checking non-TT moves are first searched
  `1..3` plies shallower - the reduction grows with move index and depth and
  shrinks by one for killers / positive-history moves. A reduced search that
  beats `alpha` is repeated at full depth. New `MoveOrderer.is_killer` /
  `MoveOrderer.history_score` accessors support the reduction decision.
- Principal variation search in `Negamax.search`: only the first (best-ordered)
  move gets the full `(alpha, beta)` window; every later move is scouted with a
  null window and re-searched at full depth and width only when the scout beats
  `alpha` without an already-certain cut-off. The LMR scout now shares that
  null window.
- In-tree draw detection: threefold repetition and the fifty-move rule are now
  scored as draws inside the search (`negamax.claims_draw`), not just the
  automatic five-fold / seventy-five-move draws. Every draw scores a flat `0`
  (previously the game-over branch could return `0 - depth`); a `CONTEMPT`
  constant is the hook for a non-zero draw score.
- Mate-distance pruning in `Negamax.search`: the window is clamped to the
  best/worst mate still reachable from the node, so the search never chases a
  slower mate than one already found.
- Positional evaluation terms (`eval_terms`) layered on the PeSTO tables:
  passed / isolated / doubled pawns, bishop pair, rooks on open / half-open
  files, knight outposts, a pawn-shield king-safety penalty, and a tempo bonus.
  The pure-pawn terms are memoised on the pawn bitboards by `PestoEvaluator`.

### Changed

- Mate scores are now distance-to-mate from the search root (`MATE - ply`)
  instead of `-MATE - remaining_depth`. The transposition table rebases them on
  store/probe (`constants.tt_store_score` / `tt_probe_score`) so mate bounds
  propagate through it; `MATE_GUARD` is gone. `TranspositionTable` /
  `SharedTT` `probe` / `store` take a `ply` argument.
- UCI `info` lines report `score mate N` (signed, in moves) for mate scores
  instead of a large `score cp`.

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
