from apps.backend.app.modules.economy.trade.external.application.ports.agente_carga_repository_port import (
    AgenteCargaRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.cancelamento_radar_repository_port import (
    CancelamentoRadarRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.citizen_service_port import (
    CitizenServicePort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.comercio_service_port import (
    ComercioServicePort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.despachante_repository_port import (
    DespachanteRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.drawback_externo_repository_port import (
    DrawbackExternoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.drawback_integrado_repository_port import (
    DrawbackIntegradoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.drawback_interno_repository_port import (
    DrawbackInternoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.drawback_isencao_repository_port import (
    DrawbackIsencaoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.drawback_repository_port import (
    DrawbackRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.drawback_restituicao_repository_port import (
    DrawbackRestituicaoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.drawback_substituicao_repository_port import (
    DrawbackSubstituicaoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.drawback_suspensao_repository_port import (
    DrawbackSuspensaoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.drawback_verde_amarelo_repository_port import (
    DrawbackVerdeAmareloRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.exportador_repository_port import (
    ExportadorRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.financas_impostos_service_port import (
    FinancasImpostosServicePort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.financas_service_port import (
    FinancasServicePort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.geosampa_service_port import (
    GeosampaServicePort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.habilitacao_exportador_repository_port import (
    HabilitacaoExportadorRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.habilitacao_importador_repository_port import (
    HabilitacaoImportadorRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.habilitacao_radar_repository_port import (
    HabilitacaoRadarRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.habilitacao_repository_port_base import (
    HabilitacaoRepositoryPortBase,
)
from apps.backend.app.modules.economy.trade.external.application.ports.importador_repository_port import (
    ImportadorRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.industria_service_port import (
    IndustriaServicePort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.operador_logistico_repository_port import (
    OperadorLogisticoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.radar_repository_port import (
    RadarRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.siscomex_drawback_repository_port import (
    SiscomexDrawbackRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.suspensao_radar_repository_port import (
    SuspensaoRadarRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.transportador_internacional_repository_port import (
    TransportadorInternacionalRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.application.ports.transportes_logistica_service_port import (
    TransportesLogisticaServicePort,
)

ComercioInternacionalServicePort = ComercioServicePort
TributacaoFiscalServicePort = FinancasImpostosServicePort
__all__ = [
    "OperadorLogisticoRepositoryPort",
    "HabilitacaoRepositoryPortBase",
    "ExportadorRepositoryPort",
    "ImportadorRepositoryPort",
    "HabilitacaoExportadorRepositoryPort",
    "HabilitacaoImportadorRepositoryPort",
    "HabilitacaoRadarRepositoryPort",
    "CancelamentoRadarRepositoryPort",
    "SuspensaoRadarRepositoryPort",
    "DrawbackRepositoryPort",
    "DrawbackExternoRepositoryPort",
    "DrawbackInternoRepositoryPort",
    "DrawbackIsencaoRepositoryPort",
    "DrawbackIntegradoRepositoryPort",
    "DrawbackRestituicaoRepositoryPort",
    "DrawbackSubstituicaoRepositoryPort",
    "DrawbackSuspensaoRepositoryPort",
    "DrawbackVerdeAmareloRepositoryPort",
    "SiscomexDrawbackRepositoryPort",
    "DespachanteRepositoryPort",
    "AgenteCargaRepositoryPort",
    "TransportadorInternacionalRepositoryPort",
    "RadarRepositoryPort",
    "CitizenServicePort",
    "RequestServicePort",
    "IndustriaServicePort",
    "ComercioServicePort",
    "ComercioInternacionalServicePort",
    "TransportesLogisticaServicePort",
    "FinancasServicePort",
    "FinancasImpostosServicePort",
    "TributacaoFiscalServicePort",
    "GeosampaServicePort",
]
