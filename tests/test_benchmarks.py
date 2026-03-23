#!/usr/bin/env python3
"""Performance benchmarks for pigame core functions.

Run with:
    pytest tests/test_benchmarks.py --benchmark-only
    pytest tests/test_benchmarks.py --benchmark-only --benchmark-sort=mean
    pytest tests/test_benchmarks.py --benchmark-only \
        --benchmark-json=.benchmarks/results.json
"""

from __future__ import annotations

import contextlib
import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).parent.parent))
from src.python import pigame


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

PI_5 = pigame.calculate_pi(5)
PI_50 = pigame.calculate_pi(50)
PI_500 = pigame.calculate_pi(500)

WRONG_PI_5 = "3.14158"  # one digit off
WRONG_PI_50 = PI_50[:-1] + ("0" if PI_50[-1] != "0" else "1")
WRONG_PI_500 = PI_500[:-1] + ("0" if PI_500[-1] != "0" else "1")

# Maximum digits available in the hardcoded pi_digits string (~507).
# Using 500 keeps us safely within the available range.
MAX_PI_BENCH = 500


# ---------------------------------------------------------------------------
# calculate_pi  -lookup speed at various precisions
# ---------------------------------------------------------------------------


class TestBenchmarkCalculatePi:
    """Benchmarks for calculate_pi at increasing precision levels."""

    def test_calculate_pi_5(self, benchmark) -> None:
        """calculate_pi at 5 decimal places."""
        benchmark(pigame.calculate_pi, 5)

    def test_calculate_pi_50(self, benchmark) -> None:
        """calculate_pi at 50 decimal places."""
        benchmark(pigame.calculate_pi, 50)

    def test_calculate_pi_500_exact(self, benchmark) -> None:
        """calculate_pi at exactly 500 decimal places."""
        benchmark(pigame.calculate_pi, 500)

    def test_calculate_pi_500_max(self, benchmark) -> None:
        """calculate_pi at 500 decimal places (near the available digit limit)."""
        benchmark(pigame.calculate_pi, MAX_PI_BENCH)


# ---------------------------------------------------------------------------
# calculate_constant  -lookup speed for each constant
# ---------------------------------------------------------------------------


class TestBenchmarkCalculateConstant:
    """Benchmarks for calculate_constant across all supported constants."""

    @pytest.mark.parametrize("name", ["pi", "e", "phi", "sqrt2"])
    def test_calculate_constant_10(self, benchmark, name: str) -> None:
        """calculate_constant at 10 decimal places."""
        max_len = pigame.MAX_LENGTH if name == "pi" else pigame.MAX_CONSTANT_LENGTH
        length = min(10, max_len)
        benchmark(pigame.calculate_constant, name, length)

    @pytest.mark.parametrize("name", ["pi", "e", "phi", "sqrt2"])
    def test_calculate_constant_100(self, benchmark, name: str) -> None:
        """calculate_constant at 100 decimal places."""
        max_len = pigame.MAX_LENGTH if name == "pi" else pigame.MAX_CONSTANT_LENGTH
        length = min(100, max_len)
        benchmark(pigame.calculate_constant, name, length)

    @pytest.mark.parametrize("name", ["e", "phi", "sqrt2"])
    def test_calculate_constant_max(self, benchmark, name: str) -> None:
        """calculate_constant at the maximum available precision for each constant."""
        benchmark(pigame.calculate_constant, name, pigame.MAX_CONSTANT_LENGTH)


# ---------------------------------------------------------------------------
# format_pi_with_spaces  -formatting speed
# ---------------------------------------------------------------------------


class TestBenchmarkFormatPiWithSpaces:
    """Benchmarks for the digit-spacing formatter at various string lengths."""

    def test_format_short(self, benchmark) -> None:
        """Format a 5-decimal pi string (no spaces expected)."""
        benchmark(pigame.format_pi_with_spaces, PI_5)

    def test_format_medium(self, benchmark) -> None:
        """Format a 50-decimal pi string."""
        benchmark(pigame.format_pi_with_spaces, PI_50)

    def test_format_long(self, benchmark) -> None:
        """Format a 500-decimal pi string."""
        benchmark(pigame.format_pi_with_spaces, PI_500)

    def test_format_maximum(self, benchmark) -> None:
        """Format a 500-decimal pi string (near the available digit limit)."""
        benchmark(pigame.format_pi_with_spaces, PI_500)


# ---------------------------------------------------------------------------
# input_validation  -validation speed
# ---------------------------------------------------------------------------


