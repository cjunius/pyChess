# Agent guide

`pychess` is a UCI chess engine: Lazy SMP negamax with a tapered PeSTO
evaluation. `src/` layout, Python 3.12+.

## Commands

```bash
pip install -e ".[dev]"   # required - tests import the installed package

ruff check .              # lint  (also: ruff check --fix .)
ruff format .             # format
mypy                      # strict on src/, relaxed for tests/
pytest                    # tests + coverage; gate is 85%
```

All tool config lives in `pyproject.toml`. CI (`.github/workflows/ci.yml`) runs
exactly these on 3.12 and 3.13; `pre-commit` mirrors lint/format/type locally.

Skills in `.claude/skills/`: `/pr-check`, `/update-docs`, `/bench`, `/release`.

## Architecture

- `negamax.py` - `Negamax`: fail-soft alpha-beta + quiescence. Takes an
  evaluator, move orderer, TT, and clock as constructor args (composition, not
  inheritance). Raises `SearchAbortError` when the clock says stop.
- `lazy_smp.py` - `search()` spawns one iterative-deepening `Negamax` per core
  against a shared-memory TT (`SharedTT`) and returns a `SearchResult`.
  `_worker` runs in a spawned subprocess.
- `transposition.py` / `shared_tt.py` - same `key`/`probe`/`store` interface;
  in-process dict vs lock-free shared memory.
- `evaluation.py` + `eval_board.py` - PeSTO tables and an incremental
  accumulator on `EvalBoard`.
- `__main__.py` - the UCI protocol loop and the ONLY place that prints
  `info` / `bestmove`. The engine layer returns data, never prints.
- `clock.py`, `move_ordering.py`, `constants.py`, `types.py` - supporting bits.

See `docs/design.md` for the full picture, `docs/tasks.md` for the roadmap.

## Conventions & gotchas

- **Don't hand-format.** `ruff format` owns layout. The piece-square-table
  literals in `evaluation.py` are fenced with `# fmt: off` - leave them.
- `mypy` is `strict` for `src/`; annotate new public functions fully.
- One `tests/test_<module>.py` per source module. New behaviour needs a test.
- `pytest` runs with `filterwarnings = ["error"]` - a new warning fails CI.
- The GitHub repo is `pyChess`, the package is `pychess`. On a case-insensitive
  filesystem these collide; rename dirs via a temp name.
- `opening_book/bookfish.bin` is an 18 MB vendored binary - don't move or
  regenerate it casually (see `opening_book/README.md`).
- Update `CHANGELOG.md` (`## [Unreleased]`) and `docs/` when behaviour changes.

`AGENTS.md` is a symlink to this file.
