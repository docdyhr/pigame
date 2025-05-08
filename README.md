# PIGAME - How many decimals of π can you remember?

[![CI/CD Pipeline](https://github.com/docdyhr/pigame/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/docdyhr/pigame/actions/workflows/ci.yml)
[![Test Coverage](https://img.shields.io/codecov/c/github/docdyhr/pigame)](https://codecov.io/gh/docdyhr/pigame)
[![Version](https://img.shields.io/badge/version-1.7.1-blue)](https://github.com/docdyhr/pigame/blob/master/src/VERSION)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/docdyhr/pigame/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/docdyhr/pigame/blob/master/CONTRIBUTING.md)

## Overview

* Version: 1.7.1
* Multiple implementations available: Bash (original), C, and Python
* Author: Thomas J. Dyhr
* Purpose: Memorisation of π
* Release date: 26. Apr 2025

## Usage

```shell
pigame [-v] [-p LENGTH] [-V] [-c] YOUR_PI
```

Evaluate your version of π (3.141.. )

* `-v` Increase verbosity.
* `-p LENGTH` Calculate and show π with LENGTH number of decimals.
* `-V` Version.
* `-c` Color-blind mode (use underscores instead of color).
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

- **Ruff** (Python linter): Install via Homebrew on macOS:
  ```sh
  brew install ruff
  ```
  Do not install Ruff with pip or add it to requirements.txt.
- `bc` (for Bash implementation)
- C compiler (gcc or clang, for C implementation)
- Python 3.6+ (for Python implementation)

- **isort is no longer used. Ruff now handles all import sorting and linting for Python.**

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

## Development

### Setup Development Environment

```shell
# Clone the repository
git clone https://github.com/docdyhr/pigame
cd pigame

# Install system dependencies
# Ubuntu/Debian:
sudo apt-get install bc shellcheck clang-format
# macOS:
# brew install bc shellcheck clang-format

# Set up Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .

# Set up pre-commit hooks
pip install pre-commit
pre-commit install
```

### Building

```shell
make              # Build all implementations
make build-c      # Build only the C implementation
make build-python # Build only the Python implementation
```

### Testing

```shell
make test          # Test all implementations
make test-bash     # Test only the Bash implementation
make test-c        # Test only the C implementation
make test-python   # Test only the Python implementation
make test-pytest   # Run Python unit tests with pytest

# Run tests in Docker
docker-compose up test
```

### Linting

- All Python code must pass Ruff linting before merging or release.
- Run Ruff directly from the command line:
  ```sh
  ruff check src/python/ tests/
  ruff check --fix src/python/ tests/  # Auto-fix issues
  ```
- Ruff is not managed by pip or requirements.txt.
- isort is no longer used; import sorting is handled by Ruff.
- Run shellcheck on bash scripts:
  ```sh
  shellcheck pigame src/bash/pigame.sh
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
- The canonical version is always stored in src/VERSION; all references must match.
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
