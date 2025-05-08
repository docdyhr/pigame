#!/usr/bin/env bash
# setup.sh - One-command setup script for PIGAME development environment
# This script sets up a complete development environment for PIGAME

set -euo pipefail

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
RESET="\033[0m"
BOLD="\033[1m"

# Function to print section headers
print_header() {
    echo -e "\n${BOLD}${YELLOW}===== $1 =====${RESET}\n"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}✓ $1${RESET}"
}

# Function to print error messages and exit
print_error() {
    echo -e "${RED}✗ $1${RESET}"
    exit 1
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Install system dependencies
install_dependencies() {
    local os
    os=$(detect_os)

    print_header "Installing system dependencies"

    case "$os" in
        linux)
            if command_exists apt-get; then
                echo "Detected Debian/Ubuntu system"
                sudo apt-get update
                sudo apt-get install -y bc build-essential clang clang-format shellcheck python3 python3-pip python3-venv
                print_success "System dependencies installed successfully"
            elif command_exists dnf; then
                echo "Detected Fedora/RHEL system"
                sudo dnf install -y bc gcc gcc-c++ clang clang-tools-extra ShellCheck python3 python3-pip
                print_success "System dependencies installed successfully"
            else
                print_error "Unsupported Linux distribution. Please install dependencies manually."
            fi
            ;;
        macos)
            if command_exists brew; then
                echo "Using Homebrew to install dependencies"
                brew install bc shellcheck clang-format python3
                print_success "System dependencies installed successfully"
            else
                echo "Homebrew not found. Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                brew install bc shellcheck clang-format python3
                print_success "Homebrew and system dependencies installed successfully"
            fi
            ;;
        windows)
            if command_exists choco; then
                echo "Using Chocolatey to install dependencies"
                choco install -y bc shellcheck llvm python3
                print_success "System dependencies installed successfully"
            else
                print_error "Chocolatey not found. Please install dependencies manually."
            fi
            ;;
        *)
            print_error "Unsupported operating system. Please install dependencies manually."
            ;;
    esac
}

# Setup Python environment
setup_python_env() {
    print_header "Setting up Python environment"

    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv .venv
        print_success "Virtual environment created"
    else
        echo "Virtual environment already exists"
    fi

    # Activate virtual environment
    if [ -f ".venv/bin/activate" ]; then
        echo "Activating virtual environment..."
        # shellcheck disable=SC1091
        source .venv/bin/activate
    elif [ -f ".venv/Scripts/activate" ]; then
        echo "Activating virtual environment..."
        # shellcheck disable=SC1091
        source .venv/Scripts/activate
    else
        print_error "Virtual environment activation script not found"
    fi

    # Install Python dependencies
    echo "Installing Python dependencies..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    python -m pip install -e .
    print_success "Python dependencies installed"
}

# Setup pre-commit hooks
setup_precommit() {
    print_header "Setting up pre-commit hooks"

    if ! command_exists pre-commit; then
        echo "Installing pre-commit..."
        python -m pip install pre-commit
    else
        echo "pre-commit already installed"
    fi

    echo "Installing git hooks..."
    pre-commit install
    print_success "pre-commit hooks installed"
}

# Build all implementations
build_all() {
    print_header "Building PIGAME"

    echo "Running make to build all implementations..."
    make build
    print_success "Build completed successfully"
}

# Run tests
run_tests() {
    print_header "Running tests"

    echo "Running tests for all implementations..."
    make test
    print_success "All tests passed"
}

# Main function
main() {
    print_header "PIGAME Development Environment Setup"

    # Navigate to project root
    cd "$(dirname "$0")/.." || print_error "Could not navigate to project root"

    # Check if required commands exist
    if ! command_exists python3; then
        print_error "Python 3 not found. Please install Python 3 before running this script."
    fi

    # Install dependencies
    install_dependencies

    # Setup Python environment
    setup_python_env

    # Setup pre-commit hooks
    setup_precommit

    # Build all implementations
    build_all

    # Run tests
    run_tests

    print_header "Setup Complete!"
    echo -e "Your PIGAME development environment is now ready."
    echo -e "To activate the virtual environment, run:"
    echo -e "    ${YELLOW}source .venv/bin/activate${RESET} (Linux/macOS)"
    echo -e "    ${YELLOW}.venv\\Scripts\\activate${RESET} (Windows)"
    echo -e "\nHappy coding!"
}

# Run the main function
main
