from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_db

db_dep = Depends(get_db)

from apps.backend.app.modules.economy.trade.external.application.services import (
    AgenteCargaService,
    CancelamentoRadarService,
    DespachanteService,
    DrawbackExternoService,
    DrawbackIntegradoService,
    DrawbackInternoService,
    DrawbackIsencaoService,
    DrawbackRestituicaoService,
    DrawbackService,
    DrawbackSubstituicaoService,
    DrawbackSuspensaoService,
    DrawbackVerdeAmareloService,
    ExportadorService,
    HabilitacaoExportadorService,
    HabilitacaoImportadorService,
    HabilitacaoRadarService,
    ImportadorService,
    RadarService,
    SiscomexDrawbackService,
    SuspensaoRadarService,
    TransportadorInternacionalService,
)
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories import (
    SQLAlchemyAgenteCargaRepository,
    SQLAlchemyCancelamentoRadarRepository,
    SQLAlchemyDespachanteRepository,
    SQLAlchemyDrawbackExternoRepository,
    SQLAlchemyDrawbackIntegradoRepository,
    SQLAlchemyDrawbackInternoRepository,
    SQLAlchemyDrawbackIsencaoRepository,
    SQLAlchemyDrawbackRepository,
    SQLAlchemyDrawbackRestituicaoRepository,
    SQLAlchemyDrawbackSubstituicaoRepository,
    SQLAlchemyDrawbackSuspensaoRepository,
    SQLAlchemyDrawbackVerdeAmareloRepository,
    SQLAlchemyExportadorRepository,
    SQLAlchemyHabilitacaoExportadorRepository,
    SQLAlchemyHabilitacaoImportadorRepository,
    SQLAlchemyHabilitacaoRadarRepository,
    SQLAlchemyImportadorRepository,
    SQLAlchemyRadarRepository,
    SQLAlchemySiscomexDrawbackRepository,
    SQLAlchemySuspensaoRadarRepository,
    SQLAlchemyTransportadorInternacionalRepository,
)
from apps.backend.core.auth import PermissionGuard, PolicyEngine

_permission_guard = PermissionGuard(PolicyEngine())

exportador_manage_dep = Depends(_permission_guard.required_permission("trade.exportador.manage"))
importador_manage_dep = Depends(_permission_guard.required_permission("trade.importador.manage"))
radar_manage_dep = Depends(_permission_guard.required_permission("trade.radar.manage"))
drawback_manage_dep = Depends(_permission_guard.required_permission("trade.drawback.manage"))
drawback_isencao_approve_dep = Depends(
    _permission_guard.required_permission("trade.drawback.isencao.approve")
)
drawback_suspensao_approve_dep = Depends(
    _permission_guard.required_permission("trade.drawback.suspensao.approve")
)
drawback_restituicao_approve_dep = Depends(
    _permission_guard.required_permission("trade.drawback.restituicao.approve")
)
drawback_interno_approve_dep = Depends(
    _permission_guard.required_permission("trade.drawback.interno.approve")
)
drawback_externo_approve_dep = Depends(
    _permission_guard.required_permission("trade.drawback.externo.approve")
)
drawback_integrado_approve_dep = Depends(
    _permission_guard.required_permission("trade.drawback.integrado.approve")
)
drawback_verde_amarelo_approve_dep = Depends(
    _permission_guard.required_permission("trade.drawback.verde_amarelo.approve")
)
drawback_substituicao_approve_dep = Depends(
    _permission_guard.required_permission("trade.drawback.substituicao.approve")
)


async def get_exportador_service(session: AsyncSession = db_dep) -> ExportadorService:
    repository = SQLAlchemyExportadorRepository(session)
    return ExportadorService(repository=repository)


async def get_importador_service(session: AsyncSession = db_dep) -> ImportadorService:
    repository = SQLAlchemyImportadorRepository(session)
    return ImportadorService(repository=repository)


async def get_despachante_service(session: AsyncSession = db_dep) -> DespachanteService:
    repository = SQLAlchemyDespachanteRepository(session)
    return DespachanteService(repository=repository)


