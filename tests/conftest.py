"""Test configuration file for pytest."""

import sys
from collections.abc import Iterator
from pathlib import Path

import pytest


# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def pigame_exec() -> Iterator[Path]:
    """Provides the path to the pigame executable."""
    path = Path(__file__).parent.parent / "src/python/pigame.py"
    original_mode = path.stat().st_mode & 0o777
    path.chmod(original_mode | 0o700)
    yield path
    path.chmod(original_mode)
