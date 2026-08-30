## Summary

<!-- What does this change and why? Link any issue it closes. -->

## Testing

<!-- What you ran / added. Include before-after numbers for perf changes. -->

## Checklist

With Claude Code, `/pr-check` runs the whole list below.

- [ ] `ruff check .` and `ruff format --check .` pass
- [ ] `mypy` passes (strict on `src/`)
- [ ] `pytest` passes; coverage stays >= 85%
- [ ] Tests added or updated for the change
- [ ] `CHANGELOG.md` updated under `## [Unreleased]`
- [ ] `README.md` / `docs/*.md` updated if behaviour or structure changed (`/update-docs`)
- [ ] `docs/performance.md` refreshed if search speed changed (`/bench`)
