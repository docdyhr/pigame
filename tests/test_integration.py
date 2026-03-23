#!/usr/bin/env python3
"""Cross-implementation integration tests for pigame.

These tests verify that the Bash, C, and Python implementations produce
identical output for the same inputs, ensuring consistency across all
three implementations.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
BASH_IMPL = REPO_ROOT / "src" / "bash" / "pigame.sh"
C_IMPL = REPO_ROOT / "src" / "c" / "pigame"
PYTHON_IMPL = REPO_ROOT / "src" / "python" / "pigame.py"


# ---------------------------------------------------------------------------
# Availability helpers
# ---------------------------------------------------------------------------


def _bash_available() -> bool:
    """Return True if the Bash implementation and bash interpreter are present."""
    return BASH_IMPL.exists() and shutil.which("bash") is not None


def _c_available() -> bool:
    """Return True if the compiled C binary exists."""
    return C_IMPL.exists() and C_IMPL.is_file()


def _python_available() -> bool:
    """Return True if the Python implementation exists."""
    return PYTHON_IMPL.exists()


# ---------------------------------------------------------------------------
# Runner helpers
# ---------------------------------------------------------------------------


def _run(cmd: list[str], *, env: dict | None = None) -> subprocess.CompletedProcess:
    """Run *cmd* and return the CompletedProcess (never raises on non-zero exit)."""
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def _run_bash(*args: str) -> subprocess.CompletedProcess:
    """Run the Bash implementation with *args*."""
    return _run(["bash", str(BASH_IMPL), *args])


def _run_c(*args: str) -> subprocess.CompletedProcess:
    """Run the compiled C implementation with *args*.

    Sets ``SCRIPT_DIR`` so the binary can locate ``src/VERSION``.
    """
    import os  # noqa: PLC0415

    env = os.environ.copy()
    env["SCRIPT_DIR"] = str(REPO_ROOT)
    return _run([str(C_IMPL), *args], env=env)


def _run_python(*args: str) -> subprocess.CompletedProcess:
    """Run the Python implementation with *args*."""
    python = sys.executable
    return _run([python, str(PYTHON_IMPL), *args])


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from *text*."""
    import re  # noqa: PLC0415

    return re.sub(r"\033\[[0-9;]*m", "", text)


# ---------------------------------------------------------------------------
# Shared test data
# ---------------------------------------------------------------------------

PRECISION_CASES = [5, 10, 15, 20]
CORRECT_PI_5 = "3.14159"
CORRECT_PI_10 = "3.1415926535"
WRONG_PI_5 = "3.14158"

EASTER_EGG_TRIGGERS = ["Archimedes", "pi", "PI"]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def require_bash() -> None:
    """Skip the test module if Bash is not available."""
    if not _bash_available():
        pytest.skip("Bash implementation not available")


@pytest.fixture(scope="module")
def require_c() -> None:
    """Skip the test module if the C binary is not compiled."""
    if not _c_available():
        pytest.skip("C implementation not compiled (run `make build-c` first)")


# ---------------------------------------------------------------------------
# Tests: individual implementation smoke-tests
# ---------------------------------------------------------------------------


