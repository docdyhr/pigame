# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added automated dependency and security monitoring with Dependabot and GitHub security workflows
- Added support for additional mathematical constants (e, φ, √2) via `--constant` flag
- Added cross-implementation integration tests comparing Bash, C, and Python outputs
- Added property-based tests using `hypothesis` for mathematical correctness

### Changed

- Consolidated release automation to a single CI-driven release flow
- Converted version bumping from automatic-on-push to an explicit manual workflow
- Improved CI package validation and made coverage artifacts unique per matrix job

### Fixed

- Fixed Python console entry point packaging metadata
- Fixed pytest executable fixture to restore original file permissions
- Fixed linting workflow to check files in CI instead of mutating the checkout
- Fixed README version metadata drift

## [1.9.14] - 2026-01-20

### Added

- Added automated dependency and security monitoring with Dependabot and GitHub security workflows

### Changed

- Consolidated release automation to a single CI-driven release flow; release job now triggers only on version tags
- Converted version bumping from automatic-on-push to an explicit manual workflow (`version-bump.yml`)
- Improved CI coverage artifact naming to be unique per OS and Python version matrix entry

### Fixed

- Fixed Python console entry point packaging metadata in `setup.py` and `pyproject.toml`
- Fixed pytest executable fixture to restore original file permissions after test run
- Fixed linting workflow to check files in CI rather than mutating the checkout
- Fixed README version badge and overview version field to stay in sync with `src/VERSION`

## [1.9.13] - 2026-01-20

### Changed

- Updated CI matrix to test against Python 3.11, 3.12, and 3.13
- Updated `python_requires` in `setup.py` to reflect minimum supported version (3.11)
- Pinned GitHub Actions runner image to `ubuntu-latest` and `macos-latest` across all jobs

## [1.9.12] - 2026-01-20

### Changed

- Updated all Python development dependencies to latest compatible versions
- Improved inline documentation for test helper functions and fixtures

### Fixed

- Fixed minor code quality issues flagged by updated Ruff rules
- Fixed stale docstring references after refactoring of test configuration

## [1.9.11] - 2025-11-08

### Changed

- Refactored `conftest.py` to centralise shared pytest fixtures used across test modules
- Updated pinned dependency versions in `requirements.txt` and `requirements-dev.txt`

### Fixed

- Fixed test isolation issue where `pigame_exec` fixture did not reliably restore file permissions on failure

## [1.9.10] - 2025-11-08

### Fixed

- Fixed multiple code quality warnings flagged by Ruff (unused imports, missing type annotations, bare exceptions)
- Fixed executable permission on `src/python/pigame.py` to match the `#!/usr/bin/env python3` shebang

### Changed

- Updated inline documentation and module-level docstrings across the Python implementation

## [1.9.9] - 2025-06-14

### Changed

- Updated project dependencies to latest versions

### Fixed

- Fixed executable permission on `src/python/pigame.py` to match shebang

## [1.9.8] - 2025-05-22

### Changed

- Updated README with dependency management information
- Removed compiled C binary from version control (added to `.gitignore`)

### Fixed

- Fixed version inconsistency between VERSION file and hardcoded values
- Improved error handling in bash implementation input validation
- Separated development from runtime dependencies with `requirements-dev.txt`
- Fixed path resolution for VERSION file in C implementation
- Removed unused `binomial` and `factorial` functions in C implementation
- Removed unnecessary `math.h` dependency in C implementation
- Updated `setup.sh` to allow selective installation of dev dependencies
- Enhanced input validation with better error messages
- Fixed pytest fixture style by removing redundant parentheses

## [1.9.7] - 2025-05-20

### Changed

- Updated `.gitignore` to exclude AI assistant configuration and cache files

## [1.9.6] - 2025-05-10

### Changed

- Updated README and contributing docs to reflect the new unified CI/CD scripts
- Updated `scripts/lint.sh` and `scripts/run_tests.sh` documentation with usage examples

## [1.9.5] - 2025-05-10

### Changed

