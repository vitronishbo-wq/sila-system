from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.domain.bridges.resources_external_services_bridge import get_exportador_service, get_imovel_service
from app.domain.territory.service import TerritoryService
from apps.backend.app.modules.resources.agricultura.api.deps import get_propriedade_service
from apps.backend.app.modules.resources.ambiente.api.deps import get_cadastro_service
from apps.backend.app.modules.energy.api.deps import get_geracao_service
from apps.backend.app.modules.resources.florestas.application.services.inventario_service import InventarioService
from apps.backend.app.modules.resources.florestas.application.services.manejo_service import ManejoService
from apps.backend.app.modules.resources.florestas.application.services.operador_florestal_service import OperadorFlorestalService
from apps.backend.app.modules.resources.florestas.application.services.plano_manejo_service import PlanoManejoService
from apps.backend.app.modules.resources.florestas.application.services.estatistica_florestal_service import EstatisticaFlorestalService
from apps.backend.app.modules.resources.florestas.infrastructure.adapters.agricultura_service_adapter import AgriculturaServiceAdapter
from apps.backend.app.modules.resources.florestas.infrastructure.adapters.ambiente_service_adapter import AmbienteServiceAdapter
from apps.backend.app.modules.resources.florestas.infrastructure.adapters.comercio_externo_service_adapter import ComercioExternoServiceAdapter
from apps.backend.app.modules.resources.florestas.infrastructure.adapters.energia_service_adapter import EnergiaServiceAdapter
from apps.backend.app.modules.resources.florestas.infrastructure.adapters.geosampa_service_adapter import GeosampaServiceAdapter
from apps.backend.app.modules.resources.florestas.infrastructure.adapters.gestao_fundiaria_service_adapter import GestaoFundiariaServiceAdapter
from apps.backend.app.modules.resources.florestas.infrastructure.repositories.sqlalchemy_inventario_florestal_repository import SQLAlchemyInventarioFlorestalRepository
from apps.backend.app.modules.resources.florestas.infrastructure.repositories.sqlalchemy_operador_florestal_repository import SQLAlchemyOperadorFlorestalRepository
from apps.backend.app.modules.resources.florestas.infrastructure.repositories.sqlalchemy_plano_manejo_florestal_repository import SQLAlchemyPlanoManejoFlorestalRepository
from apps.backend.app.modules.resources.florestas.infrastructure.repositories.sqlalchemy_unidade_manejo_repository import SQLAlchemyUnidadeManejoRepository

async def get_operador_florestal_service(session: AsyncSession=Depends(get_db)) -> OperadorFlorestalService:
    return OperadorFlorestalService(repository=SQLAlchemyOperadorFlorestalRepository(session))

async def get_manejo_service(session: AsyncSession=Depends(get_db)) -> ManejoService:
    return ManejoService(unidade_repo=SQLAlchemyUnidadeManejoRepository(session))

async def get_plano_manejo_service(session: AsyncSession=Depends(get_db)) -> PlanoManejoService:
    return PlanoManejoService(plano_repo=SQLAlchemyPlanoManejoFlorestalRepository(session), unidade_repo=SQLAlchemyUnidadeManejoRepository(session))

async def get_inventario_service(session: AsyncSession=Depends(get_db)) -> InventarioService:
    return InventarioService(inventario_repo=SQLAlchemyInventarioFlorestalRepository(session))

async def get_estatistica_florestal_service(session: AsyncSession=Depends(get_db)) -> EstatisticaFlorestalService:
    operador_repo = SQLAlchemyOperadorFlorestalRepository(session)
    unidade_repo = SQLAlchemyUnidadeManejoRepository(session)
    plano_repo = SQLAlchemyPlanoManejoFlorestalRepository(session)
    inventario_repo = SQLAlchemyInventarioFlorestalRepository(session)
    ambiente_service = AmbienteServiceAdapter(get_cadastro_service())
    gestao_fundiaria_service = GestaoFundiariaServiceAdapter(get_imovel_service())
    agricultura_service = AgriculturaServiceAdapter(get_propriedade_service())
    energia_service = EnergiaServiceAdapter(get_geracao_service())
    comercio_externo_service = ComercioExternoServiceAdapter(await get_exportador_service(session))
    geosampa_service = GeosampaServiceAdapter(TerritoryService)
    return EstatisticaFlorestalService(operador_repo=operador_repo, unidade_repo=unidade_repo, plano_repo=plano_repo, inventario_repo=inventario_repo, ambiente_service=ambiente_service, gestao_fundiaria_service=gestao_fundiaria_service, agricultura_service=agricultura_service, energia_service=energia_service, comercio_externo_service=comercio_externo_service, geosampa_service=geosampa_service)