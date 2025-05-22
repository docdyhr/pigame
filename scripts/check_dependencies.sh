#!/usr/bin/env bash
# check_dependencies.sh - Identify and check for pigame dependencies
# 
# This script checks if all required and recommended dependencies for pigame
# are installed on the system, and provides installation instructions for
# any missing dependencies.

set -e  # Exit immediately if a command exits with a non-zero status

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print header
echo -e "${CYAN}=== Checking pigame dependencies ===${NC}"

# Function to check if a command exists
check_command() {
    local cmd=$1
    local required=$2
    local install_instructions=$3
    
    if command -v "$cmd" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Found $cmd${NC}"
        return 0
    else
        if [ "$required" = "required" ]; then
            echo -e "${RED}✗ Missing required dependency: $cmd${NC}"
            echo -e "${YELLOW}   $install_instructions${NC}"
            MISSING_REQUIRED=$((MISSING_REQUIRED+1))
        else
            echo -e "${YELLOW}! Optional dependency not found: $cmd${NC}"
            echo -e "${YELLOW}   $install_instructions${NC}"
            MISSING_OPTIONAL=$((MISSING_OPTIONAL+1))
        fi
        return 1
    fi
}

# Initialize counters
MISSING_REQUIRED=0
MISSING_OPTIONAL=0

echo -e "\n${CYAN}Checking required dependencies:${NC}"
check_command "bash" "required" "Install bash (required for core functionality)"
check_command "bc" "required" "Install bc: 'apt install bc' or 'brew install bc' (required for calculations)"

echo -e "\n${CYAN}Checking optional dependencies:${NC}"
check_command "gcc" "optional" "Install gcc: 'apt install build-essential' or 'brew install gcc' (needed for C implementation)"
check_command "python3" "optional" "Install Python 3: see https://www.python.org/downloads/ (needed for Python implementation)"
check_command "shellcheck" "optional" "Install shellcheck: 'apt install shellcheck' or 'brew install shellcheck' (helpful for development)"
check_command "clang-format" "optional" "Install clang-format: 'apt install clang-format' or 'brew install clang-format' (helpful for development)"

# Check Python packages if Python is installed
if command -v python3 >/dev/null 2>&1; then
    echo -e "\n${CYAN}Checking Python environment:${NC}"
    if [ -d ".venv" ]; then
        echo -e "${GREEN}✓ Virtual environment exists${NC}"
    else
        echo -e "${YELLOW}! Virtual environment not found${NC}"
        echo -e "${YELLOW}   Run ./scripts/setup.sh to create it${NC}"
    fi
fi

# Summary
echo -e "\n${CYAN}=== Dependency Check Summary ===${NC}"
if [ $MISSING_REQUIRED -eq 0 ]; then
    echo -e "${GREEN}All required dependencies are installed.${NC}"
else
    echo -e "${RED}Missing $MISSING_REQUIRED required dependencies.${NC}"
fi

if [ $MISSING_OPTIONAL -gt 0 ]; then
    echo -e "${YELLOW}Missing $MISSING_OPTIONAL optional dependencies.${NC}"
    echo -e "${YELLOW}Some features may not be available.${NC}"
fi

# Exit with appropriate code
if [ $MISSING_REQUIRED -eq 0 ]; then
    echo -e "\n${GREEN}You're ready to use pigame!${NC}"
    exit 0
else
    echo -e "\n${RED}Please install the required dependencies.${NC}"
    exit 1
fi