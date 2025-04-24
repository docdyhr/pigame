#!/usr/bin/env python3
"""
PIGAME - Test your memory of π digits

Python implementation using verified digits from trusted mathematical sources
for perfect accuracy and consistent results across all implementations.

Version: (see VERSION file)
Author: Thomas J. Dyhr
Date: April 2024
"""

import argparse
import os
import re
import sys

# Read version from file or use default
def get_version():
    """Read version from VERSION file or return default version."""
    try:
        version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "VERSION")
        with open(version_file, "r") as f:
            return f.read().strip()
    except (IOError, OSError):
        return "1.6.0"

VERSION = get_version()
DEFAULT_LENGTH = 15
MAX_LENGTH = 5001


def usage():
    """
    Print the usage information for the pigame script.
    """
    print(f"Usage: {sys.argv[0]} [-v] [-p LENGTH] [-V] [-c] YOUR_PI", file=sys.stderr)
    print("\tEvaluate your version of π (3.141.. )", file=sys.stderr)
    print("\t-v          Increase verbosity.", file=sys.stderr)
    print("\t-p LENGTH   Calculate and show π with LENGTH number of decimals.", file=sys.stderr)
    print("\t-V          Version.", file=sys.stderr)
    print("\t-c          Color-blind mode (use underscores instead of color).", file=sys.stderr)
    sys.exit(1)


def input_validation(pi_input: str) -> None:
    """
    Validates the input to ensure it is a float.

    Args:
        pi_input (str): The input to be validated.

    Raises:
        SystemExit: If the input is not a valid float.
        ValueError: For testing purposes when the input is invalid.
    """
    if not re.match(r"^[0-9]+(\.[0-9]+)?$", pi_input):
        print("pigame error: Invalid input - NOT a float", file=sys.stderr)
        usage()
        # For unit tests
        raise ValueError("Input is not a valid float")


def length_validation(length_str: str) -> int:
    """
    Validates the length input.

    Args:
        length_str (str): The input length to be validated.

    Returns:
        int: The validated length.

    Raises:
        SystemExit: If the input is not a valid integer or if it is too big.
        ValueError: If the input cannot be converted to an integer.
    """
    # First check if the input is a valid integer
    if not re.match(r"^-?[0-9]+$", length_str):
        print("pigame error: Invalid input - NOT an integer", file=sys.stderr)
        usage()
        # For unit tests, raise ValueError explicitly
        raise ValueError("Input is not an integer")
        
    # Convert to integer
    length = int(length_str)

    # Check range
    if length <= 0:
        # Default value if 0
        return DEFAULT_LENGTH
    elif length > MAX_LENGTH:
        print("pigame error: Invalid input - too big a number for display", file=sys.stderr)
        usage()
        # For unit tests
        raise SystemExit("Input is too large")

    return length


