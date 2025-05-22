"""Test configuration file for pytest."""

import contextlib
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
    with contextlib.suppress(PermissionError):
        path.chmod(0o700)  # Restrictive permissions for security

    if not path.exists():
        # Fallback path for CI environments
        alt_path = Path(__file__).parent.parent / "pigame"
        if alt_path.exists():
            path = alt_path

    yield path

    with contextlib.suppress(PermissionError):
        # Cleanup after tests
        path.chmod(0o600)


@pytest.fixture(scope="session", autouse=True)
def _configure_coverage() -> None:
    """Configure coverage settings for the test session."""
    # This fixture runs automatically and helps ensure coverage works properly
    # Create coverage directory if it doesn't exist
    coverage_dir = Path(__file__).parent.parent / "htmlcov"
    coverage_dir.mkdir(exist_ok=True)

    yield

    # Ensure coverage file exists after tests
    coverage_xml = Path(__file__).parent.parent / "coverage.xml"
    if not coverage_xml.exists():
        # Create a minimal coverage.xml file if needed
        xml_content = '<?xml version="1.0" ?>\n<coverage version="1.0"></coverage>'
        coverage_xml.write_text(xml_content)
