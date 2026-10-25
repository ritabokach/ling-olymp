import importlib
import importlib.metadata
import tomllib
from pathlib import Path

import pytest

import lingpuzzle


def test_package_imports() -> None:
    assert lingpuzzle.__name__ == "lingpuzzle"


@pytest.mark.parametrize(
    "name",
    ["lingpuzzle.core", "lingpuzzle.core.common", "lingpuzzle.core.numerals"],
)
def test_core_subpackages_import(name: str) -> None:
    assert importlib.import_module(name).__name__ == name


def test_version_value() -> None:
    assert lingpuzzle.__version__ == "0.1.0"


def test_version_matches_metadata() -> None:
    pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
    distribution = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"][
        "name"
    ]
    assert importlib.metadata.version(distribution) == lingpuzzle.__version__


def test_package_loaded_from_src() -> None:
    package_dir = Path(lingpuzzle.__file__).resolve().parent
    assert package_dir.name == "lingpuzzle"
    assert package_dir.parent.name == "src"