def calculate_pi(length: int) -> str:
    """
    Return pi digits from a verified source.

    Parameters:
    - length (int): The number of decimal places to return.

    Returns:
    - str: The value of pi with the specified decimal length.

    Raises:
    - ValueError: If length is negative
    """
    # Verified digits of π from a trusted source
    PI_DIGITS = (
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
    digits = PI_DIGITS[:length]
    if len(digits) < length:
        raise ValueError(f"Requested {length} digits but only {len(digits)} are available")
    
    # Return "3." + digits
    return f"3.{digits}"


def format_pi_with_spaces(pi_str: str) -> str:
    """
    Format pi with spaces every 5 digits for better readability.
    
    Args:
        pi_str (str): The pi string to format.
        
    Returns:
        str: The formatted pi string with spaces.
    """
    # Start with the first 2 characters "3."
    result = pi_str[:2]
    
    # Add the rest with spaces every 5 digits
    for i, digit in enumerate(pi_str[2:]):
        # Add space after every 5 digits
        if i > 0 and i % 5 == 0:
            result += " "
        result += digit
    
    return result


def color_your_pi(user_pi: str, calculated_pi: str, verbose: bool, colorblind_mode: bool = False) -> int:
    """
    Colors the digits of user_pi that do not match the corresponding digits of calculated_pi in red.
    Or uses underlines in colorblind mode.

    Args:
        user_pi (str): The user's input of pi digits.
        calculated_pi (str): The calculated pi digits.
        verbose (bool): If True, prints the number of errors.
        colorblind_mode (bool): If True, uses underlines instead of color.

    Returns:
        int: The number of errors found.
    """
    RED = "\033[0;31m"
    UNDERLINE = "\033[4m"
    NO_COLOR = "\033[0m"
    error_count = 0
    result = []

    for i, digit in enumerate(user_pi):
        # Add space after every 5 digits for better readability (after the "3.")
        if i > 1 and (i - 2) % 5 == 0:
            result.append(" ")
            
        if i < len(calculated_pi) and digit == calculated_pi[i]:
            result.append(digit)
        else:
            error_count += 1
            if colorblind_mode:
                result.append(f"{UNDERLINE}{digit}{NO_COLOR}")
            else:
                result.append(f"{RED}{digit}{NO_COLOR}")

    print("".join(result))
    if verbose:
        print(f"Number of errors: {error_count}")
    
    return error_count


def print_results(user_pi: str, calculated_pi: str, decimals: int, verbose: bool, colorblind_mode: bool = False) -> None:
    """
    Print the results of the pi calculation.

    Parameters:
    - user_pi (str): The user's version of pi.
    - calculated_pi (str): The calculated value of pi.
    - decimals (int): The number of decimals to display.
    - verbose (bool): If True, display additional information.
    - colorblind_mode (bool): If True, uses underlines instead of color.
    """
    # Format pi with spaces for better readability
    formatted_pi = format_pi_with_spaces(calculated_pi)
    
    if verbose:
        print(f"π with {decimals} decimals:\t{formatted_pi}")
        print("Your version of π:\t", end="")
        
    color_your_pi(user_pi, calculated_pi, verbose, colorblind_mode)
    
    if calculated_pi == user_pi:
        if verbose:
            if decimals < 15:
                print("Well done.")
            else:
                print("Perfect!")
        else:
            print("Match")
    else:
        if verbose:
            print("You can do better!")
        else:
            print("No match")


def handle_easter_egg(input_str: str) -> bool:
    """
    Handle easter egg inputs like "Archimedes" or "pi".

    Args:
        input_str (str): The input to check for easter eggs.

    Returns:
        bool: True if the input was an easter egg and was handled, False otherwise.
    """
    if input_str in ["Archimedes", "pi", "PI"]:
        print("π is also called Archimedes constant and is commonly defined as")
        print("the ratio of a circles circumference C to its diameter d:")
        print("π = C / d")
        return True
    return False


def main():
    """
    Main function for the pigame.py script.

    Parses command line arguments and performs calculations based on the provided arguments.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-v", action="store_true", help="Increase verbosity.")
    parser.add_argument(
        "-p", 
        type=str,
        help="Calculate and show π with LENGTH number of decimals.",
    )
    parser.add_argument("-V", action="store_true", help="Version.")
    parser.add_argument("-c", action="store_true", help="Color-blind mode (use underscores instead of color).")
    parser.add_argument(
        "YOUR_PI", nargs="?", type=str, help="Your version of π"
    )

    try:
        args = parser.parse_args()
    except (argparse.ArgumentError, SystemExit):
        usage()

    if args.V:
        print(f"{os.path.basename(sys.argv[0])} version: {VERSION} (https://github.com/docdyhr/pigame)")
        sys.exit(0)

    if not args.YOUR_PI and not args.p and not args.v and not args.c:
        usage()

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
        input_validation(args.YOUR_PI)
        user_pi = args.YOUR_PI
        
        # If -p was not provided, determine length from user_pi
        if not args.p:
            # Number of decimals is length - 2 (for "3.")
            decimals = len(user_pi) - 2 if len(user_pi) >= 3 else len(user_pi)
            calculated_pi = calculate_pi(decimals)
        else:
            decimals = length
            calculated_pi = calculate_pi(decimals)
        
        print_results(user_pi, calculated_pi, decimals, args.v, args.c)


if __name__ == "__main__":
    main()