class TestBashImplementation:
    """Smoke tests for the Bash implementation in isolation."""

    @pytest.mark.skipif(not _bash_available(), reason="Bash not available")
    def test_version_flag(self) -> None:
        """Bash -V should print a version string."""
        result = _run_bash("-V")
        assert result.returncode == 0
        assert "version" in result.stdout.lower() or "version" in result.stderr.lower()

    @pytest.mark.skipif(not _bash_available(), reason="Bash not available")
    def test_pi_precision(self) -> None:
        """Bash -p 5 should output 3.14159."""
        result = _run_bash("-p", "5")
        assert result.returncode == 0
        assert CORRECT_PI_5 in _strip_ansi(result.stdout)

    @pytest.mark.skipif(not _bash_available(), reason="Bash not available")
    def test_correct_input(self) -> None:
        """Bash should report 'Match' for correct pi."""
        result = _run_bash(CORRECT_PI_5)
        assert result.returncode == 0
        assert "Match" in result.stdout

    @pytest.mark.skipif(not _bash_available(), reason="Bash not available")
    def test_wrong_input(self) -> None:
        """Bash should report 'No match' for wrong pi."""
        result = _run_bash(WRONG_PI_5)
        assert result.returncode == 0
        assert "No match" in result.stdout

    @pytest.mark.skipif(not _bash_available(), reason="Bash not available")
    def test_verbose_correct(self) -> None:
        """Bash verbose mode should say 'Well done' for a short correct pi."""
        result = _run_bash("-v", CORRECT_PI_5)
        assert result.returncode == 0
        assert "Well done" in result.stdout

    @pytest.mark.skipif(not _bash_available(), reason="Bash not available")
    def test_verbose_wrong(self) -> None:
        """Bash verbose mode should say 'You can do better!' for wrong pi."""
        result = _run_bash("-v", WRONG_PI_5)
        assert result.returncode == 0
        assert "You can do better!" in result.stdout

    @pytest.mark.skipif(not _bash_available(), reason="Bash not available")
    def test_invalid_input(self) -> None:
        """Bash should exit non-zero for invalid input."""
        result = _run_bash("abc")
        assert result.returncode != 0
        assert "Invalid input" in result.stderr or "Invalid input" in result.stdout

    @pytest.mark.skipif(not _bash_available(), reason="Bash not available")
    @pytest.mark.parametrize("trigger", EASTER_EGG_TRIGGERS)
    def test_easter_egg(self, trigger: str) -> None:
        """Bash should print Archimedes info for Easter-egg triggers."""
        result = _run_bash(trigger)
        assert result.returncode == 0
        assert "Archimedes" in result.stdout


class TestCImplementation:
    """Smoke tests for the C implementation in isolation."""

    @pytest.mark.skipif(not _c_available(), reason="C binary not compiled")
    def test_version_flag(self) -> None:
        """C -V should print a version string."""
        result = _run_c("-V")
        assert result.returncode == 0
        assert "version" in result.stdout.lower()

    @pytest.mark.skipif(not _c_available(), reason="C binary not compiled")
    def test_pi_precision(self) -> None:
        """C -p 5 should output 3.14159."""
        result = _run_c("-p", "5")
        assert result.returncode == 0
        assert CORRECT_PI_5 in _strip_ansi(result.stdout)

    @pytest.mark.skipif(not _c_available(), reason="C binary not compiled")
    def test_correct_input(self) -> None:
        """C should report 'Match' for correct pi."""
        result = _run_c(CORRECT_PI_5)
        assert result.returncode == 0
        assert "Match" in result.stdout

    @pytest.mark.skipif(not _c_available(), reason="C binary not compiled")
    def test_wrong_input(self) -> None:
        """C should report 'No match' for wrong pi."""
        result = _run_c(WRONG_PI_5)
        assert result.returncode == 0
        assert "No match" in result.stdout

    @pytest.mark.skipif(not _c_available(), reason="C binary not compiled")
    def test_verbose_correct(self) -> None:
        """C verbose mode should say 'Well done' for a short correct pi."""
        result = _run_c("-v", CORRECT_PI_5)
        assert result.returncode == 0
        assert "Well done" in result.stdout

    @pytest.mark.skipif(not _c_available(), reason="C binary not compiled")
    def test_verbose_wrong(self) -> None:
        """C verbose mode should say 'You can do better!' for wrong pi."""
        result = _run_c("-v", WRONG_PI_5)
        assert result.returncode == 0
        assert "You can do better!" in result.stdout

    @pytest.mark.skipif(not _c_available(), reason="C binary not compiled")
    def test_invalid_input(self) -> None:
        """C should exit non-zero for non-numeric input."""
        result = _run_c("abc")
        assert result.returncode != 0 or "Invalid input" in result.stdout

    @pytest.mark.skipif(not _c_available(), reason="C binary not compiled")
    @pytest.mark.parametrize("trigger", EASTER_EGG_TRIGGERS)
    def test_easter_egg(self, trigger: str) -> None:
        """C should print Archimedes info for Easter-egg triggers."""
        result = _run_c(trigger)
        assert result.returncode == 0
        assert "Archimedes" in result.stdout


