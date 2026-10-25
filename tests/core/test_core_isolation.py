import ast
import subprocess
import sys
from pathlib import Path

import lingpuzzle.core

FORBIDDEN = ("lingpuzzle.api", "lingpuzzle.web", "fastapi", "starlette", "uvicorn")


def is_forbidden(imported: str) -> bool:
    return any(
        imported == name or imported.startswith(name + ".") for name in FORBIDDEN
    )


def resolve_relative(
    module: str, level: int, target: str | None, is_package: bool = False
) -> str:
    parts = module.split(".")
    keep = len(parts) - (level - 1 if is_package else level)
    base = parts[: max(keep, 0)]
    if target:
        base.append(target)
    return ".".join(base)


def find_forbidden_imports(
    source: str, module: str, is_package: bool = False
) -> list[str]:
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            candidates = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = resolve_relative(module, node.level, node.module, is_package)
            else:
                base = node.module or ""
            if is_forbidden(base):
                candidates = [base]
            else:
                candidates = [f"{base}.{alias.name}" for alias in node.names]
        else:
            continue
        found.extend(name for name in candidates if is_forbidden(name))
    return found


def test_forbidden_absolute_import_detected() -> None:
    result = find_forbidden_imports("import lingpuzzle.api", "lingpuzzle.core.x")
    assert result == ["lingpuzzle.api"]


def test_forbidden_from_import_detected() -> None:
    source = "from lingpuzzle.web.views import page"
    result = find_forbidden_imports(source, "lingpuzzle.core.x")
    assert result == ["lingpuzzle.web.views"]


def test_forbidden_relative_import_detected() -> None:
    result = find_forbidden_imports(
        "from ...api import app", "lingpuzzle.core.numerals.solver"
    )
    assert result == ["lingpuzzle.api"]


def test_forbidden_name_from_package_import_detected() -> None:
    result = find_forbidden_imports(
        "from lingpuzzle import api, core", "lingpuzzle.core.x"
    )
    assert result == ["lingpuzzle.api"]


def test_relative_import_from_package_init_detected() -> None:
    result = find_forbidden_imports(
        "from ..api import app", "lingpuzzle.core", is_package=True
    )
    assert result == ["lingpuzzle.api"]


def test_relative_import_from_package_init_inside_core_allowed() -> None:
    result = find_forbidden_imports(
        "from .common import x", "lingpuzzle.core", is_package=True
    )
    assert result == []


def test_relative_import_inside_core_allowed() -> None:
    result = find_forbidden_imports(
        "from ..common import words", "lingpuzzle.core.numerals.solver"
    )
    assert result == []


def test_third_party_web_import_detected() -> None:
    source = "import fastapi\nfrom starlette.requests import Request\nimport uvicorn"
    result = find_forbidden_imports(source, "lingpuzzle.core.x")
    assert result == ["fastapi", "starlette.requests", "uvicorn"]


def test_similar_prefix_not_flagged() -> None:
    source = "import lingpuzzle.apiary\nimport fastapi_utils_fake"
    assert find_forbidden_imports(source, "lingpuzzle.core.x") == []


def test_allowed_imports_not_flagged() -> None:
    source = "import os\nfrom lingpuzzle.core.common import x\nimport lingpuzzle"
    assert find_forbidden_imports(source, "lingpuzzle.core.x") == []


def test_empty_source_has_no_forbidden_imports() -> None:
    assert find_forbidden_imports("", "lingpuzzle.core") == []


def module_name(core_dir: Path, path: Path) -> str:
    parts = ["lingpuzzle", "core", *path.relative_to(core_dir).with_suffix("").parts]
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def test_core_sources_have_no_forbidden_imports() -> None:
    core_dir = Path(lingpuzzle.core.__file__).parent
    files = sorted(core_dir.rglob("*.py"))
    offenders = {
        str(path): found
        for path in files
        if (
            found := find_forbidden_imports(
                path.read_text(encoding="utf-8"),
                module_name(core_dir, path),
                is_package=path.name == "__init__.py",
            )
        )
    }
    assert offenders == {}
    assert len(files) >= 3


def test_core_import_does_not_load_web_modules() -> None:
    code = (
        "import sys, lingpuzzle.core.common, lingpuzzle.core.numerals; "
        "print('\\n'.join(sorted(sys.modules)))"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code], check=True, capture_output=True, text=True
    )
    loaded = completed.stdout.splitlines()
    assert "lingpuzzle.core.numerals" in loaded
    assert [name for name in loaded if is_forbidden(name)] == []