async def get_agente_carga_service(session: AsyncSession = db_dep) -> AgenteCargaService:
    repository = SQLAlchemyAgenteCargaRepository(session)
    return AgenteCargaService(repository=repository)


async def get_transportador_internacional_service(
    session: AsyncSession = db_dep,
) -> TransportadorInternacionalService:
    repository = SQLAlchemyTransportadorInternacionalRepository(session)
    return TransportadorInternacionalService(repository=repository)


async def get_habilitacao_exportador_service(
    session: AsyncSession = db_dep,
) -> HabilitacaoExportadorService:
    repository = SQLAlchemyHabilitacaoExportadorRepository(session)
    return HabilitacaoExportadorService(repository=repository)


async def get_habilitacao_importador_service(
    session: AsyncSession = db_dep,
) -> HabilitacaoImportadorService:
    repository = SQLAlchemyHabilitacaoImportadorRepository(session)
    return HabilitacaoImportadorService(repository=repository)


async def get_radar_service(session: AsyncSession = db_dep) -> RadarService:
    repository = SQLAlchemyRadarRepository(session)
    return RadarService(repository=repository)


async def get_habilitacao_radar_service(
    session: AsyncSession = db_dep,
) -> HabilitacaoRadarService:
    repository = SQLAlchemyHabilitacaoRadarRepository(session)
    return HabilitacaoRadarService(repository=repository)


async def get_cancelamento_radar_service(
    session: AsyncSession = db_dep,
) -> CancelamentoRadarService:
    repository = SQLAlchemyCancelamentoRadarRepository(session)
    return CancelamentoRadarService(repository=repository)


async def get_suspensao_radar_service(
    session: AsyncSession = db_dep,
) -> SuspensaoRadarService:
    repository = SQLAlchemySuspensaoRadarRepository(session)
    return SuspensaoRadarService(repository=repository)


async def get_drawback_service(session: AsyncSession = db_dep) -> DrawbackService:
    repository = SQLAlchemyDrawbackRepository(session)
    return DrawbackService(repository=repository)


async def get_drawback_externo_service(
    session: AsyncSession = db_dep,
) -> DrawbackExternoService:
    repository = SQLAlchemyDrawbackExternoRepository(session)
    return DrawbackExternoService(repository=repository)


async def get_drawback_interno_service(
    session: AsyncSession = db_dep,
) -> DrawbackInternoService:
    repository = SQLAlchemyDrawbackInternoRepository(session)
    return DrawbackInternoService(repository=repository)


async def get_drawback_suspensao_service(
    session: AsyncSession = db_dep,
) -> DrawbackSuspensaoService:
    repository = SQLAlchemyDrawbackSuspensaoRepository(session)
    return DrawbackSuspensaoService(repository=repository)


async def get_drawback_isencao_service(
    session: AsyncSession = db_dep,
) -> DrawbackIsencaoService:
    repository = SQLAlchemyDrawbackIsencaoRepository(session)
    return DrawbackIsencaoService(repository=repository)


async def get_drawback_restituicao_service(
    session: AsyncSession = db_dep,
) -> DrawbackRestituicaoService:
    repository = SQLAlchemyDrawbackRestituicaoRepository(session)
    return DrawbackRestituicaoService(repository=repository)


async def get_drawback_substituicao_service(
    session: AsyncSession = db_dep,
) -> DrawbackSubstituicaoService:
    repository = SQLAlchemyDrawbackSubstituicaoRepository(session)
    return DrawbackSubstituicaoService(repository=repository)


async def get_drawback_integrado_service(
    session: AsyncSession = db_dep,
) -> DrawbackIntegradoService:
    repository = SQLAlchemyDrawbackIntegradoRepository(session)
    return DrawbackIntegradoService(repository=repository)


async def get_drawback_verde_amarelo_service(
    session: AsyncSession = db_dep,
) -> DrawbackVerdeAmareloService:
    repository = SQLAlchemyDrawbackVerdeAmareloRepository(session)
    return DrawbackVerdeAmareloService(repository=repository)


