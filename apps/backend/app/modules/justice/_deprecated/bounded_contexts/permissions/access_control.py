"""Deprecated: Access control is now managed in core/auth"""
try:
    from apps.backend.core.auth import PermissionGuard, PolicyEngine
except ImportError:
    PermissionGuard = None
    PolicyEngine = None
__all__ = ['PermissionGuard', 'PolicyEngine']