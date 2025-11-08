# !/usr/bin/env python3
"""Tests for the practice mode of pigame."""

import json
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest


# Add the src directory to the path for importing pigame
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "python"))
import pigame


@pytest.fixture
def _mock_practice_config() -> None:
    """Create a temporary directory for practice mode configuration."""
    original_config_dir = pigame.PRACTICE_CONFIG_DIR
    original_stats_file = pigame.PRACTICE_STATS_FILE

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        pigame.PRACTICE_CONFIG_DIR = temp_path
        pigame.PRACTICE_STATS_FILE = temp_path / "stats.json"

        # Make sure the directory exists but the file doesn't
        if not temp_path.exists():
            temp_path.mkdir(parents=True)
        if pigame.PRACTICE_STATS_FILE.exists():
            pigame.PRACTICE_STATS_FILE.unlink()

        yield
        # Restore original values
        pigame.PRACTICE_CONFIG_DIR = original_config_dir
        pigame.PRACTICE_STATS_FILE = original_stats_file


@pytest.mark.usefixtures("_mock_practice_config")
class TestPracticeMode:
    """Test suite for practice mode functionality."""

    def test_load_practice_stats_new_file(self) -> None:
        """Test loading practice stats when no file exists."""
        # Should create a new file with default stats
        stats = pigame.load_practice_stats()

        assert isinstance(stats, dict)
        assert stats["max_digits"] == 0
        assert stats["total_digits_correct"] == 0
        assert stats["total_practice_sessions"] == 0
        assert stats["last_session_date"] is None
        assert isinstance(stats["history"], list)
        assert len(stats["history"]) == 0

        # Check that the file was created
        assert pigame.PRACTICE_STATS_FILE.exists()

    def test_save_practice_stats(self) -> None:
        """Test saving practice stats."""
        # Create test stats
        test_stats = {
            "max_digits": 10,
            "total_digits_correct": 50,
            "total_practice_sessions": 5,
            "last_session_date": "2025-04-30 12:34:56",
            "history": [
                {
                    "date": "2025-04-30 12:34:56",
                    "max_level": 10,
                    "correct_digits": 50,
                    "duration_seconds": 120,
                },
            ],
        }

        # Save the stats
        pigame.save_practice_stats(test_stats)

        # Load the stats again to verify
        loaded_stats = pigame.load_practice_stats()

        assert loaded_stats == test_stats


@pytest.mark.parametrize(
    ("digit", "expected"),
    [
        ("5", "5"),  # Valid digit
    ],
)
def test_input_digit(digit: str, expected: str) -> None:
    """Test the input_digit function with mocked stdin."""
    with (
        mock.patch("sys.stdin.fileno", return_value=0),
        mock.patch(
            "termios.tcgetattr",
            return_value=[0, 0, 0, 0, 0, 0],
        ),
        mock.patch("termios.tcsetattr"),
        mock.patch("tty.setraw"),
        mock.patch(
            "sys.stdin.read",
            return_value=digit,
        ),
    ):
        result = pigame.input_digit()
        assert result == expected


@pytest.mark.usefixtures("_mock_practice_config")
def test_practice_mode_keyboard_interrupt() -> None:
    """Test practice mode with keyboard interrupt."""
    # Create a mock stdin with fileno method
    mock_stdin = mock.MagicMock()
    mock_stdin.fileno.return_value = 0

    # Mock dependencies
    with (
        mock.patch("pigame.input_digit", side_effect=KeyboardInterrupt),
        mock.patch("sys.stdin", mock_stdin),
        mock.patch(
            "termios.tcgetattr",
            return_value=[0, 0, 0, 0, 0, 0],
        ),
        mock.patch("termios.tcsetattr"),
        mock.patch("time.sleep"),
        mock.patch(
            "sys.stdout.write",
        ),
        mock.patch(
            "sys.stdout.flush",
        ),
        # Ensure the test runs with a fresh configuration each time
        mock.patch(
            "pigame.load_practice_stats",
            return_value={
                "max_digits": 0,
                "total_digits_correct": 0,
                "total_practice_sessions": 0,
                "last_session_date": None,
                "fastest_time": None,
                "best_speed": None,
                "history": [],
            },
        ),
    ):
        # Should not raise exception
        pigame.practice_mode()

        # Check that stats were saved
        assert pigame.PRACTICE_STATS_FILE.exists()

        # Verify stats content
        with pigame.PRACTICE_STATS_FILE.open("r") as f:
            stats = json.load(f)
            assert stats["total_practice_sessions"] == 1
            assert len(stats["history"]) == 1


if __name__ == "__main__":
    pytest.main()
