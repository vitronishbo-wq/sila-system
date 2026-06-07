from __future__ import annotations

from datetime import datetime
from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.events import (
    OcorrenciaRegistradaEvent,
    event_bus,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.ports.ocorrencia_repository_port import (
    OcorrenciaRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import (
    FaseVoo,
    TipoOcorrencia,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.models.ocorrencia import (
    Ocorrencia,
)
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.persistence.outbox import (
    InMemoryOutbox,
)


class OcorrenciaService:
    def __init__(
        self, *, ocorrencia_repo: OcorrenciaRepositoryPort, outbox: InMemoryOutbox
    ) -> None:
        self.ocorrencia_repo = ocorrencia_repo
        self.outbox = outbox

    async def registrar_ocorrencia(
        self,
        *,
        tipo: TipoOcorrencia,
        aeronave_id: UUID,
        data_ocorrencia: datetime,
        local: dict,
        fase_voo: FaseVoo,
        descricao: str,
        vitimas: dict[str, int],
        danos: str,
        voo_id: UUID | None = None,
    ) -> Ocorrencia:
        ocorrencia = Ocorrencia(
            tipo=tipo,
            voo_id=voo_id,
            aeronave_id=aeronave_id,
            data_ocorrencia=data_ocorrencia,
            local=local,
            fase_voo=fase_voo,
            descricao=descricao,
            vitimas=vitimas,
            danos=danos,
        )
        await self.ocorrencia_repo.save(ocorrencia)
        evento = OcorrenciaRegistradaEvent(
            ocorrencia_id=ocorrencia.id,
            numero_ocorrencia=ocorrencia.numero_ocorrencia,
            tipo=ocorrencia.tipo.value,
            aeronave_id=ocorrencia.aeronave_id,
            gravidade=ocorrencia.gravidade.value,
            data_ocorrencia=ocorrencia.data_ocorrencia,
        )
        await self.outbox.append(evento)
        await event_bus.publish(evento)
        return ocorrencia

    async def listar_ocorrencias(self) -> list[Ocorrencia]:
        return await self.ocorrencia_repo.list_all()
