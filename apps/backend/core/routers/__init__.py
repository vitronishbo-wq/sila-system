"""Core routers module - shared across all domains"""
from .router_factory import RouterFactory
from .health_factory import HealthRouterFactory

__all__ = [
    "RouterFactory",
    "HealthRouterFactory",
]
