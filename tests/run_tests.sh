#!/usr/bin/env bash

# Main test runner for all pigame implementations

GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
RESET="\033[0m"

cd "$(dirname "$0")" || exit

# Make all test scripts executable
chmod +x ./*.sh

# Variables to track overall test results
TOTAL_TESTS_PASSED=0
TOTAL_TESTS_FAILED=0

# Run tests for each implementation
run_implementation_tests() {
    local implementation=$1
    local test_script=$2

    echo -e "${YELLOW}=== Testing $implementation implementation ===${RESET}"

    if [[ -x "$test_script" ]]; then
        # Run the test script
        if $test_script; then
            echo -e "${GREEN}All $implementation tests passed!${RESET}"
            return 0
        else
            echo -e "${RED}Some $implementation tests failed!${RESET}"
            return 1
        fi
    else
        echo -e "${RED}Test script not found or not executable: $test_script${RESET}"
        return 1
    fi
}

# Run Python unit tests
run_python_unit_tests() {
    echo -e "${YELLOW}=== Running Python unit tests ===${RESET}"

    if python3 ./test_python_unit.py -v; then
        echo -e "${GREEN}All Python unit tests passed!${RESET}"
        return 0
    else
        echo -e "${RED}Some Python unit tests failed!${RESET}"
        return 1
    fi
}

# Track test results
track_result() {
    local implementation=$1
    local result=$2

    if [[ $result -eq 0 ]]; then
        ((TOTAL_TESTS_PASSED++))
    else
        ((TOTAL_TESTS_FAILED++))
    fi
}

echo "Running all pigame tests..."
echo

# Run tests for each implementation
run_implementation_tests "Bash" "./test_bash.sh"
track_result "Bash" $?

run_implementation_tests "C" "./test_c.sh"
track_result "C" $?

run_implementation_tests "Python" "./test_python.sh"
track_result "Python" $?

run_python_unit_tests
track_result "Python unit tests" $?

# Print overall summary
echo
echo -e "${YELLOW}=======================================${RESET}"
echo -e "${YELLOW}=== Overall Test Summary ===${RESET}"
echo -e "${YELLOW}=======================================${RESET}"
echo "Implementations tested: 3"
echo "Test suites passed: $TOTAL_TESTS_PASSED"
echo "Test suites failed: $TOTAL_TESTS_FAILED"
echo -e "${YELLOW}=======================================${RESET}"

# Return appropriate exit code
if [[ $TOTAL_TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${RESET}"
    exit 0
else
    echo -e "${RED}Some tests failed!${RESET}"
    exit 1
fi
