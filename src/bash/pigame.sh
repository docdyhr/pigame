#!/usr/bin/env bash

# This scripts calculates pi with bc and compares it with your version.

# Name: pigame
# Author: thomas@dyhr.com
# Date: 14. Jan 2022
# Version: $(cat "$(dirname "$0")/../VERSION" 2>/dev/null || echo "1.6.0")

# shellcheck source=src/VERSION
VERSION=$(cat "$(dirname "$0")/../VERSION" 2>/dev/null || echo "1.6.0")

# Default LENGTH of π: '3.141592653589793'
DEFAULT_LENGTH=15

# Max length of decimals for π for calc with bc
MAX_LENGTH=5001

# Print Usage
usage() {
    echo -e "Usage:\t$(basename "${0}") [-v] [-p LENGTH] [-V] [-c] YOUR_PI" >&2
    echo -e "\tEvaluate your version of π (3.141.. )" >&2
    echo -e '\t-v          Increase verbosity.' >&2
    echo -e '\t-p LENGTH   Calculate and show π with LENGTH number of decimals.' >&2
    echo -e '\t-V          Version.' >&2
    echo -e '\t-c          Color-blind mode (use underscores instead of color).' >&2
    exit 1
}

# YOUR_PI input validation: only float numbers are accepted
input_validation() {
    re='^[0-9]+([.][0-9]+)?$' # regex for an unsigned float number
    if ! [[ "${1}" =~ $re ]]; then
        echo "pigame error: Invalid input - NOT a float" >&2
        usage
    fi
    return 0
}

# Validation of LENGTH in -p option
length_validation() {
    # Validate -P ${OPTARG} is a number
    re='^-?[0-9]+$' # regex for an integer
    if ! [[ "${OPTARG}" =~ $re ]]; then
        echo "pigame error: Invalid input - NOT an integer" >&2
        usage
    fi
    # Set a max length for calc of π
    if [[ "${OPTARG}" -gt ${MAX_LENGTH} ]]; then
        echo "pigame error: Invalid input - too big a number for display" >&2
        usage
    fi

    return 0
}

# Print to STDOUT
print_results() {
    # Print results to STDOUT
    if [[ "${VERBOSE}" = 'true' ]]; then
        echo -e "π with ${DEC} decimals:\t${PI}"
        echo -e "Your version of π:\t$(color_your_pi)"
        if [[ "${PI}" == "${YOUR_PI}" ]]; then # NB! In BASH you can use = or == for comparison
            if [[ "${LENGTH}" -lt 15 ]]; then
                echo 'Well done.'
            else
                echo 'Perfect!'
            fi
        else
            echo -e 'You can do better!'
        fi
    else
        echo "${PI}"
        color_your_pi
        if [[ "${PI}" = "${YOUR_PI}" ]]; then
            echo 'Match'
        else
            echo 'No match'
        fi
    fi
}

# colorize mistakes in YOUR_PI if any
color_your_pi() {
    # Styling options
    local RED='\033[0;31m'
    local NO_COLOR='\033[0m' # No Color
    local UNDERLINE='\033[4m'

    # Reset Count number of errors
    local error_count=0

    # Loop over each character in $YOUR_PI and compare it to $PI
    for ((i = 0; i < ${#YOUR_PI}; i++)); do
        if [[ "${YOUR_PI:$i:1}" = "${PI:$i:1}" ]]; then
            printf "%s" "${YOUR_PI:$i:1}"
        else
            ((error_count++))
            if [[ "${COLOR_BLIND_MODE}" = 'true' ]]; then
                printf "${UNDERLINE}%s${NO_COLOR}" "${YOUR_PI:$i:1}"
            else
                printf "${RED}%s${NO_COLOR}" "${YOUR_PI:$i:1}"
            fi
        fi
    done
    echo # terminate printf
    if [[ "${VERBOSE}" = 'true' ]]; then
        echo "Number of errors: ${error_count}"
    fi
}

# Calculate π
calc_pi() {
    # Avoid rounding and keep precision of π's last decimal by
    # adding 2 decimals and truncate with substring parameter expansion

    # Calculate π with ${SCALE} number of decimals using bc
    if [[ "${LENGTH}" -lt 4 ]]; then
        PI=$(echo "scale=$((LENGTH + 2)); 4*a(1)" | bc -l) # Bash arithmetic expansion.
    else
        PI=$(echo "scale=${LENGTH}; 4*a(1)" | bc -l)
    fi

    # Truncate with substring parameter expansion 3. equals 2 ie. reuse $LENGTH
    PI="${PI:0:LENGTH}"
}

# Check if BC is available on the system
if ! command -v bc &>/dev/null; then
    echo "bc could not be found, see https://www.gnu.org/software/bc/bc.html" >&2
    exit 1
fi

# MENU: get command line options with Bash getopts
# first : indicates we handle errors ourselves
while getopts :vp:Vc OPTION; do
    case ${OPTION} in
    v)
        VERBOSE='true'
        ;;
    p)
        length_validation
        
        # Default value for -p = 15 decimals
        if [[ "${OPTARG}" -eq 0 ]]; then
            OPTARG="${DEFAULT_LENGTH}"
        fi

        LENGTH=$((OPTARG + 2)) # validate & calc_pi chops two decimals

        calc_pi

        if [[ "${VERBOSE}" = 'true' ]]; then
            echo -e "π with $((LENGTH - 2)) decimals:\t${PI}" # remove 2 decimals (calc_pi)
        else
            echo -e "${PI}"
        fi
        ;;
    V)
        echo "$(basename "${0}") version: ${VERSION} (https://github.com/docdyhr/pigame)"
        ;;
    c)
        COLOR_BLIND_MODE='true'
        ;;
    ?)
        usage
        ;;
    esac
done

# Remove the options while leaving the remaining arguments.
shift "$((OPTIND - 1))"

# Don't allow more than 1 parameter
if [[ "${#}" -gt 1 ]]; then
    echo 'pigame error: Invalid input (too many arguments)' >&2
    usage
# Allow 1 positional parameter: YOUR_PI
elif [[ "${#}" -eq 1 ]]; then
    # Easter egg
    if [[ "${1}" == "Archimedes" ]] || [[ "${1}" == "pi" ]] || [[ "${1}" == "PI" ]]; then
        echo 'π is also called Archimedes constant and is commonly defined as'
        echo 'the ratio of a circles circumference C to its diameter d:'
        echo 'π = C / d'
        exit 0
    fi
    # Input Validation: only float numbers are accepted
    input_validation "${1}"

    # User version of π
    YOUR_PI="${1}"

    # Number of decimals
    LENGTH=$(echo "${1}" | awk '{print length}')

    # π with $DEC number of decimals
    if [[ "${LENGTH}" -lt 4 ]]; then # account for 3.1
        DEC=${LENGTH}
    else
        DEC=$((LENGTH - 2)) # arithmetic expansion & chop 2 dec
    fi

    # Calculate π
    calc_pi

    # Print results to STDOUT
    print_results

    exit 0
else
    if [[ "${OPTIND}" -eq 1 ]]; then # OPTIND is 1 only when pigame has NO positional parameters
        usage
    fi
fi