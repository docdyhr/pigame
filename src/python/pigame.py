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
        return "1.7.0"  # Default version


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
    if not input_str:
        msg = "Invalid input"
        raise ValueError(msg)
    dot_count = input_str.count(".")
    comma_count = input_str.count(",")

    if comma_count > 0:
        msg = "Invalid input"
        raise ValueError(msg)

    if not all(c.isdigit() or c == "." for c in input_str):
        msg = "Invalid input"
        raise ValueError(msg)

    if dot_count > 1:
        msg = "Invalid input"
        raise ValueError(msg)

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
        msg = "Invalid input"
        raise ValueError(msg)

    length = int(length_str)

    if length <= 0:
        return DEFAULT_LENGTH
    if length > MAX_LENGTH:
        msg = "too big"
        sys.exit(msg)  # This exits the program

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
        print(f"Your version of π:\t{user_pi}")

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


def configure_practice_mode() -> None:
    """Interactive configuration for practice mode settings."""
    # Load current configuration
    config = load_practice_config()

    print("\n🔧 PIGAME PRACTICE MODE CONFIGURATION 🔧")
    print("======================================\n")

    # Show current settings
    print("Current settings:")
    print(f"1. Practice mode: {config.get('mode', DEFAULT_PRACTICE_MODE)}")
    print(f"2. Minimum digits: {config.get('min_digits', PRACTICE_MIN_DIGITS)}")
    print(f"3. Maximum digits: {config.get('max_digits', PRACTICE_MAX_DIGITS)}")
    print(f"4. Chunk size: {config.get('chunk_size', DEFAULT_CHUNK_SIZE)}")
    print(f"5. Time limit: {config.get('time_limit', DEFAULT_TIME_LIMIT)} seconds")
    print(f"6. Show timer: {'Yes' if config.get('show_timer', True) else 'No'}")
    print(f"7. Visual aid: {'Yes' if config.get('visual_aid', True) else 'No'}")
    print("8. Save and exit")
    print("9. Reset to defaults")
    print("\n")

    while True:
        try:
            choice = input("Select an option (1-9): ").strip()

            if choice == "1":
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

            elif choice == "2":
                prompt = f"Enter minimum digits ({PRACTICE_MIN_DIGITS}-{PRACTICE_MAX_DIGITS}): "
                min_digits_input = input(prompt).strip()
                try:
                    min_digits = int(min_digits_input)
                    if PRACTICE_MIN_DIGITS <= min_digits <= PRACTICE_MAX_DIGITS:
                        config["min_digits"] = min_digits
                    else:
                        msg = f"Value must be between {PRACTICE_MIN_DIGITS} and {PRACTICE_MAX_DIGITS}."
                        print(msg)
                except ValueError:
                    print("Invalid input. Please enter a number.")

            elif choice == "3":
                prompt = f"Enter maximum digits ({PRACTICE_MIN_DIGITS}-{PRACTICE_MAX_DIGITS}): "
                max_digits_input = input(prompt).strip()
                try:
                    max_digits = int(max_digits_input)
                    if PRACTICE_MIN_DIGITS <= max_digits <= PRACTICE_MAX_DIGITS:
                        config["max_digits"] = max_digits
                    else:
                        msg = f"Value must be between {PRACTICE_MIN_DIGITS} and {PRACTICE_MAX_DIGITS}."
                        print(msg)
                except ValueError:
                    print("Invalid input. Please enter a number.")

            elif choice == "4":
                chunk_size_input = input("Enter chunk size (2-10): ").strip()
                try:
                    chunk_size = int(chunk_size_input)
                    # Check against defined constants for min/max chunk size
                    if MIN_CHUNK_SIZE <= chunk_size <= MAX_CHUNK_SIZE:
                        config["chunk_size"] = chunk_size
                    else:
                        msg = f"Value must be between {MIN_CHUNK_SIZE} and {MAX_CHUNK_SIZE}."
                        print(msg)
                except ValueError:
                    print("Invalid input. Please enter a number.")

            elif choice == "5":
                prompt = (
                    f"Enter time limit in seconds ({MIN_TIME_LIMIT}-{MAX_TIME_LIMIT}): "
                )
                time_limit_input = input(prompt).strip()
                try:
                    time_limit = int(time_limit_input)
                    # Check against defined constants for min/max time limit
                    if MIN_TIME_LIMIT <= time_limit <= MAX_TIME_LIMIT:
                        config["time_limit"] = time_limit
                    else:
                        msg = f"Value must be between {MIN_TIME_LIMIT} and {MAX_TIME_LIMIT}."
                        print(msg)
                except ValueError:
                    print("Invalid input. Please enter a number.")

            elif choice == "6":
                show_timer = input("Show timer? (y/n): ").strip().lower()
                if show_timer in ("y", "yes"):
                    config["show_timer"] = True
                elif show_timer in ("n", "no"):
                    config["show_timer"] = False
                else:
                    print("Invalid input. No changes made.")

            elif choice == "7":
                visual_aid = (
                    input("Enable visual progress indicators? (y/n): ").strip().lower()
                )
                if visual_aid in ("y", "yes"):
                    config["visual_aid"] = True
                elif visual_aid in ("n", "no"):
                    config["visual_aid"] = False
                else:
                    print("Invalid input. No changes made.")

            elif choice == "8":
                # Validate configuration
                if config.get("min_digits", 0) > config.get("max_digits", 0):
                    print(
                        "Error: Minimum digits cannot be greater than maximum digits.",
                    )
                    continue

                save_practice_config(config)
                print("\nConfiguration saved successfully!")
                break

            elif choice == "9":
                confirm = (
                    input("Are you sure you want to reset to defaults? (y/n): ")
                    .strip()
                    .lower()
                )
                if confirm in ("y", "yes"):
                    default_config = {
                        "mode": DEFAULT_PRACTICE_MODE,
                        "min_digits": PRACTICE_MIN_DIGITS,
                        "max_digits": PRACTICE_MAX_DIGITS,
                        "chunk_size": DEFAULT_CHUNK_SIZE,
                        "time_limit": DEFAULT_TIME_LIMIT,
                        "show_timer": True,
                        "visual_aid": True,
                    }
                    save_practice_config(default_config)
                    print("\nConfiguration reset to defaults.")
                    config = default_config
                else:
                    print("Reset cancelled.")

            else:
                print("Invalid selection. Please choose 1-9.")

            # Show updated settings after each change
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


