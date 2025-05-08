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
   make setup-python  # For Python development
   make build-c       # For C development
   ```

4. **Install required system dependencies**:

   - **bc**: Arbitrary precision calculator (required for all implementations)
   - **ShellCheck**: Shell script linter (required for development)
   - **clang-format**: C code formatter (required for C development)

   ```
   # On Ubuntu/Debian
   sudo apt-get install bc shellcheck clang-format

   # On macOS with Homebrew
   brew install bc shellcheck clang-format

   # On Windows with Chocolatey
   choco install shellcheck gnuwin32-bc llvm
   ```

5. **Set up pre-commit hooks**:

   ```
   # Install pre-commit
   pip install pre-commit

   # Install the git hooks
   pre-commit install
   ```


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
   make lint          # Run all linters
   make lint-bash     # Lint Bash implementation
   make lint-python   # Lint Python implementation
   ```

   - **Python linting and import sorting is handled exclusively by Ruff. isort is no longer used.**
   - All Python code must pass `ruff check src/python/ tests/` with no errors before merging or release.
   - Ruff will automatically fix most issues with `ruff check --fix src/python/ tests/`.
   - Pre-commit hooks will automatically run linters on each commit.
   - If pre-commit hooks fail, fix the issues and try committing again.

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

## Pull Request Process

1. Ensure all tests pass and lint checks succeed
2. Update the documentation if necessary
3. The PR will be reviewed by maintainers
4. Once approved, your PR will be merged

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment. The CI/CD pipeline includes:

1. **Lint job**: Checks code quality using Ruff, ShellCheck, and clang-format
2. **Build job**: Builds the project and verifies it compiles correctly
3. **Test job**: Runs all tests for Bash, C, and Python implementations
4. **Release job**: Creates release artifacts when a new version tag is pushed

When you create a PR, the CI pipeline will automatically run to verify your changes. Your PR will only be merged if all CI checks pass.

## Development Environment

We recommend using a virtual environment for Python development:

```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

For IDE integration:
- VS Code: The repository includes recommended extensions and settings in .vscode
- PyCharm: Import the project and use the provided pytest configuration

## Communication

- Use GitHub Issues for bug reports and feature requests
- Use Pull Requests for code contributions
- Be clear and respectful in all communications

Thank you for contributing to PIGAME!
