"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from fastapi import APIRouter
from .endpoints import router as training_router

# Router principal do módulo
router = training_router

__all__ = ["router"]
