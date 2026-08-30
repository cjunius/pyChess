---
name: release
description: >
  Cut a new release: bump the version, roll the changelog, run the full gate,
  commit, and tag. Use when the user asks to "cut a release", "tag a version",
  or "release vX.Y.Z".
---

# release

The version is single-sourced from `src/pychess/__init__.py` (`__version__`);
`pyproject.toml` reads it via `[tool.hatch.version]`. Do **not** edit the
version anywhere else.

## 1. Preconditions

```bash
git status                    # working tree must be clean
git fetch && git status       # branch must not be behind its upstream
git log -1 --format='%H %s'   # note the commit being released
```

- Be on `main` (or a `release/*` branch the user names).
- The latest `main` CI run (`ci-ok`) must be green. If you can't verify it, ask.
- If the tree is dirty or the branch is behind, stop and tell the user.

## 2. Choose the version

Read `## [Unreleased]` in `CHANGELOG.md` and the current `__version__`. Pick the
next version by semver from what's in Unreleased:

- breaking API / CLI change -> major
- new user-facing capability -> minor
- fixes / internal only -> patch

Confirm the number with the user before writing anything. (For the very first
release, `__version__` may already equal the target.)

## 3. Apply the changes

1. Set `__version__` in `src/pychess/__init__.py` to `X.Y.Z`.
2. In `CHANGELOG.md`:
   - rename `## [Unreleased]` to `## [X.Y.Z] - <today's date, YYYY-MM-DD>`
   - add a fresh empty `## [Unreleased]` section above it
   - if Unreleased was empty, stop - there's nothing to release.

Get today's date with `date +%F` (do not guess it).

## 4. Verify

```bash
pip install -e ".[dev]"
ruff check . && ruff format --check . && mypy && pytest
python -c "import pychess; print(pychess.__version__)"   # == X.Y.Z
pip install .    # throwaway build sanity check (in a temp venv if possible)
```

## 5. Commit and tag

```bash
git add src/pychess/__init__.py CHANGELOG.md
git commit -m "chore(release): vX.Y.Z"
git tag -a vX.Y.Z -m "vX.Y.Z"
```

## 6. Hand off (do not push without the user's OK)

Pushing and publishing are outward-facing. Print these for the user to run:

```bash
git push origin <branch> --follow-tags
```

Then draft the GitHub Release from the `CHANGELOG.md` section for this version:

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <(sed -n '/## \[X.Y.Z\]/,/## \[/p' CHANGELOG.md | sed '$d')
```

or paste that changelog section into the Release UI.

## 7. Report

State the new version, the files changed, the tag name, and the exact push /
release commands the user still needs to run.
