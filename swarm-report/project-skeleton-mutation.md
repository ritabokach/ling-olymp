# Mutation report

Base: `HEAD` · tests: `.venv/bin/python -m pytest -q` · mutants: 2 of 2 candidates
Score: **0/2 = 0%** (min 60%)

## Survived — tests stay green with this bug

- `src/lingpuzzle/core/__init__.py:3` or → and: `Must never import lingpuzzle.api, lingpuzzle.web or a web framework: the core` → `Must never import lingpuzzle.api, lingpuzzle.web and a web framework: the core`
- `src/lingpuzzle/core/__init__.py:4` and → or: `has to stay runnable and testable without any server.` → `has to stay runnable or testable without any server.`

## Killed


## Orchestrator note
Both survivors are equivalent mutants: the mutated `or`/`and` are words inside the docstring of `src/lingpuzzle/core/__init__.py`, not code. Behaviour cannot change, so no test is needed. The skeleton has no non-test logic. `find_forbidden_imports` lives in `tests/core/test_core_isolation.py` and the script does not mutate test files; it has its own 8 unit tests. Effective score: n/a (0 real mutants), not a rework trigger.
