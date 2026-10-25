# ling-olymp

[![CI](https://github.com/ritabokach/ling-olymp/actions/workflows/ci.yml/badge.svg)](https://github.com/ritabokach/ling-olymp/actions/workflows/ci.yml)

A generator of linguistics olympiad puzzles in the style of the Traditional Olympiad and IOL. Every puzzle it produces has exactly one correct answer. The plan is to put the puzzles on a timed solving platform with a leaderboard, like speedcubing.

## Why rule-based

A linguistics puzzle is only fair if the data admits one solution. The generator builds a puzzle from explicit rules, and a solver then checks that no second answer fits. This is the same idea as a sudoku generator: a puzzle with two solutions is rejected.

An LLM cannot give that guarantee. It also solves these tasks poorly: on the harder problems of the [LingOly benchmark](https://arxiv.org/abs/2406.06196) (NeurIPS 2024, Datasets and Benchmarks Track) even the top model reached only 38.7% accuracy. So the core is plain Python code, with no LLM in it.

## Status

Early skeleton. The package installs, the empty core packages import, CI is configured in GitHub Actions. No puzzle logic yet.

The MVP is numeral-system puzzles: generate a made-up language with its number words, check that the answer is unique, then add a task page, answer checking, timing and a leaderboard.

## Quickstart

Requires Python 3.12 or newer.

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/python -c 'import lingpuzzle; print(lingpuzzle.__version__)'
```

The last command prints `0.1.0`.

## Development

```bash
.venv/bin/python -m pytest -q       # tests
.venv/bin/ruff check .              # lint
.venv/bin/ruff format .             # format (use --check to only verify)
```

The CI workflow runs the same checks on Python 3.12 and 3.14 for every push and pull request.

The architecture rule is that the core never imports the web layer. `tests/core/test_core_isolation.py` scans the source under `src/lingpuzzle/core/` for imports of `lingpuzzle.api`, `lingpuzzle.web`, `fastapi`, `starlette` and `uvicorn`, and fails when it finds one. The scan is static, so it covers plain, `from` and relative imports but not dynamic ones such as `importlib`.

## Layout

```
src/lingpuzzle/
  core/
    common/      shared parts for all puzzle types
    numerals/    numeral-system puzzles
  api/           planned, stage 2
  web/           planned, stage 2
tests/core/      package and core-isolation tests
.github/workflows/ci.yml
```

## Decisions

Architecture and product decisions, with the reason for each, are logged in [`.memory-bank/decisions.md`](.memory-bank/decisions.md).

## License

[MIT](LICENSE)
