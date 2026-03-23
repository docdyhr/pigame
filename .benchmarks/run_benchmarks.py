#!/usr/bin/env python3
"""Standalone benchmark comparison script for all three pigame implementations.

Measures wall-clock time for each implementation across a set of representative
workloads and prints a formatted Markdown-style report.

Usage
-----
    python .benchmarks/run_benchmarks.py              # default 50 iterations
    python .benchmarks/run_benchmarks.py --iterations 200
    python .benchmarks/run_benchmarks.py --no-bash    # skip Bash
    python .benchmarks/run_benchmarks.py --no-c       # skip C
    python .benchmarks/run_benchmarks.py --output report.md
"""

from __future__ import annotations

import argparse
import contextlib
import io
import math
import os
import platform
import shutil
import subprocess
import sys
import timeit
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
BASH_IMPL = REPO_ROOT / "src" / "bash" / "pigame.sh"
C_IMPL = REPO_ROOT / "src" / "c" / "pigame"
PYTHON_IMPL = REPO_ROOT / "src" / "python" / "pigame.py"

# Add repo root to path so we can import the Python module directly.
sys.path.insert(0, str(REPO_ROOT))


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass
class TimingResult:
    """Raw timing samples (milliseconds) for one benchmark case."""

    label: str
    impl: str
    samples: list[float] = field(default_factory=list)

    @property
    def mean(self) -> float:
        return sum(self.samples) / len(self.samples) if self.samples else 0.0

    @property
    def stdev(self) -> float:
        if len(self.samples) < 2:
            return 0.0
        m = self.mean
        return math.sqrt(
            sum((x - m) ** 2 for x in self.samples) / (len(self.samples) - 1)
        )

    @property
    def minimum(self) -> float:
        return min(self.samples) if self.samples else 0.0

    @property
    def maximum(self) -> float:
        return max(self.samples) if self.samples else 0.0

    @property
    def n(self) -> int:
        return len(self.samples)


@dataclass
class BenchmarkGroup:
    """A named workload with results from multiple implementations."""

    name: str
    description: str
    results: list[TimingResult] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Availability helpers
# ---------------------------------------------------------------------------


def _bash_available() -> bool:
    return BASH_IMPL.exists() and shutil.which("bash") is not None


def _c_available() -> bool:
    return C_IMPL.exists() and C_IMPL.is_file()


def _python_available() -> bool:
    return PYTHON_IMPL.exists()


# ---------------------------------------------------------------------------
# Low-level timing helpers
# ---------------------------------------------------------------------------


def _time_subprocess(
    cmd: list[str], iterations: int, env: dict | None = None
) -> list[float]:
    """Time *cmd* over *iterations* runs; returns elapsed times in milliseconds."""
    run_env = {**os.environ, **(env or {})}
    samples: list[float] = []
    for _ in range(iterations):
        start = timeit.default_timer()
        subprocess.run(cmd, capture_output=True, env=run_env, check=False)
        elapsed_ms = (timeit.default_timer() - start) * 1_000
        samples.append(elapsed_ms)
    return samples


def _time_callable(fn: Callable, iterations: int) -> list[float]:
    """Time a zero-arg callable *fn* over *iterations* runs; returns ms."""
    samples: list[float] = []
    for _ in range(iterations):
        start = timeit.default_timer()
        fn()
        elapsed_ms = (timeit.default_timer() - start) * 1_000
        samples.append(elapsed_ms)
    return samples


# ---------------------------------------------------------------------------
# Subprocess runner wrappers
# ---------------------------------------------------------------------------


def _run_bash(*args: str) -> list[str]:
    return ["bash", str(BASH_IMPL), *args]


def _run_c(*args: str) -> tuple[list[str], dict]:
    env = {"SCRIPT_DIR": str(REPO_ROOT)}
    return [str(C_IMPL), *args], env


def _run_python(*args: str) -> list[str]:
    return [sys.executable, str(PYTHON_IMPL), *args]


# ---------------------------------------------------------------------------
# Benchmark definitions
# ---------------------------------------------------------------------------

#: Representative precision levels for the -p N workload
#: Capped at 500 – the number of verified pi digits available in the implementations.
PRECISION_LEVELS = [10, 100, 500]

#: Representative pi strings for the comparison workload
COMPARISON_CASES = [
    ("3.14159", "5-digit (correct)"),
    ("3.14158", "5-digit (wrong)"),
    ("3.14159265358979323846", "20-digit (correct)"),
    ("3.14159265358979323845", "20-digit (wrong)"),
]


