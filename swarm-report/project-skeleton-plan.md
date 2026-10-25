```yaml
summary: Installable core skeleton — pyproject.toml (src layout, package lingpuzzle, hatchling, pytest + ruff config, dev extras), empty packages lingpuzzle.core.{common,numerals}, smoke tests in tests/core/, GitHub Actions CI (ruff check, ruff format --check, pytest on 3.12 and 3.14), English README, local .venv with editable install. No api/, no web/.

acceptance_criteria:
  - "`/opt/homebrew/bin/python3.12 -m venv .venv && .venv/bin/pip install -e '.[dev]'` succeeds from a clean checkout"
  - "`.venv/bin/python -c 'import lingpuzzle.core.common, lingpuzzle.core.numerals'` exits 0"
  - "`lingpuzzle.__version__ == \"0.1.0\"` and equals `importlib.metadata.version(\"lingpuzzle\")` (single source of version)"
  - "`.venv/bin/python -m pytest -q` passes, all tests in tests/core/ collected, 0 failed"
  - "`.venv/bin/ruff check .` and `.venv/bin/ruff format --check .` both exit 0; harness files under .claude/ excluded"
  - "Static test fails if any file under src/lingpuzzle/core/ imports lingpuzzle.api, lingpuzzle.web, fastapi, starlette or uvicorn (absolute or relative import)"
  - "Runtime test: after importing lingpuzzle.core in a fresh interpreter, no lingpuzzle.api / lingpuzzle.web / fastapi module is in sys.modules"
  - ".github/workflows/ci.yml runs on push and pull_request, matrix python-version [\"3.12\", \"3.14\"], steps: install -e .[dev], ruff check, ruff format --check, pytest"
  - "Tests run against installed package (src layout): no sys.path hacks, no conftest inserting src/"
  - "README.md in English: what the project is, why rule-based not LLM, status, quickstart, layout, dev commands, CI badge"
  - "No src/lingpuzzle/api/, no web/, no tests/api/ created"

affected_files:
  - path: pyproject.toml
    change: "new. [build-system] hatchling. [project] name=lingpuzzle, dynamic=[\"version\"], requires-python='>=3.12', description, readme=README.md, license, no runtime deps. [project.optional-dependencies] dev=[\"pytest>=8\", \"ruff>=0.8\"]. [tool.hatch.version] path='src/lingpuzzle/__init__.py'. [tool.hatch.build.targets.wheel] packages=['src/lingpuzzle']. [tool.pytest.ini_options] testpaths=['tests'], addopts=['--import-mode=importlib','-ra','--strict-markers']. [tool.ruff] target-version='py312', line-length=88, src=['src','tests'], extend-exclude=['.claude','swarm-report']. [tool.ruff.lint] select=['E','F','W','I','B','UP','SIM']. [tool.ruff.format] defaults."
    owner: python-core
  - path: src/lingpuzzle/__init__.py
    change: "new. Module docstring (one line, what the package is). `__version__ = \"0.1.0\"`. Nothing else, no imports of subpackages."
    owner: python-core
  - path: src/lingpuzzle/core/__init__.py
    change: "new. Docstring only: rule-based puzzle core, must not import web/api (why-comment about the invariant)."
    owner: python-core
  - path: src/lingpuzzle/core/common/__init__.py
    change: "new. Docstring only: shared parts for all puzzle types (word generator, puzzle model — later)."
    owner: python-core
  - path: src/lingpuzzle/core/numerals/__init__.py
    change: "new. Docstring only: numeral-system puzzles (language, number to word, solver, generator — later)."
    owner: python-core
  - path: tests/core/test_package.py
    change: "new. Import + version smoke tests (test_cases 1-4)."
    owner: python-core
  - path: tests/core/test_core_isolation.py
    change: "new. Helper `find_forbidden_imports(source: str, module: str) -> list[str]` (ast-based, resolves relative ImportFrom against `module`, matches FORBIDDEN prefixes on dotted boundary) + its unit tests + scan of real core files + subprocess sys.modules check (test_cases 5-15)."
    owner: python-core
  - path: .github/workflows/ci.yml
    change: "new. name: CI. on: push, pull_request. jobs.test: runs-on ubuntu-latest, strategy.fail-fast false, matrix python-version ['3.12','3.14'] (quoted strings, else YAML reads 3.12 fine but 3.10-style floats break). steps: actions/checkout@v4, actions/setup-python@v5 with python-version + cache: pip, `python -m pip install -e '.[dev]'`, `ruff check .`, `ruff format --check .`, `pytest`."
    owner: python-core
  - path: README.md
    change: "rewrite (currently only `# ling-olymp`). English, portfolio: title + CI badge (github.com/ritabokach/ling-olymp/actions/workflows/ci.yml/badge.svg), one-paragraph pitch, why rule-based (uniqueness guarantee; LingOly NeurIPS 2024 — top model 38.7% on hard tasks; sudoku-generator analogy), status: skeleton, MVP = numeral systems, quickstart (venv + pip install -e '.[dev]'), dev commands (pytest, ruff check, ruff format), layout tree (only what exists + planned api/web marked 'stage 2'), link to .memory-bank/decisions.md as decision log. Follow anti-ai-slop-writing."
    owner: none

