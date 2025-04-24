# Copilot Instructions for PIGAME Project

## Code Style Guidelines

### Python Files

1. **Code Formatting**
   - Ensure all Python files end with a final newline
   - Remove all trailing whitespace
   - Use Ruff for automatic linting and fixing:
     ```bash
     ruff check --fix src/python/ tests/
     ```
   - Maximum line length: 88 characters (Black default)
   - Use 4 spaces for indentation
   - Use snake_case for functions and variables
   - Use PascalCase for classes

2. **Documentation**
   - All functions must have docstrings with:
     - Description
     - Args/Parameters
     - Returns (if applicable)
     - Raises (if applicable)
   - Use Google-style docstrings format

3. **Imports**
   - Group imports in the following order:
     1. Standard library
     2. Third-party packages
     3. Local project imports
   - Always use explicit, specific imports
   - Add `# type: ignore` for pytest imports in test files

4. **Error Handling**
   - Always specify encoding when opening files:
     ```python
     with open(file_path, 'r', encoding='utf-8') as f:
     ```
   - Use specific exception types, avoid bare except clauses
   - Handle subprocess calls with explicit check parameter:
     ```python
     subprocess.run(cmd, check=False)
     ```

### Shell Scripts

1. **Code Style**
   - Use shellcheck for linting
   - Use 4 spaces for indentation
   - Add execute permissions: `chmod +x script.sh`

2. **Best Practices**
   - Use `#!/usr/bin/env bash` shebang
   - Quote all variable expansions
   - Use `set -e` to fail on errors
   - Use meaningful variable names in ALL_CAPS

### C Files

1. **Code Style**
   - Use clang-format for formatting
   - Follow Linux kernel style
   - Use 4 spaces for indentation
   - Maximum line length: 80 characters

## Testing Guidelines

1. **Python Tests**
   - Use pytest for all Python tests
   - Maintain 100% test coverage
   - Use fixtures for test setup
   - Test both success and error cases
   - Use descriptive test names
   - Avoid redundant assertions

2. **Shell Tests**
   - Test all command-line options
   - Test edge cases and error handling
   - Use meaningful test descriptions

## Git Commit Guidelines

1. **Commit Messages**
   - Use conventional commits format:
     - `feat:` for new features
     - `fix:` for bug fixes
     - `docs:` for documentation
     - `style:` for formatting
     - `refactor:` for code restructuring
     - `test:` for test changes
     - `chore:` for maintenance

2. **Pull Requests**
   - Ensure all tests pass
   - Update documentation if needed
   - Add tests for new features

## Documentation

1. **README Updates**
   - Keep version numbers current
   - Document new features
   - Update requirements

2. **CHANGELOG**
   - Follow Keep a Changelog format
   - Add all notable changes
   - Use semantic versioning

## CI/CD Pipeline

1. **GitHub Actions**
   - All tests must pass
   - Code coverage must be 100%
   - All linters must pass:
     - Ruff for Python
     - Shellcheck for Bash
     - Clang-format for C

## Version Management

1. **Version Updates**
   - Use semantic versioning
   - Update VERSION file
   - Update CHANGELOG.md

## Dependencies

1. **Python**
   - Keep requirements.txt updated
   - Pin specific versions
   - Run dependency updates weekly

2. **System**
   - Document all system dependencies
   - Test on multiple platforms

## Project Structure

1. **File Organization**
   - Keep implementations separate:
     - src/python/
     - src/bash/
     - src/c/
   - Maintain parallel test structure
   - Use __init__.py for Python packages

## Performance

1. **Optimization**
   - Use verified pi digits for calculations
   - Avoid unnecessary computations
   - Cache frequently used values

## Security

1. **Input Validation**
   - Validate all user inputs
   - Handle edge cases gracefully
   - Prevent command injection

## IDE Configuration

1. **VS Code Settings**
   - Enable format on save
   - Use Ruff as the default linter
   - Configure pytest for testing
   - Enable shellcheck for bash files