def practice_mode(
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

    # Load practice config and stats
    config = load_practice_config()
    stats = load_practice_stats()

    # Use provided parameters or config values
    practice_mode = mode if mode else config.get("mode", DEFAULT_PRACTICE_MODE)
    practice_min_digits = (
        min_digits if min_digits else config.get("min_digits", PRACTICE_MIN_DIGITS)
    )
    practice_max_digits = (
        max_digits if max_digits else config.get("max_digits", PRACTICE_MAX_DIGITS)
    )
    chunk_size = (
        chunk_size if chunk_size else config.get("chunk_size", DEFAULT_CHUNK_SIZE)
    )
    time_limit = (
        time_limit if time_limit else config.get("time_limit", DEFAULT_TIME_LIMIT)
    )
    show_timer = config.get("show_timer", True)
    show_visual_aid = (
        visual_aid if visual_aid is not None else config.get("visual_aid", True)
    )

    # Print mode-specific instructions
    if practice_mode == "standard":
        print("Practice memorizing digits of π one by one.")
        print("Type each digit (0-9) without pressing Enter.")
    elif practice_mode == "timed":
        print(
            f"Timed practice: You have {time_limit} seconds to enter digits.",
        )
        print("Type each digit (0-9) without pressing Enter.")
    elif practice_mode == "chunk":
        print(f"Chunk-based practice: Memorize π in chunks of {chunk_size} digits.")
        print("Type each digit (0-9) without pressing Enter.")

    print("Press Ctrl+C at any time to exit.\n")

    # Determine starting digits (either continue from last time or start at minimum)
    current_digits = max(stats.get("max_digits", 0) + 1, practice_min_digits)
    current_digits = min(current_digits, practice_max_digits)

    print(f"Your best: {stats.get('max_digits', 0)} digits")
    if stats.get("best_speed"):
        print(f"Best speed: {stats.get('best_speed'):.1f} digits/minute")
    print(f"Starting with {current_digits} digits\n")

    # Get pi digits
    pi_digits = calculate_pi(current_digits)

    try:
        # Track session stats
        session_start_time = time.time()
        session_correct_digits = 0
        session_max_level = stats.get("max_digits", 0)

        # Show first digits as reference (except in timed mode)
        if practice_mode != "timed":
            ref_digits = min(5, current_digits)
            print(f"First {ref_digits} digits: {pi_digits[:ref_digits+2]}")
            time.sleep(1)

        # Start practice session
        while current_digits <= practice_max_digits:
            print(f"\n--- Level: {current_digits} digits ---")

            # Use appropriate practice strategy
            if practice_mode == "standard":
                all_correct, correct_count = standard_practice(
                    pi_digits,
                    current_digits,
                    colorblind_mode,
                    show_visual_aid,
                )
                session_correct_digits += correct_count
                elapsed_time = None
            elif practice_mode == "timed":
                all_correct, correct_count, elapsed_time = timed_practice(
                    pi_digits,
                    current_digits,
                    time_limit,
                    colorblind_mode,
                    show_timer,
                )
                session_correct_digits += correct_count

                # Calculate speed (digits per minute)
                if elapsed_time > 0:
                    speed = (correct_count / elapsed_time) * 60
                    print(f"\nSpeed: {speed:.1f} digits/minute")

                    # Update best speed
                    if not stats.get("best_speed") or speed > stats.get("best_speed"):
                        stats["best_speed"] = speed
            elif practice_mode == "chunk":
                all_correct, correct_count = chunk_based_practice(
                    pi_digits,
                    chunk_size,
                    current_digits,
                    colorblind_mode,
                )
                session_correct_digits += correct_count
                elapsed_time = None

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

                # Take a brief pause between levels
                time.sleep(1)
            else:
                print("\n\nTry again for this level.")
                time.sleep(1)

        # Reached maximum difficulty!
        print("\n🏆 Congratulations! You've reached the maximum level!")

    except KeyboardInterrupt:
        # Restore terminal settings
        termios.tcsetattr(
            sys.stdin.fileno(),
            termios.TCSADRAIN,
            termios.tcgetattr(sys.stdin.fileno()),
        )
        print("\n\nPractice session ended.")

    # Calculate session stats
    session_duration = time.time() - session_start_time

    # Update overall stats
    stats["max_digits"] = max(stats.get("max_digits", 0), session_max_level)
    stats["total_digits_correct"] = (
        stats.get("total_digits_correct", 0) + session_correct_digits
    )
    stats["total_practice_sessions"] = stats.get("total_practice_sessions", 0) + 1
    stats["last_session_date"] = time.strftime("%Y-%m-%d %H:%M:%S")

    # For timed mode, update fastest time if applicable
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

    # Limit history to last max_history sessions
    if len(stats["history"]) > max_history:
        stats["history"] = stats["history"][-max_history:]

    # Save updated stats
    save_practice_stats(stats)

    # Show session summary
    print("\n=== Session Summary ===")
    print(f"Mode: {practice_mode}")
    print(
        f"Time: {round(session_duration // 60)} min {round(session_duration % 60)} sec",
    )
    print(f"Digits correct: {session_correct_digits}")
    print(f"Maximum level: {session_max_level}")
    print(f"All-time best: {stats['max_digits']} digits")

    # Show mode-specific stats
    if practice_mode == "timed" and session_correct_digits > 0:
        speed = (session_correct_digits / session_duration) * 60
        print(f"Average speed: {speed:.1f} digits/minute")
        print(f"All-time best speed: {stats.get('best_speed', 0):.1f} digits/minute")


def input_digit() -> str:
    """Get a single digit of input from the user (non-blocking)."""
    import sys
    import termios

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


def main() -> None:
    """Parse command line arguments and perform calculations."""
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
    parser.add_argument("YOUR_PI", nargs="?", type=str, help="Your version of π")

    try:
        args = parser.parse_args()
    except (argparse.ArgumentError, SystemExit):
        # If this is help output, we don't need to report it as an error
        if "--help" in sys.argv or "-h" in sys.argv:
            sys.exit(0)
        logger.exception("Argument parsing failed")
        usage(1)

    # Handle version display
    if args.V:
        print(f"version: {VERSION}")
        sys.exit(0)

    # Handle practice mode
    if args.practice:
        # Determine visual aid setting
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

    # Handle stats display
    if args.stats:
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
                    f"  {i+1}. {session['date']} - {mode_str}Level {session['max_level']}"
                    f" ({session['correct_digits']} correct digits,"
                    f" {session['duration_seconds'] // 60}m {session['duration_seconds'] % 60}s)",
                )
        print("=================================")
        sys.exit(0)

    # Handle configuration
    if args.config:
        configure_practice_mode()
        sys.exit(0)

    # Show usage if no arguments provided
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
        except ValueError:
            logger.exception("pigame error: Invalid input")
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
