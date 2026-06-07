"""
Centralized Authorization & Authentication System (SILA Core)

This module consolidates all authentication and authorization logic across SILA services.
It provides:
- JWT token management (creation, validation, expiration)
- Policy-based access control (who can do what)
- Permission guards for FastAPI route protection
- Centralized role management and hierarchy

All modules should import auth from this namespace instead of maintaining
separate auth implementations.

Example:
    from core.auth import JWTHandler, PolicyEngine, PermissionGuard, RoleManager

    jwt_handler = JWTHandler()
    policy_engine = PolicyEngine()
    permission_guard = PermissionGuard(policy_engine)
    role_manager = RoleManager()
"""

from .guards.permission_guard import PermissionGuard
from .jwt_handler import JWTHandler
from .policies.policy_engine import PolicyEngine
from .providers.keycloak import KeycloakAuthProvider
from .roles.role_manager import RoleManager

__all__ = [
    "JWTHandler",
    "PolicyEngine",
    "PermissionGuard",
    "RoleManager",
    "KeycloakAuthProvider",
]
