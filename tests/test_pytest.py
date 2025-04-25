#!/usr/bin/env python3
"""Integration tests for the pigame command-line interface."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from src.python import pigame


if TYPE_CHECKING:
    from collections.abc import Iterator

# Test constants
VALID_PI_SHORT = "3.14159"
VALID_PI_LONG = "3.141592653589793238462643383279"
INCORRECT_PI = "3.14158"
TEST_LENGTH_SHORT = 5
TEST_LENGTH_MEDIUM = 15
TEST_LENGTH_LONG = 100
LINES_EASTER_EGG = 3
LINES_ERROR_MSG = 2


@pytest.fixture()
def test_path() -> Iterator[Path]:
    """Provides a secure test environment path."""
    path = Path(__file__).parent.parent / "src/python/pigame.py"
    path.chmod(0o700)  # Restrictive permissions for security
    yield path
    # Cleanup after tests
    path.chmod(0o600)


class TestPiGameFunctions:
    """Unit tests for the core functions of the pigame.py module."""

    def test_input_validation_valid(self: TestPiGameFunctions) -> None:
        """Test input validation with valid inputs."""
        assert pigame.input_validation(VALID_PI_SHORT) is True
        assert pigame.input_validation(VALID_PI_LONG) is True
        assert pigame.input_validation("3.1") is True

    def test_input_validation_invalid(self: TestPiGameFunctions) -> None:
        """Test input validation with invalid inputs."""
        with pytest.raises(ValueError, match="Invalid input"):
            pigame.input_validation("abc")
        with pytest.raises(ValueError, match="Invalid input"):
            pigame.input_validation("3,14159")
        with pytest.raises(ValueError, match="Invalid input"):
            pigame.input_validation("")

    def test_length_validation_valid(self: TestPiGameFunctions) -> None:
        """Test length validation with valid inputs."""
        assert pigame.length_validation(str(TEST_LENGTH_SHORT)) == TEST_LENGTH_SHORT
        assert pigame.length_validation(str(TEST_LENGTH_MEDIUM)) == TEST_LENGTH_MEDIUM
        assert pigame.length_validation(str(TEST_LENGTH_LONG)) == TEST_LENGTH_LONG

    def test_length_validation_invalid(self: TestPiGameFunctions) -> None:
        """Test length validation with invalid inputs."""
        with pytest.raises(ValueError, match="Invalid input"):
            pigame.length_validation("abc")
        with pytest.raises(SystemExit, match="too big"):
            pigame.length_validation(str(pigame.MAX_LENGTH + 1))

    def test_calculate_pi(self: TestPiGameFunctions) -> None:
        """Test pi calculation with various lengths."""
        assert pigame.calculate_pi(1) == "3.1"
        assert pigame.calculate_pi(TEST_LENGTH_SHORT) == VALID_PI_SHORT
        assert (
            len(pigame.calculate_pi(TEST_LENGTH_MEDIUM)) == TEST_LENGTH_MEDIUM + 2
        )  # +2 for "3."

    def test_color_your_pi(self: TestPiGameFunctions) -> None:
        """Test color_your_pi function with various inputs."""
        error_count = pigame.color_your_pi(
            input_pi=VALID_PI_SHORT,
            correct_pi=VALID_PI_SHORT,
            verbose=False,
        )
        assert error_count == 0

        error_count = pigame.color_your_pi(
            input_pi=INCORRECT_PI,
            correct_pi=VALID_PI_SHORT,
            verbose=True,
        )
        assert error_count == 1

        error_count = pigame.color_your_pi(
            input_pi=INCORRECT_PI,
            correct_pi=VALID_PI_SHORT,
            verbose=True,
            colorblind_mode=True,
        )
        assert error_count == 1

    def test_handle_easter_egg(self: TestPiGameFunctions) -> None:
        """Test the easter egg handler."""
        with patch("builtins.print") as mock_print:
            assert pigame.handle_easter_egg("Archimedes") is True
            assert mock_print.call_count == LINES_EASTER_EGG

        with patch("builtins.print") as mock_print:
            assert pigame.handle_easter_egg("pi") is True
            assert mock_print.call_count == LINES_EASTER_EGG

        with patch("builtins.print") as mock_print:
            assert pigame.handle_easter_egg("PI") is True
            assert mock_print.call_count == LINES_EASTER_EGG

        with patch("builtins.print") as mock_print:
            assert pigame.handle_easter_egg(VALID_PI_SHORT) is False
            mock_print.assert_not_called()


class TestPiGameIntegration:
    """Integration tests for the pigame command-line interface."""

    def test_version_flag(self: TestPiGameIntegration, test_path: Path) -> None:
        """Test the version flag."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(test_path), "-V"],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "version" in result.stdout.lower()

    def test_help_flag(self: TestPiGameIntegration, test_path: Path) -> None:
        """Test the help flag."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(test_path), "-h"],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "usage:" in result.stdout.lower()

    def test_pi_calculation(self: TestPiGameIntegration, test_path: Path) -> None:
        """Test pi calculation with specified precision."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(test_path), "-p", str(TEST_LENGTH_SHORT)],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert VALID_PI_SHORT in result.stdout

    def test_correct_input(self: TestPiGameIntegration, test_path: Path) -> None:
        """Test with correct pi input."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(test_path), VALID_PI_SHORT],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "Match" in result.stdout

    def test_incorrect_input(self: TestPiGameIntegration, test_path: Path) -> None:
        """Test with incorrect pi input."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(test_path), INCORRECT_PI],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "No match" in result.stdout

    def test_verbose_mode(self: TestPiGameIntegration, test_path: Path) -> None:
        """Test verbose mode output."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(test_path), "-v", INCORRECT_PI],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "You can do better!" in result.stdout

    def test_invalid_input(self: TestPiGameIntegration, test_path: Path) -> None:
        """Test with invalid input."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        with pytest.raises(subprocess.CalledProcessError) as excinfo:
            subprocess.run(
                [str(test_path), "abc"],
                capture_output=True,
                text=True,
                check=True,
            )  # - trusted input
        assert "Invalid input" in excinfo.value.stderr

    def test_easter_egg(self: TestPiGameIntegration, test_path: Path) -> None:
        """Test the easter egg functionality."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(test_path), "Archimedes"],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "Archimedes constant" in result.stdout