unowned_files:
  - README.md

steps:
  - "1. Write pyproject.toml (python-core). Verify hook will fail until venv exists — expected; do step 2 right after."
  - "2. Write src/lingpuzzle/__init__.py, src/lingpuzzle/core/__init__.py, core/common/__init__.py, core/numerals/__init__.py."
  - "3. Create venv: `/opt/homebrew/bin/python3.12 -m venv .venv` (3.12 = lowest supported version; CI covers 3.14). Then `.venv/bin/python -m pip install --upgrade pip` and `.venv/bin/pip install -e '.[dev]'`."
  - "4. Write tests/core/test_package.py and tests/core/test_core_isolation.py exactly per test_cases. No tests/__init__.py, no tests/core/__init__.py (importlib mode)."
  - "5. Run `.venv/bin/python -m pytest -q` — all green."
  - "6. Run `.venv/bin/ruff check .` and `.venv/bin/ruff format --check .`; fix by `.venv/bin/ruff format .` if needed. Confirm .claude/ not linted (`ruff check . --show-files | grep -c .claude` == 0)."
  - "7. Write .github/workflows/ci.yml. Locally sanity-check YAML by eye (no yaml lib in stdlib); CI proof comes on first push."
  - "8. README.md (unowned → orchestrator assigns general-purpose sonnet or main session after user picks)."
  - "9. Confirm `git status` shows no .venv/, no *.egg-info, no .ruff_cache content tracked (.gitignore already covers .venv, __pycache__, .pytest_cache, *.egg-info; ruff writes its own .gitignore inside .ruff_cache)."
  - "10. Update .memory-bank/tasks/current.md item 1a → [x] via Steward suggestion (orchestrator, not exec agent)."

