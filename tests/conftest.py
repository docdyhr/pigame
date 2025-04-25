"""Test configuration file for pytest."""

import sys
from pathlib import Path


# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