class TestBenchmarkInputValidation:
    """Benchmarks for input_validation with valid and invalid inputs."""

    def test_valid_short(self, benchmark) -> None:
        """Validate a short valid pi string."""
        benchmark(pigame.input_validation, "3.14159")

    def test_valid_long(self, benchmark) -> None:
        """Validate a long valid pi string."""
        benchmark(pigame.input_validation, PI_500)

    def test_invalid_alpha(self, benchmark) -> None:
        """Validate (and reject) an alphabetic string."""

        def _validate_raises() -> None:
            with contextlib.suppress(ValueError):
                pigame.input_validation("notanumber")

        benchmark(_validate_raises)

    def test_invalid_comma(self, benchmark) -> None:
        """Validate (and reject) a string with a comma separator."""

        def _validate_raises() -> None:
            with contextlib.suppress(ValueError):
                pigame.input_validation("3,14159")

        benchmark(_validate_raises)


# ---------------------------------------------------------------------------
# color_your_pi  -digit-comparison speed
# ---------------------------------------------------------------------------


class TestBenchmarkColorYourPi:
    """Benchmarks for the colorised digit-comparison routine."""

    def test_compare_correct_5(self, benchmark) -> None:
        """Compare a correct 5-digit pi (0 errors)."""
        benchmark(
            pigame.color_your_pi,
            input_pi=PI_5,
            correct_pi=PI_5,
            verbose=False,
        )

    def test_compare_wrong_5(self, benchmark) -> None:
        """Compare a 5-digit pi with one error."""
        benchmark(
            pigame.color_your_pi,
            input_pi=WRONG_PI_5,
            correct_pi=PI_5,
            verbose=False,
        )

    def test_compare_correct_50(self, benchmark) -> None:
        """Compare a correct 50-digit pi (0 errors)."""
        benchmark(
            pigame.color_your_pi,
            input_pi=PI_50,
            correct_pi=PI_50,
            verbose=False,
        )

    def test_compare_wrong_50(self, benchmark) -> None:
        """Compare a 50-digit pi with one error."""
        benchmark(
            pigame.color_your_pi,
            input_pi=WRONG_PI_50,
            correct_pi=PI_50,
            verbose=False,
        )

    def test_compare_correct_500(self, benchmark) -> None:
        """Compare a correct 500-digit pi (0 errors)."""
        benchmark(
            pigame.color_your_pi,
            input_pi=PI_500,
            correct_pi=PI_500,
            verbose=False,
        )

    def test_compare_wrong_500(self, benchmark) -> None:
        """Compare a 500-digit pi with one error."""
        benchmark(
            pigame.color_your_pi,
            input_pi=WRONG_PI_500,
            correct_pi=PI_500,
            verbose=False,
        )

    def test_compare_correct_500_colorblind(self, benchmark) -> None:
        """Compare a correct 500-digit pi in color-blind mode."""
        benchmark(
            pigame.color_your_pi,
            input_pi=PI_500,
            correct_pi=PI_500,
            verbose=False,
            colorblind_mode=True,
        )


# ---------------------------------------------------------------------------
# End-to-end round-trip  -full pipeline for a single comparison
# ---------------------------------------------------------------------------


class TestBenchmarkRoundTrip:
    """Benchmarks for a full validate → calculate → compare pipeline."""

    def _round_trip(self, user_input: str) -> int:
        """Run the full comparison pipeline and return the error count."""
        pigame.input_validation(user_input)
        decimals = len(user_input) - 2
        correct = pigame.calculate_pi(decimals)
        return pigame.color_your_pi(
            input_pi=user_input,
            correct_pi=correct,
            verbose=False,
        )

    def test_round_trip_correct_5(self, benchmark) -> None:
        """Full round-trip: validate + calculate + compare 5 correct digits."""
        result = benchmark(self._round_trip, PI_5)
        assert result == 0

    def test_round_trip_wrong_5(self, benchmark) -> None:
        """Full round-trip: validate + calculate + compare 5 digits with 1 error."""
        result = benchmark(self._round_trip, WRONG_PI_5)
        assert result >= 1

    def test_round_trip_correct_50(self, benchmark) -> None:
        """Full round-trip: validate + calculate + compare 50 correct digits."""
        result = benchmark(self._round_trip, PI_50)
        assert result == 0

    def test_round_trip_correct_500(self, benchmark) -> None:
        """Full round-trip: validate + calculate + compare 500 correct digits."""
        result = benchmark(self._round_trip, PI_500)
        assert result == 0

    def test_round_trip_correct_500_colorblind(self, benchmark) -> None:
        """Full round-trip in color-blind mode with 500 correct digits."""

        def _round_trip_cb() -> int:
            pigame.input_validation(PI_500)
            decimals = len(PI_500) - 2
            correct = pigame.calculate_pi(decimals)
            return pigame.color_your_pi(
                input_pi=PI_500,
                correct_pi=correct,
                verbose=False,
                colorblind_mode=True,
            )

        result = benchmark(_round_trip_cb)
        assert result == 0
