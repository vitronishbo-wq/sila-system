"""Deprecated: Policies are now managed in core/auth.PolicyEngine"""
try:
    from apps.backend.core.auth import PolicyEngine
except ImportError:
    PolicyEngine = None
__all__ = ['PolicyEngine']