- Simplified CI/CD pipeline by introducing unified local scripts `scripts/lint.sh` and `scripts/run_tests.sh`
- CI pipeline now calls the same scripts used locally, ensuring consistent behaviour between environments

## [1.9.4] - 2025-05-10

### Fixed

- Fixed CI/CD pipeline job ordering and dependency graph
- Fixed Codecov integration — upload now uses the correct `coverage.xml` artifact path
- Fixed missing `build-essential` and `bc` installation steps on Linux CI runners

## [1.9.3] - 2025-05-10

### Added

- Added `.markdownlint.json` configuration for consistent Markdown style enforcement
- Added `.markdownlintignore.md` to exclude generated files from linting

### Changed

- All Markdown lists are now surrounded by blank lines as required by linting rules

## [1.9.2] - 2025-05-09

### Fixed

- Fixed practice mode function calls to use keyword-only arguments properly
- Updated test suite to properly isolate practice mode test cases
- Added proper mocking of system stdin for keyboard interrupt tests
- Improved test fixture cleanup for more reliable testing

## [1.9.1] - 2025-05-09

### Fixed

- Fixed linting issues in the practice mode implementation flagged by Ruff
- Fixed docstring formatting and exception chaining style throughout `pigame.py`

## [1.9.0] - 2025-05-09

### Added

- Interactive practice mode with `--practice` flag for memorizing π digits
- Statistics tracking with `--stats` flag to show progress over time
- Session history and performance metrics for practice mode
- Difficulty progression system that adapts based on user performance
- User data saved in `~/.pigame` directory for persistent progress tracking
- Multiple practice strategies: standard, timed, and chunk-based modes
- Interactive configuration with `--config` flag for customizing practice settings
- Visual progress indicators and timers during practice sessions
- Speed tracking in digits per minute with personal bests
- Command-line options for all practice mode settings (`--min-digits`, `--max-digits`, `--time-limit`, etc.)

## [1.8.0] - 2025-05-08

### Added

- Added `SECURITY.md` with vulnerability reporting process and security best practices
- Added `.devcontainer/` configuration for VS Code Dev Container development workflow
- Added `docker-compose.yml` with a dedicated `dev` service for containerised development
- Added `.benchmarks/` directory structure for future performance benchmarking
- Added `scripts/check_dependencies.sh` to verify all required system dependencies

### Changed

- Improved input sanitisation and validation error messages across all implementations
- Enhanced VS Code workspace settings (`.vscode/settings.json`) for a better developer experience
- Updated Dockerfile to include all runtime and optional development dependencies

## [1.7.6] - 2025-05-08

### Fixed

- Cleaned up spurious debug `echo` statements left in Bash and shell test scripts
- Fixed `test_python.sh` to correctly capture and compare stderr output from the Python implementation
- Fixed `test_python_unit.py` to add the project root to `sys.path`, resolving module import failures when run directly

## [1.7.5] - 2025-05-08

### Fixed

- Made Python integration tests resilient to ANSI colour escape codes in captured output by stripping them before assertion

## [1.7.4] - 2025-05-08

### Fixed

- Improved C code linting step in the CI pipeline to report `clang-format` diff output clearly
- Made `clang-format` check non-fatal on platforms where it is unavailable

## [1.7.3] - 2025-05-08

### Fixed

- Made C code formatting checks non-blocking in CI so that a missing `clang-format` binary does not fail the pipeline

## [1.7.2] - 2025-05-08

### Changed

- Updated CI/CD pipeline to resolve compatibility issues with newer GitHub Actions runner images
- Markdown style: all lists in Markdown files must now be surrounded by blank lines

## [1.7.1] - 2025-04-26

### Changed

- Removed `isort` from pre-commit hooks and project dependencies; Ruff now handles all import sorting and linting for Python code
- Updated all documentation and project files to reflect Ruff as the sole Python linter
- Fixed all Ruff and pre-commit errors in Python code, including docstrings, exception formatting, and file permissions
- Updated CI/CD and development instructions for the new workflow

## [1.7.0] - 2025-04-25

### Added

