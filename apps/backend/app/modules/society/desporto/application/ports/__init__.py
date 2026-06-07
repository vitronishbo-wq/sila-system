from apps.backend.app.modules.society.desporto.application.ports.atleta_repository_port import (
    AtletaRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.citizen_service_port import (
    CitizenServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.clube_repository_port import (
    ClubeRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.competicao_repository_port import (
    CompeticaoRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.educacao_service_port import (
    EducacaoServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.estadio_repository_port import (
    EstadioRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.federacao_service_port import (
    FederacaoServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.jogo_repository_port import (
    JogoRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.obras_publicas_service_port import (
    ObrasPublicasServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.outbox_repository_port import (
    OutboxRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.saude_service_port import (
    SaudeServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.turismo_service_port import (
    TurismoServicePort,
)

__all__ = [
    "AtletaRepositoryPort",
    "CompeticaoRepositoryPort",
    "ClubeRepositoryPort",
    "JogoRepositoryPort",
    "EstadioRepositoryPort",
    "CitizenServicePort",
    "RequestServicePort",
    "SaudeServicePort",
    "EducacaoServicePort",
    "ObrasPublicasServicePort",
    "TurismoServicePort",
    "OutboxRepositoryPort",
    "FederacaoServicePort",
]
