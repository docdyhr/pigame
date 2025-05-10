#!/usr/bin/env bash

# Unified test script for both local development and CI
# This ensures consistency between local development and CI pipeline

set -e  # Exit immediately if a command exits with a non-zero status

# Get the repository root directory
REPO_ROOT=$(git rev-parse --show-toplevel || echo ".")
cd "$REPO_ROOT" || exit 1

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
RUN_BASH_TESTS=true
RUN_C_TESTS=true
RUN_PYTHON_TESTS=true
RUN_COVERAGE=true

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-bash)
            RUN_BASH_TESTS=false
            shift
            ;;
        --no-c)
            RUN_C_TESTS=false
            shift
            ;;
        --no-python)
            RUN_PYTHON_TESTS=false
            shift
            ;;
        --no-coverage)
            RUN_COVERAGE=false
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --no-bash     Skip Bash tests"
            echo "  --no-c        Skip C tests"
            echo "  --no-python   Skip Python tests"
            echo "  --no-coverage Skip coverage report generation"
            echo "  --help        Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "${CYAN}=== Running unified test suite ===${NC}"

# Initialize flags to track failures
BASH_TESTS_FAILED=0
C_TESTS_FAILED=0
PYTHON_TESTS_FAILED=0
COVERAGE_FAILED=0
ANY_FAILURES=0

# Function to run a test suite and track its result
run_test() {
    local name="$1"
    local cmd="$2"
    
    echo -e "\n${CYAN}Running $name tests...${NC}"
    if eval "$cmd"; then
        echo -e "${GREEN}✓ $name tests passed${NC}"
        return 0
    else
        echo -e "${RED}✗ $name tests failed${NC}"
        ANY_FAILURES=1
        return 1
    fi
}

# Set up Python virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo -e "${CYAN}Setting up Python virtual environment...${NC}"
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    python -m pip install -e .
else
    source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null || true
fi

# Build C implementation if needed
if [ "$RUN_C_TESTS" = true ]; then
    echo -e "${CYAN}Building C implementation...${NC}"
    make build-c || {
        echo -e "${YELLOW}⚠ Failed to build C implementation, skipping C tests${NC}"
        RUN_C_TESTS=false
        C_TESTS_FAILED=1
        ANY_FAILURES=1
    }
fi

# Run Bash tests
if [ "$RUN_BASH_TESTS" = true ]; then
    if command -v bash &> /dev/null; then
        chmod +x src/bash/pigame.sh 2>/dev/null || true
        chmod +x tests/test_bash.sh 2>/dev/null || true
        run_test "Bash" "tests/test_bash.sh" || BASH_TESTS_FAILED=1
    else
        echo -e "${YELLOW}⚠ Bash not available, skipping Bash tests${NC}"
        BASH_TESTS_FAILED=1
    fi
fi

# Run C tests
if [ "$RUN_C_TESTS" = true ]; then
    chmod +x tests/test_c.sh 2>/dev/null || true
    run_test "C" "tests/test_c.sh" || C_TESTS_FAILED=1
fi

# Run Python tests
if [ "$RUN_PYTHON_TESTS" = true ]; then
    chmod +x src/python/pigame.py 2>/dev/null || true
    chmod +x tests/test_python.sh 2>/dev/null || true
    run_test "Python" "tests/test_python.sh" || PYTHON_TESTS_FAILED=1
    
    # Run Python unit tests
    run_test "Python unit" "python tests/test_python_unit.py -v" || PYTHON_TESTS_FAILED=1
fi

# Generate coverage report
if [ "$RUN_COVERAGE" = true ] && [ "$RUN_PYTHON_TESTS" = true ]; then
    echo -e "\n${CYAN}Generating coverage report...${NC}"
    
    # Create coverage directory if it doesn't exist
    mkdir -p htmlcov
    
    # Run pytest with coverage
    if pytest tests/test_pytest.py -v --cov=src/python --cov-report=term-missing --cov-report=html --cov-report=xml; then
        echo -e "${GREEN}✓ Coverage report generated successfully${NC}"
    else
        echo -e "${YELLOW}⚠ Coverage report generation failed${NC}"
        COVERAGE_FAILED=1
        ANY_FAILURES=1
    fi
    
    # Ensure coverage file exists even if tests failed
    if [ ! -f "coverage.xml" ]; then
        echo '<?xml version="1.0" ?><coverage version="1.0"></coverage>' > coverage.xml
    fi
fi

# Summary
echo -e "\n${CYAN}=== Test summary ===${NC}"

if [ "$RUN_BASH_TESTS" = true ]; then
    if [ "$BASH_TESTS_FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ Bash tests: PASSED${NC}"
    else
        echo -e "${RED}✗ Bash tests: FAILED${NC}"
    fi
fi

if [ "$RUN_C_TESTS" = true ]; then
    if [ "$C_TESTS_FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ C tests: PASSED${NC}"
    else
        echo -e "${RED}✗ C tests: FAILED${NC}"
    fi
fi

if [ "$RUN_PYTHON_TESTS" = true ]; then
    if [ "$PYTHON_TESTS_FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ Python tests: PASSED${NC}"
    else
        echo -e "${RED}✗ Python tests: FAILED${NC}"
    fi
fi

if [ "$RUN_COVERAGE" = true ] && [ "$RUN_PYTHON_TESTS" = true ]; then
    if [ "$COVERAGE_FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓ Coverage report: GENERATED${NC}"
    else
        echo -e "${YELLOW}⚠ Coverage report: INCOMPLETE${NC}"
    fi
fi

echo -e "\n${CYAN}=== Overall result ===${NC}"
if [ "$ANY_FAILURES" -eq 0 ]; then
    echo -e "${GREEN}All tests passed successfully!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. See above for details.${NC}"
    exit 1
fi