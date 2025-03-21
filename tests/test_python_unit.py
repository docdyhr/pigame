#!/usr/bin/env python3

import unittest
import sys
import os
import re
import subprocess
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import pigame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/python')))
import pigame

class TestPiGameFunctions(unittest.TestCase):
    """Unit tests for the core functions of the pigame.py module."""

    def test_input_validation_valid(self):
        """Test input validation with valid inputs."""
        # These should not raise an exception
        try:
            pigame.input_validation("3.14159")
            pigame.input_validation("3")
            pigame.input_validation("3.1")
            self.assertTrue(True)  # If we get here, the test passes
        except SystemExit:
            self.fail("input_validation() raised SystemExit unexpectedly!")

    @patch('sys.exit')
    def test_input_validation_invalid(self, mock_exit):
        """Test input validation with invalid inputs."""
        # These should raise a SystemExit
        pigame.input_validation("abc")
        mock_exit.assert_called()
        
        mock_exit.reset_mock()
        pigame.input_validation("3.14.15")
        mock_exit.assert_called()
        
        mock_exit.reset_mock()
        pigame.input_validation("-3.14")
        mock_exit.assert_called()

    def test_length_validation_valid(self):
        """Test length validation with valid inputs."""
        self.assertEqual(pigame.length_validation("15"), 15)
        self.assertEqual(pigame.length_validation("100"), 100)
        # Test that 0 returns the default length
        self.assertEqual(pigame.length_validation("0"), pigame.DEFAULT_LENGTH)

    def test_length_validation_invalid(self):
        """Test length validation with invalid inputs."""
        # Test invalid string input
        with self.assertRaises(ValueError):
            with patch('sys.exit'):  # Prevent actual exit
                pigame.length_validation("abc")
        
        # Test too large input - the function calls sys.exit, so it might not raise directly
        # Instead, patch sys.exit and just make sure our function tries to call it
        with patch('sys.exit') as mock_exit:
            with self.assertRaises(SystemExit):
                pigame.length_validation(str(pigame.MAX_LENGTH + 1))
                mock_exit.assert_called()

    def test_calculate_pi(self):
        """Test pi calculation with various lengths."""
        self.assertEqual(pigame.calculate_pi(1), "3.1")
        self.assertEqual(pigame.calculate_pi(5), "3.14159")
        # Test a longer calculation to ensure precision
        pi_15 = pigame.calculate_pi(15)
        self.assertEqual(len(pi_15), 17)  # "3." + 15 digits
        self.assertTrue(pi_15.startswith("3.14159265358979"))

    def test_color_your_pi(self):
        """Test the function that colors differences in pi."""
        # Test with matching input
        with patch('builtins.print') as mock_print:
            error_count = pigame.color_your_pi("3.14159", "3.14159", False)
            mock_print.assert_called()
            self.assertEqual(error_count, 0)
        
        # Test with non-matching input
        with patch('builtins.print') as mock_print:
            error_count = pigame.color_your_pi("3.14158", "3.14159", True)
            # Should print the string and the error count
            self.assertEqual(mock_print.call_count, 2)
            self.assertEqual(error_count, 1)

    def test_handle_easter_egg(self):
        """Test the easter egg handler."""
        # Test with various easter egg inputs
        with patch('builtins.print') as mock_print:
            result = pigame.handle_easter_egg("Archimedes")
            self.assertTrue(result)
            self.assertEqual(mock_print.call_count, 3)  # Should print 3 lines
        
        with patch('builtins.print') as mock_print:
            result = pigame.handle_easter_egg("pi")
            self.assertTrue(result)
        
        with patch('builtins.print') as mock_print:
            result = pigame.handle_easter_egg("PI")
            self.assertTrue(result)
        
        # Test with non-easter egg input
        with patch('builtins.print') as mock_print:
            result = pigame.handle_easter_egg("3.14159")
            self.assertFalse(result)
            mock_print.assert_not_called()


class TestPiGameIntegration(unittest.TestCase):
    """Integration tests that call the pigame.py script as a subprocess."""
    
    def setUp(self):
        """Set up the test environment."""
        self.pigame_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/python/pigame.py'))
        # Ensure the script is executable
        os.chmod(self.pigame_path, 0o755)
    
    def run_pigame(self, args):
        """Helper function to run the pigame script with given arguments."""
        cmd = [self.pigame_path] + args
        process = subprocess.run(cmd, capture_output=True, text=True)
        return process.stdout, process.stderr, process.returncode
    
    def test_version_flag(self):
        """Test the -V flag."""
        stdout, stderr, returncode = self.run_pigame(["-V"])
        self.assertIn("version:", stdout)
        self.assertEqual(returncode, 0)
    
    def test_pi_calculation(self):
        """Test pi calculation with -p flag."""
        stdout, stderr, returncode = self.run_pigame(["-p", "5"])
        self.assertIn("3.14159", stdout)
        self.assertEqual(returncode, 0)
    
    def test_correct_input_verbose(self):
        """Test with correct pi input and verbose flag."""
        stdout, stderr, returncode = self.run_pigame(["-v", "3.14159"])
        self.assertTrue("Well done" in stdout or "Perfect" in stdout)
        self.assertEqual(returncode, 0)
    
    def test_incorrect_input_verbose(self):
        """Test with incorrect pi input and verbose flag."""
        stdout, stderr, returncode = self.run_pigame(["-v", "3.14158"])
        self.assertIn("You can do better", stdout)
        self.assertEqual(returncode, 0)
    
    def test_correct_input(self):
        """Test with correct pi input without verbose flag."""
        stdout, stderr, returncode = self.run_pigame(["3.14159"])
        self.assertIn("Match", stdout)
        self.assertEqual(returncode, 0)
    
    def test_incorrect_input(self):
        """Test with incorrect pi input without verbose flag."""
        stdout, stderr, returncode = self.run_pigame(["3.14158"])
        self.assertIn("No match", stdout)
        self.assertEqual(returncode, 0)
    
    def test_invalid_input(self):
        """Test with invalid input."""
        stdout, stderr, returncode = self.run_pigame(["abc"])
        self.assertIn("Invalid input", stderr)
        self.assertEqual(returncode, 1)
    
    def test_easter_egg(self):
        """Test the easter egg functionality."""
        stdout, stderr, returncode = self.run_pigame(["Archimedes"])
        self.assertIn("Archimedes constant", stdout)
        self.assertEqual(returncode, 0)


if __name__ == '__main__':
    unittest.main()