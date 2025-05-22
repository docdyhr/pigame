# PIGAME - How many decimals of π can you remember?

[![CI/CD Pipeline](https://github.com/docdyhr/pigame/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/docdyhr/pigame/actions/workflows/ci.yml)
[![Test Coverage](https://img.shields.io/codecov/c/github/docdyhr/pigame)](https://codecov.io/gh/docdyhr/pigame)
[![Version](https://img.shields.io/badge/version-1.9.7-blue)](https://github.com/docdyhr/pigame/blob/master/src/VERSION)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/docdyhr/pigame/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/docdyhr/pigame/blob/master/CONTRIBUTING.md)

## Overview

* Version: 1.9.7
* Multiple implementations available: Bash (original), C, and Python
* Author: Thomas J. Dyhr
* Purpose: Memorisation of π
* Release date: 26. Apr 2025

## Usage

```shell
pigame [-v] [-p LENGTH] [-V] [-c] [--practice] [--stats] YOUR_PI
```

Evaluate your version of π (3.141.. )

* `-v` Increase verbosity.
* `-p LENGTH` Calculate and show π with LENGTH number of decimals.
* `-V` Version.
* `-c` Color-blind mode (use underscores instead of color).
* `--practice` Start interactive practice mode for memorizing digits.
* `--practice-mode [standard|timed|chunk]` Select practice mode strategy.
* `--min-digits N` Set minimum starting digits for practice.
* `--max-digits N` Set maximum digits to practice.
* `--chunk-size N` Set size of chunks in chunk practice mode.
* `--time-limit N` Set time limit in seconds for timed practice mode.
* `--visual-aid` Enable visual progress indicators in practice mode.
* `--no-visual-aid` Disable visual progress indicators in practice mode.
* `--stats` Show your practice statistics.
* `--config` Configure practice mode settings interactively.
* `--list` Show available implementations.

## Installation

### Quick Install

Clone the repository and run make install:

```shell
git clone https://github.com/docdyhr/pigame
cd pigame
make install  # May require sudo
```

### Manual Install

Clone the repository and install pigame in your `$PATH`:

```shell
git clone https://github.com/docdyhr/pigame
cd pigame/
chmod 755 pigame
cp pigame ~/bin  # Or any directory in your PATH
```

### Docker Install

You can also run PIGAME using Docker:

```shell
# Build the Docker image
docker build -t pigame .

# Run PIGAME with Docker
docker run -it pigame -p 10

# Run with custom input
docker run -it pigame 3.14159

# For development environment
docker-compose up -d dev
docker-compose exec dev bash
```

### Requirements

* `bc` - An arbitrary precision calculator language (required for legacy Bash implementation)
  * Linux/Unix: install with your standard package manager
  * Windows: a 32-bit Windows version is available
  * Ref.: <https://www.gnu.org/software/bc/bc.html>
* For C implementation: C compiler (gcc or clang)
* For Python implementation: Python 3.6+

### Development Environment

For local development, you can use the provided setup script:

```shell
# Quick environment setup
./scripts/setup.sh

# Or using Docker
docker-compose up -d dev
docker-compose exec dev bash
```

## Dependencies

- `bc` (for Bash implementation) - Required for core functionality
- C compiler (gcc or clang) - Optional, needed for C implementation
- Python 3.6+ - Optional, needed for Python implementation
- shellcheck - Optional, helpful for development
- clang-format - Optional, helpful for development

### Development Dependencies
Development dependencies are now separated from runtime dependencies:
- Runtime: `requirements.txt`
- Development: `requirements-dev.txt`

You can check your system for all required dependencies:
```sh
./scripts/check_dependencies.sh
```

## Implementations

PIGAME comes in three implementations, each with its own strengths:

1. **Bash** (Original): Lightweight and works on any Unix-like system with bash.
2. **C**: Highly efficient, uses verified pi digits for perfect accuracy.
3. **Python**: More readable code with strong error handling.

All implementations now use verified pi digits from trusted mathematical sources, ensuring:

* Perfect accuracy across all precision levels
* Consistent results across implementations
* Fast constant-time digit retrieval
* No external library dependencies

## Examples

Basic usage with a pi estimate:

```shell
pigame 3.14158
```

Output:

```shell
3.14159
3.14158
No match
```

Verbose mode with specified precision:

```shell
pigame -v -p 25
```

Output:

```shell
π with 25 decimals: 3.1415926535897932384626434
```

Verbose mode with a correct pi estimate:

```shell
pigame -v 3.1415926
```

Output:

```shell
π with 7 decimals: 3.1415926
Your version of π: 3.1415926
Number of errors: 0
Perfect!
```

Practice mode for interactive learning:

```shell
pigame --practice                               # Standard mode
pigame --practice --practice-mode timed         # Timed mode with countdown
pigame --practice --practice-mode chunk         # Chunk-based mode
pigame --practice --min-digits 10 --max-digits 50 # Custom difficulty
```

Output (Standard mode):

```shell
🔢 PIGAME PRACTICE MODE 🔢
=========================

Practice memorizing digits of π one by one.
Type each digit (0-9) without pressing Enter.
Press Ctrl+C at any time to exit.

Your best: 0 digits
Starting with 5 digits

First 5 digits: 3.14159
...
```

Output (Timed mode):

```shell
🔢 PIGAME PRACTICE MODE 🔢
=========================

Timed practice: You have 180 seconds to enter as many digits as possible.
Type each digit (0-9) without pressing Enter.
Press Ctrl+C at any time to exit.

Your best: 12 digits
Best speed: 8.5 digits/minute
Starting with 13 digits
...
```

Configure practice mode settings:

```shell
pigame --config
```

## Development

### Setup Development Environment

The easiest way to set up your development environment is to use our unified setup script:

```shell
# Clone the repository
git clone https://github.com/docdyhr/pigame
cd pigame

# Run the setup script (automatically sets up environment)
./scripts/setup.sh
# The setup script will:
# - Create and activate a Python virtual environment
# - Install runtime dependencies
# - Optionally install development dependencies (recommended for contributors)
# - Set up pre-commit hooks
# - Make all scripts executable
```

### Building

```shell
make              # Build all implementations
make build-c      # Build only the C implementation
```

### Testing

We now have unified testing scripts that provide consistent results across all environments:

```shell
./scripts/run_tests.sh           # Run all tests with coverage
./scripts/run_tests.sh --no-c    # Skip C tests
./scripts/run_tests.sh --no-bash # Skip Bash tests
make test                        # Run all tests (calls the script)
make coverage                    # Run Python tests with coverage
```

### Linting

We now have a unified linting script that handles all code formatting and style checks:

```shell
./scripts/lint.sh                # Run all linting checks
make lint                        # Run all linting checks (calls the script)
```

This script handles:
- Python code formatting and checks (using Ruff)
- Bash script linting (using ShellCheck)
- C code formatting (using clang-format)
- Common file formatting (trailing whitespace, file endings)

### CI/CD Pipeline

The CI/CD pipeline uses the same scripts as local development, ensuring consistent results:

```shell
./scripts/lint.sh      # Same script used in CI for linting
./scripts/run_tests.sh # Same script used in CI for tests
```
- 100% test coverage is the goal. To check coverage:
  ```sh
  .venv/bin/pytest --cov=src/python --cov-report=html
  open htmlcov/index.html
  ```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

- Use type hints and Google-style docstrings in all Python code.
- Follow the code style and linting requirements in [copilot-instructions.md](copilot-instructions.md).
- Use conventional commit messages (feat:, fix:, docs:, etc.).
- All code must pass tests and linting before submitting a pull request.
- The canonical version is always stored in src/VERSION; all implementations read from this file.
- All implementations (Bash, C, Python) must maintain compatibility with each other.
- CI/CD pipeline will automatically verify your changes.

## Security

For security issues, please see [SECURITY.md](SECURITY.md) for our vulnerability reporting process.

## To-Do List

See [TODO.md](https://github.com/docdyhr/pigame/blob/master/TODO.md) for the list of planned improvements.

## License

[MIT](https://github.com/docdyhr/pigame/blob/master/LICENSE)

## References

- [CALCULATING_PI.md](CALCULATING_PI.md) – Technical background and pi calculation details.
