# PIGAME - How many decimals of π can you remember?

[![CI/CD Pipeline](https://github.com/docdyhr/pigame/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/docdyhr/pigame/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-1.6.7-blue)](https://github.com/docdyhr/pigame/blob/master/src/VERSION)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/docdyhr/pigame/blob/master/LICENSE)

## Overview

* Version: 1.6.7
* Multiple implementations available: Bash (original), C, and Python
* Author: Thomas J. Dyhr
* Purpose: Memorisation of π
* Release date: 14. Jan 2022

## Usage

```
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

### Requirements

* `bc` - An arbitrary precision calculator language (required for legacy Bash implementation)
  * Linux/Unix: install with your standard package manager
  * Windows: a 32-bit Windows version is available
  * Ref.: https://www.gnu.org/software/bc/bc.html
* For C implementation: C compiler (gcc or clang)
* For Python implementation: Python 3.6+

## Implementations

PIGAME comes in three implementations, each with its own strengths:

1. **Bash** (Original): Lightweight and works on any Unix-like system with bash.
2. **C**: Highly efficient, uses verified pi digits for perfect accuracy.
3. **Python**: More readable code with strong error handling.

All implementations now use verified pi digits from trusted mathematical sources, ensuring:
- Perfect accuracy across all precision levels
- Consistent results across implementations
- Fast constant-time digit retrieval
- No external library dependencies

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