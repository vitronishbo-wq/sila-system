"""Middleware layer: Cross-cutting concerns (auth, logging, etc)."""

from apps.backend.app.modules.identity.middleware.trust_middleware import TrustEvaluationMiddleware

__all__ = ['TrustEvaluationMiddleware']
