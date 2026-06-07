from __future__ import annotations

from apps.backend.app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.economy.trade.services.application.services import (
    EstabelecimentoComercialService,
)
from apps.backend.app.modules.economy.trade.services.infrastructure.repositories import (
    SQLAlchemyEstabelecimentoComercialRepository,
)
from apps.backend.core.auth import PermissionGuard, PolicyEngine

_permission_guard = PermissionGuard(PolicyEngine())
estabelecimento_comercial_repo_singleton = SQLAlchemyEstabelecimentoComercialRepository()
estabelecimento_comercial_service_singleton = EstabelecimentoComercialService(
    repository=estabelecimento_comercial_repo_singleton
)
db_dep = Depends(get_db)
trade_permission_dep = Depends(
    _permission_guard.required_permission("trade.estabelecimento_comercial.manage")
)


def get_estabelecimento_comercial_service() -> EstabelecimentoComercialService:
    return estabelecimento_comercial_service_singleton


async def get_estabelecimento_comercial_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = trade_permission_dep,
) -> EstabelecimentoComercialService:
    """Trade services with permission guard: requires trade.estabelecimento_comercial.manage"""
    repository = SQLAlchemyEstabelecimentoComercialRepository(session)
    return EstabelecimentoComercialService(repository=repository)