#!/usr/bin/env python3
"""PIGAME - Test your memory of π digits.

Python implementation using verified digits from trusted mathematical sources
for perfect accuracy and consistent results across all implementations.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import NoReturn

# Constants
MIN_PI_LENGTH = 3
SHORT_PI_LENGTH = 15
DEFAULT_LENGTH = SHORT_PI_LENGTH
MAX_LENGTH = 5001
MIN_DIGITS_WITH_POINT = 3
PERFECT_SCORE_THRESHOLD = 15

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ANSI color codes
red = "\033[0;31m"
underline = "\033[4m"
no_color = "\033[0m"


class PiError(Exception):
    """Base class for Pi-related exceptions."""

    def __init__(self, msg: str) -> None:
        """Initialize the base Pi error.

        Args:
            msg: The error message to display.
        """
        self.msg = msg
        super().__init__(self.msg)


class NegativeLengthError(PiError):
    """Raised when a negative length is provided."""

    def __init__(self, length: int) -> None:
        """Initialize negative length error.

        Args:
            length: The negative length that caused the error.
        """
        super().__init__(f"Length {length} cannot be negative")


class TooManyDigitsError(PiError):
    """Raised when more digits are requested than available."""

    def __init__(self, requested: int, available: int) -> None:
        """Initialize too many digits error.

        Args:
            requested: The number of digits requested.
            available: The number of digits available.
        """
        super().__init__(
            f"Requested {requested} digits but only {available} are available",
        )


def get_version() -> str:
    """Read version from VERSION file or return default version."""
    try:
        version_file = Path(__file__).parent.parent / "VERSION"
        return version_file.read_text(encoding="utf-8").strip()
    except OSError:
        return "1.7.0"  # Default version


VERSION = get_version()


def usage(exit_code: int = 1) -> NoReturn:
    """Print usage information and exit."""
    program = Path(sys.argv[0]).name
    logger.error("Usage: %s [-v] [-p LENGTH] [-V] [-c] YOUR_PI", program)
    logger.error("\tEvaluate your version of π (3.141.. )")
    logger.error("\t-v          Increase verbosity.")
    logger.error("\t-p LENGTH   Calculate and show π with LENGTH number of decimals.")
    logger.error("\t-V          Version.")
    logger.error("\t-c          Color-blind mode (use underscores instead of color).")
    sys.exit(exit_code)


def input_validation(input_str: str) -> bool:
    """Validate that input contains only digits and at most one decimal point."""
    if not input_str:
        raise ValueError("Invalid input")
    dot_count = input_str.count('.')
    comma_count = input_str.count(',')

    if comma_count > 0:
        raise ValueError("Invalid input")

    if not all(c.isdigit() or c == '.' for c in input_str):
        raise ValueError("Invalid input")

    if dot_count > 1:
        raise ValueError("Invalid input")

    return True


def length_validation(length_str: str) -> int:
    """Validate the length input and return the validated length.

    Args:
        length_str: The length string to validate

    Returns:
        int: The validated length

    Raises:
        ValueError: If input is not a valid integer
        SystemExit: If length is too large
    """
    if not re.match(r"^-?[0-9]+$", length_str):
        raise ValueError("Invalid input")

    length = int(length_str)

    if length <= 0:
        return DEFAULT_LENGTH
    if length > MAX_LENGTH:
        sys.exit("too big")  # This exits the program

    return length


def calculate_pi(length: int) -> str:
    """Return pi digits from a verified source."""
    # Verified digits of π from a trusted source
    pi_digits = (
        "141592653589793238462643383279502884197169399375105820974944592307816406286"
        "208998628034825342117067982148086513282306647093844609550582231725359408128"
        "481117450284102701938521105559644622948954930381964428810975665933446128475"
        "648233786783165271201909145648566923460348610454326648213393607260249141273"
        "724587006606315588174881520920962829254091715364367892590360011330530548820"
        "466521384146951941511609433057270365759591953092186117381932611793105118548"
        "074462379962749567351885752724891227938183011949129833673362440656643"
    )

    # Check for negative length
    if length < 0:
        raise ValueError("Length cannot be negative")

    # For zero length, use default length
    if length == 0:
        length = DEFAULT_LENGTH

    # Return exactly the requested number of digits
    digits = pi_digits[:length]
    if len(digits) < length:
        raise TooManyDigitsError(length, len(digits))

    # Return "3." + digits
    return f"3.{digits}"


def format_pi_with_spaces(pi_str: str) -> str:
    """Format pi with spaces every 5 digits for better readability."""
    # Start with the first 2 characters "3."
    result = pi_str[:2]

    # Add the rest with spaces every 5 digits
    for i, digit in enumerate(pi_str[2:]):
        # Add space after every 5 digits
        if i > 0 and i % 5 == 0:
            result += " "
        result += digit

    return result


def color_your_pi(input_pi: str, correct_pi: str, *, verbose: bool = False, colorblind_mode: bool = False) -> int:
    """Compare input pi digits with correct pi digits and colorize differences.

    Args:
        input_pi: Input pi digits to check
        correct_pi: Correct pi digits to compare against
        verbose: Whether to show verbose output
        colorblind_mode: Whether to use colorblind-friendly colors

    Returns:
        Number of incorrect digits found
    """
    error_count = 0
    for input_digit, correct_digit in zip(input_pi, correct_pi):
        if input_digit != correct_digit:
            error_count += 1
            if colorblind_mode:
                print(f"\033[38;5;208m{input_digit}\033[0m", end='')  # Orange for colorblind
            else:
                print(f"\033[91m{input_digit}\033[0m", end='')  # Red for incorrect
        else:
            if colorblind_mode:
                print(f"\033[38;5;34m{input_digit}\033[0m", end='')  # Green for colorblind
            else:
                print(f"\033[92m{input_digit}\033[0m", end='')  # Green for correct
    print()

    if verbose:
        print(f"Found {error_count} incorrect digits")

    return error_count


def print_results(
    *,
    user_pi: str,
    calculated_pi: str,
    decimals: int,
    verbose: bool = False,
    colorblind_mode: bool = False,
) -> None:
    """Print the results of comparing user's pi with calculated pi."""
    # Format pi with spaces for better readability
    formatted_pi = format_pi_with_spaces(calculated_pi)

    if verbose:
        print(f"π with {decimals} decimals:\t{formatted_pi}")
        print("Your version of π:\t", end="")

    color_your_pi(
        input_pi=user_pi,
        correct_pi=calculated_pi,
        verbose=verbose,
        colorblind_mode=colorblind_mode,
    )

    if calculated_pi == user_pi:
        if verbose:
            if decimals < PERFECT_SCORE_THRESHOLD:
                print("Well done.")
            else:
                print("Perfect!")
        else:
            print("Match")
    elif verbose:
        print("You can do better!")
    else:
        print("No match")


