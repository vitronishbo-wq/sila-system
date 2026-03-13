from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from apps.backend.app.modules.economy.trade.external.application.services import AgenteCargaService, CancelamentoRadarService, DrawbackExternoService, DrawbackIntegradoService, DrawbackInternoService, DrawbackIsencaoService, DrawbackRestituicaoService, DrawbackSubstituicaoService, DespachanteService, DrawbackService, DrawbackSuspensaoService, DrawbackVerdeAmareloService, ExportadorService, HabilitacaoExportadorService, HabilitacaoImportadorService, HabilitacaoRadarService, ImportadorService, RadarService, SiscomexDrawbackService, SuspensaoRadarService, TransportadorInternacionalService
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories import SQLAlchemyCancelamentoRadarRepository, SQLAlchemyDrawbackExternoRepository, SQLAlchemyDrawbackIntegradoRepository, SQLAlchemyDrawbackInternoRepository, SQLAlchemyDrawbackIsencaoRepository, SQLAlchemyDrawbackRestituicaoRepository, SQLAlchemyDrawbackSubstituicaoRepository, SQLAlchemyHabilitacaoExportadorRepository, SQLAlchemyHabilitacaoImportadorRepository, SQLAlchemyHabilitacaoRadarRepository, SQLAlchemyAgenteCargaRepository, SQLAlchemyDespachanteRepository, SQLAlchemyDrawbackRepository, SQLAlchemyDrawbackSuspensaoRepository, SQLAlchemyDrawbackVerdeAmareloRepository, SQLAlchemyImportadorRepository, SQLAlchemyRadarRepository, SQLAlchemySiscomexDrawbackRepository, SQLAlchemySuspensaoRadarRepository, SQLAlchemyTransportadorInternacionalRepository, SQLAlchemyExportadorRepository

async def get_exportador_service(session: AsyncSession=Depends(get_db)) -> ExportadorService:
    repository = SQLAlchemyExportadorRepository(session)
    return ExportadorService(repository=repository)

async def get_importador_service(session: AsyncSession=Depends(get_db)) -> ImportadorService:
    repository = SQLAlchemyImportadorRepository(session)
    return ImportadorService(repository=repository)

async def get_despachante_service(session: AsyncSession=Depends(get_db)) -> DespachanteService:
    repository = SQLAlchemyDespachanteRepository(session)
    return DespachanteService(repository=repository)

async def get_agente_carga_service(session: AsyncSession=Depends(get_db)) -> AgenteCargaService:
    repository = SQLAlchemyAgenteCargaRepository(session)
    return AgenteCargaService(repository=repository)

async def get_transportador_internacional_service(session: AsyncSession=Depends(get_db)) -> TransportadorInternacionalService:
    repository = SQLAlchemyTransportadorInternacionalRepository(session)
    return TransportadorInternacionalService(repository=repository)

async def get_habilitacao_exportador_service(session: AsyncSession=Depends(get_db)) -> HabilitacaoExportadorService:
    repository = SQLAlchemyHabilitacaoExportadorRepository(session)
    return HabilitacaoExportadorService(repository=repository)

async def get_habilitacao_importador_service(session: AsyncSession=Depends(get_db)) -> HabilitacaoImportadorService:
    repository = SQLAlchemyHabilitacaoImportadorRepository(session)
    return HabilitacaoImportadorService(repository=repository)

async def get_radar_service(session: AsyncSession=Depends(get_db)) -> RadarService:
    repository = SQLAlchemyRadarRepository(session)
    return RadarService(repository=repository)

async def get_habilitacao_radar_service(session: AsyncSession=Depends(get_db)) -> HabilitacaoRadarService:
    repository = SQLAlchemyHabilitacaoRadarRepository(session)
    return HabilitacaoRadarService(repository=repository)

async def get_cancelamento_radar_service(session: AsyncSession=Depends(get_db)) -> CancelamentoRadarService:
    repository = SQLAlchemyCancelamentoRadarRepository(session)
    return CancelamentoRadarService(repository=repository)

async def get_suspensao_radar_service(session: AsyncSession=Depends(get_db)) -> SuspensaoRadarService:
    repository = SQLAlchemySuspensaoRadarRepository(session)
    return SuspensaoRadarService(repository=repository)

async def get_drawback_service(session: AsyncSession=Depends(get_db)) -> DrawbackService:
    repository = SQLAlchemyDrawbackRepository(session)
    return DrawbackService(repository=repository)

async def get_drawback_externo_service(session: AsyncSession=Depends(get_db)) -> DrawbackExternoService:
    repository = SQLAlchemyDrawbackExternoRepository(session)
    return DrawbackExternoService(repository=repository)

async def get_drawback_interno_service(session: AsyncSession=Depends(get_db)) -> DrawbackInternoService:
    repository = SQLAlchemyDrawbackInternoRepository(session)
    return DrawbackInternoService(repository=repository)

async def get_drawback_suspensao_service(session: AsyncSession=Depends(get_db)) -> DrawbackSuspensaoService:
    repository = SQLAlchemyDrawbackSuspensaoRepository(session)
    return DrawbackSuspensaoService(repository=repository)

async def get_drawback_isencao_service(session: AsyncSession=Depends(get_db)) -> DrawbackIsencaoService:
    repository = SQLAlchemyDrawbackIsencaoRepository(session)
    return DrawbackIsencaoService(repository=repository)

async def get_drawback_restituicao_service(session: AsyncSession=Depends(get_db)) -> DrawbackRestituicaoService:
    repository = SQLAlchemyDrawbackRestituicaoRepository(session)
    return DrawbackRestituicaoService(repository=repository)

async def get_drawback_substituicao_service(session: AsyncSession=Depends(get_db)) -> DrawbackSubstituicaoService:
    repository = SQLAlchemyDrawbackSubstituicaoRepository(session)
    return DrawbackSubstituicaoService(repository=repository)

async def get_drawback_integrado_service(session: AsyncSession=Depends(get_db)) -> DrawbackIntegradoService:
    repository = SQLAlchemyDrawbackIntegradoRepository(session)
    return DrawbackIntegradoService(repository=repository)

async def get_drawback_verde_amarelo_service(session: AsyncSession=Depends(get_db)) -> DrawbackVerdeAmareloService:
    repository = SQLAlchemyDrawbackVerdeAmareloRepository(session)
    return DrawbackVerdeAmareloService(repository=repository)

async def get_siscomex_drawback_service(session: AsyncSession=Depends(get_db)) -> SiscomexDrawbackService:
    repository = SQLAlchemySiscomexDrawbackRepository(session)
    return SiscomexDrawbackService(repository=repository)