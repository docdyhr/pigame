#!/usr/bin/env python3

import argparse
import re
import sys
from math import pi

VERSION = "1.5.1"
DEFAULT_LENGTH = 15
MAX_LENGTH = 5001


def usage():
    """
    Print the usage information for the pigame script.

    Usage: pigame.py [-v] [-p LENGTH] [-V] YOUR_PI

    Options:
    -v          Increase verbosity.
    -p LENGTH   Calculate and show π with LENGTH number of decimals.
    -V          Version.
    """
    print(f"Usage: {sys.argv[0]} [-v] [-p LENGTH] [-V] YOUR_PI")
    print("\tEvaluate your version of π (3.141.. )")
    print("\t-v          Increase verbosity.")
    print("\t-p LENGTH   Calculate and show π with LENGTH number of decimals.")
    print("\t-V          Version.")
    sys.exit(1)


def input_validation(pi_input: str):
    """
    Validates the input to ensure it is a float.

    Args:
        pi_input (str): The input to be validated.

    Raises:
        None

    Returns:
        None
    """
    if not re.match(r"^[0-9]+(\.[0-9]+)?$", pi_input):
        print("pigame error: Invalid input - NOT a float", file=sys.stderr)
        usage()


def length_validation(length: str) -> int:
    """
    Validates the length input.

    Args:
        length (str): The input length to be validated.

    Returns:
        int: The validated length.

    Raises:
        ValueError: If the input is not a valid integer or if it is too big.

    """
    if not re.match(r"^-?[0-9]+$", length):
        print("pigame error: Invalid input - NOT an integer", file=sys.stderr)
        usage()
        try:
            length = int(length)
        except ValueError:
            print(
                "pigame error: Invalid input - NOT an integer", file=sys.stderr
            )
            usage()

        if length > MAX_LENGTH:
            print(
                "pigame error: Invalid input - too big a number for display",
                file=sys.stderr,
            )
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
    format_string = "{:." + str(length) + "f}"
    return format_string.format(pi)


def color_your_pi(user_pi: str, calculated_pi: str, verbose: bool):
    """
    Colors the digits of user_pi that do not match the corresponding digits of calculated_pi in red.

    Args:
        user_pi (str): The user's input of pi digits.
        calculated_pi (str): The calculated pi digits.
        verbose (bool): If True, prints the colored pi digits and the number of errors. If False, only prints the colored pi digits.

    Returns:
        None
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

    if verbose:
        print("".join(result))
        print(f"Number of errors: {error_count}")
    else:
        print("".join(result))


def print_results(
    user_pi: str, calculated_pi: str, decimals: int, verbose: bool
):
    """
    Print the results of the pi calculation.

    Parameters:
    - user_pi (str): The user's version of pi.
    - calculated_pi (str): The calculated value of pi.
    - decimals (int): The number of decimals to display.
    - verbose (bool): If True, display additional information.

    Returns:
    None
    """
    if verbose:
        print(f"π with {decimals} decimals:\t{calculated_pi}")
        print("Your version of π:\t", end="")
        color_your_pi(user_pi, calculated_pi, verbose)
        if calculated_pi == user_pi:
            if decimals < 15:
                print("Well done.")
            else:
                print("Perfect!")
        else:
            print("You can do better!")
    else:
        print(calculated_pi)
        color_your_pi(user_pi, calculated_pi, verbose)
        if calculated_pi == user_pi:
            print("Match")
        else:
            print("No match")


def main():
    """
    Main function for the pigame.py script.

    Parses command line arguments and performs calculations based on the provided arguments.

    Args:
        -v (bool): Increase verbosity.
        -p (int): Calculate and show π with LENGTH number of decimals.
        -V (bool): Version.
        YOUR_PI (str): Your version of π.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-v", action="store_true", help="Increase verbosity.")
    parser.add_argument(
        "-p",
        type=int,
        help="Calculate and show π with LENGTH number of decimals.",
    )
    parser.add_argument("-V", action="store_true", help="Version.")
    parser.add_argument(
        "YOUR_PI", nargs="?", type=str, help="Your version of π"
    )

    args = parser.parse_args()

    if args.V:
        print(
            f"{sys.argv[0]} version: {VERSION} (https://github.com/docdyhr/pigame)"
        )
        sys.exit(0)

    if not args.YOUR_PI and not args.p:
        usage()

    length = args.p if args.p else DEFAULT_LENGTH
    length = length_validation(str(length))

    calculated_pi = calculate_pi(length)
    if args.v:
        print(f"π with {length} decimals:\t{calculated_pi}")
    else:
        print(calculated_pi)

    if args.YOUR_PI:
        input_validation(args.YOUR_PI)
        user_pi = args.YOUR_PI
        print_results(user_pi, calculated_pi, length, args.v)


if __name__ == "__main__":
    main()
