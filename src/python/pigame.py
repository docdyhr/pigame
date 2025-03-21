#!/usr/bin/env python3

import argparse
import os
import re
import sys
from math import pi

# Read version from file or use default
def get_version():
    try:
        version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "VERSION")
        with open(version_file, "r") as f:
            return f.read().strip()
    except:
        return "1.6.0"

VERSION = get_version()
DEFAULT_LENGTH = 15
MAX_LENGTH = 5001


def usage():
    """
    Print the usage information for the pigame script.
    """
    print(f"Usage: {sys.argv[0]} [-v] [-p LENGTH] [-V] YOUR_PI", file=sys.stderr)
    print("\tEvaluate your version of π (3.141.. )", file=sys.stderr)
    print("\t-v          Increase verbosity.", file=sys.stderr)
    print("\t-p LENGTH   Calculate and show π with LENGTH number of decimals.", file=sys.stderr)
    print("\t-V          Version.", file=sys.stderr)
    sys.exit(1)


def input_validation(pi_input: str) -> None:
    """
    Validates the input to ensure it is a float.

    Args:
        pi_input (str): The input to be validated.

    Raises:
        SystemExit: If the input is not a valid float.
    """
    if not re.match(r"^[0-9]+(\.[0-9]+)?$", pi_input):
        print("pigame error: Invalid input - NOT a float", file=sys.stderr)
        usage()


def length_validation(length_str: str) -> int:
    """
    Validates the length input.

    Args:
        length_str (str): The input length to be validated.

    Returns:
        int: The validated length.

    Raises:
        SystemExit: If the input is not a valid integer or if it is too big.
    """
    try:
        length = int(length_str)
    except ValueError:
        print("pigame error: Invalid input - NOT an integer", file=sys.stderr)
        usage()

    if length <= 0:
        # Default value if 0
        return DEFAULT_LENGTH
    elif length > MAX_LENGTH:
        print("pigame error: Invalid input - too big a number for display", file=sys.stderr)
        usage()

    return length


def calculate_pi(length: int) -> str:
    """
    Calculate the value of pi with a specified decimal length.

    Parameters:
    - length (int): The number of decimal places to calculate pi.

    Returns:
    - str: The value of pi formatted as a string with the specified decimal length.
    """
    # Format pi to the required precision
    format_string = f"{{:.{length+2}f}}".format(pi)
    # Remove leading "3." if present and trim to exact length needed
    if format_string.startswith("3."):
        digits = format_string[2:]
    else:
        digits = format_string.replace(".", "")
    
    return f"3.{digits[:length]}"


def color_your_pi(user_pi: str, calculated_pi: str, verbose: bool) -> int:
    """
    Colors the digits of user_pi that do not match the corresponding digits of calculated_pi in red.

    Args:
        user_pi (str): The user's input of pi digits.
        calculated_pi (str): The calculated pi digits.
        verbose (bool): If True, prints the number of errors.

    Returns:
        int: The number of errors found.
    """
    RED = "\033[0;31m"
    NO_COLOR = "\033[0m"
    error_count = 0
    result = []

    for i, digit in enumerate(user_pi):
        if i < len(calculated_pi) and digit == calculated_pi[i]:
            result.append(digit)
        else:
            error_count += 1
            result.append(f"{RED}{digit}{NO_COLOR}")

    print("".join(result))
    if verbose:
        print(f"Number of errors: {error_count}")
    
    return error_count


def print_results(user_pi: str, calculated_pi: str, decimals: int, verbose: bool) -> None:
    """
    Print the results of the pi calculation.

    Parameters:
    - user_pi (str): The user's version of pi.
    - calculated_pi (str): The calculated value of pi.
    - decimals (int): The number of decimals to display.
    - verbose (bool): If True, display additional information.
    """
    if verbose:
        print(f"π with {decimals} decimals:\t{calculated_pi}")
        print("Your version of π:\t", end="")
        
    error_count = color_your_pi(user_pi, calculated_pi, verbose)
    
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
    parser.add_argument(
        "YOUR_PI", nargs="?", type=str, help="Your version of π"
    )

    try:
        args = parser.parse_args()
    except:
        usage()

    if args.V:
        print(f"{os.path.basename(sys.argv[0])} version: {VERSION} (https://github.com/docdyhr/pigame)")
        sys.exit(0)

    if not args.YOUR_PI and not args.p and not args.v:
        usage()

    # Handle the -p option
    if args.p:
        length = length_validation(args.p)
        calculated_pi = calculate_pi(length)
        
        if args.v:
            print(f"π with {length} decimals:\t{calculated_pi}")
        else:
            print(calculated_pi)
        
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
        
        print_results(user_pi, calculated_pi, decimals, args.v)


if __name__ == "__main__":
    main()