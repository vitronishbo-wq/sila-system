from apps.backend.app.modules.logistics.domain.ports.ambiente_service_port import (
    AmbienteServicePort,
)
from apps.backend.app.modules.logistics.domain.ports.bilhetagem_repository_port import (
    BilhetagemRepositoryPort,
)
from apps.backend.app.modules.logistics.domain.ports.citizen_service_port import CitizenServicePort
from apps.backend.app.modules.logistics.domain.ports.comercio_externo_service_port import (
    ComercioExternoServicePort,
)
from apps.backend.app.modules.logistics.domain.ports.financas_service_port import (
    FinancasServicePort,
)
from apps.backend.app.modules.logistics.domain.ports.frota_repository_port import (
    FrotaRepositoryPort,
)
from apps.backend.app.modules.logistics.domain.ports.geosampa_service_port import (
    GeosampaServicePort,
)
from apps.backend.app.modules.logistics.domain.ports.linha_repository_port import (
    LinhaRepositoryPort,
)
from apps.backend.app.modules.logistics.domain.ports.obras_publicas_service_port import (
    ObrasPublicasServicePort,
)
from apps.backend.app.modules.logistics.domain.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.logistics.domain.ports.seguranca_publica_service_port import (
    SegurancaPublicaServicePort,
)
from apps.backend.app.modules.logistics.domain.ports.service_requests_service_port import (
    ServiceRequestsServicePort,
)
from apps.backend.app.modules.logistics.domain.ports.urbanismo_service_port import (
    UrbanismoServicePort,
)
from apps.backend.app.modules.logistics.domain.ports.veiculo_repository_port import (
    VeiculoRepositoryPort,
)
from apps.backend.app.modules.logistics.domain.ports.viagem_repository_port import (
    ViagemRepositoryPort,
)
from apps.backend.app.modules.logistics.domain.ports.workflow_service_port import (
    WorkflowServicePort,
)

__all__ = [
    "ViagemRepositoryPort",
    "FrotaRepositoryPort",
    "LinhaRepositoryPort",
    "VeiculoRepositoryPort",
    "BilhetagemRepositoryPort",
    "CitizenServicePort",
    "RequestServicePort",
    "ServiceRequestsServicePort",
    "ObrasPublicasServicePort",
    "UrbanismoServicePort",
    "ComercioExternoServicePort",
    "AmbienteServicePort",
    "GeosampaServicePort",
    "WorkflowServicePort",
    "FinancasServicePort",
    "SegurancaPublicaServicePort",
]
