#!/usr/bin/env python3
"""Unit tests for the pigame Python implementation."""

from __future__ import annotations

import pytest

from src.python import pigame


# Test constants
VALID_PI = "3.14159"
INVALID_PI = "abc"
DECIMAL_PI = "3,14159"
TEST_LENGTH = 5
INVALID_LENGTH = "abc"
TOO_LARGE_LENGTH = str(pigame.MAX_LENGTH + 1)


def test_input_validation_valid() -> None:
    """Test input validation with valid input."""
    assert pigame.input_validation(VALID_PI) is True


def test_input_validation_invalid() -> None:
    """Test input validation with invalid input."""
    with pytest.raises(ValueError, match="Invalid input"):
        pigame.input_validation(INVALID_PI)


def test_input_validation_decimal_comma() -> None:
    """Test input validation with decimal comma instead of point."""
    with pytest.raises(ValueError, match="Invalid input"):
        pigame.input_validation(DECIMAL_PI)


def test_length_validation_valid() -> None:
    """Test length validation with valid input."""
    assert pigame.length_validation(str(TEST_LENGTH)) == TEST_LENGTH


def test_length_validation_invalid() -> None:
    """Test length validation with invalid input."""
    with pytest.raises(ValueError, match="Invalid input"):
        pigame.length_validation(INVALID_LENGTH)


def test_length_validation_too_large() -> None:
    """Test length validation with value exceeding maximum."""
    with pytest.raises(SystemExit):
        pigame.length_validation(TOO_LARGE_LENGTH)


def test_calculate_pi() -> None:
    """Test pi calculation with specific length."""
    result = pigame.calculate_pi(TEST_LENGTH)
    assert isinstance(result, str)
    assert len(result) == TEST_LENGTH + 2  # +2 for "3."
    assert result.startswith("3.14159")


def test_color_your_pi_match() -> None:
    """Test color_your_pi with matching input."""
    error_count = pigame.color_your_pi(
        input_pi=VALID_PI,
        correct_pi=VALID_PI,
        verbose=True,
    )
    assert error_count == 0


def test_color_your_pi_no_match() -> None:
    """Test color_your_pi with non-matching input."""
    error_count = pigame.color_your_pi(
        input_pi=VALID_PI,
        correct_pi="3.14158",
        verbose=True,
    )
    assert error_count == 1


def test_color_your_pi_colorblind() -> None:
    """Test color_your_pi with colorblind mode."""
    error_count = pigame.color_your_pi(
        input_pi=VALID_PI,
        correct_pi=VALID_PI,
        verbose=True,
        colorblind_mode=True,
    )
    assert error_count == 0


def test_handle_easter_egg_archimedes() -> None:
    """Test easter egg handling with 'Archimedes'."""
    assert pigame.handle_easter_egg("Archimedes") is True


def test_handle_easter_egg_pi() -> None:
    """Test easter egg handling with 'pi'."""
    assert pigame.handle_easter_egg("pi") is True
    assert pigame.handle_easter_egg("PI") is True


def test_handle_easter_egg_invalid() -> None:
    """Test easter egg handling with invalid input."""
    assert pigame.handle_easter_egg(VALID_PI) is False
