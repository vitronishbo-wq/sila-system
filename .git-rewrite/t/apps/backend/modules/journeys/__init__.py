"""
Journeys Module - Intelligent Civic Journey Orchestration

This module implements smart civic journeys that orchestrate multiple services
across different modules to provide complete citizen-centric workflows.

Example: "Birth of a Child" journey triggers:
- Registry: Birth certificate registration
- Health: Vaccination scheduling
- Social: Family support enrollment
"""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from fastapi import APIRouter

router = APIRouter()

__all__ = ["router"]