- Improved test framework with pytest adoption
- Added type hints throughout test files
- Enhanced test organisation and documentation
- Improved shell script safety and error handling
- Added comprehensive command argument validation
- Converted `test_python_unit.py` from `unittest` to pytest framework
- Added type hints and improved code organisation across test files
- Enhanced test coverage with more comprehensive assertions
- Added proper command argument validation

## [1.6.20] - 2025-04-24

### Changed

- Minor dependency and CI configuration updates

## [1.6.19] - 2025-04-24

### Fixed

- Fixed edge case in argument parsing when no positional argument is provided alongside flags

## [1.6.18] - 2025-04-24

### Fixed

- Resolved intermittent test failures caused by shell environment differences between CI and local runs

## [1.6.17] - 2025-04-24

### Changed

- Refactored Python argument parser into a dedicated `_create_argument_parser()` helper function

## [1.6.16] - 2025-04-24

### Fixed

- Fixed version string display format to be consistent across all three implementations

## [1.6.15] - 2025-04-24

### Changed

- Cleaned up unused imports and variables across all Python source and test files

## [1.6.14] - 2025-04-24

### Fixed

- Fixed incorrect exit codes returned by the Python implementation on error paths

## [1.6.13] - 2025-04-24

### Fixed

- Fixed edge case where `format_pi_with_spaces` would insert a leading space for very short inputs

## [1.6.12] - 2025-04-24

### Added

- Switched to using verified π digits instead of runtime calculation via `bc`
- Improved accuracy and performance by eliminating floating-point arithmetic
- Removed GMP library dependency for C implementation
- Consistent π digits across all three implementations (Bash, C, Python)

## [1.6.11] - 2025-04-24

### Changed

- Aligned colorblind mode highlight style between Bash and Python implementations

## [1.6.10] - 2025-04-24

### Fixed

- Fixed colour output not being reset correctly after the last digit in some terminal emulators

## [1.6.9] - 2025-04-24

### Fixed

- Fixed off-by-one error in digit spacing logic for inputs shorter than 7 characters

## [1.6.8] - 2025-03-21

### Changed

- Minor internal refactoring and code style improvements ahead of the 1.6.x series

## [1.6.7] - 2025-03-21

### Added

- Improved spacing between digits for better readability (groups of 5)
- Added colorblind mode to the C implementation (`-c` flag)

## [1.6.6] - 2025-03-21

### Added

- Color-blind mode with `-c` option — uses underlines instead of red colour to mark errors

## [1.6.5] - 2025-03-21

### Added

- GitHub release workflow automation (`release.yml`)
- Improved `test-release.sh` script for local pre-release validation
- Version badge in README linking to `src/VERSION`
- Release notes generation from `CHANGELOG.md`

## [1.6.4] - 2025-03-21

### Added

- Test coverage reports for the Python implementation via `pytest-cov`
- HTML and XML coverage report artefacts uploaded in CI

## [1.6.0] - 2025-03-21

### Added

- Multi-implementation support (Bash, C, Python)
- Comprehensive test suite for all implementations
- Virtual environment support for Python
- GitHub Actions for CI/CD
- Automated testing with pytest
- Makefile for building, testing, and installation
- Man page for better documentation
- Improved error handling across all implementations

### Changed

- Restructured project with proper directory organisation under `src/`
- Improved π calculation in the C implementation
- Enhanced documentation with usage examples
- Consistent behaviour across all implementations

### Fixed

- Color output consistency across implementations
- Argument handling edge cases
- Input validation in all implementations

## [1.5.1] - 2022-01-14

### Added

- Initial release with Bash implementation
- Basic π calculation using `bc`
- Command-line interface with flags for verbosity and precision
- Easter egg references to Archimedes

