from apps.backend.app.modules.resources.pescas.application.ports.ambiente_service_port import (
    AmbienteServicePort,
)
from apps.backend.app.modules.resources.pescas.application.ports.armador_repository_port import (
    ArmadorRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.captura_repository_port import (
    CapturaRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.citizen_service_port import (
    CitizenServicePort,
)
from apps.backend.app.modules.resources.pescas.application.ports.comercializacao_pesca_repository_port import (
    ComercializacaoPescaRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.comercio_externo_service_port import (
    ComercioExternoServicePort,
)
from apps.backend.app.modules.resources.pescas.application.ports.defeso_repository_port import (
    DefesoRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.desembarque_repository_port import (
    DesembarqueRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.embarcacao_repository_port import (
    EmbarcacaoRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.especie_repository_port import (
    EspecieRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.fiscalizacao_pesca_repository_port import (
    FiscalizacaoPescaRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.geosampa_service_port import (
    GeosampaServicePort,
)
from apps.backend.app.modules.resources.pescas.application.ports.licenca_pesca_repository_port import (
    LicencaPescaRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.pescador_repository_port import (
    PescadorRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.producao_pesca_repository_port import (
    ProducaoPescaRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.quota_repository_port import (
    QuotaRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.rastreabilidade_pesca_repository_port import (
    RastreabilidadePescaRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.resources.pescas.application.ports.transportes_logistica_service_port import (
    TransportesLogisticaServicePort,
)
from apps.backend.app.modules.resources.pescas.application.ports.zona_pesca_repository_port import (
    ZonaPescaRepositoryPort,
)

__all__ = [
    "PescadorRepositoryPort",
    "ArmadorRepositoryPort",
    "EmbarcacaoRepositoryPort",
    "LicencaPescaRepositoryPort",
    "CapturaRepositoryPort",
    "EspecieRepositoryPort",
    "ZonaPescaRepositoryPort",
    "QuotaRepositoryPort",
    "DefesoRepositoryPort",
    "DesembarqueRepositoryPort",
    "ProducaoPescaRepositoryPort",
    "ComercializacaoPescaRepositoryPort",
    "FiscalizacaoPescaRepositoryPort",
    "RastreabilidadePescaRepositoryPort",
    "CitizenServicePort",
    "RequestServicePort",
    "AmbienteServicePort",
    "ComercioExternoServicePort",
    "TransportesLogisticaServicePort",
    "GeosampaServicePort",
]
