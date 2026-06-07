"""Core routers module - shared across all domains"""

from .health_factory import HealthRouterFactory
from .router_factory import RouterFactory

__all__ = [
    "RouterFactory",
    "HealthRouterFactory",
]