class TestPythonImplementation:
    """Smoke tests for the Python implementation in isolation."""

    def test_version_flag(self) -> None:
        """Python -V should print a version string."""
        result = _run_python("-V")
        assert result.returncode == 0
        assert "version" in result.stdout.lower()

    def test_pi_precision(self) -> None:
        """Python -p 5 should output 3.14159."""
        result = _run_python("-p", "5")
        assert result.returncode == 0
        assert CORRECT_PI_5 in _strip_ansi(result.stdout)

    def test_correct_input(self) -> None:
        """Python should report 'Match' for correct pi."""
        result = _run_python(CORRECT_PI_5)
        assert result.returncode == 0
        assert "Match" in result.stdout

    def test_wrong_input(self) -> None:
        """Python should report 'No match' for wrong pi."""
        result = _run_python(WRONG_PI_5)
        assert result.returncode == 0
        assert "No match" in result.stdout

    def test_verbose_correct(self) -> None:
        """Python verbose mode should say 'Well done' for a short correct pi."""
        result = _run_python("-v", CORRECT_PI_5)
        assert result.returncode == 0
        assert "Well done" in result.stdout

    def test_verbose_wrong(self) -> None:
        """Python verbose mode should say 'You can do better!' for wrong pi."""
        result = _run_python("-v", WRONG_PI_5)
        assert result.returncode == 0
        assert "You can do better!" in result.stdout

    def test_invalid_input(self) -> None:
        """Python should exit non-zero for invalid input."""
        result = _run_python("abc")
        assert result.returncode != 0

    @pytest.mark.parametrize("trigger", EASTER_EGG_TRIGGERS)
    def test_easter_egg(self, trigger: str) -> None:
        """Python should print Archimedes info for Easter-egg triggers."""
        result = _run_python(trigger)
        assert result.returncode == 0
        assert "Archimedes" in result.stdout

    def test_constant_e(self) -> None:
        """Python should calculate e with --constant e."""
        result = _run_python("--constant", "e", "-p", "5")
        assert result.returncode == 0
        assert "2.71828" in _strip_ansi(result.stdout)

    def test_constant_phi(self) -> None:
        """Python should calculate phi with --constant phi."""
        result = _run_python("--constant", "phi", "-p", "5")
        assert result.returncode == 0
        assert "1.61803" in _strip_ansi(result.stdout)

    def test_constant_sqrt2(self) -> None:
        """Python should calculate sqrt2 with --constant sqrt2."""
        result = _run_python("--constant", "sqrt2", "-p", "5")
        assert result.returncode == 0
        assert "1.41421" in _strip_ansi(result.stdout)

    def test_list_flag(self) -> None:
        """Python --list should show all available constants."""
        result = _run_python("--list")
        assert result.returncode == 0
        for key in ("pi", "e", "phi", "sqrt2"):
            assert key in result.stdout


# ---------------------------------------------------------------------------
# Cross-implementation consistency tests
# ---------------------------------------------------------------------------


def _implementations_for_precision() -> list[tuple[str, callable]]:
    """Return available (name, runner) pairs for precision tests."""
    impls: list[tuple[str, callable]] = [("python", _run_python)]
    if _bash_available():
        impls.append(("bash", _run_bash))
    if _c_available():
        impls.append(("c", _run_c))
    return impls


