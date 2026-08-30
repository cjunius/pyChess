---
name: update-docs
description: >
  Review the current changes and update README.md and every markdown file under
  docs/ so the documentation matches the code. Use after implementing a feature,
  refactor, or structural change, or when the user asks to "update the docs".
---

# update-docs

Bring `README.md` and `docs/*.md` back in sync with the code. Only reflect
changes that are actually in the diff - never invent features or numbers.

## 1. Find what changed

Determine the review range:

- If the user named a base (branch, tag, commit), diff against that.
- Else if the branch is not `main`, use `git diff main...HEAD` plus any
  uncommitted changes (`git diff` / `git status`).
- Else review uncommitted changes only.

```bash
git status
git diff <base>...HEAD
git diff              # unstaged
```

Summarise, for yourself, what changed: new/removed/renamed modules, changed
public APIs or class names, new/changed UCI commands or `go` options, new CLI
entry points, dependency or Python-version changes, tooling changes, and any
behaviour change a user or contributor would notice.

## 2. Read the current docs

Read `README.md` and each file in `docs/` (currently `design.md`,
`engine-strength.md`, `performance.md`, `tasks.md`). Note their structure and
tone so edits blend in.

## 3. Update each file where the diff touches it

Match the existing style; make the smallest edit that makes the doc correct.

| File | Update when the change affects... |
|---|---|
| `README.md` | the one-paragraph description, badges, quick-start commands, UCI usage, the repository-layout tree, or the development commands |
| `docs/design.md` | architecture (collaborators, coordinator, layers), the "Implemented" list, or the "Backlog" list |
| `docs/engine-strength.md` | evaluation/search features that move the estimate, or the calibration/time-control notes. **Do not change Elo numbers** unless the diff contains a measured result. |
| `docs/performance.md` | only when the diff includes fresh benchmark numbers. Never fabricate timings. |
| `docs/tasks.md` | a roadmap item was implemented (move it into "Recently completed" and delete it from the numbered list), or a housekeeping item was done |

Also check: the repo-layout tree in `README.md` lists every `src/pychess/*.py`
module with a one-line description - add/rename/remove rows to match.

Cross-references: if you rename or move a doc, fix every link to it in the other
docs and the README.

## 4. Adjacent files (mention, don't silently skip)

- `CLAUDE.md` - update the architecture map / gotchas if a module moved or a
  convention changed.
- `CHANGELOG.md` - add a bullet under `## [Unreleased]`. This is outside the
  skill's core scope; do it if it's clearly missing, otherwise flag it.

## 5. Verify

- Every relative link in the edited files resolves (`ls` the targets).
- Every shell command / code snippet shown in the docs still runs or matches
  current config (`pyproject.toml`, `.github/workflows/ci.yml`).
- No stale references to removed names:
  ```bash
  git grep -nE 'removed_name_1|removed_name_2' -- '*.md'
  ```

## 6. Report

List each file you changed and the one-line reason, and each doc you
deliberately left alone. If a change needs numbers you can't derive (Elo,
benchmarks), say so and leave a clear TODO rather than guessing.
