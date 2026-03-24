#!/usr/bin/env python3
"""Generate a Keep-a-Changelog-formatted markdown block from git conventional commits.

Usage:
    python scripts/generate_changelog.py            # since last tag
    python scripts/generate_changelog.py --base-tag v1.9.14
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict


# Map conventional commit types to changelog sections.
_TYPE_TO_SECTION: dict[str, str] = {
    "feat": "Added",
    "fix": "Fixed",
    "refactor": "Changed",
    "perf": "Changed",
    "style": "Changed",
    "chore": "Changed",
    "docs": "Changed",
    "test": "Changed",
    "ci": "CI/Infrastructure",
    "build": "CI/Infrastructure",
}

# Section display order.
_SECTION_ORDER = ["Added", "Fixed", "Changed", "CI/Infrastructure"]

# Regex for a conventional commit subject line.
_CONV_RE = re.compile(
    r"^(?P<type>[a-z]+)"
    r"(?:\((?P<scope>[^)]+)\))?"
    r"(?P<breaking>!)?"
    r": (?P<desc>.+)$"
)


def _run(args: list[str]) -> str:
    """Run a git command and return stdout, stripping trailing whitespace."""
    result = subprocess.run(  # noqa: S603
        args,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def _last_tag() -> str | None:
    """Return the most recent annotated or lightweight tag, or None."""
    try:
        return _run(["git", "describe", "--tags", "--abbrev=0"])
    except RuntimeError:
        return None


def _commits_since(base: str | None) -> list[tuple[str, str]]:
    """Return list of (hash, subject) tuples since *base* tag (or all commits)."""
    rev_range = f"{base}..HEAD" if base else "HEAD"
    raw = _run(["git", "log", rev_range, "--format=%H|%s"])
    if not raw:
        return []
    result = []
    for line in raw.splitlines():
        parts = line.split("|", 1)
        if len(parts) == 2:  # noqa: PLR2004
            result.append((parts[0], parts[1]))
    return result


def _categorize(commits: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group commit descriptions by changelog section."""
    sections: dict[str, list[str]] = defaultdict(list)
    for _sha, subject in commits:
        # Skip merge commits.
        if subject.startswith("Merge "):
            continue
        # Skip [skip ci] / version-bump bot commits.
        if "[skip ci]" in subject:
            continue
        match = _CONV_RE.match(subject)
        if not match:
            # Non-conventional commit: put in Changed.
            sections["Changed"].append(subject)
            continue
        commit_type = match.group("type")
        desc = match.group("desc")
        is_breaking = match.group("breaking") == "!"
        prefix = "[BREAKING] " if is_breaking else ""
        section = _TYPE_TO_SECTION.get(commit_type, "Changed")
        sections[section].append(f"{prefix}{desc}")
    return sections


def _format(sections: dict[str, list[str]]) -> str:
    """Render sections as a markdown string."""
    lines: list[str] = []
    for section in _SECTION_ORDER:
        entries = sections.get(section)
        if not entries:
            continue
        lines.append(f"### {section}")
        lines.extend(f"- {entry}" for entry in entries)
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> int:  # noqa: D103
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-tag",
        metavar="TAG",
        help="Base tag to compare against (default: auto-detect last tag)",
    )
    args = parser.parse_args()

    base = args.base_tag or _last_tag()
    if base:
        print(f"# Generating changelog since {base}", file=sys.stderr)
    else:
        print("# No prior tag found - using all commits", file=sys.stderr)

    try:
        commits = _commits_since(base)
    except RuntimeError as exc:
        print(f"git error: {exc}", file=sys.stderr)
        return 1

    if not commits:
        print("# No commits found since last tag", file=sys.stderr)
        print("### Added\n- No changes since last release")
        return 0

    sections = _categorize(commits)
    print(_format(sections))
    return 0


if __name__ == "__main__":
    sys.exit(main())