def handle_easter_egg(input_str: str) -> bool:
    """Handle easter egg inputs like 'Archimedes' or 'pi'."""
    if input_str in ["Archimedes", "pi", "PI"]:
        print("π is also called Archimedes constant and is commonly defined as")
        print("the ratio of a circles circumference C to its diameter d:")
        print("π = C / d")
        return True
    return False


def main() -> None:
    """Parse command line arguments and perform calculations."""
    parser = argparse.ArgumentParser(
        description="Evaluate your version of π (3.141..)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-v", action="store_true", help="Increase verbosity.")
    parser.add_argument(
        "-p",
        type=str,
        help="Calculate and show π with LENGTH number of decimals.",
    )
    parser.add_argument("-V", action="store_true", help="Version.")
    parser.add_argument(
        "-c",
        action="store_true",
        help="Color-blind mode (use underscores instead of color).",
    )
    parser.add_argument("YOUR_PI", nargs="?", type=str, help="Your version of π")

    try:
        args = parser.parse_args()
    except (argparse.ArgumentError, SystemExit):
        usage(0)

    if args.V:
        print(f"version: {VERSION}")
        sys.exit(0)

    if not args.YOUR_PI and not args.p and not args.v and not args.c:
        usage(0)

    # Handle the -p option
    if args.p:
        length = length_validation(args.p)
        calculated_pi = calculate_pi(length)
        formatted_pi = format_pi_with_spaces(calculated_pi)

        if args.v:
            print(f"π with {length} decimals:\t{formatted_pi}")
        else:
            print(formatted_pi)

        # If no user pi is provided, exit after displaying
        if not args.YOUR_PI:
            sys.exit(0)
    else:
        length = DEFAULT_LENGTH

    # Handle YOUR_PI argument
    if args.YOUR_PI:
        # Check for easter eggs
        if handle_easter_egg(args.YOUR_PI):
            sys.exit(0)

        # Validate input
        try:
            input_validation(args.YOUR_PI)
        except ValueError as e:
            logger.error("pigame error: %s", e)
            sys.exit(1)
        user_pi = args.YOUR_PI

        # If -p was not provided, determine length from user_pi
        if not args.p:
            # Number of decimals is length - 2 (for "3.")
            decimals = (
                len(user_pi) - 2
                if len(user_pi) >= MIN_DIGITS_WITH_POINT
                else len(user_pi)
            )
            calculated_pi = calculate_pi(decimals)
        else:
            decimals = length
            calculated_pi = calculate_pi(decimals)

        print_results(
            user_pi=user_pi,
            calculated_pi=calculated_pi,
            decimals=decimals,
            verbose=args.v,
            colorblind_mode=args.c,
        )


if __name__ == "__main__":
    main()
