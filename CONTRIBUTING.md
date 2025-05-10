# Contributing to PIGAME

Thank you for considering contributing to PIGAME! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to be respectful and considerate of others. We are committed to providing a welcoming and inspiring community for all.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**:


   ```
   git clone https://github.com/YOUR_USERNAME/pigame.git
   cd pigame

   ```


3. **Set up the development environment**:

   ```
   # One-command setup for all dependencies and configurations
   ./scripts/setup.sh
   ```

4. **Required system dependencies**:

   The setup script will check for these dependencies and provide instructions if they're missing:
   
   - **Python 3**: Required for all development
   - **bc**: Arbitrary precision calculator (for Bash implementation)
   - **ShellCheck**: Shell script linter (optional for development)
   - **clang-format**: C code formatter (optional for C development)
   - **gcc/clang**: C compiler (optional for C development)

   The `./scripts/setup.sh` script handles all Python dependencies and pre-commit hooks automatically.


## Development Workflow

1. **Create a new branch** for your changes:

   ```
   git checkout -b feature/your-feature-name
   ```


2. **Make your changes** following the coding standards

3. **Test your changes**:

   ```
   make test          # Run all tests
   make test-bash     # Test Bash implementation
   make test-c        # Test C implementation
   make test-python   # Test Python implementation
   make test-pytest   # Run pytest with coverage
   ```

4. **Lint your code**:


   ```
   ./scripts/lint.sh  # Run all linters
   make lint          # Run all linters (uses the script)
   ```

   - Our unified linting script handles Python (Ruff), Bash (ShellCheck), and C (clang-format) in a single command.
   - Pre-commit hooks will automatically run the linting script on each commit.
   - If pre-commit hooks fail, fix the issues and try committing again.
   - The same script is used both locally and in CI to ensure consistent results.

5. **Commit your changes** with a descriptive commit message:

   - For new features: `feat: Add new feature X`
   - For bug fixes: `fix: Correct behavior in scenario Y`
   - For documentation: `docs: Improve installation instructions`
   - For refactoring: `refactor: Simplify calculation method`
   - Append `BREAKING CHANGE:` in the commit body for breaking changes

6. **Push your branch** to your fork:

   ```

   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** to the main repository


## Versioning

We use [Semantic Versioning](https://semver.org/):

- MAJOR version for incompatible API changes
- MINOR version for backward-compatible functionality additions
- PATCH version for backward-compatible bug fixes

The version is managed in the `src/VERSION` file and can be updated using:

```
make version-patch  # For bug fixes
make version-minor  # For new features

make version-major  # For breaking changes
```

## Changelog

When making significant changes, add an entry to the `CHANGELOG.md` file under the "Unreleased" section. The version number will be automatically updated during the release process.

## Releasing

New releases are created automatically when a new version tag is pushed:

```
make release  # Updates version, creates commit and tag
git push && git push --tags  # Trigger the release workflow
```

## Testing

- All implementations (Bash, C, Python) must have tests
- Maintain or improve test coverage with your changes
- Both integration and unit tests are encouraged
- Run tests with our unified test script:
  ```
  ./scripts/run_tests.sh           # Run all tests
  ./scripts/run_tests.sh --no-c    # Skip C tests
  ./scripts/run_tests.sh --no-bash # Skip Bash tests
  ```
- The same script is used in CI, ensuring consistent results

## Pull Request Process

1. Ensure all tests pass and lint checks succeed
2. Update the documentation if necessary
3. The PR will be reviewed by maintainers
4. Once approved, your PR will be merged

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment. Our CI/CD pipeline is designed to match local development exactly:

1. **Lint job**: Runs `./scripts/lint.sh` - the same script you run locally
2. **Build job**: Builds the project and verifies it compiles correctly
3. **Test job**: Runs `./scripts/run_tests.sh` - the same script you use for local testing
4. **Release job**: Creates release artifacts when a new version tag is pushed

This unified approach ensures that if tests pass locally, they'll pass in CI. When you create a PR, the CI pipeline will automatically run to verify your changes. Your PR will only be merged if all CI checks pass.

## Development Environment

Setting up your development environment is simple using our unified setup script:

```
./scripts/setup.sh  # One command sets up the entire environment
```

This script handles:
- Creating and activating a Python virtual environment
- Installing all dependencies
- Setting up pre-commit hooks
- Making all scripts executable

For IDE integration:
- VS Code: The repository includes recommended extensions and settings in .vscode
- PyCharm: Import the project and use the provided pytest configuration

## Communication

- Use GitHub Issues for bug reports and feature requests
- Use Pull Requests for code contributions
- Be clear and respectful in all communications

Thank you for contributing to PIGAME!
