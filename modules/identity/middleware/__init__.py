"""Middleware layer: Cross-cutting concerns (auth, logging, etc)."""

from modules.identity.middleware.trust_middleware import TrustEvaluationMiddleware

__all__ = ['TrustEvaluationMiddleware']
