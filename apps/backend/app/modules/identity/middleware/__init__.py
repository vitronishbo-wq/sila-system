"""Middleware layer: Cross-cutting concerns (auth, logging, etc)."""

from .trust_middleware import TrustEvaluationMiddleware

__all__ = ['TrustEvaluationMiddleware']
