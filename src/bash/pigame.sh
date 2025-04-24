#!/usr/bin/env bash

# PIGAME - Test your memory of π digits
#
# Bash implementation using verified digits from trusted mathematical sources
# for perfect accuracy and consistent results across all implementations.
#
# Version: $(cat "$(dirname "$0")/../VERSION" 2>/dev/null || echo "1.6.12")
# Author: thomas@dyhr.com
# Date: April 2024

# shellcheck source=src/VERSION
VERSION=$(cat "$(dirname "$0")/../VERSION" 2>/dev/null || echo "1.6.12")

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

# Format PI with spaces for better readability
format_pi_with_spaces() {
    local pi_str="$1"
    local result=""
    
    # Add "3." to result
    result="${pi_str:0:2}"
    
    # Process the rest of the digits with spaces every 5 digits
    local remaining_digits="${pi_str:2}"
    local i=0
    while [[ $i -lt ${#remaining_digits} ]]; do
        # Add space after every 5 digits
        if ((i > 0 && i % 5 == 0)); then
            result="${result} "
        fi
        result="${result}${remaining_digits:$i:1}"
        ((i++))
    done
    
    echo "$result"
}

# Print to STDOUT
print_results() {
    # Format PI with spaces
    local formatted_pi
    formatted_pi=$(format_pi_with_spaces "${PI}")
    
    # Print results to STDOUT
    if [[ "${VERBOSE}" = 'true' ]]; then
        echo -e "π with ${DEC} decimals:\t${formatted_pi}"
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
        echo "${formatted_pi}"
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
        # Add space after every 5 digits for better readability
        if ((i > 1)) && (((i - 2) % 5 == 0)); then
            printf " "
        fi
        
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

# Verified digits of π from a trusted source
PI_DIGITS="141592653589793238462643383279502884197169399375105820974944592307816406286\
208998628034825342117067982148086513282306647093844609550582231725359408128\
481117450284102701938521105559644622948954930381964428810975665933446128475\
648233786783165271201909145648566923460348610454326648213393607260249141273\
724587006606315588174881520920962829254091715364367892590360011330530548820\
466521384146951941511609433057270365759591953092186117381932611793105118548\
074462379962749567351885752724891227938183011949129833673362440656643"

# Calculate π
calc_pi() {
    # Check if we need to truncate the result
    if [[ "${LENGTH}" -gt "${MAX_LENGTH}" ]]; then
        LENGTH="${MAX_LENGTH}"
    fi
    
    # Start with "3."
    result="3."
    
    # Add requested number of digits without extra whitespace
    result="${result}${PI_DIGITS:0:$((LENGTH-2))}"
    
    PI="${result}"
}

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

        # Format PI with spaces
        formatted_pi=$(format_pi_with_spaces "${PI}")
        
        if [[ "${VERBOSE}" = 'true' ]]; then
            echo -e "π with $((LENGTH - 2)) decimals:\t${formatted_pi}" # remove 2 decimals (calc_pi)
        else
            echo -e "${formatted_pi}"
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