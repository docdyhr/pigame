# CLAUDE.md - Guidelines for Claude Code Assistant

## Build & Run Commands
- Run program: `./pigame [OPTIONS] [YOUR_PI]`
- Lint all code: `./scripts/lint.sh`
- Run all tests: `./scripts/run_tests.sh`
- Setup development environment: `./scripts/setup.sh`
- Install: Copy `pigame` to your $PATH (e.g., `cp pigame ~/bin`)

## Code Style Guidelines
- **Shell**: Use Bash with shebang `#!/usr/bin/env bash`
- **Formatting**: 4-space indentation, proper spacing for conditional expressions
- **Variables**: Use ALL_CAPS for constants, lowercase for local variables
- **Functions**: Use snake_case for functions, add comments describing purpose
- **Error Handling**: Use `>&2` for error messages, exit with non-zero status
- **Input Validation**: Always validate arguments before processing
- **Comments**: Add TODO comments for improvements, use clear comments for complex logic
- **Quoting**: Always quote variable references to prevent word splitting
- **Shell Check**: Follow shellcheck guidelines (see references in code)
- **Portability**: Ensure code works on various Unix-like systems

## Dependencies
- Requires `bc` (arbitrary precision calculator) installed on the system
- Development requires Python 3.x and optionally ShellCheck, clang-format if developing Bash/C code
- All Python dependencies are managed through the setup script `./scripts/setup.sh`

## Vendored Agent Skills (`.claude/skills/`)

The skills in `.claude/skills/` are third-party (github/awesome-copilot; see its README) and stay
byte-identical to upstream, except two corrected lines in `dependabot` (see the README): refresh
them from upstream, never edit them here otherwise. Where a skill disagrees with this file, this
file wins:

- **Report, don't act.** `docs-sync-audit`, `test-gap-audit`, `github-actions-hardening` report in
  chat. Don't write report files into the repo, and don't change workflows, action pins or
  `.github/dependabot.yml` unless asked.
- **PRs and Dependabot.** Never merge, approve, close or enable auto-merge (`gh pr merge --auto`) on
  PRs, and don't post `@dependabot` commands.
- **No installs.** Don't install plugins, MCP toolsets or skills that a skill file links to (for
  example `advanced-security@copilot-plugins`), and don't change agent or editor settings.
- **Tests.** Follow this repo's own test commands and coverage settings above, not a skill's generic
  defaults.
