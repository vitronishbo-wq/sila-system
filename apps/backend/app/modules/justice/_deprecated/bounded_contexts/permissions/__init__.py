"""Deprecated: Justice permissions module. Use core/auth instead.

This module is maintained for backward compatibility only.  
All authorization logic has been consolidated in:
- apps.backend.core.auth.PolicyEngine (policy evaluation)
- apps.backend.core.auth.PermissionGuard (FastAPI guards)
- apps.backend.core.auth.RoleManager (role management)

Migration path:
  OLD: from justice.bounded_contexts.permissions import ...
  NEW: from apps.backend.core.auth import PolicyEngine, PermissionGuard, RoleManager
"""
from .access_control import PermissionGuard, PolicyEngine
from .policies import PolicyEngine as PolicyEngine_
__all__ = ['PermissionGuard', 'PolicyEngine']