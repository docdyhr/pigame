#!/usr/bin/env bash

# Test script for C implementation of pigame

GREEN="\033[0;32m"
RED="\033[0;31m"
RESET="\033[0m"

PIGAME="../src/c/pigame"
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

# First make sure the C version is compiled
cd "$(dirname "$0")"
if [[ ! -x $PIGAME ]]; then
    echo "Compiling C implementation..."
    (cd ../src/c && gcc -o pigame pigame.c -lm -lgmp)
fi

# Run tests

# Test 1: Version flag (-V)
run_test "Version flag" "$PIGAME -V" "version"

# Test 2: Basic pi calculation (low precision)
run_test "Pi calculation (5 decimals)" "$PIGAME -p 5" "3.14159"

# Test 3: Medium precision calculation (30 decimals)
run_test "Pi calculation (30 decimals)" "$PIGAME -p 30" "3.14159 26535 89793 23846 26433 83279"

# Test 4: High precision calculation (50 decimals)
run_test "Pi calculation (50 decimals)" "$PIGAME -p 50" "3.14159 26535 89793 23846 26433 83279 50288 41971 69399 37510"

# Test 5: Verify precision transitions
# The C implementation switches from hardcoded to Chudnovsky at 15 digits
run_test "Precision transition (15 decimals)" "$PIGAME -p 15" "3.14159 26535 89793"

# Test 6: Precision transition above hardcoded threshold
run_test "Precision transition (16 decimals)" "$PIGAME -p 16" "3.14159 26535 89793 2"

# Test 7: Test spacing in output with smaller numbers
run_test "Output spacing (10 decimals)" "$PIGAME -p 10" "3.14159 26535"

# Test 8: Correct input with verbose flag
run_test "Correct input with verbose" "$PIGAME -v 3.14159" "Well done"

# Test 9: Incorrect input with verbose flag
run_test "Incorrect input with verbose" "$PIGAME -v 3.14158" "You can do better!"

# Test 10: Correct input without verbose flag
run_test "Correct input without verbose" "$PIGAME 3.14159" "Match"

# Test 11: Incorrect input without verbose flag
run_test "Incorrect input without verbose" "$PIGAME 3.14158" "No match"

# Test 12: Invalid input
run_test "Invalid input" "$PIGAME abc 2>&1" "Invalid input"

# Test 13: Easter egg
run_test "Easter egg" "$PIGAME Archimedes" "Archimedes constant"

# Test 14: Color-blind mode with incorrect input
run_test "Color-blind mode incorrect input" "$PIGAME -c 3.14158 2>&1" "3.14159"

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