#!/usr/bin/env python3
"""Integration tests for the pigame command-line interface."""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from src.python import pigame


if TYPE_CHECKING:
    from pathlib import Path


# Test constants
VALID_PI_SHORT = "3.14159"
VALID_PI_LONG = "3.141592653589793238462643383279"
INCORRECT_PI = "3.14158"
TEST_LENGTH_SHORT = 5
TEST_LENGTH_MEDIUM = 15
TEST_LENGTH_LONG = 100
LINES_EASTER_EGG = 3
LINES_ERROR_MSG = 2


# This fixture is now imported from conftest.py


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

    def test_version_flag(self: TestPiGameIntegration, pigame_exec: Path) -> None:
        """Test the version flag."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(pigame_exec), "-V"],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "version" in result.stdout.lower()

    def test_help_flag(self: TestPiGameIntegration, pigame_exec: Path) -> None:
        """Test the help flag."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(pigame_exec), "-h"],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "usage:" in result.stdout.lower()

    def test_pi_calculation(self: TestPiGameIntegration, pigame_exec: Path) -> None:
        """Test pi calculation with specified precision."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(pigame_exec), "-p", str(TEST_LENGTH_SHORT)],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert VALID_PI_SHORT in result.stdout

    def test_correct_input(self: TestPiGameIntegration, pigame_exec: Path) -> None:
        """Test with correct pi input."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(pigame_exec), VALID_PI_SHORT],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "Match" in result.stdout

    def test_incorrect_input(self: TestPiGameIntegration, pigame_exec: Path) -> None:
        """Test with incorrect pi input."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(pigame_exec), INCORRECT_PI],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "No match" in result.stdout

    def test_verbose_mode(self: TestPiGameIntegration, pigame_exec: Path) -> None:
        """Test verbose mode output."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(pigame_exec), "-v", INCORRECT_PI],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "You can do better!" in result.stdout

    def test_invalid_input(self: TestPiGameIntegration, pigame_exec: Path) -> None:
        """Test with invalid input."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        with pytest.raises(subprocess.CalledProcessError) as excinfo:
            subprocess.run(
                [str(pigame_exec), "abc"],
                capture_output=True,
                text=True,
                check=True,
            )  # - trusted input
        assert "Invalid input" in excinfo.value.stderr

    def test_easter_egg(self: TestPiGameIntegration, pigame_exec: Path) -> None:
        """Test the easter egg functionality."""
        # subprocess calls below use only trusted, static input (test scripts)
        # no user input is passed to subprocess
        result = subprocess.run(
            [str(pigame_exec), "Archimedes"],
            capture_output=True,
            text=True,
            check=True,
        )  # - trusted input
        assert "Archimedes constant" in result.stdout


class TestExceptionClasses:
    """Tests for custom exception classes."""

    def test_pi_error(self: TestExceptionClasses) -> None:
        """Test base PiError exception."""
        error = pigame.PiError("test message")
        assert str(error) == "test message"

    def test_negative_length_error(self: TestExceptionClasses) -> None:
        """Test NegativeLengthError exception."""
        error = pigame.NegativeLengthError(-5)
        assert "Length -5 cannot be negative" in str(error)

    def test_too_many_digits_error(self: TestExceptionClasses) -> None:
        """Test TooManyDigitsError exception."""
        error = pigame.TooManyDigitsError(10000, 5001)
        assert "Requested 10000 digits" in str(error)
        assert "5001 are available" in str(error)


class TestFormatting:
    """Tests for formatting functions."""

    def test_format_pi_with_spaces_short(self: TestFormatting) -> None:
        """Test formatting short pi string."""
        result = pigame.format_pi_with_spaces("3.14159")
        assert result == "3.14159"

    def test_format_pi_with_spaces_medium(self: TestFormatting) -> None:
        """Test formatting medium pi string with spaces."""
        result = pigame.format_pi_with_spaces("3.1415926535")
        assert result == "3.14159 26535"

    def test_format_pi_with_spaces_long(self: TestFormatting) -> None:
        """Test formatting long pi string with multiple spaces."""
        result = pigame.format_pi_with_spaces("3.141592653589793")
        assert result == "3.14159 26535 89793"

    def test_get_version(self: TestFormatting) -> None:
        """Test version retrieval."""
        version = pigame.get_version()
        assert version is not None
        assert len(version) > 0


class TestPrintResults:
    """Tests for print_results function."""

    def test_print_results_match_verbose(self: TestPrintResults) -> None:
        """Test print_results with matching pi in verbose mode."""
        with patch("builtins.print") as mock_print:
            pigame.print_results(
                user_pi="3.14159",
                calculated_pi="3.14159",
                decimals=5,
                verbose=True,
            )
            # Should print pi info and "Well done."
            min_expected_calls = 2
            assert mock_print.call_count >= min_expected_calls

    def test_print_results_match_non_verbose(self: TestPrintResults) -> None:
        """Test print_results with matching pi in non-verbose mode."""
        with patch("builtins.print") as mock_print:
            pigame.print_results(
                user_pi="3.14159",
                calculated_pi="3.14159",
                decimals=5,
                verbose=False,
            )
            # Should print "Match"
            calls = [str(c) for c in mock_print.call_args_list]
            assert any("Match" in c for c in calls)

    def test_print_results_no_match_verbose(self: TestPrintResults) -> None:
        """Test print_results with non-matching pi in verbose mode."""
        with patch("builtins.print") as mock_print:
            pigame.print_results(
                user_pi="3.14158",
                calculated_pi="3.14159",
                decimals=5,
                verbose=True,
            )
            calls = [str(c) for c in mock_print.call_args_list]
            assert any("better" in c for c in calls)

    def test_print_results_perfect_score(self: TestPrintResults) -> None:
        """Test print_results with high decimal count."""
        pi_20 = pigame.calculate_pi(20)
        with patch("builtins.print") as mock_print:
            pigame.print_results(
                user_pi=pi_20,
                calculated_pi=pi_20,
                decimals=20,
                verbose=True,
            )
            calls = [str(c) for c in mock_print.call_args_list]
            assert any("Perfect" in c for c in calls)


class TestLengthValidationEdgeCases:
    """Additional edge case tests for length validation."""

    def test_length_validation_negative_returns_default(
        self: TestLengthValidationEdgeCases,
    ) -> None:
        """Test length validation with negative number returns default."""
        result = pigame.length_validation("-5")
        assert result == pigame.DEFAULT_LENGTH

    def test_length_validation_zero_returns_default(
        self: TestLengthValidationEdgeCases,
    ) -> None:
        """Test length validation with zero returns default."""
        result = pigame.length_validation("0")
        assert result == pigame.DEFAULT_LENGTH


class TestInputValidationEdgeCases:
    """Additional edge case tests for input validation."""

    def test_input_validation_multiple_dots(
        self: TestInputValidationEdgeCases,
    ) -> None:
        """Test input validation with multiple decimal points."""
        with pytest.raises(ValueError, match="Invalid input"):
            pigame.input_validation("3..14159")

    def test_input_validation_valid_integer(
        self: TestInputValidationEdgeCases,
    ) -> None:
        """Test input validation accepts valid integer format."""
        # The function only validates format, not pi correctness
        assert pigame.input_validation("3.14") is True


class TestCalculatePiEdgeCases:
    """Additional edge case tests for calculate_pi."""

    def test_calculate_pi_zero_uses_default(self: TestCalculatePiEdgeCases) -> None:
        """Test pi calculation with zero uses default length."""
        result = pigame.calculate_pi(0)
        # Zero length uses DEFAULT_LENGTH (15)
        assert len(result) == pigame.DEFAULT_LENGTH + 2  # "3." + 15 digits

    def test_calculate_pi_negative_raises(self: TestCalculatePiEdgeCases) -> None:
        """Test pi calculation with negative raises ValueError."""
        with pytest.raises(ValueError, match="cannot be negative"):
            pigame.calculate_pi(-5)

    def test_calculate_pi_large(self: TestCalculatePiEdgeCases) -> None:
        """Test pi calculation with large number of decimals."""
        num_decimals = 100
        result = pigame.calculate_pi(num_decimals)
        expected_length = num_decimals + 2  # "3." + decimals
        assert len(result) == expected_length
        assert result.startswith("3.14159265358979323846")
