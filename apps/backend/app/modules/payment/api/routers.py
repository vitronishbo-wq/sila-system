"""Consolidação de routers para o módulo de Pagamentos."""

from fastapi import APIRouter

from .health import router as health_router
from .router import router as payment_router

# Router consolidado que agrupa health + pagamentos
combined_router = APIRouter()

# Adiciona routers de health
combined_router.include_router(health_router, tags=["health"])

# Adiciona routers de pagamentos
combined_router.include_router(payment_router)

__all__ = ["combined_router", "health_router", "payment_router"]
