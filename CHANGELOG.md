# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- TBD

## [1.9.10] - 2025-11-08

### Added
- TBD

## [1.9.9] - 2025-06-14

### Changed
- Updated project dependencies to latest versions

### Fixed
- Fixed executable permission on src/python/pigame.py to match shebang

## [1.9.8] - 2025-05-22

### Changed
- Updated README with dependency management information
- Removed compiled C binary from version control (added to .gitignore)

### Fixed
- Fixed version inconsistency between VERSION file and hardcoded values
- Improved error handling in bash implementation input validation
- Separated development from runtime dependencies with requirements-dev.txt
- Fixed path resolution for VERSION file in C implementation
- Removed unused binomial and factorial functions in C implementation
- Removed unnecessary math.h dependency in C implementation
- Updated setup.sh to allow selective installation of dev dependencies
- Enhanced input validation with better error messages
- Fixed pytest fixture style by removing redundant parentheses

## [1.9.7] - 2025-05-20

### Added
- TBD

## [1.9.6] - 2025-05-10

### Added
- TBD

## [1.9.5] - 2025-05-10

### Added
- TBD

## [1.9.4] - 2025-05-10

### Added
- TBD

## [1.9.3] - 2025-05-10

### Added
- TBD

## [1.9.2] - 2025-05-09

### Added
- TBD

### Fixed
- Fixed practice mode function calls to use keyword-only arguments properly
- Updated test suite to properly isolate practice mode test cases
- Added proper mocking of system stdin for keyboard interrupt tests
- Improved test fixture cleanup for more reliable testing

## [1.9.1] - 2025-05-09

### Added
- TBD

## [1.9.0] - 2025-05-09

### Added
- Interactive practice mode with `--practice` flag for memorizing π digits
- Statistics tracking with `--stats` flag to show progress over time
- Session history and performance metrics for practice mode
- Difficulty progression system that adapts based on user performance
- User data saved in ~/.pigame directory for persistent progress tracking
- Multiple practice strategies: standard, timed, and chunk-based modes
- Interactive configuration with `--config` flag for customizing practice settings
- Visual progress indicators and timers during practice sessions
- Speed tracking in digits per minute with personal bests
- Command-line options for all practice mode settings (min/max digits, time limits, etc.)

## [1.8.0] - 2025-05-08

### Added
- TBD

## [1.7.6] - 2025-05-08

### Added
- TBD

## [1.7.5] - 2025-05-08

### Added
- TBD

## [1.7.4] - 2025-05-08

### Added
- TBD

## [1.7.3] - 2025-05-08

### Added
- TBD

## [1.7.2] - 2025-05-08

### Added

- TBD

### Changed

- Markdown style: All lists in markdown files must now be surrounded by blank lines (before and after the list), as required by copilot-instructions.md.

## [1.7.1] - 2025-04-26

### Changed
- Removed isort from pre-commit hooks and project dependencies; Ruff now handles all import sorting and linting for Python code.
- Updated all documentation and project files to reflect Ruff as the only Python linter.
- Fixed all ruff/pre-commit errors in Python code, including docstrings, exception formatting, and file permissions.
- Updated CI/CD and development instructions for the new workflow.

## [1.7.1] - 2025-04-25

### Added
- TBD

## [1.7.0] - 2025-04-25

### Added

- Improved test framework with pytest adoption
- Added type hints throughout test files
- Enhanced test organization and documentation
- Improved shell script safety and error handling
- Added comprehensive command argument validation
- Converted test_python_unit.py from unittest to pytest framework
- Added type hints and improved code organization across test files
- Enhanced test coverage with more comprehensive assertions
- Improved shell script safety and error handling in test runners
- Added proper command argument validation
- TBD

## [1.6.20] - 2025-04-24

### Added

- TBD

## [1.6.19] - 2025-04-24

### Added

- TBD

## [1.6.18] - 2025-04-24

### Added

- TBD

## [1.6.17] - 2025-04-24

### Added

- TBD

## [1.6.16] - 2025-04-24

### Added

- TBD

## [1.6.15] - 2025-04-24

### Added

- TBD

## [1.6.14] - 2025-04-24

### Added

- TBD

## [1.6.13] - 2025-04-24

### Added

- TBD

## [1.6.12] - 2025-04-24

### Added

- Switched to using verified pi digits instead of runtime calculation
- Improved accuracy and performance by eliminating floating-point arithmetic
- Removed GMP library dependency for C implementation
- Consistent pi digits across all implementations

## [1.6.11] - 2025-04-24

### Added

- TBD

## [1.6.10] - 2025-04-24

### Added

- TBD

## [1.6.9] - 2025-04-24

### Added

- TBD

## [1.6.8] - 2025-03-21

### Added

- TBD

## [1.6.7] - 2025-03-21

### Added

- Improved spacing between digits for better readability
- Added colorblind mode to C implementation

## [1.6.6] - 2025-03-21

### Added

- Color-blind mode with -c option (uses underlines instead of colors)

## [1.6.5] - 2025-03-21

### Added

- GitHub release workflow automation
- Improved test release script
- Version badge in README
- Release notes generation from CHANGELOG

## [1.6.4] - 2025-03-21

### Added

- Test coverage reports for Python implementation

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

- Restructured project with proper directory organization
- Improved pi calculation in C implementation
- Enhanced documentation with usage examples
- Consistent behavior across all implementations

### Fixed

- Color output consistency across implementations
- Argument handling edge cases
- Input validation in all implementations

## [1.5.1] - 2022-01-14

### Added

- Initial release with Bash implementation
- Basic pi calculation using bc
- Command-line interface with flags for verbosity and precision
- Easter egg references to Archimedes

[Unreleased]: https://github.com/docdyhr/pigame/compare/v1.9.10...HEAD
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
