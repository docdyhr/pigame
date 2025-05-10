#!/usr/bin/env bash

# Unified linting script for both local development and CI
# This ensures consistency between pre-commit hooks and CI pipeline

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

echo -e "${CYAN}=== Running unified linting checks ===${NC}"

# Initialize flags to track failures
PYTHON_LINT_FAILED=0
BASH_LINT_FAILED=0
C_LINT_FAILED=0
ANY_FAILURES=0

# Function to run a check and track its result
run_check() {
    local name="$1"
    local cmd="$2"
    
    echo -e "\n${CYAN}Running $name check...${NC}"
    if eval "$cmd"; then
        echo -e "${GREEN}✓ $name check passed${NC}"
        return 0
    else
        echo -e "${RED}✗ $name check failed${NC}"
        ANY_FAILURES=1
        return 1
    fi
}

# Python checks
if command -v ruff &> /dev/null; then
    run_check "Ruff linting" "ruff check src/python/ tests/ --fix || exit 1"
    run_check "Ruff formatting" "ruff format src/python/ tests/ || exit 1"
else
    echo -e "${YELLOW}⚠ Ruff not found, skipping Python checks${NC}"
    echo -e "${YELLOW}  Install with: pip install ruff${NC}"
    PYTHON_LINT_FAILED=1
fi

# Bash checks
if command -v shellcheck &> /dev/null; then
    run_check "ShellCheck" "shellcheck src/bash/*.sh scripts/*.sh || exit 1"
else
    echo -e "${YELLOW}⚠ ShellCheck not found, skipping Bash checks${NC}"
    echo -e "${YELLOW}  Install with: apt-get install shellcheck or brew install shellcheck${NC}"
    BASH_LINT_FAILED=1
fi

# C code checks
if command -v clang-format &> /dev/null; then
    # Create a copy of the C files before formatting
    mkdir -p /tmp/c-orig
    find src/c -name "*.c" -o -name "*.h" | xargs -I{} cp {} /tmp/c-orig/ 2>/dev/null || true
    
    # Apply formatting
    find src/c -name "*.c" -o -name "*.h" | xargs clang-format -i --style=file 2>/dev/null || true
    
    # Show diffs but don't fail the build
    C_FILES=$(find src/c -name "*.c" -o -name "*.h" 2>/dev/null || echo "")
    if [ -n "$C_FILES" ]; then
        for file in $C_FILES; do
            filename=$(basename "$file")
            if [ -f "/tmp/c-orig/$filename" ]; then
                if ! diff -u "/tmp/c-orig/$filename" "$file" > /dev/null; then
                    echo -e "${YELLOW}→ Formatting applied to $filename${NC}"
                fi
            fi
        done
    fi
else
    echo -e "${YELLOW}⚠ clang-format not found, skipping C formatting${NC}"
    echo -e "${YELLOW}  Install with: apt-get install clang-format or brew install clang-format${NC}"
    C_LINT_FAILED=1
fi

# Check for trailing whitespace, fix end of files
echo -e "\n${CYAN}Checking for trailing whitespace and fixing file endings...${NC}"
if command -v git &> /dev/null; then
    git ls-files | xargs sed -i 's/[[:space:]]*$//' 2>/dev/null || true
    
    # Ensure files end with a newline
    git ls-files | while read -r file; do
        if [ -f "$file" ] && [ -s "$file" ] && [ "$(tail -c 1 "$file" | wc -l)" -eq 0 ]; then
            echo "" >> "$file"
        fi
    done
else
    echo -e "${YELLOW}⚠ git not available to list files${NC}"
fi

# Summary
echo -e "\n${CYAN}=== Linting summary ===${NC}"

if [ $ANY_FAILURES -eq 0 ]; then
    echo -e "${GREEN}All checks passed!${NC}"
    exit 0
else
    echo -e "${RED}Some checks failed. Please fix the issues before committing.${NC}"
    exit 1
fi