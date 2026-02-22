"""
Identity module models.

This module contains models for:
- External identity provider relationships (OAuth/SSO)
- Role and permission management
- Citizen identity proxies (for backward compatibility)
"""

from .identity import Identity
from .citizen_identity import Citizen as CitizenIdentity
from .role_permission import role_permissions

__all__ = ["Identity", "CitizenIdentity", "role_permissions"]
