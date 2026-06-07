from apps.backend.app.modules.resources.aguas_saneamento.application.ports.abastecimento_repository_port import (
    AbastecimentoRepositoryPort,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.ambiente_service_port import (
    AmbienteServicePort,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.citizen_service_port import (
    CitizenServicePort,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.consumo_repository_port import (
    ConsumoRepositoryPort,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.fatura_repository_port import (
    FaturaRepositoryPort,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.financas_gateway_port import (
    FinancasGatewayPort,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.geosampa_service_port import (
    GeosampaServicePort,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.infraestrutura_repository_port import (
    InfraestruturaRepositoryPort,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.outbox_repository_port import (
    OutboxRepositoryPort,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.outorga_repository_port import (
    OutorgaRepositoryPort,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.request_service_port import (
    RequestServicePort,
)

__all__ = [
    "OutorgaRepositoryPort",
    "InfraestruturaRepositoryPort",
    "AbastecimentoRepositoryPort",
    "ConsumoRepositoryPort",
    "FaturaRepositoryPort",
    "CitizenServicePort",
    "RequestServicePort",
    "AmbienteServicePort",
    "GeosampaServicePort",
    "FinancasGatewayPort",
    "OutboxRepositoryPort",
]
