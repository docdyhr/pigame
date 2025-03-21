#!/usr/bin/env python3

import os
import sys
import re
import subprocess
from unittest.mock import patch, MagicMock
import pytest

# Add the parent directory to the path so we can import pigame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/python')))
import pigame


# Unit tests for core functions
class TestPiGameFunctions:
    """Unit tests for the core functions of the pigame.py module."""

    def test_input_validation_valid(self):
        """Test input validation with valid inputs."""
        # These should not raise an exception
        pigame.input_validation("3.14159")
        pigame.input_validation("3")
        pigame.input_validation("3.1")
        assert True  # If we get here, the test passes

    def test_input_validation_invalid(self):
        """Test input validation with invalid inputs."""
        # These should raise a SystemExit
        with pytest.raises(ValueError):
            with patch('sys.exit'):  # Prevent actual exit
                pigame.input_validation("abc")
        
        with pytest.raises(ValueError):
            with patch('sys.exit'):  # Prevent actual exit
                pigame.input_validation("3.14.15")

        with pytest.raises(ValueError):
            with patch('sys.exit'):  # Prevent actual exit
                pigame.input_validation("-3.14")

    def test_length_validation_valid(self):
        """Test length validation with valid inputs."""
        assert pigame.length_validation("15") == 15
        assert pigame.length_validation("100") == 100
        # Test that 0 returns the default length
        assert pigame.length_validation("0") == pigame.DEFAULT_LENGTH

    def test_length_validation_invalid(self):
        """Test length validation with invalid inputs."""
        # Test invalid string input
        with pytest.raises(ValueError):
            with patch('sys.exit'):  # Prevent actual exit
                pigame.length_validation("abc")
        
        # Test too large input
        with pytest.raises(SystemExit):
            with patch('sys.exit'):  # Prevent actual exit
                pigame.length_validation(str(pigame.MAX_LENGTH + 1))

    def test_calculate_pi(self):
        """Test pi calculation with various lengths."""
        assert pigame.calculate_pi(1) == "3.1"
        assert pigame.calculate_pi(5) == "3.14159"
        
        # Test a longer calculation to ensure precision
        pi_15 = pigame.calculate_pi(15)
        assert len(pi_15) == 17  # "3." + 15 digits
        assert pi_15.startswith("3.14159265358979")

    def test_color_your_pi(self, capsys):
        """Test the function that colors differences in pi."""
        # Test with matching input
        error_count = pigame.color_your_pi("3.14159", "3.14159", False)
        assert error_count == 0
        
        # Test with non-matching input
        error_count = pigame.color_your_pi("3.14158", "3.14159", True)
        captured = capsys.readouterr()
        assert error_count == 1
        assert "Number of errors: 1" in captured.out

    def test_handle_easter_egg(self, capsys):
        """Test the easter egg handler."""
        # Test with various easter egg inputs
        result = pigame.handle_easter_egg("Archimedes")
        captured = capsys.readouterr()
        assert result is True
        assert "Archimedes constant" in captured.out
        
        result = pigame.handle_easter_egg("pi")
        captured = capsys.readouterr()
        assert result is True
        
        result = pigame.handle_easter_egg("PI")
        captured = capsys.readouterr()
        assert result is True
        
        # Test with non-easter egg input
        result = pigame.handle_easter_egg("3.14159")
        captured = capsys.readouterr()
        assert result is False
        assert captured.out == ""


# Integration tests for the CLI interface
class TestPiGameIntegration:
    """Integration tests that call the pigame.py script as a subprocess."""
    
    @pytest.fixture
    def pigame_path(self):
        """Set up the test environment."""
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/python/pigame.py'))
        # Ensure the script is executable
        os.chmod(path, 0o755)
        return path
    
    def run_pigame(self, args, pigame_path):
        """Helper function to run the pigame script with given arguments."""
        cmd = [pigame_path] + args
        process = subprocess.run(cmd, capture_output=True, text=True)
        return process.stdout, process.stderr, process.returncode
    
    def test_version_flag(self, pigame_path):
        """Test the -V flag."""
        stdout, stderr, returncode = self.run_pigame(["-V"], pigame_path)
        assert "version:" in stdout
        assert returncode == 0
    
    def test_pi_calculation(self, pigame_path):
        """Test pi calculation with -p flag."""
        stdout, stderr, returncode = self.run_pigame(["-p", "5"], pigame_path)
        assert "3.14159" in stdout
        assert returncode == 0
    
    def test_correct_input_verbose(self, pigame_path):
        """Test with correct pi input and verbose flag."""
        stdout, stderr, returncode = self.run_pigame(["-v", "3.14159"], pigame_path)
        assert ("Well done" in stdout or "Perfect" in stdout)
        assert returncode == 0
    
    def test_incorrect_input_verbose(self, pigame_path):
        """Test with incorrect pi input and verbose flag."""
        stdout, stderr, returncode = self.run_pigame(["-v", "3.14158"], pigame_path)
        assert "You can do better" in stdout
        assert returncode == 0
    
    def test_correct_input(self, pigame_path):
        """Test with correct pi input without verbose flag."""
        stdout, stderr, returncode = self.run_pigame(["3.14159"], pigame_path)
        assert "Match" in stdout
        assert returncode == 0
    
    def test_incorrect_input(self, pigame_path):
        """Test with incorrect pi input without verbose flag."""
        stdout, stderr, returncode = self.run_pigame(["3.14158"], pigame_path)
        assert "No match" in stdout
        assert returncode == 0
    
    def test_invalid_input(self, pigame_path):
        """Test with invalid input."""
        stdout, stderr, returncode = self.run_pigame(["abc"], pigame_path)
        assert "Invalid input" in stderr
        assert returncode == 1
    
    def test_easter_egg(self, pigame_path):
        """Test the easter egg functionality."""
        stdout, stderr, returncode = self.run_pigame(["Archimedes"], pigame_path)
        assert "Archimedes constant" in stdout
        assert returncode == 0