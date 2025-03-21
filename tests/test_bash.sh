#!/usr/bin/env bash

# Test script for Bash implementation of pigame

GREEN="\033[0;32m"
RED="\033[0;31m"
RESET="\033[0m"

PIGAME="../src/bash/pigame.sh"
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name=$1
    local command=$2
    local expected_output=$3
    local actual_output

    echo -n "Running test: $test_name... "
    
    # Execute the command
    actual_output=$(eval "$command")
    
    # Check if the output matches the expected output
    if [[ "$actual_output" =~ "$expected_output" ]]; then
        echo -e "${GREEN}PASSED${RESET}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAILED${RESET}"
        echo "Expected output: '$expected_output'"
        echo "Actual output: '$actual_output'"
        ((TESTS_FAILED++))
    fi
}

# Run tests
cd "$(dirname "$0")"

# Test 1: Version flag (-V)
run_test "Version flag" "$PIGAME -V" "version"

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

# Print summary
echo "---------------------------------------"
echo "Test summary:"
echo "Passed: $TESTS_PASSED"
echo "Failed: $TESTS_FAILED"
echo "Total: $((TESTS_PASSED + TESTS_FAILED))"
echo "---------------------------------------"

# Return appropriate exit code
if [[ $TESTS_FAILED -eq 0 ]]; then
    exit 0
else
    exit 1
fi