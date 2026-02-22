"""Common module for shared components across all modules."""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from . import exceptions, bases, utils

__all__ = [
    "exceptions",
    "bases",
    "utils",
    "models",
    "schemas",
    "crud",
    "services",
    "endpoints",
]
