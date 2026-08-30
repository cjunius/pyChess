---
name: pr-check
description: >
  Run the full CI gate locally and check the softer PR requirements (tests,
  changelog, docs) against the diff. Use before opening or updating a pull
  request, or when the user asks to "check my PR" / "am I ready to push".
---

# pr-check

Mirror what CI and review will check, and report a pass/fail list matching
`.github/PULL_REQUEST_TEMPLATE.md`. Stop at the first hard failure and show its
output.

## 1. Hard gate (same as CI, in order)

```bash
pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy
pytest
```

- `ruff check` / `ruff format --check` - style. If it fails, `ruff check --fix`
  and `ruff format` fix most of it.
- `mypy` - strict on `src/`. New public functions need full annotations.
- `pytest` - all tests pass and coverage stays >= 85% (the run fails the build
  otherwise). `pytest` also runs with `filterwarnings = ["error"]`, so a new
  warning is a failure.

## 2. Soft checks against the diff

```bash
git fetch origin main
git diff --stat origin/main...HEAD
git diff origin/main...HEAD
```

Then verify:

| Check | How |
|---|---|
| Tests for the change | `src/` behaviour changed -> a matching `tests/test_<module>.py` change is in the diff. New module -> new test file. |
| Changelog | `CHANGELOG.md` has a new bullet under `## [Unreleased]`. |
| Docs | the diff touches something `README.md` or `docs/` describes (a module, a UCI command, the layout, an architecture claim, a feature list). If so, those files are updated - run `/update-docs` if not. |
| No stray debug | no leftover `print(...)` in `src/` outside `__main__.py`, no commented-out code, no `# type: ignore` without a reason. |
| Public API typed | any new function/method in `src/` has argument and return annotations (mypy strict enforces this, but confirm). |

## 3. Report

Produce the checklist from the PR template with each item marked pass / fail /
n/a, plus a one-line note on anything that needs the author's attention. If
everything passes, say so and give the branch name for the PR.
