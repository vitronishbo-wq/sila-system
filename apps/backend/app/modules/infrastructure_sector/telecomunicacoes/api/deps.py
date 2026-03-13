from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.bridges import CitizenRepository, ServiceRequestLifecycleBridge
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.events import event_bus
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.events.definitions import FaturaTelecomGeradaEvent, QualidadeServicoAferidaEvent, ReclamacaoTelecomAbertaEvent
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.handlers import AnatelHandler, FaturamentoHandler, QualidadeHandler
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.assinante_service import AssinanteService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.espectro_service import EspectroService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.faturamento_service import FaturamentoService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.indicador_qualidade_service import IndicadorQualidadeService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.infraestrutura_service import InfraestruturaService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.operadora_service import OperadoraService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.outorga_espectro_service import OutorgaEspectroService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.qualidade_servico_service import QualidadeServicoService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.reclamacao_service import ReclamacaoService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.sla_service import SLAService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.persistence import SQLAlchemyOutboxRepository
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.adapters.anatel_adapter import AnatelAdapter
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.adapters.citizen_service_adapter import CitizenServiceAdapter
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.adapters.request_service_adapter import RequestServiceAdapter
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_espectro_repository import SQLAlchemyEspectroRepository
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_fatura_repository import SQLAlchemyFaturaRepository
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_infraestrutura_repository import SQLAlchemyInfraestruturaRepository
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_indicador_qualidade_repository import SQLAlchemyIndicadorQualidadeRepository
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_assinante_repository import SQLAlchemyAssinanteRepository
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_operadora_repository import SQLAlchemyOperadoraRepository
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_outorga_espectro_repository import SQLAlchemyOutorgaEspectroRepository
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_qualidade_servico_repository import SQLAlchemyQualidadeServicoRepository
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_reclamacao_repository import SQLAlchemyReclamacaoRepository
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.repositories.sqlalchemy_sla_repository import SQLAlchemySLARepository
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.workers import OutboxWorker
anatel_adapter_singleton = AnatelAdapter()
anatel_handler_singleton = AnatelHandler(anatel_adapter=anatel_adapter_singleton)
faturamento_handler_singleton = FaturamentoHandler()
qualidade_handler_singleton = QualidadeHandler()
outbox_worker_singleton = OutboxWorker()
_subscriptions_configured = False

def _configure_subscriptions() -> None:
    global _subscriptions_configured
    if _subscriptions_configured:
        return
    event_bus.subscribe(FaturaTelecomGeradaEvent, faturamento_handler_singleton.on_fatura_gerada)
    event_bus.subscribe(ReclamacaoTelecomAbertaEvent, anatel_handler_singleton.on_reclamacao_aberta)
    event_bus.subscribe(QualidadeServicoAferidaEvent, anatel_handler_singleton.on_qualidade_aferida)
    event_bus.subscribe(QualidadeServicoAferidaEvent, qualidade_handler_singleton.on_qualidade_aferida)
    _subscriptions_configured = True
_configure_subscriptions()

async def get_operadora_service(session: AsyncSession=Depends(get_db)) -> OperadoraService:
    return OperadoraService(operadora_repo=SQLAlchemyOperadoraRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_assinante_service(session: AsyncSession=Depends(get_db)) -> AssinanteService:
    operadora_repo = SQLAlchemyOperadoraRepository(session)
    return AssinanteService(assinante_repo=SQLAlchemyAssinanteRepository(session), operadora_repo=operadora_repo, citizen_service=CitizenServiceAdapter(CitizenRepository(session)), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_infraestrutura_service(session: AsyncSession=Depends(get_db)) -> InfraestruturaService:
    operadora_repo = SQLAlchemyOperadoraRepository(session)
    return InfraestruturaService(infraestrutura_repo=SQLAlchemyInfraestruturaRepository(session), operadora_repo=operadora_repo, request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_outorga_espectro_service(session: AsyncSession=Depends(get_db)) -> OutorgaEspectroService:
    operadora_repo = SQLAlchemyOperadoraRepository(session)
    return OutorgaEspectroService(outorga_repo=SQLAlchemyOutorgaEspectroRepository(session), operadora_repo=operadora_repo, request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_espectro_service(session: AsyncSession=Depends(get_db)) -> EspectroService:
    return EspectroService(espectro_repo=SQLAlchemyEspectroRepository(session), outorga_repo=SQLAlchemyOutorgaEspectroRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_sla_service(session: AsyncSession=Depends(get_db)) -> SLAService:
    operadora_repo = SQLAlchemyOperadoraRepository(session)
    return SLAService(sla_repo=SQLAlchemySLARepository(session), operadora_repo=operadora_repo, request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_qualidade_servico_service(session: AsyncSession=Depends(get_db)) -> QualidadeServicoService:
    return QualidadeServicoService(qualidade_repo=SQLAlchemyQualidadeServicoRepository(session), sla_repo=SQLAlchemySLARepository(session), operadora_repo=SQLAlchemyOperadoraRepository(session), assinante_repo=SQLAlchemyAssinanteRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_indicador_qualidade_service(session: AsyncSession=Depends(get_db)) -> IndicadorQualidadeService:
    return IndicadorQualidadeService(indicador_repo=SQLAlchemyIndicadorQualidadeRepository(session), qualidade_repo=SQLAlchemyQualidadeServicoRepository(session), operadora_repo=SQLAlchemyOperadoraRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)))

async def get_faturamento_service(session: AsyncSession=Depends(get_db)) -> FaturamentoService:
    return FaturamentoService(assinante_repo=SQLAlchemyAssinanteRepository(session), fatura_repo=SQLAlchemyFaturaRepository(session), outbox_repo=SQLAlchemyOutboxRepository(session))

async def get_reclamacao_service(session: AsyncSession=Depends(get_db)) -> ReclamacaoService:
    return ReclamacaoService(assinante_repo=SQLAlchemyAssinanteRepository(session), reclamacao_repo=SQLAlchemyReclamacaoRepository(session), request_service=RequestServiceAdapter(ServiceRequestLifecycleBridge(session)), outbox_repo=SQLAlchemyOutboxRepository(session))

def get_outbox_worker() -> OutboxWorker:
    return outbox_worker_singleton