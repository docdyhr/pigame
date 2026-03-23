#!/usr/bin/env python3
"""PIGAME - Test your memory of π digits.

Python implementation using verified digits from trusted mathematical sources
for perfect accuracy and consistent results across all implementations.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import termios
import time
import tty
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn


# Constants
MIN_PI_LENGTH = 3
SHORT_PI_LENGTH = 15
DEFAULT_LENGTH = SHORT_PI_LENGTH
MAX_LENGTH = 5001
MIN_DIGITS_WITH_POINT = 3
PERFECT_SCORE_THRESHOLD = 15
PRACTICE_CONFIG_DIR = Path.home() / ".pigame"
PRACTICE_STATS_FILE = PRACTICE_CONFIG_DIR / "stats.json"
PRACTICE_CONFIG_FILE = PRACTICE_CONFIG_DIR / "config.json"
PRACTICE_MIN_DIGITS = 5
PRACTICE_MAX_DIGITS = 100

# Practice mode constants
PRACTICE_MODES = ["standard", "timed", "chunk"]
DEFAULT_PRACTICE_MODE = "standard"
DEFAULT_CHUNK_SIZE = 5
DEFAULT_TIME_LIMIT = 180  # 3 minutes

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
# Format matches the Bash and C implementations: [LEVEL] pigame: <message>
# Default level: WARNING (only warnings and errors are shown).
# Enable DEBUG output with --debug flag or PIGAME_DEBUG=1 env var.
# ---------------------------------------------------------------------------

import os as _os  # noqa: E402 - used only for env-var check below


logger = logging.getLogger(__name__)
_log_handler = logging.StreamHandler(sys.stderr)
_log_handler.setFormatter(logging.Formatter("[%(levelname)s] pigame: %(message)s"))
logger.addHandler(_log_handler)

# Honour PIGAME_DEBUG env-var so that debug output is available even when the
# --debug flag cannot be parsed yet (e.g. during module import in tests).
if _os.environ.get("PIGAME_DEBUG"):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARNING)

del _os  # keep module namespace clean

# ANSI color codes
red = "\033[0;31m"
underline = "\033[4m"
no_color = "\033[0m"


class PiError(Exception):
    """Base class for Pi-related exceptions."""

    def __init__(self: PiError, msg: str) -> None:
        """Initialize the base Pi error.

        Args:
            msg: The error message to display.
        """
        super().__init__(msg)


class NegativeLengthError(PiError):
    """Raised when a negative length is provided."""

    def __init__(self: NegativeLengthError, length: int) -> None:
        """Initialize negative length error.

        Args:
            length: The negative length that caused the error.
        """
        msg = f"Length {length} cannot be negative"
        super().__init__(msg)


class TooManyDigitsError(PiError):
    """Raised when more digits are requested than available."""

    def __init__(self: TooManyDigitsError, requested: int, available: int) -> None:
        """Initialize too many digits error.

        Args:
            requested: The number of digits requested.
            available: The number of digits available.
        """
        msg = f"Requested {requested} digits but only {available} are available"
        super().__init__(msg)


def get_version() -> str:
    """Read version from VERSION file or return default version."""
    try:
        version_file = Path(__file__).parent.parent / "VERSION"
        return version_file.read_text(encoding="utf-8").strip()
    except OSError:
        return "0.0.0"


VERSION = get_version()


def usage(exit_code: int = 1) -> NoReturn:
    """Print usage information and exit."""
    program = Path(sys.argv[0]).name
    print(f"Usage: {program} [-v] [-p LENGTH] [-V] [-c] YOUR_PI")
    print("\tEvaluate your version of π (3.141.. )")
    print("\t-v          Increase verbosity.")
    print("\t-p LENGTH   Calculate and show π with LENGTH number of decimals.")
    print("\t-V          Version.")
    print("\t-c          Color-blind mode (use underscores instead of color).")
    sys.exit(exit_code)


def input_validation(input_str: str) -> bool:
    """Validate that input contains only digits and at most one decimal point."""
    logger.debug("input_validation: checking %r", input_str)

    if not input_str:
        msg = "Invalid input"
        raise ValueError(msg)

    dot_count = input_str.count(".")
    comma_count = input_str.count(",")

    if comma_count > 0:
        logger.debug("input_validation: comma found in %r", input_str)
        msg = "Invalid input"
        raise ValueError(msg)

    if not all(c.isdigit() or c == "." for c in input_str):
        logger.debug("input_validation: non-digit character in %r", input_str)
        msg = "Invalid input"
        raise ValueError(msg)

    if dot_count > 1:
        logger.debug("input_validation: %d decimal points in %r", dot_count, input_str)
        msg = "Invalid input"
        raise ValueError(msg)

    logger.debug("input_validation: %r OK", input_str)
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
    logger.debug("length_validation: checking %r", length_str)

    if not re.match(r"^-?[0-9]+$", length_str):
        logger.debug("length_validation: %r is not an integer", length_str)
        msg = "Invalid input"
        raise ValueError(msg)

    length = int(length_str)

    if length <= 0:
        logger.debug(
            "length_validation: %d <= 0, returning default %d", length, DEFAULT_LENGTH
        )
        return DEFAULT_LENGTH

    if length > MAX_LENGTH:
        logger.warning("length_validation: %d exceeds maximum %d", length, MAX_LENGTH)
        msg = "too big"
        sys.exit(msg)  # This exits the program

    logger.debug("length_validation: %d OK", length)
    return length


def calculate_pi(length: int) -> str:
    """Return pi digits from a verified source."""
    logger.debug("calculate_pi: requesting %d decimal digit(s)", length)
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
        msg = "Length cannot be negative"
        raise ValueError(msg)

    # For zero length, use default length
    if length == 0:
        length = DEFAULT_LENGTH

    # Return exactly the requested number of digits
    digits = pi_digits[:length]
    if len(digits) < length:
        msg = f"Requested {length} digits but only {len(digits)} are available"
        raise TooManyDigitsError(length, len(digits))

    # Return "3." + digits
    result = f"3.{digits}"
    logger.debug("calculate_pi: returning %r…", result[:14])
    return result


# ---------------------------------------------------------------------------
# Mathematical constants - verified high-precision digit strings
# ---------------------------------------------------------------------------

# Maximum number of digits available for each non-π constant
MAX_CONSTANT_LENGTH = 500

# Verified decimal digits (after the integer part and decimal point) for each
# supported mathematical constant.  Sources: OEIS A001113 (e), A001622 (φ),
# A002193 (√2).
_CONSTANT_DIGIT_STRINGS: dict[str, str] = {
    "pi": (
        "141592653589793238462643383279502884197169399375105820974944592307816406286"
        "208998628034825342117067982148086513282306647093844609550582231725359408128"
        "481117450284102701938521105559644622948954930381964428810975665933446128475"
        "648233786783165271201909145648566923460348610454326648213393607260249141273"
        "724587006606315588174881520920962829254091715364367892590360011330530548820"
        "466521384146951941511609433057270365759591953092186117381932611793105118548"
        "074462379962749567351885752724891227938183011949129833673362440656643"
    ),
    # e = 2.71828… (OEIS A001113)
    "e": (
        "71828182845904523536028747135266249775724709369995"
        "95749669676277240766303535475945713821785251664274"
        "27466391932003059921817413596629043572900334295260"
        "59563073813232862794349076323382988075319525101901"
        "15738341879307021540891499348841675092447614606680"
        "82264800168477411853742345442437107539077744992069"
        "55170276183860626133138458300075204493382656029760"
        "67371132007093287091274437470472306969772093101416"
        "92836819025515108657463772111252389784425056953696"
        "77078544996996794686445490598793163688923009879312"
    ),
    # φ = 1.61803… (OEIS A001622)
    "phi": (
        "61803398874989484820458683436563811772030917980576"
        "28621354486227052604628189024497072072041893911374"
        "84754088075386891752126633862223536931793180060715"
        "60791243189776704376718038552847207897028684278325"
        "23905430285673960400617854062296730597638073640786"
        "80917173144627838350073548994081639751941814101989"
        "26527384088034049098793280793052263870384985490299"
        "62924420438492428760547231098498621166130572678655"
        "78671005507209492905578064067901989451867527979441"
        "88782782898249522765424340088432036624084066985164"
    ),
    # √2 = 1.41421… (OEIS A002193)
    "sqrt2": (
        "41421356237309504880168872420969807856967187537694"
        "81228662789068955957049048445132481117450284102701"
        "93852110555964462294895493038196442881097566593344"
        "61284756482337867831652712019091456485669234603486"
        "10454326648213393607260249141273724587006606315588"
        "17488152092096282925409171536436789259036001133053"
        "05488204665213841469519415116094330572703657595919"
        "53092186117381932611793105118548074462379962749567"
        "35188575272489122793818301194912983367336244065664"
        "30860213949463952247371907021798609437027705392171"
    ),
}

# Metadata for each supported mathematical constant.
MATHEMATICAL_CONSTANTS: dict[str, dict[str, str]] = {
    "pi": {
        "symbol": "π",
        "name": "Pi",
        "integer_part": "3",
        "also_known_as": "Archimedes constant, Ludolph's number",
        "description": "The ratio of a circle's circumference to its diameter",
        "history": (
            "Known since antiquity. Archimedes (~250 BCE) bounded it between 223/71 "
            "and 22/7. The symbol π was first used by William Jones in 1706 and "
            "popularised by Leonhard Euler."
        ),
    },
    "e": {
        "symbol": "e",
        "name": "Euler's number",
        "integer_part": "2",
        "also_known_as": "Napier's constant",
        "description": (
            "The base of the natural logarithm; lim(1 + 1/n)^n as n -> infinity"
        ),
        "history": (
            "First described by Jacob Bernoulli (1683) while studying compound "
            "interest. Named 'e' by Leonhard Euler in 1731 and proven irrational "
            "by Euler in 1737."
        ),
    },
    "phi": {
        "symbol": "φ",
        "name": "Golden ratio",
        "integer_part": "1",
        "also_known_as": "Divine proportion, golden mean, golden section",
        "description": (
            "The ratio a/b such that (a+b)/a = a/b; positive root of x^2 - x - 1 = 0"
        ),
        "history": (
            "Known to ancient Greeks. Described in Euclid's Elements (~300 BCE). "
            "Appears in art, architecture, and nature. Called 'phi' (φ) after the "
            "Greek sculptor Phidias."
        ),
    },
    "sqrt2": {
        "symbol": "√2",
        "name": "Square root of 2",
        "integer_part": "1",
        "also_known_as": "Pythagoras' constant",
        "description": (
            "The positive real solution of x^2 = 2; the diagonal of the unit square"
        ),
        "history": (
            "The first number proven irrational. The Pythagoreans (~500 BCE) "
            "discovered that √2 cannot be expressed as a ratio of integers, "
            "which caused a major crisis in ancient mathematics."
        ),
    },
}


def calculate_constant(name: str, length: int) -> str:
    """Return verified digits of a mathematical constant to the requested length.

    Args:
        name: Constant identifier - one of ``"pi"``, ``"e"``, ``"phi"``,
            ``"sqrt2"``.
        length: Number of decimal places to return (not counting the integer part).

    Returns:
        String of the form ``"<integer>.<decimals>"``.

    Raises:
        ValueError: If *name* is unknown, or *length* is negative.
        TooManyDigitsError: If more digits are requested than are available.
    """
    logger.debug("calculate_constant: name=%r length=%d", name, length)

    if name not in MATHEMATICAL_CONSTANTS:
        known = ", ".join(MATHEMATICAL_CONSTANTS)
        msg = f"Unknown constant '{name}'. Choose from: {known}"
        raise ValueError(msg)

    if name == "pi":
        return calculate_pi(length)

    meta = MATHEMATICAL_CONSTANTS[name]
    digits_str = _CONSTANT_DIGIT_STRINGS[name]

    if length < 0:
        msg = "Length cannot be negative"
        raise ValueError(msg)

    if length == 0:
        length = DEFAULT_LENGTH

    available = len(digits_str)
    if length > available:
        raise TooManyDigitsError(length, available)

    result = f"{meta['integer_part']}.{digits_str[:length]}"
    logger.debug("calculate_constant: returning %r…", result[:14])
    return result


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


def color_your_pi(
    input_pi: str,
    correct_pi: str,
    *,
    verbose: bool = False,
    colorblind_mode: bool = False,
) -> int:
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
    output = []
    for input_digit, correct_digit in zip(input_pi, correct_pi, strict=False):
        if input_digit != correct_digit:
            error_count += 1
            if colorblind_mode:
                colored_digit = f"\033[38;5;208m{input_digit}\033[0m"
                output.append(colored_digit)
            else:
                colored_digit = f"\033[91m{input_digit}\033[0m"
                output.append(colored_digit)
        elif colorblind_mode:
            colored_digit = f"\033[38;5;34m{input_digit}\033[0m"
            output.append(colored_digit)
        else:
            colored_digit = f"\033[92m{input_digit}\033[0m"
            output.append(colored_digit)
    print("".join(output))

    if verbose:
        print(f"Found {error_count} incorrect digits")

    return error_count


def print_results(  # noqa: PLR0913
    *,
    user_pi: str,
    calculated_pi: str,
    decimals: int,
    verbose: bool = False,
    colorblind_mode: bool = False,
    symbol: str = "π",
    constant_name: str = "Pi",
) -> None:
    """Print the results of comparing user's input with a calculated constant.

    Args:
        user_pi: The user's input string.
        calculated_pi: The correct value of the constant.
        decimals: Number of decimal places being tested.
        verbose: Whether to show verbose output.
        colorblind_mode: Whether to use colorblind-friendly highlighting.
        symbol: Unicode symbol for the constant (e.g. ``"π"``, ``"e"``, ``"φ"``).
        constant_name: Human-readable name of the constant (e.g. ``"Pi"``).
    """
    # Format constant with spaces for better readability
    formatted_pi = format_pi_with_spaces(calculated_pi)

    if verbose:
        print(f"{symbol} with {decimals} decimals:\t{formatted_pi}")
        print(f"Your version of {symbol}:\t{user_pi}")

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
                print(
                    f"Perfect! You know {decimals} decimal places of {constant_name}!"
                )
        else:
            print("Match")
    elif verbose:
        print("You can do better!")
    else:
        print("No match")


def handle_easter_egg(input_str: str) -> bool:
    """Handle easter egg inputs - display info about a mathematical constant.

    Recognised triggers: ``"Archimedes"``, ``"pi"``, ``"PI"``, ``"e"``,
    ``"euler"``, ``"phi"``, ``"golden"``, ``"sqrt2"``, ``"pythagoras"``.

    Args:
        input_str: The raw input provided by the user.

    Returns:
        ``True`` if an easter egg was triggered, ``False`` otherwise.
    """
    key = input_str.lower()

    # Map trigger words to constant keys
    triggers: dict[str, str] = {
        "archimedes": "pi",
        "pi": "pi",
        "e": "e",
        "euler": "e",
        "napier": "e",
        "phi": "phi",
        "golden": "phi",
        "sqrt2": "sqrt2",
        "pythagoras": "sqrt2",
        "pythagorean": "sqrt2",
    }

    constant_key = triggers.get(key)
    if constant_key is None:
        return False

    meta = MATHEMATICAL_CONSTANTS[constant_key]
    symbol = meta["symbol"]
    name = meta["name"]
    also = meta["also_known_as"]
    desc = meta["description"]
    history = meta["history"]

    print(f"{symbol}  —  {name}")
    print(f"Also known as: {also}")
    print(f"Description:   {desc}")
    print(f"History:       {history}")
    return True


def load_practice_stats() -> dict[str, object]:
    """Load practice statistics from file."""
    # Create directory if it doesn't exist
    if not PRACTICE_CONFIG_DIR.exists():
        PRACTICE_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Create stats file if it doesn't exist
    if not PRACTICE_STATS_FILE.exists():
        default_stats = {
            "max_digits": 0,
            "total_digits_correct": 0,
            "total_practice_sessions": 0,
            "last_session_date": None,
            "fastest_time": None,
            "best_speed": None,  # digits per minute
            "history": [],
        }
        with PRACTICE_STATS_FILE.open("w", encoding="utf-8") as f:
            json.dump(default_stats, f, indent=2)
        return default_stats

    # Load existing stats
    try:
        with PRACTICE_STATS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Return default stats if there's an error
        return {
            "max_digits": 0,
            "total_digits_correct": 0,
            "total_practice_sessions": 0,
            "last_session_date": None,
            "fastest_time": None,
            "best_speed": None,
            "history": [],
        }


def save_practice_stats(stats: dict[str, object]) -> None:
    """Save practice statistics to file."""
    # Create directory if it doesn't exist
    if not PRACTICE_CONFIG_DIR.exists():
        PRACTICE_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Save stats
    with PRACTICE_STATS_FILE.open("w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


def load_practice_config() -> dict[str, object]:
    """Load practice configuration from file."""
    # Create directory if it doesn't exist
    if not PRACTICE_CONFIG_DIR.exists():
        PRACTICE_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Create config file if it doesn't exist
    if not PRACTICE_CONFIG_FILE.exists():
        default_config = {
            "mode": DEFAULT_PRACTICE_MODE,
            "min_digits": PRACTICE_MIN_DIGITS,
            "max_digits": PRACTICE_MAX_DIGITS,
            "chunk_size": DEFAULT_CHUNK_SIZE,
            "time_limit": DEFAULT_TIME_LIMIT,
            "show_timer": True,
            "visual_aid": True,
        }
        with PRACTICE_CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)
        return default_config

    # Load existing config
    try:
        with PRACTICE_CONFIG_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Return default config if there's an error
        return {
            "mode": DEFAULT_PRACTICE_MODE,
            "min_digits": PRACTICE_MIN_DIGITS,
            "max_digits": PRACTICE_MAX_DIGITS,
            "chunk_size": DEFAULT_CHUNK_SIZE,
            "time_limit": DEFAULT_TIME_LIMIT,
            "show_timer": True,
            "visual_aid": True,
        }


def save_practice_config(config: dict[str, object]) -> None:
    """Save practice configuration to file."""
    # Create directory if it doesn't exist
    if not PRACTICE_CONFIG_DIR.exists():
        PRACTICE_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Save config
    with PRACTICE_CONFIG_FILE.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


# Module-level constants for configuration constraints
MIN_CHUNK_SIZE = 2
MAX_CHUNK_SIZE = 10
MIN_TIME_LIMIT = 30
MAX_TIME_LIMIT = 600


def _display_config_menu(config: dict[str, object]) -> None:
    """Display the configuration menu with current settings.

    Args:
        config: The configuration dictionary to display.
    """
    print("\nCurrent settings:")
    print(f"1. Practice mode: {config.get('mode', DEFAULT_PRACTICE_MODE)}")
    print(f"2. Minimum digits: {config.get('min_digits', PRACTICE_MIN_DIGITS)}")
    print(f"3. Maximum digits: {config.get('max_digits', PRACTICE_MAX_DIGITS)}")
    print(f"4. Chunk size: {config.get('chunk_size', DEFAULT_CHUNK_SIZE)}")
    time_limit_str = (
        f"5. Time limit: {config.get('time_limit', DEFAULT_TIME_LIMIT)} seconds"
    )
    print(time_limit_str)
    print(f"6. Show timer: {'Yes' if config.get('show_timer', True) else 'No'}")
    print(f"7. Visual aid: {'Yes' if config.get('visual_aid', True) else 'No'}")
    print("8. Save and exit")
    print("9. Reset to defaults")
    print("\n")


def _get_default_config() -> dict[str, object]:
    """Get the default practice configuration.

    Returns:
        Dictionary with default configuration values.
    """
    return {
        "mode": DEFAULT_PRACTICE_MODE,
        "min_digits": PRACTICE_MIN_DIGITS,
        "max_digits": PRACTICE_MAX_DIGITS,
        "chunk_size": DEFAULT_CHUNK_SIZE,
        "time_limit": DEFAULT_TIME_LIMIT,
        "show_timer": True,
        "visual_aid": True,
    }


def _handle_mode_selection(config: dict[str, object]) -> None:
    """Handle practice mode selection.

    Args:
        config: The configuration dictionary to update.
    """
    print("\nSelect practice mode:")
    print("1. Standard - Digit by digit practice")
    print("2. Timed - Race against the clock")
    print("3. Chunk - Practice in groups of digits\n")
    mode_choice = input("Select mode (1-3): ").strip()

    if mode_choice == "1":
        config["mode"] = "standard"
    elif mode_choice == "2":
        config["mode"] = "timed"
    elif mode_choice == "3":
        config["mode"] = "chunk"
    else:
        print("Invalid selection. No changes made.")


def _handle_min_digits(config: dict[str, object]) -> None:
    """Handle minimum digits configuration.

    Args:
        config: The configuration dictionary to update.
    """
    prompt = f"Enter minimum digits ({PRACTICE_MIN_DIGITS}-{PRACTICE_MAX_DIGITS}): "
    min_digits_input = input(prompt).strip()
    try:
        min_digits = int(min_digits_input)
        if PRACTICE_MIN_DIGITS <= min_digits <= PRACTICE_MAX_DIGITS:
            config["min_digits"] = min_digits
        else:
            msg = (
                f"Value must be between {PRACTICE_MIN_DIGITS} "
                f"and {PRACTICE_MAX_DIGITS}."
            )
            print(msg)
    except ValueError:
        print("Invalid input. Please enter a number.")


def _handle_max_digits(config: dict[str, object]) -> None:
    """Handle maximum digits configuration.

    Args:
        config: The configuration dictionary to update.
    """
    prompt = f"Enter maximum digits ({PRACTICE_MIN_DIGITS}-{PRACTICE_MAX_DIGITS}): "
    max_digits_input = input(prompt).strip()
    try:
        max_digits = int(max_digits_input)
        if PRACTICE_MIN_DIGITS <= max_digits <= PRACTICE_MAX_DIGITS:
            config["max_digits"] = max_digits
        else:
            msg = (
                f"Value must be between {PRACTICE_MIN_DIGITS} "
                f"and {PRACTICE_MAX_DIGITS}."
            )
            print(msg)
    except ValueError:
        print("Invalid input. Please enter a number.")


def _handle_chunk_size(config: dict[str, object]) -> None:
    """Handle chunk size configuration.

    Args:
        config: The configuration dictionary to update.
    """
    chunk_size_input = input("Enter chunk size (2-10): ").strip()
    try:
        chunk_size = int(chunk_size_input)
        if MIN_CHUNK_SIZE <= chunk_size <= MAX_CHUNK_SIZE:
            config["chunk_size"] = chunk_size
        else:
            msg = f"Value must be between {MIN_CHUNK_SIZE} and {MAX_CHUNK_SIZE}."
            print(msg)
    except ValueError:
        print("Invalid input. Please enter a number.")


def _handle_time_limit(config: dict[str, object]) -> None:
    """Handle time limit configuration.

    Args:
        config: The configuration dictionary to update.
    """
    prompt = f"Enter time limit in seconds ({MIN_TIME_LIMIT}-{MAX_TIME_LIMIT}): "
    time_limit_input = input(prompt).strip()
    try:
        time_limit = int(time_limit_input)
        if MIN_TIME_LIMIT <= time_limit <= MAX_TIME_LIMIT:
            config["time_limit"] = time_limit
        else:
            msg = f"Value must be between {MIN_TIME_LIMIT} and {MAX_TIME_LIMIT}."
            print(msg)
    except ValueError:
        print("Invalid input. Please enter a number.")


def _handle_show_timer(config: dict[str, object]) -> None:
    """Handle show timer configuration.

    Args:
        config: The configuration dictionary to update.
    """
    show_timer = input("Show timer? (y/n): ").strip().lower()
    if show_timer in ("y", "yes"):
        config["show_timer"] = True
    elif show_timer in ("n", "no"):
        config["show_timer"] = False
    else:
        print("Invalid input. No changes made.")


def _handle_visual_aid(config: dict[str, object]) -> None:
    """Handle visual aid configuration.

    Args:
        config: The configuration dictionary to update.
    """
    visual_aid = input("Enable visual progress indicators? (y/n): ").strip().lower()
    if visual_aid in ("y", "yes"):
        config["visual_aid"] = True
    elif visual_aid in ("n", "no"):
        config["visual_aid"] = False
    else:
        print("Invalid input. No changes made.")


def _validate_and_save_config(config: dict[str, object]) -> bool:
    """Validate and save the configuration.

    Args:
        config: The configuration dictionary to validate and save.

    Returns:
        True if saved successfully, False if validation failed.
    """
    if config.get("min_digits", 0) > config.get("max_digits", 0):
        print(
            "Error: Minimum digits cannot be greater than maximum digits.",
        )
        return False

    save_practice_config(config)
    print("\nConfiguration saved successfully!")
    return True


def _handle_reset_to_defaults(config: dict[str, object]) -> dict[str, object]:
    """Handle resetting configuration to defaults.

    Args:
        config: The current configuration dictionary.

    Returns:
        The default configuration if confirmed, otherwise the original config.
    """
    confirm = (
        input("Are you sure you want to reset to defaults? (y/n): ").strip().lower()
    )
    if confirm in ("y", "yes"):
        default_config = _get_default_config()
        save_practice_config(default_config)
        print("\nConfiguration reset to defaults.")
        return default_config
    print("Reset cancelled.")
    return config


def configure_practice_mode() -> None:
    """Interactive configuration for practice mode settings."""
    # Load current configuration
    config = load_practice_config()

    print("\n🔧 PIGAME PRACTICE MODE CONFIGURATION 🔧")
    print("======================================\n")

    # Show initial menu
    _display_config_menu(config)

    # Menu option handlers
    handlers = {
        "1": _handle_mode_selection,
        "2": _handle_min_digits,
        "3": _handle_max_digits,
        "4": _handle_chunk_size,
        "5": _handle_time_limit,
        "6": _handle_show_timer,
        "7": _handle_visual_aid,
    }

    while True:
        try:
            choice = input("Select an option (1-9): ").strip()

            # Handle save and exit
            if choice == "8":
                if _validate_and_save_config(config):
                    break
                continue

            # Handle reset to defaults
            if choice == "9":
                config = _handle_reset_to_defaults(config)
                _display_config_menu(config)
                continue

            # Handle configuration options
            if choice in handlers:
                handlers[choice](config)
                _display_config_menu(config)
            else:
                print("Invalid selection. Please choose 1-9.")

        except KeyboardInterrupt:
            print("\n\nConfiguration cancelled. No changes saved.")
            break


def display_timer(start_time: float, time_limit: int | None = None) -> None:
    """Display a timer in the top-right corner of the terminal.

    Args:
        start_time: The time when the timer started
        time_limit: Optional time limit in seconds
    """
    elapsed = time.time() - start_time
    mins, secs = divmod(int(elapsed), 60)

    # Create timer string
    if time_limit:
        remaining = max(0, time_limit - elapsed)
        r_mins, r_secs = divmod(int(remaining), 60)
        timer_str = f"⏱️  {mins:02d}:{secs:02d} | Remaining: {r_mins:02d}:{r_secs:02d}"
    else:
        timer_str = f"⏱️  {mins:02d}:{secs:02d}"

    # Position cursor at top-right, print timer, then return cursor
    sys.stdout.write(f"\033[s\033[1;40H{timer_str}\033[u")
    sys.stdout.flush()


def display_progress_bar(current: int, total: int, width: int = 30) -> None:
    """Display a progress bar.

    Args:
        current: Current progress value
        total: Total value for 100% completion
        width: Width of the progress bar in characters
    """
    percent = min(100, int(current / total * 100))
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    sys.stdout.write(f"\r[{bar}] {percent}%")
    sys.stdout.flush()


def chunk_based_practice(
    pi_digits: str,
    chunk_size: int,
    current_digits: int,
    *,
    colorblind_mode: bool = False,
) -> tuple[bool, int]:
    """Implement chunk-based practice strategy.

    Args:
        pi_digits: String containing the digits of pi
        chunk_size: Number of digits per chunk
        current_digits: Current level (total digits to practice)
        colorblind_mode: Whether to use colorblind-friendly colors

    Returns:
        Tuple of (all_correct, correct_digits_count)
    """
    all_correct = True
    correct_digits = 0

    # Split into chunks
    digits_after_decimal = pi_digits[2 : current_digits + 2]  # Skip "3."
    chunks = [
        digits_after_decimal[i : i + chunk_size]
        for i in range(0, len(digits_after_decimal), chunk_size)
    ]

    # Print the first 2 characters (3.)
    sys.stdout.write("3.")
    sys.stdout.flush()

    # Process each chunk
    for chunk_index, chunk in enumerate(chunks):
        # Print chunk separator
        if chunk_index > 0:
            sys.stdout.write(" | ")

        # Process each digit in chunk
        for correct_digit in chunk:
            # Get input for this digit (non-blocking)
            digit = input_digit()

            # Check if digit is correct
            if digit == correct_digit:
                correct_digits += 1

                # Show correct digit in green
                if colorblind_mode:
                    sys.stdout.write(f"\033[38;5;34m{digit}\033[0m")
                else:
                    sys.stdout.write(f"\033[92m{digit}\033[0m")
            else:
                # Show incorrect digit in red/orange
                if colorblind_mode:
                    sys.stdout.write(f"\033[38;5;208m{digit}\033[0m")
                else:
                    sys.stdout.write(f"\033[91m{digit}\033[0m")

                # Restore terminal settings for proper printing
                termios.tcsetattr(
                    sys.stdin.fileno(),
                    termios.TCSADRAIN,
                    termios.tcgetattr(sys.stdin.fileno()),
                )

                # Show the correct digit
                print(f" ✗ Correct: {correct_digit}")
                all_correct = False
                return all_correct, correct_digits

        sys.stdout.flush()

    return all_correct, correct_digits


def timed_practice(
    pi_digits: str,
    current_digits: int,
    time_limit: int,
    *,
    colorblind_mode: bool = False,
    show_timer: bool = True,
) -> tuple[bool, int, float]:
    """Implement timed practice strategy.

    Args:
        pi_digits: String containing the digits of pi
        current_digits: Current level (total digits to practice)
        time_limit: Time limit in seconds
        colorblind_mode: Whether to use colorblind-friendly colors
        show_timer: Whether to show the timer

    Returns:
        Tuple of (all_correct, correct_digits_count, elapsed_time)
    """
    all_correct = True
    correct_digits = 0
    start_time = time.time()

    # Print the first 2 characters (3.)
    sys.stdout.write("3.")
    sys.stdout.flush()

    # Process each digit after the decimal point
    for i, correct_digit in enumerate(pi_digits[2 : current_digits + 2]):
        # Update timer if showing
        if show_timer and i % 3 == 0:  # Update every few digits to avoid flicker
            display_timer(start_time, time_limit)

            # Check if time's up
            if time.time() - start_time > time_limit:
                termios.tcsetattr(
                    sys.stdin.fileno(),
                    termios.TCSADRAIN,
                    termios.tcgetattr(sys.stdin.fileno()),
                )
                print("\n\n⏰ Time's up!")
                return False, correct_digits, time.time() - start_time

        # Get input for this digit (non-blocking)
        digit = input_digit()

        # Check if digit is correct
        if digit == correct_digit:
            correct_digits += 1

            # Show correct digit in green
            if colorblind_mode:
                sys.stdout.write(f"\033[38;5;34m{digit}\033[0m")
            else:
                sys.stdout.write(f"\033[92m{digit}\033[0m")
        else:
            # Show incorrect digit in red/orange
            if colorblind_mode:
                sys.stdout.write(f"\033[38;5;208m{digit}\033[0m")
            else:
                sys.stdout.write(f"\033[91m{digit}\033[0m")

            # Restore terminal settings for proper printing
            termios.tcsetattr(
                sys.stdin.fileno(),
                termios.TCSADRAIN,
                termios.tcgetattr(sys.stdin.fileno()),
            )

            # Show the correct digit
            print(f" ✗ Correct: {correct_digit}")
            all_correct = False
            return all_correct, correct_digits, time.time() - start_time

        # Add spacing for readability
        if (i + 1) % 5 == 0:
            sys.stdout.write(" ")

        sys.stdout.flush()

    # Calculate total time
    elapsed_time = time.time() - start_time

    return all_correct, correct_digits, elapsed_time


@dataclass
class PracticeConfig:
    """Configuration for practice mode.

    Attributes:
        colorblind_mode: Whether to use colorblind-friendly colors.
        mode: Practice mode (standard, timed, chunk).
        min_digits: Minimum number of digits to start with.
        max_digits: Maximum number of digits to practice.
        chunk_size: Size of chunks for chunk mode.
        time_limit: Time limit in seconds for timed mode.
        show_timer: Whether to show the timer.
        visual_aid: Whether to show visual progress indicators.
    """

    colorblind_mode: bool = False
    mode: str = DEFAULT_PRACTICE_MODE
    min_digits: int = PRACTICE_MIN_DIGITS
    max_digits: int = PRACTICE_MAX_DIGITS
    chunk_size: int = DEFAULT_CHUNK_SIZE
    time_limit: int = DEFAULT_TIME_LIMIT
    show_timer: bool = True
    visual_aid: bool = True


def _load_practice_config_settings(  # noqa: PLR0913
    *,
    colorblind_mode: bool,
    mode: str | None,
    min_digits: int | None,
    max_digits: int | None,
    chunk_size: int | None,
    time_limit: int | None,
    visual_aid: bool | None,
) -> PracticeConfig:
    """Load practice configuration from parameters and config file.

    Args:
        colorblind_mode: Whether to use colorblind-friendly colors.
        mode: Practice mode (standard, timed, chunk).
        min_digits: Minimum number of digits to start with.
        max_digits: Maximum number of digits to practice.
        chunk_size: Size of chunks for chunk mode.
        time_limit: Time limit in seconds for timed mode.
        visual_aid: Whether to show visual progress indicators.

    Returns:
        PracticeConfig object with merged settings.
    """
    config = load_practice_config()

    return PracticeConfig(
        colorblind_mode=colorblind_mode,
        mode=mode if mode is not None else config.get("mode", DEFAULT_PRACTICE_MODE),
        min_digits=(
            min_digits
            if min_digits is not None
            else config.get("min_digits", PRACTICE_MIN_DIGITS)
        ),
        max_digits=(
            max_digits
            if max_digits is not None
            else config.get("max_digits", PRACTICE_MAX_DIGITS)
        ),
        chunk_size=(
            chunk_size
            if chunk_size is not None
            else config.get("chunk_size", DEFAULT_CHUNK_SIZE)
        ),
        time_limit=(
            time_limit
            if time_limit is not None
            else config.get("time_limit", DEFAULT_TIME_LIMIT)
        ),
        show_timer=config.get("show_timer", True),
        visual_aid=(
            visual_aid if visual_aid is not None else config.get("visual_aid", True)
        ),
    )


def _print_practice_instructions(cfg: PracticeConfig) -> None:
    """Print mode-specific instructions for practice mode.

    Args:
        cfg: The practice configuration.
    """
    if cfg.mode == "standard":
        print("Practice memorizing digits of π one by one.")
        print("Type each digit (0-9) without pressing Enter.")
    elif cfg.mode == "timed":
        print(
            f"Timed practice: You have {cfg.time_limit} seconds to enter digits.",
        )
        print("Type each digit (0-9) without pressing Enter.")
    elif cfg.mode == "chunk":
        print(f"Chunk-based practice: Memorize π in chunks of {cfg.chunk_size} digits.")
        print("Type each digit (0-9) without pressing Enter.")

    print("Press Ctrl+C at any time to exit.\n")


def _get_starting_digits(
    stats: dict[str, object],
    min_digits: int,
    max_digits: int,
) -> int:
    """Determine starting digit count for practice session.

    Args:
        stats: Practice statistics dictionary.
        min_digits: Minimum number of digits.
        max_digits: Maximum number of digits.

    Returns:
        The starting digit count for this session.
    """
    current_digits = max(stats.get("max_digits", 0) + 1, min_digits)
    return min(current_digits, max_digits)


def _print_practice_header(stats: dict[str, object], current_digits: int) -> None:
    """Print practice session header with stats.

    Args:
        stats: Practice statistics dictionary.
        current_digits: Starting digit count.
    """
    print(f"Your best: {stats.get('max_digits', 0)} digits")
    if stats.get("best_speed"):
        print(f"Best speed: {stats.get('best_speed'):.1f} digits/minute")
    print(f"Starting with {current_digits} digits\n")


def _show_reference_digits(
    practice_mode: str,
    pi_digits: str,
    current_digits: int,
) -> None:
    """Show reference digits before practice (except in timed mode).

    Args:
        practice_mode: The practice mode being used.
        pi_digits: The pi digits string.
        current_digits: Number of digits to practice.
    """
    if practice_mode != "timed":
        ref_digits = min(5, current_digits)
        print(f"First {ref_digits} digits: {pi_digits[: ref_digits + 2]}")
        time.sleep(1)


def _run_practice_strategy(
    cfg: PracticeConfig,
    pi_digits: str,
    current_digits: int,
    stats: dict[str, object],
) -> tuple[bool, int, float | None]:
    """Run the appropriate practice strategy based on configuration.

    Args:
        cfg: Practice configuration.
        pi_digits: The pi digits string.
        current_digits: Number of digits to practice.
        stats: Practice statistics dictionary.

    Returns:
        Tuple of (all_correct, correct_count, elapsed_time).
    """
    if cfg.mode == "standard":
        all_correct, correct_count = standard_practice(
            pi_digits,
            current_digits,
            colorblind_mode=cfg.colorblind_mode,
            visual_aid=cfg.visual_aid,
        )
        return all_correct, correct_count, None

    if cfg.mode == "timed":
        all_correct, correct_count, elapsed_time = timed_practice(
            pi_digits,
            current_digits,
            cfg.time_limit,
            colorblind_mode=cfg.colorblind_mode,
            show_timer=cfg.show_timer,
        )

        # Calculate and update speed
        if elapsed_time > 0:
            speed = (correct_count / elapsed_time) * 60
            print(f"\nSpeed: {speed:.1f} digits/minute")

            if not stats.get("best_speed") or speed > stats.get("best_speed"):
                stats["best_speed"] = speed

        return all_correct, correct_count, elapsed_time

    # Chunk mode
    all_correct, correct_count = chunk_based_practice(
        pi_digits,
        cfg.chunk_size,
        current_digits,
        colorblind_mode=cfg.colorblind_mode,
    )
    return all_correct, correct_count, None


def _update_practice_stats(
    stats: dict[str, object],
    session_max_level: int,
    session_correct_digits: int,
    session_duration: float,
    practice_mode: str,
    elapsed_time: float | None,
) -> None:
    """Update and save practice statistics.

    Args:
        stats: Practice statistics dictionary.
        session_max_level: Maximum level reached in this session.
        session_correct_digits: Total correct digits in this session.
        session_duration: Total session duration in seconds.
        practice_mode: The practice mode used.
        elapsed_time: Elapsed time for the last level (if applicable).
    """
    stats["max_digits"] = max(stats.get("max_digits", 0), session_max_level)
    stats["total_digits_correct"] = (
        stats.get("total_digits_correct", 0) + session_correct_digits
    )
    stats["total_practice_sessions"] = stats.get("total_practice_sessions", 0) + 1
    stats["last_session_date"] = time.strftime("%Y-%m-%d %H:%M:%S")

    # Update fastest time for timed mode
    time_improved = not stats.get("fastest_time") or (
        elapsed_time is not None
        and elapsed_time < stats.get("fastest_time", float("inf"))
    )
    if practice_mode == "timed" and elapsed_time is not None and time_improved:
        stats["fastest_time"] = elapsed_time

    # Add session to history
    session_record = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mode": practice_mode,
        "max_level": session_max_level,
        "correct_digits": session_correct_digits,
        "duration_seconds": round(session_duration),
    }

    if "history" not in stats:
        stats["history"] = []

    stats["history"].append(session_record)

    # Limit history to last 100 sessions
    max_history = 100
    if len(stats["history"]) > max_history:
        stats["history"] = stats["history"][-max_history:]

    save_practice_stats(stats)


def _print_session_summary(
    stats: dict[str, object],
    practice_mode: str,
    session_duration: float,
    session_correct_digits: int,
    session_max_level: int,
) -> None:
    """Print summary of practice session.

    Args:
        stats: Practice statistics dictionary.
        practice_mode: The practice mode used.
        session_duration: Total session duration in seconds.
        session_correct_digits: Total correct digits in this session.
        session_max_level: Maximum level reached in this session.
    """
    print("\n=== Session Summary ===")
    print(f"Mode: {practice_mode}")
    print(
        f"Time: {round(session_duration // 60)} min {round(session_duration % 60)} sec",
    )
    print(f"Digits correct: {session_correct_digits}")
    print(f"Maximum level: {session_max_level}")
    print(f"All-time best: {stats['max_digits']} digits")

    if practice_mode == "timed" and session_correct_digits > 0:
        speed = (session_correct_digits / session_duration) * 60
        print(f"Average speed: {speed:.1f} digits/minute")
        print(f"All-time best speed: {stats.get('best_speed', 0):.1f} digits/minute")


def standard_practice(
    pi_digits: str,
    current_digits: int,
    *,
    colorblind_mode: bool = False,
    visual_aid: bool = False,
) -> tuple[bool, int]:
    """Implement standard digit-by-digit practice strategy.

    Args:
        pi_digits: String containing the digits of pi
        current_digits: Current level (total digits to practice)
        colorblind_mode: Whether to use colorblind-friendly colors
        visual_aid: Whether to show visual progress indicators

    Returns:
        Tuple of (all_correct, correct_digits_count)
    """
    all_correct = True
    correct_digits = 0

    # Print the first 2 characters (3.)
    sys.stdout.write("3.")
    sys.stdout.flush()

    # Process each digit after the decimal point
    for i, correct_digit in enumerate(pi_digits[2 : current_digits + 2]):
        # Show progress bar if visual aid is enabled
        if visual_aid and i % 3 == 0:  # Update every few digits to avoid flicker
            total_digits = current_digits
            sys.stdout.write("\033[s\033[2;1H")  # Save cursor and move to line 2
            display_progress_bar(i, total_digits)
            sys.stdout.write("\033[u")  # Restore cursor

        # Get input for this digit (non-blocking)
        digit = input_digit()

        # Check if digit is correct
        if digit == correct_digit:
            correct_digits += 1

            # Show correct digit in green
            if colorblind_mode:
                sys.stdout.write(f"\033[38;5;34m{digit}\033[0m")
            else:
                sys.stdout.write(f"\033[92m{digit}\033[0m")
        else:
            # Show incorrect digit in red/orange
            if colorblind_mode:
                sys.stdout.write(f"\033[38;5;208m{digit}\033[0m")
            else:
                sys.stdout.write(f"\033[91m{digit}\033[0m")

            # Restore terminal settings for proper printing
            termios.tcsetattr(
                sys.stdin.fileno(),
                termios.TCSADRAIN,
                termios.tcgetattr(sys.stdin.fileno()),
            )

            # Show the correct digit
            print(f" ✗ Correct: {correct_digit}")
            all_correct = False
            return all_correct, correct_digits

        # Add spacing for readability
        if (i + 1) % 5 == 0:
            sys.stdout.write(" ")

        sys.stdout.flush()

    # Clear progress bar if used
    if visual_aid:
        sys.stdout.write("\033[2;1H\033[K")  # Move to line 2 and clear
        sys.stdout.flush()

    return all_correct, correct_digits


def practice_mode(  # noqa: PLR0913
    *,
    colorblind_mode: bool = False,
    mode: str | None = None,
    min_digits: int | None = None,
    max_digits: int | None = None,
    chunk_size: int | None = None,
    time_limit: int | None = None,
    visual_aid: bool | None = None,
) -> None:
    """Interactive practice mode for memorizing π digits.

    Args:
        colorblind_mode: Whether to use colorblind-friendly colors
        mode: Practice mode (standard, timed, chunk)
        min_digits: Minimum number of digits to start with
        max_digits: Maximum number of digits to practice
        chunk_size: Size of chunks for chunk mode
        time_limit: Time limit in seconds for timed mode
        visual_aid: Whether to show visual progress indicators
    """
    print("\n🔢 PIGAME PRACTICE MODE 🔢")
    print("=========================\n")

    # Load configuration and stats
    cfg = _load_practice_config_settings(
        colorblind_mode=colorblind_mode,
        mode=mode,
        min_digits=min_digits,
        max_digits=max_digits,
        chunk_size=chunk_size,
        time_limit=time_limit,
        visual_aid=visual_aid,
    )
    stats = load_practice_stats()

    # Print instructions and header
    _print_practice_instructions(cfg)
    current_digits = _get_starting_digits(stats, cfg.min_digits, cfg.max_digits)
    _print_practice_header(stats, current_digits)

    # Get pi digits
    pi_digits = calculate_pi(current_digits)

    try:
        # Track session stats
        session_start_time = time.time()
        session_correct_digits = 0
        session_max_level = stats.get("max_digits", 0)
        elapsed_time = None

        # Show reference digits
        _show_reference_digits(cfg.mode, pi_digits, current_digits)

        # Start practice session
        while current_digits <= cfg.max_digits:
            print(f"\n--- Level: {current_digits} digits ---")

            # Run practice strategy
            all_correct, correct_count, elapsed_time = _run_practice_strategy(
                cfg,
                pi_digits,
                current_digits,
                stats,
            )
            session_correct_digits += correct_count

            # End of level processing
            if all_correct:
                print("\n\n🎉 Perfect! Moving to next level.")
                current_digits += 1

                # Update max level if improved
                if current_digits > session_max_level:
                    session_max_level = current_digits - 1

                # Update pi_digits if needed
                if current_digits > len(pi_digits) - 2:
                    pi_digits = calculate_pi(current_digits)

                time.sleep(1)
            else:
                print("\n\nTry again for this level.")
                time.sleep(1)

        # Reached maximum difficulty
        print("\n🏆 Congratulations! You've reached the maximum level!")

    except KeyboardInterrupt:
        # Restore terminal settings
        termios.tcsetattr(
            sys.stdin.fileno(),
            termios.TCSADRAIN,
            termios.tcgetattr(sys.stdin.fileno()),
        )
        print("\n\nPractice session ended.")

    # Update and save stats
    session_duration = time.time() - session_start_time
    _update_practice_stats(
        stats,
        session_max_level,
        session_correct_digits,
        session_duration,
        cfg.mode,
        elapsed_time,
    )

    # Show session summary
    _print_session_summary(
        stats,
        cfg.mode,
        session_duration,
        session_correct_digits,
        session_max_level,
    )


def input_digit() -> str:
    """Get a single digit of input from the user (non-blocking)."""
    # Save terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        # Set terminal to raw mode
        tty.setraw(fd)

        # Read a single character
        char = sys.stdin.read(1)

        # Only accept digits
        if char.isdigit():
            return char
        # Handle non-digit input silently
        return input_digit()
    finally:
        # Restore terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def _create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        description="Evaluate your version of π (3.141..)",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-v", action="store_true", help="Increase verbosity.")
    parser.add_argument(
        "-p",
        type=str,
        metavar="LENGTH",
        help="Calculate and show π with LENGTH number of decimals.",
    )
    parser.add_argument("-V", action="store_true", help="Version.")
    parser.add_argument(
        "-c",
        action="store_true",
        help="Color-blind mode (use underscores instead of color).",
    )
    parser.add_argument(
        "--practice",
        action="store_true",
        help="Start interactive practice mode for memorizing digits.",
    )
    parser.add_argument(
        "--practice-mode",
        choices=["standard", "timed", "chunk"],
        help="Set practice mode (standard, timed, chunk).",
    )
    parser.add_argument(
        "--min-digits",
        type=int,
        help="Minimum number of digits to start practice with.",
    )
    parser.add_argument(
        "--max-digits",
        type=int,
        help="Maximum number of digits to practice.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        help="Size of chunks for chunk practice mode.",
    )
    parser.add_argument(
        "--time-limit",
        type=int,
        help="Time limit in seconds for timed practice mode.",
    )
    parser.add_argument(
        "--visual-aid",
        action="store_true",
        help="Enable visual progress indicators in practice mode.",
    )
    parser.add_argument(
        "--no-visual-aid",
        action="store_true",
        help="Disable visual progress indicators in practice mode.",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show your practice statistics.",
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="Configure practice mode settings.",
    )
    parser.add_argument(
        "--constant",
        choices=list(MATHEMATICAL_CONSTANTS.keys()),
        default="pi",
        metavar="CONSTANT",
        help=(
            "Mathematical constant to use.\n"
            "Choices: " + ", ".join(MATHEMATICAL_CONSTANTS.keys()) + "\n"
            "(default: pi)."
        ),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Show available constants with descriptions and exit.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help=(
            "Enable DEBUG-level logging to stderr.\n"
            "Equivalent to setting PIGAME_DEBUG=1 in the environment."
        ),
    )
    parser.add_argument(
        "YOUR_PI", nargs="?", type=str, help="Your version of the constant"
    )
    return parser


def _handle_stats_display() -> None:
    """Display practice statistics and exit."""
    stats = load_practice_stats()
    print("\n=== PIGAME Practice Statistics ===")
    print(f"Total practice sessions: {stats.get('total_practice_sessions', 0)}")
    print(f"Total correct digits entered: {stats.get('total_digits_correct', 0)}")
    print(f"Best level reached: {stats.get('max_digits', 0)} digits")
    print(f"Last session: {stats.get('last_session_date', 'Never')}")

    # Show speed stats if available
    if stats.get("best_speed"):
        print(f"Best speed: {stats.get('best_speed', 0):.1f} digits/minute")
    if stats.get("fastest_time"):
        mins, secs = divmod(int(stats.get("fastest_time")), 60)
        print(f"Fastest time: {mins}m {secs}s")

    # Show recent history if available
    if stats.get("history"):
        print("\nRecent sessions:")
        for i, session in enumerate(reversed(stats.get("history", []))[:5]):
            mode_str = (
                f"[{session.get('mode', 'standard')}] " if "mode" in session else ""
            )
            print(
                f"  {i + 1}. {session['date']} - "
                f"{mode_str}Level {session['max_level']}"
                f" ({session['correct_digits']} correct digits,"
                f" {session['duration_seconds'] // 60}m "
                f"{session['duration_seconds'] % 60}s)",
            )
    print("=================================")


def _handle_pi_calculation(args: argparse.Namespace) -> tuple[int, str]:
    """Handle the -p option for displaying a mathematical constant.

    Args:
        args: Parsed command line arguments.

    Returns:
        Tuple of (length, calculated_constant_string).
    """
    if args.p:
        constant_key = getattr(args, "constant", "pi")
        meta = MATHEMATICAL_CONSTANTS[constant_key]
        symbol = meta["symbol"]
        length = length_validation(args.p)
        calculated = calculate_constant(constant_key, length)
        formatted = format_pi_with_spaces(calculated)

        if args.v:
            print(f"{symbol} with {length} decimals:\t{formatted}")
        else:
            print(formatted)

        return length, calculated

    return DEFAULT_LENGTH, ""


def _handle_user_pi_input(
    args: argparse.Namespace,
    length: int,
) -> None:
    """Handle user's constant input and display results.

    Args:
        args: Parsed command line arguments.
        length: Length from -p option or default.
    """
    # Check for easter eggs
    if handle_easter_egg(args.YOUR_PI):
        sys.exit(0)

    # Validate input
    try:
        input_validation(args.YOUR_PI)
    except ValueError:
        logger.exception("Invalid input: %r", args.YOUR_PI)
        sys.exit(1)

    constant_key = getattr(args, "constant", "pi")
    meta = MATHEMATICAL_CONSTANTS[constant_key]
    symbol = meta["symbol"]
    name = meta["name"]

    # Calculate constant based on user input length or -p option
    if not args.p:
        decimals = (
            len(args.YOUR_PI) - 2
            if len(args.YOUR_PI) >= MIN_DIGITS_WITH_POINT
            else len(args.YOUR_PI)
        )
        calculated = calculate_constant(constant_key, decimals)
    else:
        decimals = length
        calculated = calculate_constant(constant_key, decimals)

    print_results(
        user_pi=args.YOUR_PI,
        calculated_pi=calculated,
        decimals=decimals,
        verbose=args.v,
        colorblind_mode=args.c,
        symbol=symbol,
        constant_name=name,
    )


def main() -> None:
    """Parse command line arguments and perform calculations."""
    # Create parser and parse arguments
    parser = _create_argument_parser()

    try:
        args = parser.parse_args()
    except (argparse.ArgumentError, SystemExit):
        if "--help" in sys.argv or "-h" in sys.argv:
            sys.exit(0)
        logger.exception("Argument parsing failed")
        usage(1)

    # Activate debug logging as early as possible (PIGAME_DEBUG env-var is
    # already handled at import time; this covers the --debug CLI flag).
    if getattr(args, "debug", False):
        logger.setLevel(logging.DEBUG)
        logger.debug("debug logging enabled via --debug flag")

    # Handle version display
    if args.V:
        print(f"version: {VERSION}")
        sys.exit(0)

    # Handle --list: show all available constants
    if getattr(args, "list", False):
        print("Available mathematical constants:\n")
        for key, meta in MATHEMATICAL_CONSTANTS.items():
            max_len = MAX_LENGTH if key == "pi" else MAX_CONSTANT_LENGTH
            print(f"  {meta['symbol']:3s}  {meta['name']:20s}  --constant {key}")
            print(f"       {meta['description']}")
            print(f"       Up to {max_len} decimal places available.\n")
        sys.exit(0)

    # Handle configuration
    if args.config:
        configure_practice_mode()
        sys.exit(0)

    # Handle stats display
    if args.stats:
        _handle_stats_display()
        sys.exit(0)

    # Handle practice mode
    if args.practice:
        visual_aid_setting = None
        if args.visual_aid:
            visual_aid_setting = True
        elif args.no_visual_aid:
            visual_aid_setting = False

        practice_mode(
            colorblind_mode=args.c,
            mode=args.practice_mode,
            min_digits=args.min_digits,
            max_digits=args.max_digits,
            chunk_size=args.chunk_size,
            time_limit=args.time_limit,
            visual_aid=visual_aid_setting,
        )
        sys.exit(0)

    # Show usage if no arguments provided
    if not args.YOUR_PI and not args.p and not args.v and not args.c:
        usage(0)

    # Handle pi calculation
    length, _ = _handle_pi_calculation(args)

    # Exit if only displaying calculated pi
    if args.p and not args.YOUR_PI:
        sys.exit(0)

    # Handle user pi input
    if args.YOUR_PI:
        _handle_user_pi_input(args, length)


if __name__ == "__main__":
    main()