test_cases:
  - name: test_package_imports
    level: unit
    given: "editable install done"
    when: "import lingpuzzle"
    then: "no exception; lingpuzzle.__name__ == 'lingpuzzle'"
    why: "catches broken src layout / wrong hatch packages path"
  - name: test_core_subpackages_import
    level: unit
    given: "editable install"
    when: "importlib.import_module for each of 'lingpuzzle.core', 'lingpuzzle.core.common', 'lingpuzzle.core.numerals' (pytest.mark.parametrize)"
    then: "each returns a module whose __name__ equals the requested name"
    why: "catches missing __init__.py in a subpackage"
  - name: test_version_value
    level: unit
    given: "package installed"
    when: "read lingpuzzle.__version__"
    then: "== '0.1.0'"
    why: "pins the declared version; catches empty/placeholder version"
  - name: test_version_matches_metadata
    level: unit
    given: "package installed via pip install -e"
    when: "importlib.metadata.version('lingpuzzle')"
    then: "== lingpuzzle.__version__"
    why: "catches drift between pyproject dynamic version and __init__ (two sources of truth)"
  - name: test_package_loaded_from_src
    level: unit
    given: "editable install"
    when: "pathlib.Path(lingpuzzle.__file__).resolve()"
    then: "parent.parent.name == 'src' and parent.name == 'lingpuzzle'"
    why: "catches a stray top-level lingpuzzle/ shadowing the src package"
  - name: test_forbidden_absolute_import_detected
    level: unit
    given: "source 'import lingpuzzle.api'"
    when: "find_forbidden_imports(source, 'lingpuzzle.core.x')"
    then: "== ['lingpuzzle.api']"
    why: "negative case for plain Import branch"
  - name: test_forbidden_from_import_detected
    level: unit
    given: "source 'from lingpuzzle.web.views import page'"
    when: "find_forbidden_imports(source, 'lingpuzzle.core.x')"
    then: "== ['lingpuzzle.web.views']"
    why: "negative case for ImportFrom branch + submodule prefix match"
  - name: test_forbidden_relative_import_detected
    level: unit
    given: "source 'from ...api import app' inside module 'lingpuzzle.core.numerals.solver'"
    when: "find_forbidden_imports(source, 'lingpuzzle.core.numerals.solver')"
    then: "== ['lingpuzzle.api']"
    why: "relative import escaping core must be resolved, else checker is blind to it (off-by-one in level resolution)"
  - name: test_relative_import_inside_core_allowed
    level: unit
    given: "source 'from ..common import words' inside 'lingpuzzle.core.numerals.solver'"
    when: "find_forbidden_imports(...)"
    then: "== []"
    why: "boundary of level resolution: level 2 stays in core; catches over-eager matching"
  - name: test_third_party_web_import_detected
    level: unit
    given: "source 'import fastapi\\nfrom starlette.requests import Request\\nimport uvicorn'"
    when: "find_forbidden_imports(source, 'lingpuzzle.core.x')"
    then: "== ['fastapi', 'starlette.requests', 'uvicorn'] (source order)"
    why: "core must not pull web frameworks directly either; checks every alias in list, not only first"
  - name: test_similar_prefix_not_flagged
    level: unit
    given: "source 'import lingpuzzle.apiary\\nimport fastapi_utils_fake'"
    when: "find_forbidden_imports(source, 'lingpuzzle.core.x')"
    then: "== []"
    why: "boundary: prefix match must stop at '.', startswith('lingpuzzle.api') without boundary is a bug"
  - name: test_allowed_imports_not_flagged
    level: unit
    given: "source 'import os\\nfrom lingpuzzle.core.common import x\\nimport lingpuzzle'"
    when: "find_forbidden_imports(...)"
    then: "== []"
    why: "negative case: stdlib, core and top-level package are fine"
  - name: test_empty_source_has_no_forbidden_imports
    level: unit
    given: "source ''"
    when: "find_forbidden_imports('', 'lingpuzzle.core')"
    then: "== []"
    why: "empty input (empty __init__.py files exist)"
  - name: test_core_sources_have_no_forbidden_imports
    level: integration
    given: "all *.py under Path(lingpuzzle.core.__file__).parent, rglob"
    when: "find_forbidden_imports per file, module name built from relative path ('__init__' → package name)"
    then: "collected dict of offenders == {}; also assert number of scanned files >= 3 (core, common, numerals)"
    why: "the real invariant from CLAUDE.md; file-count guard catches a scan that silently finds nothing"
  - name: test_core_import_does_not_load_web_modules
    level: integration
    given: "fresh interpreter: subprocess [sys.executable, '-c', 'import sys, lingpuzzle.core.common, lingpuzzle.core.numerals; print(\"\\n\".join(sorted(sys.modules)))']"
    when: "run with check=True, capture_output, text"
    then: "no printed line equals or starts with 'lingpuzzle.api', 'lingpuzzle.web', 'fastapi', 'starlette', 'uvicorn' (dotted boundary); and 'lingpuzzle.core.numerals' is among printed lines"
    why: "catches transitive runtime imports static scan misses; positive check proves the subprocess actually imported core"

