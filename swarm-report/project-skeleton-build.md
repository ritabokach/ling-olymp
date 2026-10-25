# Build: project-skeleton

## python-core — done
Files: pyproject.toml, src/lingpuzzle/__init__.py, src/lingpuzzle/core/{,common/,numerals/}__init__.py, tests/core/test_package.py, tests/core/test_core_isolation.py, .github/workflows/ci.yml, .venv (Python 3.12.13, gitignored).
Tests: `.venv/bin/python -m pytest -q` → 17 passed in 0.02s (15 planned cases; parametrize gives 17). `.venv/bin/ruff check .` → All checks passed!; `ruff format --check .` → 19 files already formatted.
Deviation: skeptic fix 5. `packages_distributions()` has no `lingpuzzle` key for a hatchling editable install, so the test reads the dist name from pyproject `[project].name` via tomllib.

## docs (run as general-purpose; the docs agent loads after a session restart) — done
Files: README.md (rewritten from the one-line stub), LICENSE (MIT, 2026, Margarita Bokach).
Tests: same command, 17 passed.

## Open
- CI on 3.14 is proven only after the first push.
- README quickstart says `python3.12 -m venv .venv`; the venv-creation line was not re-run.

## Rework round 1 (after review: rework)
- python-core: tests/core/test_core_isolation.py. Alias names in from-imports are now checked; relative imports in package `__init__` resolve against the package (`is_package`). +3 tests → 20 passed. The orchestrator probed the reviewer's cases: `from lingpuzzle import api` → ['lingpuzzle.api']; `from ..api import app` in core/__init__ → ['lingpuzzle.api'].
- docs: README.md. LingOly quote checked against arXiv 2406.06196 and linked. "CI is configured" replaces "CI runs". Isolation claim narrowed (dynamic imports not covered). Quickstart re-run in a scratch venv: ok.