def _collect_precision_group(
    precision: int,
    iterations: int,
    include_bash: bool,
    include_c: bool,
) -> BenchmarkGroup:
    """Benchmark ``-p <precision>`` across all available implementations."""
    group = BenchmarkGroup(
        name=f"pi -p {precision}",
        description=f"Calculate and display π to {precision} decimal places",
    )

    # Python (subprocess – same playing field as Bash/C)
    cmd_py = _run_python("-p", str(precision))
    group.results.append(
        TimingResult(
            label=f"-p {precision}",
            impl="Python (subprocess)",
            samples=_time_subprocess(cmd_py, iterations),
        )
    )

    if include_bash and _bash_available():
        cmd_bash = _run_bash("-p", str(precision))
        group.results.append(
            TimingResult(
                label=f"-p {precision}",
                impl="Bash",
                samples=_time_subprocess(cmd_bash, iterations),
            )
        )

    if include_c and _c_available():
        cmd_c, env_c = _run_c("-p", str(precision))
        group.results.append(
            TimingResult(
                label=f"-p {precision}",
                impl="C",
                samples=_time_subprocess(cmd_c, iterations, env=env_c),
            )
        )

    return group


def _collect_comparison_group(
    pi_str: str,
    case_label: str,
    iterations: int,
    include_bash: bool,
    include_c: bool,
) -> BenchmarkGroup:
    """Benchmark digit-comparison for a given pi string."""
    group = BenchmarkGroup(
        name=f"compare {case_label}",
        description=f"Compare user input '{pi_str}' against correct π",
    )

    cmd_py = _run_python(pi_str)
    group.results.append(
        TimingResult(
            label=case_label,
            impl="Python (subprocess)",
            samples=_time_subprocess(cmd_py, iterations),
        )
    )

    if include_bash and _bash_available():
        cmd_bash = _run_bash(pi_str)
        group.results.append(
            TimingResult(
                label=case_label,
                impl="Bash",
                samples=_time_subprocess(cmd_bash, iterations),
            )
        )

    if include_c and _c_available():
        cmd_c, env_c = _run_c(pi_str)
        group.results.append(
            TimingResult(
                label=case_label,
                impl="C",
                samples=_time_subprocess(cmd_c, iterations, env=env_c),
            )
        )

    return group


def _collect_python_internal_group(iterations: int) -> BenchmarkGroup:
    """Benchmark individual Python functions directly (no subprocess overhead)."""
    try:
        from src.python import pigame  # noqa: PLC0415
    except ImportError:
        return BenchmarkGroup(
            name="Python internal functions",
            description="(import failed – skipped)",
        )

    group = BenchmarkGroup(
        name="Python internal functions",
        description="Direct timing of Python module functions (no subprocess overhead)",
    )

    # Pre-compute values used by multiple cases to avoid measuring construction time.
    _pi20 = pigame.calculate_pi(20)
    _pi100 = pigame.calculate_pi(100)
    _pi500 = pigame.calculate_pi(500)
    _wrong20 = "3." + "1" * 20
    _long_valid = "3." + "1" * 50

    def _color_match() -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return pigame.color_your_pi(input_pi=_pi20, correct_pi=_pi20, verbose=False)

    def _color_mismatch() -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return pigame.color_your_pi(
                input_pi=_wrong20, correct_pi=_pi20, verbose=False
            )

    cases: list[tuple[str, Callable]] = [
        ("calculate_pi(10)", lambda: pigame.calculate_pi(10)),
        ("calculate_pi(100)", lambda: pigame.calculate_pi(100)),
        ("calculate_pi(500)", lambda: pigame.calculate_pi(500)),
        ("calculate_constant('e', 100)", lambda: pigame.calculate_constant("e", 100)),
        (
            "calculate_constant('phi', 100)",
            lambda: pigame.calculate_constant("phi", 100),
        ),
        (
            "calculate_constant('sqrt2', 100)",
            lambda: pigame.calculate_constant("sqrt2", 100),
        ),
        (
            "format_pi_with_spaces(100)",
            lambda: pigame.format_pi_with_spaces(_pi100),
        ),
        ("color_your_pi match (20 digits)", _color_match),
        ("color_your_pi mismatch (20 digits)", _color_mismatch),
        ("input_validation (valid)", lambda: pigame.input_validation("3.14159")),
        ("input_validation (long)", lambda: pigame.input_validation(_long_valid)),
    ]

    for name, fn in cases:
        group.results.append(
            TimingResult(
                label=name,
                impl="Python (direct)",
                samples=_time_callable(fn, iterations),
            )
        )

    return group


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

_COL_IMPL = 26
_COL_MEAN = 10
_COL_STDEV = 10
_COL_MIN = 10
_COL_MAX = 10


def _fmt_ms(value: float) -> str:
    """Format a millisecond value to a human-readable string."""
    if value < 0.001:
        return f"{value * 1_000:.3f} µs"
    if value < 1.0:
        return f"{value * 1_000:.1f} µs"
    if value < 1_000:
        return f"{value:.3f} ms"
    return f"{value / 1_000:.3f}  s"


def _header_row() -> str:
    impl = "Implementation".ljust(_COL_IMPL)
    mean = "Mean".rjust(_COL_MEAN)
    stdev = "Stdev".rjust(_COL_STDEV)
    minimum = "Min".rjust(_COL_MIN)
    maximum = "Max".rjust(_COL_MAX)
    n = "  N"
    return f"| {impl} | {mean} | {stdev} | {minimum} | {maximum} | {n} |"


