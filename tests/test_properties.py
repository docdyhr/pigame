#!/usr/bin/env python3
"""Property-based tests for pigame using hypothesis.

These tests verify mathematical correctness properties that should hold for
any valid input, complementing the example-based tests in test_pytest.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).parent.parent))
from src.python import pigame


# ---------------------------------------------------------------------------
# hypothesis import - skip entire module gracefully if not installed
# ---------------------------------------------------------------------------

try:
    from hypothesis import assume, given, settings, strategies as st

    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not HYPOTHESIS_AVAILABLE,
    reason="hypothesis not installed - run: pip install hypothesis",
)

# ---------------------------------------------------------------------------
# Shared strategies
# ---------------------------------------------------------------------------

# Valid decimal lengths for pi / constants
valid_pi_lengths = st.integers(min_value=1, max_value=100)

# Valid lengths for additional constants (≤ MAX_CONSTANT_LENGTH)
valid_constant_lengths = st.integers(min_value=1, max_value=pigame.MAX_CONSTANT_LENGTH)

# Strategy for constant names (excluding pi which has its own larger limit)
non_pi_constants = st.sampled_from(["e", "phi", "sqrt2"])

# Strategy for all constant names
all_constants = st.sampled_from(list(pigame.MATHEMATICAL_CONSTANTS.keys()))

# Strategy for digit-only strings of varying length
digit_strings = st.text(alphabet="0123456789", min_size=1, max_size=50)

# Strategy for pi-like strings (starts with "3.", followed by digits)
pi_like_strings = digit_strings.map(lambda s: f"3.{s}")


# ---------------------------------------------------------------------------
# Properties: calculate_pi
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
class TestCalculatePiProperties:
    """Property-based tests for calculate_pi."""

    @given(n=valid_pi_lengths)
    @settings(max_examples=200)
    def test_always_starts_with_3_dot(self, n: int) -> None:
        """calculate_pi(n) must always start with '3.'."""
        result = pigame.calculate_pi(n)
        assert result.startswith("3."), (
            f"calculate_pi({n}) = {result!r} does not start with '3.'"
        )

    @given(n=valid_pi_lengths)
    @settings(max_examples=200)
    def test_length_matches_request(self, n: int) -> None:
        """calculate_pi(n) must return exactly n decimal places plus '3.'."""
        result = pigame.calculate_pi(n)
        assert len(result) == n + 2, (
            f"calculate_pi({n}) returned {len(result)} chars, expected {n + 2}"
        )

    @given(n=valid_pi_lengths)
    @settings(max_examples=200)
    def test_decimal_part_contains_only_digits(self, n: int) -> None:
        """The decimal part of calculate_pi(n) must contain only digits."""
        result = pigame.calculate_pi(n)
        decimal_part = result[2:]  # strip "3."
        assert decimal_part.isdigit(), (
            f"Decimal part of calculate_pi({n}) contains non-digits: {decimal_part!r}"
        )

    @given(n=valid_pi_lengths)
    @settings(max_examples=200)
    def test_is_prefix_of_longer(self, n: int) -> None:
        """calculate_pi(n) must be a prefix of calculate_pi(n + 5)."""
        assume(n + 5 <= 100)
        short = pigame.calculate_pi(n)
        longer = pigame.calculate_pi(n + 5)
        assert longer.startswith(short), (
            f"calculate_pi({n}) = {short!r} is not a prefix of "
            f"calculate_pi({n + 5}) = {longer!r}"
        )

    def test_first_digits_are_correct(self) -> None:
        """Spot-check the first 20 known decimal digits of π."""
        result = pigame.calculate_pi(20)
        assert result == "3.14159265358979323846"

    @given(n=valid_pi_lengths)
    @settings(max_examples=50)
    def test_negative_raises_value_error(self, n: int) -> None:
        """calculate_pi with a negative number must raise ValueError."""
        with pytest.raises(ValueError, match="cannot be negative"):
            pigame.calculate_pi(-n)

    def test_zero_returns_default_length(self) -> None:
        """calculate_pi(0) must return the default number of decimal places."""
        result = pigame.calculate_pi(0)
        assert len(result) == pigame.DEFAULT_LENGTH + 2


# ---------------------------------------------------------------------------
# Properties: calculate_constant
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
class TestCalculateConstantProperties:
    """Property-based tests for calculate_constant."""

    @given(name=all_constants, n=valid_constant_lengths)
    @settings(max_examples=200)
    def test_length_matches_request(self, name: str, n: int) -> None:
        """calculate_constant(name, n) must return n decimal places."""
        assume(n <= (pigame.MAX_LENGTH if name == "pi" else pigame.MAX_CONSTANT_LENGTH))
        result = pigame.calculate_constant(name, n)
        assert len(result) == n + 2, (
            f"calculate_constant({name!r}, {n}) returned {len(result)} chars, "
            f"expected {n + 2}"
        )

    @given(name=all_constants, n=valid_constant_lengths)
    @settings(max_examples=200)
    def test_contains_dot(self, name: str, n: int) -> None:
        """calculate_constant must return a string with exactly one decimal point."""
        assume(n <= (pigame.MAX_LENGTH if name == "pi" else pigame.MAX_CONSTANT_LENGTH))
        result = pigame.calculate_constant(name, n)
        assert result.count(".") == 1

    @given(name=all_constants, n=valid_constant_lengths)
    @settings(max_examples=200)
    def test_decimal_part_is_digits_only(self, name: str, n: int) -> None:
        """The decimal part of calculate_constant must contain only digits."""
        assume(n <= (pigame.MAX_LENGTH if name == "pi" else pigame.MAX_CONSTANT_LENGTH))
        result = pigame.calculate_constant(name, n)
        decimal_part = result.split(".", 1)[1]
        assert decimal_part.isdigit(), (
            f"Non-digit chars in decimal part of {name}: {decimal_part!r}"
        )

    @given(name=all_constants, n=valid_constant_lengths)
    @settings(max_examples=100)
    def test_is_prefix_of_longer(self, name: str, n: int) -> None:
        """calculate_constant(name, n) must be a prefix of
        calculate_constant(name, n+1).
        """
        max_len = pigame.MAX_LENGTH if name == "pi" else pigame.MAX_CONSTANT_LENGTH
        assume(n + 1 <= max_len)
        short = pigame.calculate_constant(name, n)
        longer = pigame.calculate_constant(name, n + 1)
        assert longer.startswith(short), (
            f"calculate_constant({name!r}, {n}) = {short!r} is not a prefix of "
            f"calculate_constant({name!r}, {n + 1}) = {longer!r}"
        )

    @given(name=non_pi_constants)
    @settings(max_examples=50)
    def test_too_many_digits_raises(self, name: str) -> None:
        """Requesting more digits than available must raise TooManyDigitsError."""
        with pytest.raises(pigame.TooManyDigitsError):
            pigame.calculate_constant(name, pigame.MAX_CONSTANT_LENGTH + 1)

    @given(name=all_constants)
    @settings(max_examples=20)
    def test_negative_length_raises(self, name: str) -> None:
        """Negative length must raise ValueError."""
        with pytest.raises(ValueError, match="cannot be negative"):
            pigame.calculate_constant(name, -1)

    @given(
        name=st.text(min_size=1, max_size=10).filter(
            lambda s: s not in pigame.MATHEMATICAL_CONSTANTS
        )
    )
    @settings(max_examples=50)
    def test_unknown_constant_raises(self, name: str) -> None:
        """An unrecognised constant name must raise ValueError."""
        with pytest.raises(ValueError, match="Unknown constant"):
            pigame.calculate_constant(name, 5)

    def test_known_digits_e(self) -> None:
        """First 20 decimal digits of e must be correct."""
        result = pigame.calculate_constant("e", 20)
        assert result == "2.71828182845904523536"

    def test_known_digits_phi(self) -> None:
        """First 20 decimal digits of φ must be correct."""
        result = pigame.calculate_constant("phi", 20)
        assert result == "1.61803398874989484820"

    def test_known_digits_sqrt2(self) -> None:
        """First 20 decimal digits of √2 must be correct."""
        result = pigame.calculate_constant("sqrt2", 20)
        assert result == "1.41421356237309504880"


# ---------------------------------------------------------------------------
# Properties: format_pi_with_spaces
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
class TestFormatPiWithSpacesProperties:
    """Property-based tests for format_pi_with_spaces."""

    @given(digits=digit_strings)
    @settings(max_examples=300)
    def test_digit_content_preserved(self, digits: str) -> None:
        """Removing spaces from formatted output must equal the input string."""
        pi_str = f"3.{digits}"
        formatted = pigame.format_pi_with_spaces(pi_str)
        assert formatted.replace(" ", "") == pi_str, (
            f"Digit content changed: {pi_str!r} → {formatted!r}"
        )

    @given(digits=digit_strings)
    @settings(max_examples=300)
    def test_starts_with_integer_part(self, digits: str) -> None:
        """Formatted output must preserve the '3.' prefix."""
        pi_str = f"3.{digits}"
        formatted = pigame.format_pi_with_spaces(pi_str)
        assert formatted.startswith("3.")

    @given(digits=digit_strings)
    @settings(max_examples=300)
    def test_spaces_at_correct_positions(self, digits: str) -> None:
        """Spaces must appear only at multiples of 5 digits after the decimal point."""
        pi_str = f"3.{digits}"
        formatted = pigame.format_pi_with_spaces(pi_str)
        # Strip the "3." prefix, then check space placement
        after_dot = formatted[2:]
        digit_index = 0
        for char in after_dot:
            if char == " ":
                # A space must occur at digit index that is a multiple of 5
                assert digit_index % 5 == 0, (
                    f"Unexpected space at digit position {digit_index} in {formatted!r}"
                )
            else:
                digit_index += 1

    @given(n=st.integers(min_value=1, max_value=30))
    @settings(max_examples=100)
    def test_idempotent_on_pi(self, n: int) -> None:
        """format_pi_with_spaces composed with replace(' ', '') must be identity."""
        pi = pigame.calculate_pi(n)
        formatted = pigame.format_pi_with_spaces(pi)
        restored = formatted.replace(" ", "")
        assert restored == pi

    def test_short_pi_no_space(self) -> None:
        """Strings ≤ 7 chars (≤ 5 decimal digits) must not contain spaces."""
        result = pigame.format_pi_with_spaces("3.14159")
        assert " " not in result

    def test_six_decimal_digits_has_one_space(self) -> None:
        """A 6-decimal-digit string must contain exactly one space."""
        result = pigame.format_pi_with_spaces("3.141592")
        assert result.count(" ") == 1

    def test_eleven_decimal_digits_has_two_spaces(self) -> None:
        """An 11-decimal-digit string must contain exactly two spaces."""
        result = pigame.format_pi_with_spaces("3.14159265358")
        assert result.count(" ") == 2


# ---------------------------------------------------------------------------
# Properties: input_validation
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
class TestInputValidationProperties:
    """Property-based tests for input_validation."""

    @given(digits=digit_strings)
    @settings(max_examples=300)
    def test_pure_digit_string_is_valid(self, digits: str) -> None:
        """Any non-empty string of digits is valid input."""
        assert pigame.input_validation(digits) is True

    @given(s=pi_like_strings)
    @settings(max_examples=300)
    def test_pi_like_string_is_valid(self, s: str) -> None:
        """Any '3.NNNN' style string must pass validation."""
        assert pigame.input_validation(s) is True

    @given(
        s=st.text(
            alphabet=st.characters(
                blacklist_categories=("Nd",),  # exclude decimal digits
                blacklist_characters=".",
            ),
            min_size=1,
            max_size=20,
        )
    )
    @settings(max_examples=200)
    def test_string_with_non_digits_raises(self, s: str) -> None:
        """Any string containing non-digit, non-dot characters must be rejected."""
        assume(any(not c.isdigit() and c != "." for c in s))
        with pytest.raises(ValueError, match="Invalid input"):
            pigame.input_validation(s)

    def test_empty_string_raises(self) -> None:
        """Empty string must raise ValueError."""
        with pytest.raises(ValueError, match="Invalid input"):
            pigame.input_validation("")

    @given(
        a=digit_strings,
        b=digit_strings,
        c=digit_strings,
    )
    @settings(max_examples=100)
    def test_multiple_dots_raises(self, a: str, b: str, c: str) -> None:
        """A string with two decimal points must be rejected."""
        s = f"{a}.{b}.{c}"
        with pytest.raises(ValueError, match="Invalid input"):
            pigame.input_validation(s)

    @given(s=st.text(alphabet="0123456789,", min_size=1, max_size=20))
    @settings(max_examples=100)
    def test_comma_raises(self, s: str) -> None:
        """Any string containing a comma must be rejected."""
        assume("," in s)
        with pytest.raises(ValueError, match="Invalid input"):
            pigame.input_validation(s)


# ---------------------------------------------------------------------------
# Properties: color_your_pi
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
class TestColorYourPiProperties:
    """Property-based tests for color_your_pi."""

    @given(n=valid_pi_lengths)
    @settings(max_examples=200)
    def test_exact_match_gives_zero_errors(self, n: int) -> None:
        """Comparing a pi string to itself must always give 0 errors."""
        pi = pigame.calculate_pi(n)
        errors = pigame.color_your_pi(
            input_pi=pi,
            correct_pi=pi,
            verbose=False,
        )
        assert errors == 0, (
            f"Expected 0 errors when comparing pi to itself, got {errors}"
        )

    @given(n=valid_pi_lengths)
    @settings(max_examples=200)
    def test_exact_match_colorblind_gives_zero_errors(self, n: int) -> None:
        """Colorblind mode must also give 0 errors for an exact match."""
        pi = pigame.calculate_pi(n)
        errors = pigame.color_your_pi(
            input_pi=pi,
            correct_pi=pi,
            verbose=False,
            colorblind_mode=True,
        )
        assert errors == 0

    @given(n=valid_pi_lengths)
    @settings(max_examples=100)
    def test_error_count_non_negative(self, n: int) -> None:
        """Error count must always be ≥ 0."""
        pi = pigame.calculate_pi(n)
        # Construct a subtly wrong pi by replacing the last digit
        wrong = pi[:-1] + ("0" if pi[-1] != "0" else "1")
        errors = pigame.color_your_pi(
            input_pi=wrong,
            correct_pi=pi,
            verbose=False,
        )
        assert errors >= 0

    @given(n=st.integers(min_value=5, max_value=50))
    @settings(max_examples=100)
    def test_single_wrong_digit_gives_at_least_one_error(self, n: int) -> None:
        """Changing one digit must give ≥ 1 error."""
        pi = pigame.calculate_pi(n)
        # Flip the last decimal digit
        wrong_last = "0" if pi[-1] != "0" else "1"
        wrong = pi[:-1] + wrong_last
        errors = pigame.color_your_pi(
            input_pi=wrong,
            correct_pi=pi,
            verbose=False,
        )
        assert errors >= 1, (
            f"Expected ≥ 1 error for wrong pi {wrong!r} vs correct {pi!r}, got {errors}"
        )

    @given(n=valid_pi_lengths)
    @settings(max_examples=100)
    def test_prefix_errors_never_exceed_length(self, n: int) -> None:
        """Error count must never exceed the length of the input string."""
        pi = pigame.calculate_pi(n)
        # All-zeros "pi" - every decimal digit will be wrong (except the rare match)
        fake_pi = "3." + "0" * n
        errors = pigame.color_your_pi(
            input_pi=fake_pi,
            correct_pi=pi,
            verbose=False,
        )
        assert errors <= len(fake_pi), (
            f"Error count {errors} exceeds string length {len(fake_pi)}"
        )


# ---------------------------------------------------------------------------
# Properties: length_validation
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
class TestLengthValidationProperties:
    """Property-based tests for length_validation."""

    @given(n=st.integers(min_value=1, max_value=pigame.MAX_LENGTH))
    @settings(max_examples=200)
    def test_valid_integers_round_trip(self, n: int) -> None:
        """length_validation(str(n)) must return n for valid positive integers."""
        result = pigame.length_validation(str(n))
        assert result == n

    @given(
        n=st.integers(
            min_value=pigame.MAX_LENGTH + 1, max_value=pigame.MAX_LENGTH + 1000
        )
    )
    @settings(max_examples=50)
    def test_too_large_exits(self, n: int) -> None:
        """length_validation must exit for values > MAX_LENGTH."""
        with pytest.raises(SystemExit):
            pigame.length_validation(str(n))

    @given(
        s=st.text(
            alphabet=st.characters(
                blacklist_categories=("Nd",), blacklist_characters="-"
            ),
            min_size=1,
            max_size=10,
        )
    )
    @settings(max_examples=100)
    def test_non_integer_strings_raise(self, s: str) -> None:
        """Non-integer strings must raise ValueError."""
        assume(not s.lstrip("-").isdigit())
        with pytest.raises(ValueError, match="Invalid input"):
            pigame.length_validation(s)

    @given(n=st.integers(min_value=1, max_value=1000))
    @settings(max_examples=50)
    def test_negative_returns_default(self, n: int) -> None:
        """Negative lengths must return DEFAULT_LENGTH."""
        result = pigame.length_validation(str(-n))
        assert result == pigame.DEFAULT_LENGTH

    def test_zero_returns_default(self) -> None:
        """Zero must return DEFAULT_LENGTH."""
        result = pigame.length_validation("0")
        assert result == pigame.DEFAULT_LENGTH