async def get_siscomex_drawback_service(
    session: AsyncSession = db_dep,
) -> SiscomexDrawbackService:
    repository = SQLAlchemySiscomexDrawbackRepository(session)
    return SiscomexDrawbackService(repository=repository)


async def get_exportador_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = exportador_manage_dep,
) -> ExportadorService:
    """Exportador service with permission guard: requires trade.exportador.manage"""
    repository = SQLAlchemyExportadorRepository(session)
    return ExportadorService(repository=repository)


async def get_importador_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = importador_manage_dep,
) -> ImportadorService:
    """Importador service with permission guard: requires trade.importador.manage"""
    repository = SQLAlchemyImportadorRepository(session)
    return ImportadorService(repository=repository)


async def get_radar_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = radar_manage_dep,
) -> RadarService:
    """RADAR service with permission guard: requires trade.radar.manage"""
    repository = SQLAlchemyRadarRepository(session)
    return RadarService(repository=repository)


async def get_drawback_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = drawback_manage_dep,
) -> DrawbackService:
    """Drawback service with permission guard: requires trade.drawback.manage"""
    repository = SQLAlchemyDrawbackRepository(session)
    return DrawbackService(repository=repository)


async def get_drawback_isencao_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = drawback_isencao_approve_dep,
) -> DrawbackIsencaoService:
    """Drawback isencao service with permission guard: requires trade.drawback.isencao.approve"""
    repository = SQLAlchemyDrawbackIsencaoRepository(session)
    return DrawbackIsencaoService(repository=repository)


async def get_drawback_suspensao_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = drawback_suspensao_approve_dep,
) -> DrawbackSuspensaoService:
    """Drawback suspensao service with permission guard: requires trade.drawback.suspensao.approve"""
    repository = SQLAlchemyDrawbackSuspensaoRepository(session)
    return DrawbackSuspensaoService(repository=repository)


async def get_drawback_restituicao_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = drawback_restituicao_approve_dep,
) -> DrawbackRestituicaoService:
    """Drawback restituicao service with permission guard: requires trade.drawback.restituicao.approve"""
    repository = SQLAlchemyDrawbackRestituicaoRepository(session)
    return DrawbackRestituicaoService(repository=repository)


async def get_drawback_interno_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = drawback_interno_approve_dep,
) -> DrawbackInternoService:
    """Drawback interno service with permission guard: requires trade.drawback.interno.approve"""
    repository = SQLAlchemyDrawbackInternoRepository(session)
    return DrawbackInternoService(repository=repository)


async def get_drawback_externo_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = drawback_externo_approve_dep,
) -> DrawbackExternoService:
    """Drawback externo service with permission guard: requires trade.drawback.externo.approve"""
    repository = SQLAlchemyDrawbackExternoRepository(session)
    return DrawbackExternoService(repository=repository)


async def get_drawback_integrado_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = drawback_integrado_approve_dep,
) -> DrawbackIntegradoService:
    """Drawback integrado service with permission guard: requires trade.drawback.integrado.approve"""
    repository = SQLAlchemyDrawbackIntegradoRepository(session)
    return DrawbackIntegradoService(repository=repository)


async def get_drawback_verde_amarelo_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = drawback_verde_amarelo_approve_dep,
) -> DrawbackVerdeAmareloService:
    """Drawback verde amarelo service with permission guard: requires trade.drawback.verde_amarelo.approve"""
    repository = SQLAlchemyDrawbackVerdeAmareloRepository(session)
    return DrawbackVerdeAmareloService(repository=repository)


async def get_drawback_substituicao_service_protected(
    session: AsyncSession = db_dep,
    _auth: dict = drawback_substituicao_approve_dep,
) -> DrawbackSubstituicaoService:
    """Drawback substituicao service with permission guard: requires trade.drawback.substituicao.approve"""
    repository = SQLAlchemyDrawbackSubstituicaoRepository(session)
    return DrawbackSubstituicaoService(repository=repository)