def _separator_row() -> str:
    return (
        f"| {'-' * _COL_IMPL} | {'-' * _COL_MEAN} | {'-' * _COL_STDEV}"
        f" | {'-' * _COL_MIN} | {'-' * _COL_MAX} | --- |"
    )


def _data_row(result: TimingResult) -> str:
    impl = result.impl.ljust(_COL_IMPL)
    mean = _fmt_ms(result.mean).rjust(_COL_MEAN)
    stdev = _fmt_ms(result.stdev).rjust(_COL_STDEV)
    minimum = _fmt_ms(result.minimum).rjust(_COL_MIN)
    maximum = _fmt_ms(result.maximum).rjust(_COL_MAX)
    n = str(result.n).rjust(3)
    return f"| {impl} | {mean} | {stdev} | {minimum} | {maximum} | {n} |"


def _speedup_note(results: list[TimingResult]) -> str:
    """If more than one result, show fastest vs slowest relative speedup."""
    if len(results) < 2:
        return ""
    sorted_r = sorted(results, key=lambda r: r.mean)
    fastest = sorted_r[0]
    slowest = sorted_r[-1]
    if fastest.mean == 0:
        return ""
    ratio = slowest.mean / fastest.mean
    return f"> **{fastest.impl}** is **{ratio:.1f}×** faster than **{slowest.impl}**."


def render_report(
    groups: list[BenchmarkGroup],
    iterations: int,
    include_bash: bool,
    include_c: bool,
) -> str:
    """Render all benchmark groups as a Markdown report string."""
    lines: list[str] = []

    # Header
    lines.append("# PIGAME Performance Benchmark Report\n")
    lines.append(f"- **Platform**: {platform.system()} {platform.release()}  ")
    lines.append(f"- **Python**: {sys.version.split()[0]}  ")
    lines.append(f"- **Iterations per case**: {iterations}  ")
    lines.append(
        f"- **Implementations tested**: Python"
        f"{', Bash' if include_bash and _bash_available() else ''}"
        f"{', C' if include_c and _c_available() else ''}  "
    )
    lines.append("")

    for group in groups:
        lines.append(f"## {group.name}\n")
        lines.append(f"_{group.description}_\n")

        if not group.results:
            lines.append("_No results collected._\n")
            continue

        lines.append(_header_row())
        lines.append(_separator_row())
        for result in group.results:
            lines.append(_data_row(result))
        lines.append("")

        note = _speedup_note(group.results)
        if note:
            lines.append(note)
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Progress helpers
# ---------------------------------------------------------------------------


def _progress(msg: str) -> None:
    print(f"  {msg}", flush=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark all three pigame implementations and print a report.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-n",
        "--iterations",
        type=int,
        default=50,
        metavar="N",
        help="Number of iterations per benchmark case (default: 50).",
    )
    parser.add_argument(
        "--no-bash",
        action="store_true",
        help="Skip the Bash implementation.",
    )
    parser.add_argument(
        "--no-c",
        action="store_true",
        help="Skip the C implementation.",
    )
    parser.add_argument(
        "--no-internal",
        action="store_true",
        help="Skip Python internal (direct call) benchmarks.",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        default=None,
        help="Write the Markdown report to FILE in addition to stdout.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    iterations: int = args.iterations
    include_bash: bool = not args.no_bash
    include_c: bool = not args.no_c

    print(f"\nPIGAME Benchmark  (iterations={iterations})\n{'=' * 42}")

    if include_bash and not _bash_available():
        print("  [WARN] Bash implementation not found – skipping Bash benchmarks.")
        include_bash = False
    if include_c and not _c_available():
        print(
            "  [WARN] C binary not found – run `make build-c` then retry.\n"
            "         Skipping C benchmarks."
        )
        include_c = False

    groups: list[BenchmarkGroup] = []

    # 1. Precision benchmarks
    for precision in PRECISION_LEVELS:
        _progress(f"Benchmarking: pi calculation -p {precision}  …")
        groups.append(
            _collect_precision_group(precision, iterations, include_bash, include_c)
        )

    # 2. Comparison benchmarks
    for pi_str, case_label in COMPARISON_CASES:
        _progress(f"Benchmarking: comparison '{case_label}'  …")
        groups.append(
            _collect_comparison_group(
                pi_str, case_label, iterations, include_bash, include_c
            )
        )

    # 3. Python internal function benchmarks
    if not args.no_internal:
        _progress("Benchmarking: Python internal functions (direct calls)  …")
        groups.append(_collect_python_internal_group(iterations * 10))

    print("\nRendering report …\n")
    report = render_report(groups, iterations, include_bash, include_c)

    print(report)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding="utf-8")
        print(f"\nReport also saved to: {output_path}")


if __name__ == "__main__":
    main()
