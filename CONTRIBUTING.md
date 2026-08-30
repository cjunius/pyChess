# Contributing

## Setup

```bash
python3.14 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Before opening a PR

The CI gate is:

```bash
ruff check .
ruff format --check .
mypy
pytest                 # coverage must stay >= 85%
```

`pre-commit` runs the first three on every commit. All tool configuration lives
in `pyproject.toml`.

## Claude Code skills

Repo workflows are packaged as skills in `.claude/skills/`:

| Skill | Does |
|---|---|
| `/pr-check` | runs the gate above + checks tests / changelog / docs against the diff |
| `/update-docs` | reviews the diff and updates `README.md` + `docs/*.md` |
| `/bench` | runs the search benchmarks and refreshes `docs/performance.md` |
| `/release` | bumps the version, rolls `CHANGELOG.md`, runs the gate, commits, tags |

## Conventions

- Python is formatted by `ruff format` (line length 100). Don't hand-format;
  data tables that must keep a fixed layout are fenced with `# fmt: off`.
- `mypy` runs in `strict` mode on `src/`. Tests are checked too but don't
  require annotations on the test functions themselves.
- One `tests/test_<module>.py` per source module. New behaviour needs a test.
- Keep `docs/` in sync when behaviour changes, and add a `CHANGELOG.md` entry
  under `## [Unreleased]` (see `/update-docs`).

## Commit / PR

- Branch off `main`; keep PRs focused.
- Reference an issue where one exists.
- Formatting-only changes go in their own commit, separate from logic changes.
