#!/bin/bash
# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

# Path to the pigame executable
PIGAME="../src/c/pigame"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name=$1
    local command=$2
    local expected_output=$3
    local actual_output

    echo -n "Running test: $test_name... "

    # Execute the command
    actual_output=$(eval "$command")

    # Check if the output matches the expected output
    if [[ "$actual_output" =~ $expected_output ]]; then
        echo -e "${GREEN}PASSED${RESET}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}FAILED${RESET}"
        echo "Expected: $expected_output"
        echo "Got: $actual_output"
        ((TESTS_FAILED++))
    fi
}

# First make sure the C version is compiled
cd "$(dirname "$0")" || exit
if [[ ! -x $PIGAME ]]; then
    echo "Compiling C implementation..."
    (cd ../src/c && gcc -o pigame pigame.c -lm -lgmp)
fi

# Run tests
echo "Running C implementation tests..."

# Version test
run_test "Version flag" \
    "$PIGAME -V" \
    "pigame version:"

# Help test
run_test "Help flag" \
    "$PIGAME -h" \
    "Usage:"

# Calculate pi test
run_test "Calculate pi (5 digits)" \
    "$PIGAME -p 5" \
    "3.14159"

# Easter egg tests
run_test "Easter egg (Archimedes)" \
    "$PIGAME Archimedes" \
    "Archimedes constant"

run_test "Easter egg (pi)" \
    "$PIGAME pi" \
    "π"

# Invalid input tests
run_test "Invalid input (abc)" \
    "$PIGAME abc" \
    "Invalid input"

run_test "Invalid input (3..14)" \
    "$PIGAME 3..14" \
    "Invalid input"

run_test "Invalid input (-3.14)" \
    "$PIGAME -3.14" \
    "Invalid input"

# Print summary
echo ""
echo "Tests completed:"
echo "Passed: $TESTS_PASSED"
echo "Failed: $TESTS_FAILED"

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${RESET}"
    exit 0
else
    exit 1
fi
