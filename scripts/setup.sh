#!/usr/bin/env bash

# setup.sh - Unified setup script for pigame development environment
# This script sets up everything needed for development

set -e  # Exit immediately if a command exits with a non-zero status

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}=== Setting up pigame development environment ===${NC}"

# Get the repository root directory
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
cd "$REPO_ROOT" || exit 1

# Check for necessary tools
check_tool() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}$1 is required but not found.${NC}"
        if [ -n "$2" ]; then
            echo -e "${YELLOW}Install with: $2${NC}"
        fi
        return 1
    else
        echo -e "${GREEN}✓ Found $1${NC}"
        return 0
    fi
}

echo -e "\n${CYAN}Checking required tools...${NC}"
MISSING_TOOLS=0

# Check for basic tools
check_tool python3 "See https://www.python.org/downloads/" || MISSING_TOOLS=$((MISSING_TOOLS+1))
check_tool git "See https://git-scm.com/downloads" || MISSING_TOOLS=$((MISSING_TOOLS+1))

# Check for optional tools, but don't fail if not found
echo -e "\n${CYAN}Checking optional tools...${NC}"
check_tool gcc "apt install build-essential or brew install gcc" || echo -e "${YELLOW}⚠ C tests will be skipped${NC}"
check_tool bc "apt install bc or brew install bc" || echo -e "${YELLOW}⚠ Some tests may fail${NC}"
check_tool shellcheck "apt install shellcheck or brew install shellcheck" || echo -e "${YELLOW}⚠ Bash linting will be skipped${NC}"
check_tool clang-format "apt install clang-format or brew install clang-format" || echo -e "${YELLOW}⚠ C code formatting will be skipped${NC}"

if [ "$MISSING_TOOLS" -gt 0 ]; then
    echo -e "\n${RED}Some required tools are missing. Please install them and try again.${NC}"
    exit 1
fi

# Set up Python virtual environment
echo -e "\n${CYAN}Setting up Python virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓ Created virtual environment${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source .venv/Scripts/activate || {
        echo -e "${RED}Failed to activate virtual environment${NC}"
        exit 1
    }
else
    # Unix-like
    source .venv/bin/activate || {
        echo -e "${RED}Failed to activate virtual environment${NC}"
        exit 1
    }
fi

echo -e "${GREEN}✓ Activated virtual environment${NC}"

# Install dependencies
echo -e "\n${CYAN}Installing Python dependencies...${NC}"
python -m pip install --upgrade pip

# Ask if dev dependencies should be installed
INSTALL_DEV="n"
if [ -t 1 ]; then  # Check if running in interactive terminal
    read -p "Install development dependencies? (y/n) [n]: " INSTALL_DEV
fi

# Install appropriate dependencies
python -m pip install -r requirements.txt
if [[ "$INSTALL_DEV" =~ ^[Yy]$ ]]; then
    echo -e "${CYAN}Installing development dependencies...${NC}"
    python -m pip install -r requirements-dev.txt
    echo -e "${GREEN}✓ Installed development dependencies${NC}"
fi

# Install package in development mode
python -m pip install -e .
echo -e "${GREEN}✓ Installed Python dependencies${NC}"

# Set up pre-commit hooks
echo -e "\n${CYAN}Setting up pre-commit hooks...${NC}"
python -m pip install pre-commit
pre-commit install
echo -e "${GREEN}✓ Set up pre-commit hooks${NC}"

# Build C implementation
echo -e "\n${CYAN}Building C implementation...${NC}"
if command -v gcc &> /dev/null; then
    make build-c && echo -e "${GREEN}✓ Built C implementation${NC}" || echo -e "${YELLOW}⚠ Failed to build C implementation${NC}"
else
    echo -e "${YELLOW}⚠ Skipping C build (gcc not found)${NC}"
fi

# Make test scripts executable
echo -e "\n${CYAN}Making scripts executable...${NC}"
chmod +x src/bash/pigame.sh 2>/dev/null || echo -e "${YELLOW}⚠ Failed to make Bash script executable${NC}"
chmod +x src/python/pigame.py 2>/dev/null || echo -e "${YELLOW}⚠ Failed to make Python script executable${NC}"
chmod +x tests/*.sh 2>/dev/null || echo -e "${YELLOW}⚠ Failed to make test scripts executable${NC}"
chmod +x scripts/*.sh 2>/dev/null || echo -e "${YELLOW}⚠ Failed to make utility scripts executable${NC}"

echo -e "\n${GREEN}=== Development environment setup complete! ===${NC}"
echo -e "\n${CYAN}Next steps:${NC}"
echo -e "  * Run tests: ${YELLOW}./scripts/run_tests.sh${NC}"
echo -e "  * Run linting: ${YELLOW}./scripts/lint.sh${NC}" 
echo -e "  * Run the program: ${YELLOW}./pigame -h${NC}"
if [[ "$INSTALL_DEV" != *[Yy]* ]]; then
    echo -e "\n${YELLOW}Note: Development dependencies were not installed.${NC}"
    echo -e "To install them later: ${YELLOW}pip install -r requirements-dev.txt${NC}"
fi
echo -e "\n${CYAN}Happy coding!${NC}"