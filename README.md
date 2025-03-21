# PIGAME - How many decimals of π can you remember?

[![CI/CD Pipeline](https://github.com/docdyhr/pigame/actions/workflows/ci.yml/badge.svg)](https://github.com/docdyhr/pigame/actions/workflows/ci.yml)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/docdyhr/pigame)](https://github.com/docdyhr/pigame/releases/latest)
[![License](https://img.shields.io/github/license/docdyhr/pigame)](https://github.com/docdyhr/pigame/blob/master/LICENSE)

## Overview

* Version: 1.6.0
* Multiple implementations available: Bash (original), C, and Python
* Author: Thomas J. Dyhr
* Purpose: Memorisation of π
* Release date: 14. Jan 2022

## Usage

```
pigame [-v] [-p LENGTH] [-V] YOUR_PI
```

Evaluate your version of π (3.141.. )

* `-v` Increase verbosity.
* `-p LENGTH` Calculate and show π with LENGTH number of decimals.
* `-V` Version.
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

### Requirements

* `bc` - An arbitrary precision calculator language (required for Bash implementation)
  * Linux/Unix: install with your standard package manager
  * Windows: a 32-bit Windows version is available
  * Ref.: https://www.gnu.org/software/bc/bc.html
* For C implementation: C compiler (gcc or clang) and math library
* For Python implementation: Python 3.6+

## Implementations

PIGAME comes in three implementations, each with its own strengths:

1. **Bash** (Original): Lightweight and works on any Unix-like system with bash and bc.
2. **C**: Fast and efficient, ideal for resource-constrained environments.
3. **Python**: More readable code with strong error handling.

To select an implementation, set the `PIGAME_IMPLEMENTATION` environment variable:

```shell
# Use the Bash implementation
export PIGAME_IMPLEMENTATION=bash
pigame 3.14159

# Use the C implementation
export PIGAME_IMPLEMENTATION=c
pigame 3.14159

# Use the Python implementation
export PIGAME_IMPLEMENTATION=python
pigame 3.14159
```

## Examples

Basic usage with a pi estimate:

```shell
pigame 3.14158
```

Output:
```
3.14159
3.14158
No match
```

Verbose mode with specified precision:

```shell
pigame -v -p 25
```

Output:
```
π with 25 decimals: 3.1415926535897932384626434
```

Verbose mode with a correct pi estimate:

```shell
pigame -v 3.1415926
```

Output:
```
π with 7 decimals: 3.1415926
Your version of π: 3.1415926
Number of errors: 0
Perfect!
```

## Development

### Building

```shell
make         # Build all implementations
make build-c # Build only the C implementation
```

### Testing

```shell
make test          # Test all implementations
make test-bash     # Test only the Bash implementation
make test-c        # Test only the C implementation
make test-python   # Test only the Python implementation
```

### Linting

```shell
make lint          # Lint all implementations
make lint-bash     # Lint only the Bash implementation
make lint-python   # Lint only the Python implementation
```

## To-Do List

See [TODO.md](https://github.com/docdyhr/pigame/blob/master/TODO.md) for the list of planned improvements.

## License

[MIT](https://github.com/docdyhr/pigame/blob/master/LICENSE)