"""
Identity Module for SILA System.

This module provides the core civil identity management functionality,
focusing on immutable personal data while intelligently referencing
other modules to avoid data duplication.

Key Features:
- Core civil identity data (name, birth date, gender, national ID)
- Intelligent relationships with citizenship, documents, and address modules
- Comprehensive validation and business rules
- RESTful API with proper security controls
- Extensive testing coverage
- Complete documentation

Architecture:
- Models: CitizenIdentity with smart relationships
- Schemas: Pydantic validation with nested references
- Services: Business logic with anti-duplication rules
- Routes: REST API with role-based security
- Tests: Comprehensive test coverage
- Documentation: Complete usage guide

Integration:
- citizenship: References citizenship data without duplication
- documents: One-to-many relationship with documents
- address: References address data without duplication
- auth: Optional association with user accounts
"""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from .endpoints import router

__all__ = ["router"]
