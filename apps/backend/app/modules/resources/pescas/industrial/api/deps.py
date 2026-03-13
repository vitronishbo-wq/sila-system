from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.api.deps import get_db
from apps.backend.app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from apps.backend.app.core.bridges.resources_external_services_bridge import get_estabelecimento_industrial_service
from apps.backend.app.modules.resources.pescas.api.deps import get_armador_service
from apps.backend.app.modules.resources.pescas.industrial.application.services.inspecao_industrial_service import InspecaoIndustrialService
from apps.backend.app.modules.resources.pescas.industrial.application.services.lote_producao_service import LoteProducaoService
from apps.backend.app.modules.resources.pescas.industrial.application.services.produto_processado_service import ProdutoProcessadoService
from apps.backend.app.modules.resources.pescas.industrial.application.services.unidade_processamento_service import UnidadeProcessamentoService
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.adapters.citizen_service_adapter import CitizenServiceAdapter
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.adapters.industria_service_adapter import IndustriaServiceAdapter
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.adapters.pescas_service_adapter import PescasServiceAdapter
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.adapters.request_service_adapter import RequestServiceAdapter
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.repositories.sqlalchemy_inspecao_repository import SQLAlchemyInspecaoRepository
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.repositories.sqlalchemy_lote_producao_repository import SQLAlchemyLoteProducaoRepository
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.repositories.sqlalchemy_produto_processado_repository import SQLAlchemyProdutoProcessadoRepository
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.repositories.sqlalchemy_unidade_processamento_repository import SQLAlchemyUnidadeProcessamentoRepository

async def get_unidade_processamento_service(session: AsyncSession=Depends(get_db)) -> UnidadeProcessamentoService:
    unidade_repo = SQLAlchemyUnidadeProcessamentoRepository(session)
    pescas_service = PescasServiceAdapter(await get_armador_service())
    industria_service = IndustriaServiceAdapter(get_estabelecimento_industrial_service())
    citizen_service = CitizenServiceAdapter(CitizenRepository(session))
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return UnidadeProcessamentoService(unidade_repo=unidade_repo, pescas_service=pescas_service, industria_service=industria_service, citizen_service=citizen_service, request_service=request_service)

async def get_produto_processado_service(session: AsyncSession=Depends(get_db)) -> ProdutoProcessadoService:
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return ProdutoProcessadoService(produto_repo=SQLAlchemyProdutoProcessadoRepository(session), unidade_repo=SQLAlchemyUnidadeProcessamentoRepository(session), request_service=request_service)

async def get_lote_producao_service(session: AsyncSession=Depends(get_db)) -> LoteProducaoService:
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return LoteProducaoService(lote_repo=SQLAlchemyLoteProducaoRepository(session), produto_repo=SQLAlchemyProdutoProcessadoRepository(session), unidade_repo=SQLAlchemyUnidadeProcessamentoRepository(session), request_service=request_service)

async def get_inspecao_industrial_service(session: AsyncSession=Depends(get_db)) -> InspecaoIndustrialService:
    request_service = RequestServiceAdapter(ServiceRequestLifecycleBridge(session))
    return InspecaoIndustrialService(inspecao_repo=SQLAlchemyInspecaoRepository(session), unidade_repo=SQLAlchemyUnidadeProcessamentoRepository(session), lote_repo=SQLAlchemyLoteProducaoRepository(session), request_service=request_service)