risks:
  - "Verify hook runs pytest after every edit; before step 3 venv missing → red feedback. Exec agent must create venv right after pyproject + packages, not treat it as a bug."
  - "lint-gate.sh calls `ruff` from PATH, not .venv/bin/ruff. Without global ruff, per-edit ruff check silently skipped; agent must run .venv/bin/ruff itself (step 6)."
  - "Python 3.14 on GitHub runners: actions/setup-python@v5 must resolve '3.14'; if not, CI red on first push. Fallback: allow-prereleases: true. Proof only after push."
  - "ruff>=0.8 unpinned: future ruff release can change format/lint output and break CI without code change. Alternative: pin exact version (плюс: reproducible; минус: manual bumps). Plan keeps lower bound; reviewer/user may choose pin."
  - "ruff check . without extend-exclude would lint .claude/scripts/mutate.py and .claude/hooks/lib/lint_check.py (harness code) and fail CI on code we do not own."
  - "hatchling dynamic version reads __version__ via regex; keep it a plain string literal, or build fails."
  - "README.md has no exec agent owner → orchestrator must ask user (general-purpose vs /new-agent docs)."

assumptions:
  - "Build backend hatchling — Memory Bank silent. Chosen for simple src layout + single-source version. setuptools works too."
  - "Version 0.1.0 — Memory Bank silent."
  - "License: Memory Bank silent. Plan puts no license field unless user picks one (MIT typical for portfolio). Flag at after-plan checkpoint."
  - "Local venv on python3.12 (floor). CI covers 3.14."
  - "ruff rule set E,F,W,I,B,UP,SIM, line-length 88 (ruff default) — Memory Bank says only 'ruff, settings in pyproject.toml'."
  - "Forbidden-for-core list: lingpuzzle.api, lingpuzzle.web, fastapi, starlette, uvicorn. DB libs (sqlalchemy etc.) not added — CLAUDE.md names only api/web; architecture.md says core does not know DB, could add later."
  - "CI single job matrix on ubuntu-latest, triggers push + pull_request on all branches."
  - "No tests/__init__.py; pytest --import-mode=importlib so tests/core and future tests/api can share basenames."

out_of_scope:
  - "src/lingpuzzle/api/, web/, tests/api/ (stage 2)"
  - "mypy (decided later per decisions.md)"
  - "Any domain code: numeral model, word generator, solver"
  - "pre-commit hooks, Dockerfile, LICENSE file, publishing to PyPI"
  - "Switching to uv"
  - ".gitignore changes (already covers .venv, __pycache__, .pytest_cache, *.egg-info)"
```

## Skeptic fixes (merged by orchestrator, override the YAML above)

1. **Python for venv:** only `/opt/homebrew/bin/python3.12 -m venv .venv`, never bare `python3` (`/usr/bin/python3` is Apple CLT, old). Check `.venv/bin/python --version` → 3.12.x.
2. **Verify hook order:** red Verify on the `__init__.py` edits before the venv exists is expected. Create the venv right after the packages (step 3), do not debug it.
3. **CI workflow:** add `permissions: contents: read`; `actions/checkout@v5`, `actions/setup-python@v6` with `cache: pip`; `fail-fast: false`; matrix values quoted.
4. **ruff locally:** lint-gate looks for `ruff` on PATH, finds none and skips. The exec agent runs `.venv/bin/ruff check .` and `.venv/bin/ruff format --check .` itself and quotes the output in its return.
5. **Dist name in test:** `test_version_matches_metadata` takes the distribution name from `importlib.metadata.packages_distributions()["lingpuzzle"][0]` instead of hardcoding `"lingpuzzle"`, so renaming the product (`name` in pyproject) does not break the test.
6. **README.md:** edit the existing file, do not overwrite it blindly. Owner is decided at checkpoint 2.

## Blockers

- README.md has no exec agent (python-core scope excludes it). User picks the owner.
- License: none in the plan. User decides (MIT / none).
- ~~License~~ → resolved: MIT. pyproject `license = "MIT"` + `license-files = ["LICENSE"]` (python-core). `LICENSE` file is unowned → same owner as README.
