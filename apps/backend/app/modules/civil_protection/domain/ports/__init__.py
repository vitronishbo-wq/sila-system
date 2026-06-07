from apps.backend.app.modules.civil_protection.domain.ports.atendimento_repository_port import (
    AtendimentoRepositoryPort,
)
from apps.backend.app.modules.civil_protection.domain.ports.bombeiro_repository_port import (
    BombeiroRepositoryPort,
)
from apps.backend.app.modules.civil_protection.domain.ports.corporacao_repository_port import (
    CorporacaoRepositoryPort,
)
from apps.backend.app.modules.civil_protection.domain.ports.despacho_repository_port import (
    DespachoRepositoryPort,
)
from apps.backend.app.modules.civil_protection.domain.ports.ocorrencia_emergencial_repository_port import (
    OcorrenciaEmergencialRepositoryPort,
)
from apps.backend.app.modules.civil_protection.domain.ports.request_service_port import (
    RequestServicePort,
)

__all__ = [
    "CorporacaoRepositoryPort",
    "BombeiroRepositoryPort",
    "OcorrenciaEmergencialRepositoryPort",
    "DespachoRepositoryPort",
    "AtendimentoRepositoryPort",
    "RequestServicePort",
]