@pytest.mark.skipif(
    not _bash_available() and not _c_available(),
    reason="Need at least two implementations for cross-implementation tests",
)
class TestCrossImplementationConsistency:
    """Verify that all available implementations agree on their outputs."""

    @pytest.mark.parametrize("precision", PRECISION_CASES)
    def test_pi_digits_agree(self, precision: int) -> None:
        """All implementations must output the same pi digits for -p N."""
        results: dict[str, str] = {}
        for name, runner in _implementations_for_precision():
            proc = runner("-p", str(precision))
            assert proc.returncode == 0, (
                f"{name} exited with code {proc.returncode} for -p {precision}"
            )
            # Strip ANSI and whitespace for a clean digit string
            digits = _strip_ansi(proc.stdout).strip()
            results[name] = digits

        # All outputs must agree
        unique = set(results.values())
        assert len(unique) == 1, (
            f"Implementations disagree for -p {precision}:\n"
            + "\n".join(f"  {k}: {v!r}" for k, v in results.items())
        )

    def test_correct_input_all_match(self) -> None:
        """All implementations must report 'Match' for correct pi."""
        for name, runner in _implementations_for_precision():
            proc = runner(CORRECT_PI_5)
            assert proc.returncode == 0, f"{name} failed for correct pi"
            assert "Match" in proc.stdout, (
                f"{name} did not output 'Match' for correct pi; got: {proc.stdout!r}"
            )

    def test_wrong_input_all_no_match(self) -> None:
        """All implementations must report 'No match' for wrong pi."""
        for name, runner in _implementations_for_precision():
            proc = runner(WRONG_PI_5)
            assert proc.returncode == 0, f"{name} failed for wrong pi"
            assert "No match" in proc.stdout, (
                f"{name} did not output 'No match' for wrong pi; got: {proc.stdout!r}"
            )

    def test_version_same(self) -> None:
        """All implementations must report the same version number."""
        version_file = REPO_ROOT / "src" / "VERSION"
        if not version_file.exists():
            pytest.skip("VERSION file not found")
        expected_version = version_file.read_text(encoding="utf-8").strip()

        for name, runner in _implementations_for_precision():
            proc = runner("-V")
            assert proc.returncode == 0, f"{name} -V failed"
            output = (proc.stdout + proc.stderr).lower()
            assert expected_version in output, (
                f"{name} does not report version {expected_version!r}; got: {output!r}"
            )

    def test_easter_egg_all_mention_archimedes(self) -> None:
        """All implementations must mention Archimedes for the 'Archimedes' trigger."""
        for name, runner in _implementations_for_precision():
            proc = runner("Archimedes")
            assert proc.returncode == 0, f"{name} failed for 'Archimedes' easter egg"
            assert "Archimedes" in proc.stdout, (
                f"{name} did not mention Archimedes; got: {proc.stdout!r}"
            )

    @pytest.mark.parametrize("precision", [5, 10, 20])
    def test_verbose_pi_digits_agree(self, precision: int) -> None:
        """All implementations must output the same pi digits in verbose -v -p N."""
        reference_pi: str | None = None
        for name, runner in _implementations_for_precision():
            proc = runner("-v", "-p", str(precision))
            assert proc.returncode == 0, f"{name} -v -p {precision} failed"
            stdout = _strip_ansi(proc.stdout)
            # Extract the formatted pi value - it follows "decimals:" in verbose output
            for line in stdout.splitlines():
                if "decimals" in line.lower() and ":" in line:
                    digits = line.split(":", 1)[-1].strip().replace(" ", "")
                    if reference_pi is None:
                        reference_pi = digits
                    else:
                        assert digits == reference_pi, (
                            f"{name} verbose pi digits differ for -p {precision}: "
                            f"{digits!r} vs {reference_pi!r}"
                        )
                    break

    def test_colorblind_mode_does_not_change_match_result(self) -> None:
        """Color-blind mode (-c) must not change Match/No match verdict."""
        for name, runner in _implementations_for_precision():
            proc_normal = runner(CORRECT_PI_5)
            proc_cb = runner("-c", CORRECT_PI_5)
            assert proc_normal.returncode == proc_cb.returncode, (
                f"{name}: returncode differs with -c"
            )
            assert "Match" in proc_normal.stdout
            assert "Match" in proc_cb.stdout