[Unreleased]: https://github.com/docdyhr/pigame/compare/v1.9.14...HEAD
[1.9.14]: https://github.com/docdyhr/pigame/compare/v1.9.13...v1.9.14
[1.9.13]: https://github.com/docdyhr/pigame/compare/v1.9.12...v1.9.13
[1.9.12]: https://github.com/docdyhr/pigame/compare/v1.9.11...v1.9.12
[1.9.11]: https://github.com/docdyhr/pigame/compare/v1.9.10...v1.9.11
[1.9.10]: https://github.com/docdyhr/pigame/compare/v1.9.9...v1.9.10
[1.9.9]: https://github.com/docdyhr/pigame/compare/v1.9.8...v1.9.9
[1.9.8]: https://github.com/docdyhr/pigame/compare/v1.9.7...v1.9.8
[1.9.7]: https://github.com/docdyhr/pigame/compare/v1.9.6...v1.9.7
[1.9.6]: https://github.com/docdyhr/pigame/compare/v1.9.5...v1.9.6
[1.9.5]: https://github.com/docdyhr/pigame/compare/v1.9.4...v1.9.5
[1.9.4]: https://github.com/docdyhr/pigame/compare/v1.9.3...v1.9.4
[1.9.3]: https://github.com/docdyhr/pigame/compare/v1.9.2...v1.9.3
[1.9.2]: https://github.com/docdyhr/pigame/compare/v1.9.1...v1.9.2
[1.9.1]: https://github.com/docdyhr/pigame/compare/v1.9.0...v1.9.1
[1.9.0]: https://github.com/docdyhr/pigame/compare/v1.8.0...v1.9.0
[1.8.0]: https://github.com/docdyhr/pigame/compare/v1.7.6...v1.8.0
[1.7.6]: https://github.com/docdyhr/pigame/compare/v1.7.5...v1.7.6
[1.7.5]: https://github.com/docdyhr/pigame/compare/v1.7.4...v1.7.5
[1.7.4]: https://github.com/docdyhr/pigame/compare/v1.7.3...v1.7.4
[1.7.3]: https://github.com/docdyhr/pigame/compare/v1.7.2...v1.7.3
[1.7.2]: https://github.com/docdyhr/pigame/compare/v1.7.1...v1.7.2
[1.7.1]: https://github.com/docdyhr/pigame/compare/v1.7.0...v1.7.1
[1.7.0]: https://github.com/docdyhr/pigame/compare/v1.6.20...v1.7.0
[1.6.20]: https://github.com/docdyhr/pigame/compare/v1.6.19...v1.6.20
[1.6.19]: https://github.com/docdyhr/pigame/compare/v1.6.18...v1.6.19
[1.6.18]: https://github.com/docdyhr/pigame/compare/v1.6.17...v1.6.18
[1.6.17]: https://github.com/docdyhr/pigame/compare/v1.6.16...v1.6.17
[1.6.16]: https://github.com/docdyhr/pigame/compare/v1.6.15...v1.6.16
[1.6.15]: https://github.com/docdyhr/pigame/compare/v1.6.14...v1.6.15
[1.6.14]: https://github.com/docdyhr/pigame/compare/v1.6.13...v1.6.14
[1.6.13]: https://github.com/docdyhr/pigame/compare/v1.6.12...v1.6.13
[1.6.12]: https://github.com/docdyhr/pigame/compare/v1.6.11...v1.6.12
[1.6.11]: https://github.com/docdyhr/pigame/compare/v1.6.10...v1.6.11
[1.6.10]: https://github.com/docdyhr/pigame/compare/v1.6.9...v1.6.10
[1.6.9]: https://github.com/docdyhr/pigame/compare/v1.6.8...v1.6.9
[1.6.8]: https://github.com/docdyhr/pigame/compare/v1.6.7...v1.6.8
[1.6.7]: https://github.com/docdyhr/pigame/compare/v1.6.6...v1.6.7
[1.6.6]: https://github.com/docdyhr/pigame/compare/v1.6.5...v1.6.6
[1.6.5]: https://github.com/docdyhr/pigame/compare/v1.6.4...v1.6.5
[1.6.4]: https://github.com/docdyhr/pigame/compare/v1.6.3...v1.6.4
[1.6.0]: https://github.com/docdyhr/pigame/compare/v1.5.1...v1.6.0
[1.5.1]: https://github.com/docdyhr/pigame/releases/tag/v1.5.1