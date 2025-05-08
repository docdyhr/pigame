#!/usr/bin/env bash

# Test script for Python implementation of pigame
set -euo pipefail

GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
RESET="\033[0m"

PIGAME="../src/python/pigame.py"
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name=$1
    local command=$2
    local expected_output=$3
    local actual_output

    echo -e "${YELLOW}Running test:${RESET} $test_name... "

    # Execute the command and capture output
    if ! actual_output=$(eval "$command" 2>&1); then
        if [[ "$command" =~ "Invalid input" ]]; then
            # Expected failure for invalid input test
            if [[ "$actual_output" =~ $expected_output ]]; then
                echo -e "${GREEN}PASSED${RESET}"
                ((TESTS_PASSED++))
                return 0
            fi
        fi
        echo -e "${RED}FAILED${RESET} (command failed)"
        echo "Expected output: '$expected_output'"
        echo "Actual output: '$actual_output'"
        ((TESTS_FAILED++))
        return 1
    fi

    # Strip ANSI color codes for comparison
    stripped_output=$(echo "$actual_output" | sed 's/\x1b\[[0-9;]*m//g')
    
    # Check if the output matches the expected output
    if [[ "$stripped_output" =~ $expected_output ]]; then
        echo -e "${GREEN}PASSED${RESET}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAILED${RESET}"
        echo "Expected output: '$expected_output'"
        echo "Actual output: '$actual_output'"
        echo "Stripped output: '$stripped_output'"
        ((TESTS_FAILED++))
    fi
}

# Ensure we're in the correct directory
cd "$(dirname "$0")" || exit 1

# Make sure the script is executable
chmod 700 "$PIGAME"

# Test 1: Version flag (-V)
run_test "Version flag" "$PIGAME -V" "version: [0-9]+\.[0-9]+\.[0-9]+"

# Test 2: Pi calculation with 5 decimals
run_test "Pi calculation (5 decimals)" "$PIGAME -p 5" "3.14159"

# Test 3: Correct input with verbose flag
run_test "Correct input with verbose" "$PIGAME -v 3.14159" "Well done"

# Test 4: Incorrect input with verbose flag
run_test "Incorrect input with verbose" "$PIGAME -v 3.14158" "You can do better!"

# Test 5: Correct input without verbose flag
run_test "Correct input without verbose" "$PIGAME 3.14159" "Match"

# Test 6: Incorrect input without verbose flag
run_test "Incorrect input without verbose" "$PIGAME 3.14158" "No match"

# Test 7: Invalid input
run_test "Invalid input" "$PIGAME abc 2>&1" "Invalid input"

# Test 8: Easter egg
run_test "Easter egg" "$PIGAME Archimedes" "Archimedes constant"

# Print summary with improved formatting
set +e # Disable exit on error for summary and exit logic

echo -e "\n${YELLOW}---------------------------------------${RESET}"
echo -e "${YELLOW}Test summary:${RESET}"
echo -e "Passed: ${GREEN}$TESTS_PASSED${RESET}"
echo -e "Failed: ${RED}$TESTS_FAILED${RESET}"
echo -e "Total:  $((TESTS_PASSED + TESTS_FAILED))"
echo -e "${YELLOW}---------------------------------------${RESET}"

# Return appropriate exit code
if [[ $TESTS_FAILED -eq 0 ]]; then
    exit 0
else
    exit 1
fi
